import json
import os
import glob
import numpy as np

def process_experiment_results(folder_path):
    
    results = {}

    files = glob.glob(os.path.join(folder_path, "*.json"))

    for file_path in files:
        with open(file_path, 'r') as f:
            data = json.load(f)
            
            name = data["pipeline_name"]
            if name not in results:
                results[name] = {"status": [],
                                 "output_size": [],
                                 "times_min": [],
                                 "thrpt": [],
                                 "peaks": [],
                                 "completed_records_end": []}
                
            results[name]["status"].append(data["status"])
            results[name]["output_size"].append(data["result_count"])
            results[name]["times_min"].append(data["end_uptime_msecs"] / 1000 / 60)
            results[name]["thrpt"].append(data["throughput_rows_per_sec"])
            results[name]["peaks"].append(data["memory_peak_mib"])
            results[name]["completed_records_end"].append(data["completed_records_end"])

    print(f"Computing results for {folder_path}")
    print(f"{'Variant':<50} | {'Output Size':<10}| {'Time (Avg)':<10} | {'Thrpt (Avg)':<12} | {'Peak RAM':<10} |")
    print("-" * 105)
    
    for variant, metrics in results.items():

        avg_time = np.mean(metrics["times_min"])
        avg_thrpt = np.mean(metrics["thrpt"])
        max_peak_gib = np.max(metrics["peaks"]) / 1024

        status_set = set(metrics["status"])
        output_size_set = set(metrics["output_size"])
        completed_records_set = set(metrics["completed_records_end"])

        status_val = list(status_set)[0] if len(status_set) == 1 else f"MISMATCH: {metrics['status']}"
        if len(output_size_set) == 1:
            value = list(output_size_set)[0]
            output_size_val = value if value is not None else "null"
        else:
            output_size_val = f"MISMATCH: {metrics['output_size']}"
        completed_records_val = list(completed_records_set)[0] if len(completed_records_set) == 1 else f"MISMATCH: {metrics['completed_records_end']}, AVG: {np.mean(metrics['completed_records_end'])}"

        
        print(f"{variant:<50} | {output_size_val:>10}r | {avg_time:>8.2f}min | {avg_thrpt:>9.0f}r/s | {max_peak_gib:>8.1f}GiB |")
        print(f"STATUS: {status_val}, COMPLETED RECORDS: {completed_records_val}")


process_experiment_results("../results/imdb/Acyclic Query 1/decomposition_faq")