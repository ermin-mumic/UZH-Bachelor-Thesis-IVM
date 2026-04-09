import argparse
import json
import os

from feldera import FelderaClient
from feldera.pipeline import Pipeline
from feldera.enums import PipelineStatus
from feldera.rest.pipeline import Pipeline as RestPipeline

from data_loader import prepare_data


class Experiment:
    def __init__(
        self,
        pipeline_name,
        batch_size,
        trials,
        pipeline_sql_path=None,
        output_dir="results",
        feldera_url="http://localhost:8080"
    ):
        self.client = FelderaClient(feldera_url)
        self.pipeline_name = pipeline_name
        self.batch_size = batch_size
        self.trials = trials
        self.pipeline_sql_path = pipeline_sql_path
        self.output_dir = output_dir
        self.pipeline = None

    def _start_pipeline(self):
        if self.pipeline_sql_path:
            with open(self.pipeline_sql_path, "r", encoding="utf-8") as f:
                sql_code = f.read()
            print(f"Creating/updating pipeline '{self.pipeline_name}' from {self.pipeline_sql_path}")
            pipeline_def = RestPipeline(
                name=self.pipeline_name,
                sql=sql_code,
                udf_rust="",
                udf_toml="",
                program_config={},
                runtime_config={},
            )
            self.client.create_or_update_pipeline(pipeline_def)
        self.pipeline = Pipeline.get(self.pipeline_name, self.client)
        self.client.start_pipeline(self.pipeline_name)
        self.pipeline.wait_for_status(PipelineStatus.RUNNING, timeout=120)

    def _stop_pipeline(self):
        if self.pipeline is not None:
            self.pipeline.stop(force=True)

    def _stats(self):
        return self.pipeline.stats().global_metrics

    def _snapshot(self):
        stats = self._stats()
        return {
            "uptime_msecs": stats.uptime_msecs or 0,
            "total_completed_records": stats.total_completed_records or 0,
            "rss_mib": (stats.rss_bytes or 0) / (1024 * 1024),
        }

    @staticmethod
    def _count_input_rows(insert_sequence):
        return int(sum(len(df_batch) for _, df_batch in insert_sequence))

    @staticmethod
    def _compute_throughput_rows_per_sec(start_snap, end_snap):
        completed_delta = end_snap["total_completed_records"] - start_snap["total_completed_records"]
        uptime_delta_msecs = end_snap["uptime_msecs"] - start_snap["uptime_msecs"]
        if uptime_delta_msecs <= 0:
            return 0.0
        return float(completed_delta) / (float(uptime_delta_msecs) / 1000.0)

    def _save_results(self, trial_id, payload):
        os.makedirs(self.output_dir, exist_ok=True)
        filename = os.path.join(
            self.output_dir,
            f"pipeline-{self.pipeline_name}_batch{self.batch_size}_trial{trial_id}.json",
        )
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        print(f"Results saved to {filename}")

    def run_trial(self, trial_id, insert_sequence):
        print(f"\n{'#' * 70}")
        print(f"TRIAL {trial_id}/{self.trials}")
        print(f"{'#' * 70}\n")

        self._start_pipeline()
        memory_timeline = []

        start_snap = self._snapshot()
        memory_timeline.append(
            {
                "uptime_msecs": start_snap["uptime_msecs"],
                "rss_mib": start_snap["rss_mib"]
            }
        )

        for table_name, df_batch in insert_sequence:
            self.pipeline.input_pandas(table_name, df_batch)
            batch_snap = self._snapshot()
            memory_timeline.append(
                {
                    "uptime_msecs": batch_snap["uptime_msecs"],
                    "rss_mib": batch_snap["rss_mib"]
                }
            )

        self.pipeline.wait_for_completion()
        end_snap = self._snapshot()
        self._stop_pipeline()

        throughput_rows_per_sec = self._compute_throughput_rows_per_sec(start_snap, end_snap)
        peak_memory_mib = max((p["rss_mib"] for p in memory_timeline), default=0.0)

        payload = {
            "trial": trial_id,
            "pipeline_name": self.pipeline_name,
            "batch_size": self.batch_size,
            "input_batches_submitted": len(insert_sequence),
            "input_rows_submitted": self._count_input_rows(insert_sequence),
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


    def run_all(self, insert_sequence):
        print(f"\nPrepared {len(insert_sequence)} batch inserts")
        for trial in range(1, self.trials + 1):
            self.run_trial(trial, insert_sequence)


def parse_args():
    parser = argparse.ArgumentParser(description="Run Feldera experiment.")
    parser.add_argument("--pipeline-name", required=True)
    parser.add_argument("--pipeline-sql-path", required=True, help="Path to SQL file for pipeline definition.")
    parser.add_argument("--batch-size", type=int, default=1000)
    parser.add_argument("--trials", type=int, default=1)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--csv-dir", default="data")
    parser.add_argument(
        "--tables",
        default="CUSTOMER,ORDERS,LINEITEM,PARTSUPP",
        help="Comma-separated list of table names.",
    )
    return parser.parse_args()


def resolve_default_output_dir(pipeline_sql_path: str) -> str:
    pipeline_sql_name = os.path.basename(pipeline_sql_path)
    pipeline_sql_stem = os.path.splitext(pipeline_sql_name)[0]
    pipeline_parent_dir = os.path.basename(os.path.dirname(pipeline_sql_path))
    return os.path.join("results", pipeline_parent_dir, pipeline_sql_stem)


if __name__ == "__main__":
    args = parse_args()
    table_names = [t.strip().upper() for t in args.tables.split(",") if t.strip()]

    if args.output_dir is None:
        args.output_dir = resolve_default_output_dir(args.pipeline_sql_path)


    print("\n" + "=" * 70)
    print("FELDERA EXPERIMENT")
    print("=" * 70 + "\n")
    print(f"Pipeline: {args.pipeline_name}")
    print(f"Batch size: {args.batch_size}")
    print(f"Trials: {args.trials}")
    print(f"Tables: {', '.join(table_names)}")

    insert_sequence = prepare_data(
        table_names=table_names,
        csv_dir=args.csv_dir,
        batch_size=args.batch_size,
    )

    experiment = Experiment(
        pipeline_name=args.pipeline_name,
        pipeline_sql_path=args.pipeline_sql_path,
        batch_size=args.batch_size,
        trials=args.trials,

        output_dir=args.output_dir,
    )
    experiment.run_all(insert_sequence)

    print("\n" + "=" * 70)
    print("EXPERIMENT COMPLETE")
    print("=" * 70 + "\n")
