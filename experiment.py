import argparse
import json
import os
import threading
import time

from feldera import FelderaClient
from feldera.pipeline_builder import PipelineBuilder

class TaskWorker(threading.Thread):
    def __init__(
            self,
            task_func
    ):
        super().__init__(daemon=True)
        self.task_func = task_func
        self.result = None
        self.error = None

    def run(self):
        try:
            self.result = self.task_func()
        except Exception as e:
            self.error = e

class StatsPoller(threading.Thread):
    def __init__(
        self,
        snapshot_func,
        interval = 5
    ):
        super().__init__(daemon=True)
        self.snapshot_func = snapshot_func
        self.interval = interval
        self.timeline = []
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            try:
                snap = self.snapshot_func()
                self.timeline.append(snap)
            except:
                pass
            time.sleep(self.interval)
    
    def stop(self):
        self._stop_event.set()

class Experiment:
    def __init__(
        self,
        pipeline_name,
        pipeline_sql_path,
        dataset_path,
        trials,
        output_dir,
        feldera_url="http://localhost:8080"
    ):
        self.client = FelderaClient(feldera_url)
        self.pipeline_name = pipeline_name
        self.pipeline_sql_path = pipeline_sql_path
        self.dataset_path = dataset_path
        self.trials = trials
        self.output_dir = output_dir
        self.pipeline = None

    def _start_pipeline(self):
    
        with open(self.pipeline_sql_path, "r", encoding="utf-8") as f:
            template = f.read()

        sql_code = template.replace('{{FILE_PATH}}', self.dataset_path)

        print(f"Creating pipeline '{self.pipeline_name}' with '{self.dataset_path}'")

        self.pipeline = PipelineBuilder(
            client = self.client,
            name = self.pipeline_name,
            sql = sql_code
        ).create_or_replace()

        self.pipeline.start()

    def _stop_pipeline(self):
        if self.pipeline is not None:
            self.pipeline.stop(force=True)

    def _snapshot(self):
        stats = self.pipeline.stats().global_metrics
        return {
            "uptime_msecs": stats.uptime_msecs or -1,
            "total_completed_records": stats.total_completed_records or -1,
            "rss_mib": (stats.rss_bytes or -1) / (1024 * 1024),
        }
    
    def _get_result_count(self):
        result_generator = self.pipeline.query("SELECT COUNT(*) AS total_count FROM RESULT")
        first_row = next(result_generator, None)
        return first_row["total_count"] if first_row else 0

    @staticmethod
    def _compute_throughput_rows_per_sec(end_snap):
        if end_snap["uptime_msecs"] <= 0:
            return 0.0
        return float(end_snap["total_completed_records"]) / (float(end_snap["uptime_msecs"]) / 1000.0)

    def _save_results(self, trial_id, payload):
        os.makedirs(self.output_dir, exist_ok=True)

        filename = os.path.join(
            self.output_dir,
            f"trial{trial_id}.json",
        )
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        print(f"Results saved to {filename}")

    def run_trial(self, trial_id):
        print(f"\n{'#' * 70}")
        print(f"TRIAL {trial_id}/{self.trials}")
        print(f"{'#' * 70}\n")

        INGESTION_TIMEOUT = 10800 # 3h
        COUNT_TIMEOUT = 3600 # 1h
        
        status = "SUCCESS"

        stats_poller = StatsPoller(self._snapshot) 

        self._start_pipeline()
        stats_poller.start()

        ingestion_worker = TaskWorker(self.pipeline.wait_for_completion)
        ingestion_worker.start()
        ingestion_worker.join(timeout=INGESTION_TIMEOUT)

        if ingestion_worker.is_alive():
            status = "Timeout"
        elif ingestion_worker.error:
            status = f"CRASHED: {ingestion_worker.error}"

        stats_poller.stop()
        stats_poller.join()

        try:
            end_snap = self._snapshot()
            stats_poller.timeline.append(end_snap)
        except Exception:
            pass

        count_worker = TaskWorker(self._get_result_count)
        count_worker.start()
        count_worker.join(timeout=COUNT_TIMEOUT)

        if count_worker.is_alive():
            result_count = "TIMEOUT"
        elif count_worker.error:
            result_count = f"ERROR: {count_worker.error}"
        else:
            result_count = count_worker.result
        
        self._stop_pipeline()
        self.pipeline.clear_storage()

        timeline = stats_poller.timeline

        throughput_rows_per_sec = self._compute_throughput_rows_per_sec(timeline[-1]) if timeline else -1
        peak_memory_mib = max((p["rss_mib"] for p in timeline), default=0.0) if timeline else -1

        payload = {
            "trial": trial_id,
            "pipeline_name": self.pipeline_name,
            "status":status,
            "throughput_rows_per_sec": throughput_rows_per_sec,
            "end_uptime_msecs": timeline[-1]["uptime_msecs"] if timeline else -1,
            "completed_records_end": timeline[-1]["total_completed_records"] if timeline else -1,
            "result_count": result_count,
            "memory_end_mib": timeline[-1]["rss_mib"] if timeline else -1,
            "memory_peak_mib": peak_memory_mib,
            "timeline": timeline,
        }

        self._save_results(trial_id, payload)

        print(f"Throughput: {throughput_rows_per_sec:.2f} rows/sec")
        print(f"Peak memory: {peak_memory_mib:.2f} MiB")

    def run_all(self):
        for trial in range(1, self.trials + 1):
            self.run_trial(trial)

def parse_args():
    parser = argparse.ArgumentParser(description="Run Feldera experiment.")
    parser.add_argument("--pipeline-sql-path", required=True, help="Path to SQL file for pipeline definition.")
    parser.add_argument("--dataset-path", required=True, help="Path to Data CSV file. 'data/snap_data/x.csv")
    parser.add_argument("--trials", type=int, default=1)
    parser.add_argument("--output-dir", default=None)
    return parser.parse_args()

def resolve_default_output_dir(pipeline_sql_path: str, dataset_path: str) -> str:
    pipeline_sql_name = os.path.basename(pipeline_sql_path)
    pipeline_sql_stem = os.path.splitext(pipeline_sql_name)[0]
    pipeline_parent_dir = os.path.basename(os.path.dirname(pipeline_sql_path))

    return os.path.join("results", dataset_path, pipeline_parent_dir, pipeline_sql_stem)



if __name__ == "__main__":
    args = parse_args()

    if args.output_dir is None:
        args.output_dir = resolve_default_output_dir(args.pipeline_sql_path, args.dataset_path)

    print("\n" + "=" * 70)
    print("FELDERA EXPERIMENT")
    print("=" * 70 + "\n")
    print(f"Pipeline Template: {args.pipeline_sql_path}")
    print(f"Trials: {args.trials}")

    experiment = Experiment(
        pipeline_name=os.path.splitext(os.path.basename(args.pipeline_sql_path))[0],
        pipeline_sql_path=args.pipeline_sql_path,
        dataset_path=args.dataset_path,
        trials=args.trials,
        output_dir=args.output_dir,
    )

    experiment.run_all()

    print("\n" + "=" * 70)
    print("EXPERIMENT COMPLETE")
    print("=" * 70 + "\n")

