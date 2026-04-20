import argparse
import json
import os

from feldera import FelderaClient
from feldera.pipeline import Pipeline
from feldera.pipeline_builder import PipelineBuilder
from feldera.enums import PipelineStatus


class Experiment:
    def __init__(
        self,
        pipeline_name,
        pipeline_sql_path,
        sf,
        trials,
        output_dir,
        feldera_url="http://localhost:8080"
    ):
        self.client = FelderaClient(feldera_url)
        self.pipeline_name = pipeline_name
        self.pipeline_sql_path = pipeline_sql_path
        self.sf = sf
        self.trials = trials
        self.output_dir = output_dir
        self.pipeline = None

    def _start_pipeline(self):
    
        with open(self.pipeline_sql_path, "r", encoding="utf-8") as f:
            sql_code = f.read()

        print(f"Creating pipeline '{self.pipeline_name}' from {self.pipeline_sql_path}")

        self.pipeline = PipelineBuilder(
            client = self.client,
            name = self.pipeline_name,
            sql = sql_code
        ).create_or_replace()

        self.client.start_pipeline(self.pipeline_name)
        self.pipeline.wait_for_status(PipelineStatus.RUNNING, timeout=120)

    def _stop_pipeline(self):
        if self.pipeline is not None:
            self.pipeline.stop(force=True)

    def _snapshot(self):
        stats = self.pipeline.stats().global_metrics
        return {
            "uptime_msecs": stats.uptime_msecs or 0,
            "total_completed_records": stats.total_completed_records or 0,
            "rss_mib": (stats.rss_bytes or 0) / (1024 * 1024),
        }

    @staticmethod
    def _compute_throughput_rows_per_sec(start_snap, end_snap):
        completed_delta = end_snap["total_completed_records"] - start_snap["total_completed_records"]
        uptime_delta_msecs = end_snap["uptime_msecs"] - start_snap["uptime_msecs"]
        if uptime_delta_msecs <= 0:
            return 0.0
        return float(completed_delta) / (float(uptime_delta_msecs) / 1000.0)

    def _save_results(self, trial_id, payload):
        os.makedirs(self.output_dir, exist_ok=True)

        sf_suffix = f"_sf{self.sf}" if self.sf is not None else ""
        filename = os.path.join(
            self.output_dir,
            f"pipeline-{self.pipeline_name}{sf_suffix}_trial{trial_id}.json",
        )
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        print(f"Results saved to {filename}")

    def run_trial(self, trial_id):
        print(f"\n{'#' * 70}")
        print(f"TRIAL {trial_id}/{self.trials}")
        print(f"{'#' * 70}\n")

        memory_timeline = []

        self._start_pipeline()

        start_snap = self._snapshot()
        memory_timeline.append(
            {
                "uptime_msecs": start_snap["uptime_msecs"],
                "rss_mib": start_snap["rss_mib"]
            }
        )

        self.pipeline.wait_for_completion()
        
        end_snap = self._snapshot()
        memory_timeline.append(
            {
                "uptime_msecs": end_snap["uptime_msecs"],
                "rss_mib": end_snap["rss_mib"]
            }
        )
        
        self._stop_pipeline()
        self.pipeline.clear_storage()

        throughput_rows_per_sec = self._compute_throughput_rows_per_sec(start_snap, end_snap)
        peak_memory_mib = max((p["rss_mib"] for p in memory_timeline), default=0.0)

        payload = {
            "trial": trial_id,
            "pipeline_name": self.pipeline_name,
            "throughput_rows_per_sec": throughput_rows_per_sec,
            "start_uptime_msecs": start_snap["uptime_msecs"],
            "end_uptime_msecs": end_snap["uptime_msecs"],
            "completed_records_start": start_snap["total_completed_records"],
            "completed_records_end": end_snap["total_completed_records"],
            "memory_start_mib": start_snap["rss_mib"],
            "memory_end_mib": end_snap["rss_mib"],
            "memory_peak_mib": peak_memory_mib,
            "memory_timeline": memory_timeline,
        }

        self._save_results(trial_id, payload)

        print(f"Throughput: {throughput_rows_per_sec:.2f} rows/sec")
        print(f"Peak memory: {peak_memory_mib:.2f} MiB")

    def run_all(self):
        for trial in range(1, self.trials + 1):
            self.run_trial(trial)

def parse_args():
    parser = argparse.ArgumentParser(description="Run Feldera experiment.")
    parser.add_argument("--pipeline-name", required=True)
    parser.add_argument("--pipeline-sql-path", required=True, help="Path to SQL file for pipeline definition.")
    parser.add_argument("--sf", type=float, default=None)
    parser.add_argument("--trials", type=int, default=1)
    parser.add_argument("--output-dir", default=None)
    return parser.parse_args()

def resolve_default_output_dir(pipeline_sql_path: str, sf: float = None) -> str:
    pipeline_sql_name = os.path.basename(pipeline_sql_path)
    pipeline_sql_stem = os.path.splitext(pipeline_sql_name)[0]
    pipeline_parent_dir = os.path.basename(os.path.dirname(pipeline_sql_path))

    if sf is None:
        return os.path.join("results", pipeline_parent_dir, pipeline_sql_stem)
    return os.path.join("results", pipeline_parent_dir, pipeline_sql_stem, str(sf))



if __name__ == "__main__":
    args = parse_args()

    if args.output_dir is None:
        args.output_dir = resolve_default_output_dir(args.pipeline_sql_path, args.sf)

    print("\n" + "=" * 70)
    print("FELDERA EXPERIMENT")
    print("=" * 70 + "\n")
    print(f"Pipeline: {args.pipeline_name}")
    print(f"Trials: {args.trials}")

    experiment = Experiment(
        pipeline_name=args.pipeline_name,
        pipeline_sql_path=args.pipeline_sql_path,
        sf=args.sf,
        trials=args.trials,
        output_dir=args.output_dir,
    )

    experiment.run_all()

    print("\n" + "=" * 70)
    print("EXPERIMENT COMPLETE")
    print("=" * 70 + "\n")

