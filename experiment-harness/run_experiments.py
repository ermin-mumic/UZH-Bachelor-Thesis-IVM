import os
import csv
import time
import subprocess
import datetime

EXPERIMENTS = [
    # ---- 4 Table Path Query - tpc-h - sf_1.0 ----
    # {
    #     "pipeline-sql-path": f"pipelines/4 Table Path Query/baseline.sql",
    #     "dataset-path": f"data/tpch_data/sf_1.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_1.0/4 Table Path Query/baseline"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/4 Table Path Query/decomposition_full.sql",
    #     "dataset-path": f"data/tpch_data/sf_1.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_1.0/4 Table Path Query/decomposition_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/4 Table Path Query/decomposition_faq.sql",
    #     "dataset-path": f"data/tpch_data/sf_1.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_1.0/4 Table Path Query/decomposition_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/4 Table Path Query/decomposition_no_projection_full.sql",
    #     "dataset-path": f"data/tpch_data/sf_1.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_1.0/4 Table Path Query/decomposition_no_projection_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/4 Table Path Query/decomposition_no_projection_faq.sql",
    #     "dataset-path": f"data/tpch_data/sf_1.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_1.0/4 Table Path Query/decomposition_no_projection_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/4 Table Path Query/decomposition_no_projection.sql",
    #     "dataset-path": f"data/tpch_data/sf_1.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_1.0/4 Table Path Query/decomposition_no_projection"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/4 Table Path Query/decomposition.sql",
    #     "dataset-path": f"data/tpch_data/sf_1.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_1.0/4 Table Path Query/decomposition"
    # },

    # ---- 4 Table Path Query - tpc-h - sf_10.0 ----
    # {
    #     "pipeline-sql-path": f"pipelines/4 Table Path Query/baseline.sql",
    #     "dataset-path": f"data/tpch_data/sf_10.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_10.0/4 Table Path Query/baseline"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/4 Table Path Query/decomposition_full.sql",
    #     "dataset-path": f"data/tpch_data/sf_10.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_10.0/4 Table Path Query/decomposition_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/4 Table Path Query/decomposition_faq.sql",
    #     "dataset-path": f"data/tpch_data/sf_10.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_10.0/4 Table Path Query/decomposition_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/4 Table Path Query/decomposition_no_projection_full.sql",
    #     "dataset-path": f"data/tpch_data/sf_10.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_10.0/4 Table Path Query/decomposition_no_projection_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/4 Table Path Query/decomposition_no_projection_faq.sql",
    #     "dataset-path": f"data/tpch_data/sf_10.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_10.0/4 Table Path Query/decomposition_no_projection_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/4 Table Path Query/decomposition_no_projection.sql",
    #     "dataset-path": f"data/tpch_data/sf_10.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_10.0/4 Table Path Query/decomposition_no_projection"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/4 Table Path Query/decomposition.sql",
    #     "dataset-path": f"data/tpch_data/sf_10.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_10.0/4 Table Path Query/decomposition"
    # },

    # ---- 4 Table Path Query - tpc-h - sf_30.0 ----
    # {
    #     "pipeline-sql-path": f"pipelines/4 Table Path Query/baseline.sql",
    #     "dataset-path": f"data/tpch_data/sf_30.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_30.0/4 Table Path Query/baseline"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/4 Table Path Query/decomposition_full.sql",
    #     "dataset-path": f"data/tpch_data/sf_30.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_30.0/4 Table Path Query/decomposition_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/4 Table Path Query/decomposition_faq.sql",
    #     "dataset-path": f"data/tpch_data/sf_30.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_30.0/4 Table Path Query/decomposition_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/4 Table Path Query/decomposition_no_projection_full.sql",
    #     "dataset-path": f"data/tpch_data/sf_30.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_30.0/4 Table Path Query/decomposition_no_projection_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/4 Table Path Query/decomposition_no_projection_faq.sql",
    #     "dataset-path": f"data/tpch_data/sf_30.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_30.0/4 Table Path Query/decomposition_no_projection_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/4 Table Path Query/decomposition_no_projection.sql",
    #     "dataset-path": f"data/tpch_data/sf_30.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_30.0/4 Table Path Query/decomposition_no_projection"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/4 Table Path Query/decomposition.sql",
    #     "dataset-path": f"data/tpch_data/sf_30.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_30.0/4 Table Path Query/decomposition"
    # },

    # ---- 4 Table Path Query - tpc-h - sf_100.0 ----
    # {
    #     "pipeline-sql-path": f"pipelines/4 Table Path Query/baseline.sql",
    #     "dataset-path": f"data/tpch_data/sf_100.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_100.0/4 Table Path Query/baseline"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/4 Table Path Query/decomposition_full.sql",
    #     "dataset-path": f"data/tpch_data/sf_100.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_100.0/4 Table Path Query/decomposition_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/4 Table Path Query/decomposition_no_projection_full.sql",
    #     "dataset-path": f"data/tpch_data/sf_100.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_100.0/4 Table Path Query/decomposition_no_projection_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/4 Table Path Query/decomposition_no_projection.sql",
    #     "dataset-path": f"data/tpch_data/sf_100.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_100.0/4 Table Path Query/decomposition_no_projection"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/4 Table Path Query/decomposition.sql",
    #     "dataset-path": f"data/tpch_data/sf_100.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_100.0/4 Table Path Query/decomposition"
    # },


    # ---- 5 Table Path Query - tpc-h - sf_1.0 ----
    # {
    #     "pipeline-sql-path": f"pipelines/5 Table Path Query/baseline.sql",
    #     "dataset-path": f"data/tpch_data/sf_1.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_1.0/5 Table Path Query/baseline"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Table Path Query/decomposition_full.sql",
    #     "dataset-path": f"data/tpch_data/sf_1.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_1.0/5 Table Path Query/decomposition_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Table Path Query/decomposition_faq.sql",
    #     "dataset-path": f"data/tpch_data/sf_1.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_1.0/5 Table Path Query/decomposition_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Table Path Query/decomposition_no_projection_full.sql",
    #     "dataset-path": f"data/tpch_data/sf_1.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_1.0/5 Table Path Query/decomposition_no_projection_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Table Path Query/decomposition_no_projection_faq.sql",
    #     "dataset-path": f"data/tpch_data/sf_1.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_1.0/5 Table Path Query/decomposition_no_projection_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Table Path Query/decomposition_no_projection.sql",
    #     "dataset-path": f"data/tpch_data/sf_1.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_1.0/5 Table Path Query/decomposition_no_projection"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Table Path Query/decomposition.sql",
    #     "dataset-path": f"data/tpch_data/sf_1.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_1.0/5 Table Path Query/decomposition"
    # },

    # ---- 5 Table Path Query - tpc-h - sf_10.0 ----
    # {
    #     "pipeline-sql-path": f"pipelines/5 Table Path Query/baseline.sql",
    #     "dataset-path": f"data/tpch_data/sf_10.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_10.0/5 Table Path Query/baseline"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Table Path Query/decomposition_full.sql",
    #     "dataset-path": f"data/tpch_data/sf_10.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_10.0/5 Table Path Query/decomposition_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Table Path Query/decomposition_faq.sql",
    #     "dataset-path": f"data/tpch_data/sf_10.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_10.0/5 Table Path Query/decomposition_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Table Path Query/decomposition_no_projection_full.sql",
    #     "dataset-path": f"data/tpch_data/sf_10.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_10.0/5 Table Path Query/decomposition_no_projection_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Table Path Query/decomposition_no_projection_faq.sql",
    #     "dataset-path": f"data/tpch_data/sf_10.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_10.0/5 Table Path Query/decomposition_no_projection_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Table Path Query/decomposition_no_projection.sql",
    #     "dataset-path": f"data/tpch_data/sf_10.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_10.0/5 Table Path Query/decomposition_no_projection"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Table Path Query/decomposition.sql",
    #     "dataset-path": f"data/tpch_data/sf_10.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_10.0/5 Table Path Query/decomposition"
    # },

    # ---- 5 Table Path Query - tpc-h - sf_30.0 ----
    # {
    #     "pipeline-sql-path": f"pipelines/5 Table Path Query/baseline.sql",
    #     "dataset-path": f"data/tpch_data/sf_30.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_30.0/5 Table Path Query/baseline"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Table Path Query/decomposition_full.sql",
    #     "dataset-path": f"data/tpch_data/sf_30.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_30.0/5 Table Path Query/decomposition_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Table Path Query/decomposition_faq.sql",
    #     "dataset-path": f"data/tpch_data/sf_30.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_30.0/5 Table Path Query/decomposition_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Table Path Query/decomposition_no_projection_full.sql",
    #     "dataset-path": f"data/tpch_data/sf_30.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_30.0/5 Table Path Query/decomposition_no_projection_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Table Path Query/decomposition_no_projection_faq.sql",
    #     "dataset-path": f"data/tpch_data/sf_30.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_30.0/5 Table Path Query/decomposition_no_projection_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Table Path Query/decomposition_no_projection.sql",
    #     "dataset-path": f"data/tpch_data/sf_30.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_30.0/5 Table Path Query/decomposition_no_projection"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Table Path Query/decomposition.sql",
    #     "dataset-path": f"data/tpch_data/sf_30.0",
    #     "trials": 3,
    #     "output-dir": f"results/tpch_data/sf_30.0/5 Table Path Query/decomposition"
    # },


    # ---- 3 Table Path Query - tpc-h - sf_1.0 ----
    {
        "pipeline-sql-path": f"pipelines/3 Table Path Query/baseline.sql",
        "dataset-path": f"data/tpch_data/sf_1.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_1.0/3 Table Path Query/baseline"
    },
    {
        "pipeline-sql-path": f"pipelines/3 Table Path Query/decomposition_full.sql",
        "dataset-path": f"data/tpch_data/sf_1.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_1.0/3 Table Path Query/decomposition_full"
    },
    {
        "pipeline-sql-path": f"pipelines/3 Table Path Query/decomposition_faq.sql",
        "dataset-path": f"data/tpch_data/sf_1.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_1.0/3 Table Path Query/decomposition_faq"
    },
    {
        "pipeline-sql-path": f"pipelines/3 Table Path Query/decomposition_no_projection_full.sql",
        "dataset-path": f"data/tpch_data/sf_1.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_1.0/3 Table Path Query/decomposition_no_projection_full"
    },
    {
        "pipeline-sql-path": f"pipelines/3 Table Path Query/decomposition_no_projection_faq.sql",
        "dataset-path": f"data/tpch_data/sf_1.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_1.0/3 Table Path Query/decomposition_no_projection_faq"
    },
    {
        "pipeline-sql-path": f"pipelines/3 Table Path Query/decomposition_no_projection.sql",
        "dataset-path": f"data/tpch_data/sf_1.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_1.0/3 Table Path Query/decomposition_no_projection"
    },
    {
        "pipeline-sql-path": f"pipelines/3 Table Path Query/decomposition.sql",
        "dataset-path": f"data/tpch_data/sf_1.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_1.0/3 Table Path Query/decomposition"
    },

    # ---- 3 Table Path Query - tpc-h - sf_10.0 ----
    {
        "pipeline-sql-path": f"pipelines/3 Table Path Query/baseline.sql",
        "dataset-path": f"data/tpch_data/sf_10.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_10.0/3 Table Path Query/baseline"
    },
    {
        "pipeline-sql-path": f"pipelines/3 Table Path Query/decomposition_full.sql",
        "dataset-path": f"data/tpch_data/sf_10.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_10.0/3 Table Path Query/decomposition_full"
    },
    {
        "pipeline-sql-path": f"pipelines/3 Table Path Query/decomposition_faq.sql",
        "dataset-path": f"data/tpch_data/sf_10.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_10.0/3 Table Path Query/decomposition_faq"
    },
    {
        "pipeline-sql-path": f"pipelines/3 Table Path Query/decomposition_no_projection_full.sql",
        "dataset-path": f"data/tpch_data/sf_10.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_10.0/3 Table Path Query/decomposition_no_projection_full"
    },
    {
        "pipeline-sql-path": f"pipelines/3 Table Path Query/decomposition_no_projection_faq.sql",
        "dataset-path": f"data/tpch_data/sf_10.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_10.0/3 Table Path Query/decomposition_no_projection_faq"
    },
    {
        "pipeline-sql-path": f"pipelines/3 Table Path Query/decomposition_no_projection.sql",
        "dataset-path": f"data/tpch_data/sf_10.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_10.0/3 Table Path Query/decomposition_no_projection"
    },
    {
        "pipeline-sql-path": f"pipelines/3 Table Path Query/decomposition.sql",
        "dataset-path": f"data/tpch_data/sf_10.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_10.0/3 Table Path Query/decomposition"
    },

    # ---- 3 Table Path Query - tpc-h - sf_30.0 ----
    {
        "pipeline-sql-path": f"pipelines/3 Table Path Query/baseline.sql",
        "dataset-path": f"data/tpch_data/sf_30.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_30.0/3 Table Path Query/baseline"
    },
    {
        "pipeline-sql-path": f"pipelines/3 Table Path Query/decomposition_full.sql",
        "dataset-path": f"data/tpch_data/sf_30.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_30.0/3 Table Path Query/decomposition_full"
    },
    {
        "pipeline-sql-path": f"pipelines/3 Table Path Query/decomposition_faq.sql",
        "dataset-path": f"data/tpch_data/sf_30.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_30.0/3 Table Path Query/decomposition_faq"
    },
    {
        "pipeline-sql-path": f"pipelines/3 Table Path Query/decomposition_no_projection_full.sql",
        "dataset-path": f"data/tpch_data/sf_30.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_30.0/3 Table Path Query/decomposition_no_projection_full"
    },
    {
        "pipeline-sql-path": f"pipelines/3 Table Path Query/decomposition_no_projection_faq.sql",
        "dataset-path": f"data/tpch_data/sf_30.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_30.0/3 Table Path Query/decomposition_no_projection_faq"
    },
    {
        "pipeline-sql-path": f"pipelines/3 Table Path Query/decomposition_no_projection.sql",
        "dataset-path": f"data/tpch_data/sf_30.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_30.0/3 Table Path Query/decomposition_no_projection"
    },
    {
        "pipeline-sql-path": f"pipelines/3 Table Path Query/decomposition.sql",
        "dataset-path": f"data/tpch_data/sf_30.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_30.0/3 Table Path Query/decomposition"
    },


    # ---- Cyclic Query 7 - tpc-h - sf_1.0 ----
    {
        "pipeline-sql-path": f"pipelines/Cyclic Query 7/baseline.sql",
        "dataset-path": f"data/tpch_data/sf_1.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_1.0/Cyclic Query 7/baseline"
    },
    {
        "pipeline-sql-path": f"pipelines/Cyclic Query 7/decomposition_full.sql",
        "dataset-path": f"data/tpch_data/sf_1.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_1.0/Cyclic Query 7/decomposition_full"
    },
    {
        "pipeline-sql-path": f"pipelines/Cyclic Query 7/decomposition_faq.sql",
        "dataset-path": f"data/tpch_data/sf_1.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_1.0/Cyclic Query 7/decomposition_faq"
    },
    {
        "pipeline-sql-path": f"pipelines/Cyclic Query 7/decomposition_no_projection_full.sql",
        "dataset-path": f"data/tpch_data/sf_1.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_1.0/Cyclic Query 7/decomposition_no_projection_full"
    },
    {
        "pipeline-sql-path": f"pipelines/Cyclic Query 7/decomposition_no_projection_faq.sql",
        "dataset-path": f"data/tpch_data/sf_1.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_1.0/Cyclic Query 7/decomposition_no_projection_faq"
    },
    {
        "pipeline-sql-path": f"pipelines/Cyclic Query 7/decomposition_no_projection.sql",
        "dataset-path": f"data/tpch_data/sf_1.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_1.0/Cyclic Query 7/decomposition_no_projection"
    },
    {
        "pipeline-sql-path": f"pipelines/Cyclic Query 7/decomposition.sql",
        "dataset-path": f"data/tpch_data/sf_1.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_1.0/Cyclic Query 7/decomposition"
    },

    # ---- Cyclic Query 7 - tpc-h - sf_10.0 ----
    {
        "pipeline-sql-path": f"pipelines/Cyclic Query 7/baseline.sql",
        "dataset-path": f"data/tpch_data/sf_10.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_10.0/Cyclic Query 7/baseline"
    },
    {
        "pipeline-sql-path": f"pipelines/Cyclic Query 7/decomposition_full.sql",
        "dataset-path": f"data/tpch_data/sf_10.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_10.0/Cyclic Query 7/decomposition_full"
    },
    {
        "pipeline-sql-path": f"pipelines/Cyclic Query 7/decomposition_faq.sql",
        "dataset-path": f"data/tpch_data/sf_10.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_10.0/Cyclic Query 7/decomposition_faq"
    },
    {
        "pipeline-sql-path": f"pipelines/Cyclic Query 7/decomposition_no_projection_full.sql",
        "dataset-path": f"data/tpch_data/sf_10.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_10.0/Cyclic Query 7/decomposition_no_projection_full"
    },
    {
        "pipeline-sql-path": f"pipelines/Cyclic Query 7/decomposition_no_projection_faq.sql",
        "dataset-path": f"data/tpch_data/sf_10.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_10.0/Cyclic Query 7/decomposition_no_projection_faq"
    },
    {
        "pipeline-sql-path": f"pipelines/Cyclic Query 7/decomposition_no_projection.sql",
        "dataset-path": f"data/tpch_data/sf_10.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_10.0/Cyclic Query 7/decomposition_no_projection"
    },
    {
        "pipeline-sql-path": f"pipelines/Cyclic Query 7/decomposition.sql",
        "dataset-path": f"data/tpch_data/sf_10.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_10.0/Cyclic Query 7/decomposition"
    },

    # ---- Cyclic Query 7 - tpc-h - sf_30.0 ----
    {
        "pipeline-sql-path": f"pipelines/Cyclic Query 7/baseline.sql",
        "dataset-path": f"data/tpch_data/sf_30.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_30.0/Cyclic Query 7/baseline"
    },
    {
        "pipeline-sql-path": f"pipelines/Cyclic Query 7/decomposition_full.sql",
        "dataset-path": f"data/tpch_data/sf_30.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_30.0/Cyclic Query 7/decomposition_full"
    },
    {
        "pipeline-sql-path": f"pipelines/Cyclic Query 7/decomposition_faq.sql",
        "dataset-path": f"data/tpch_data/sf_30.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_30.0/Cyclic Query 7/decomposition_faq"
    },
    {
        "pipeline-sql-path": f"pipelines/Cyclic Query 7/decomposition_no_projection_full.sql",
        "dataset-path": f"data/tpch_data/sf_30.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_30.0/Cyclic Query 7/decomposition_no_projection_full"
    },
    {
        "pipeline-sql-path": f"pipelines/Cyclic Query 7/decomposition_no_projection_faq.sql",
        "dataset-path": f"data/tpch_data/sf_30.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_30.0/Cyclic Query 7/decomposition_no_projection_faq"
    },
    {
        "pipeline-sql-path": f"pipelines/Cyclic Query 7/decomposition_no_projection.sql",
        "dataset-path": f"data/tpch_data/sf_30.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_30.0/Cyclic Query 7/decomposition_no_projection"
    },
    {
        "pipeline-sql-path": f"pipelines/Cyclic Query 7/decomposition.sql",
        "dataset-path": f"data/tpch_data/sf_30.0",
        "trials": 3,
        "output-dir": f"results/tpch_data/sf_30.0/Cyclic Query 7/decomposition"
    },


    # ---- 5 Path Query - soc-Epinions1 ----
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/baseline_1_table.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/5 Path Query/baseline_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/baseline_5_tables.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/5 Path Query/baseline_5_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/chain_decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/5 Path Query/chain_decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/chain_decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/5 Path Query/chain_decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/chain_decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/5 Path Query/chain_decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/chain_decomposition_no_projection_5_tables_full.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/5 Path Query/chain_decomposition_no_projection_5_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/chain_decomposition_no_projection_5_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/5 Path Query/chain_decomposition_no_projection_5_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/chain_decomposition_no_projection_5_tables.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/5 Path Query/chain_decomposition_no_projection_5_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/5 Path Query/decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/5 Path Query/decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/5 Path Query/decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/decomposition_no_projection_5_tables_full.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/5 Path Query/decomposition_no_projection_5_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/decomposition_no_projection_5_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/5 Path Query/decomposition_no_projection_5_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/decomposition_no_projection_5_tables.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/5 Path Query/decomposition_no_projection_5_tables"
    # },

    # ---- 5 Path Query - p2p-Gnutella31 ----
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/baseline_1_table.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/5 Path Query/baseline_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/baseline_5_tables.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/5 Path Query/baseline_5_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/chain_decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/5 Path Query/chain_decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/chain_decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/5 Path Query/chain_decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/chain_decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/5 Path Query/chain_decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/chain_decomposition_no_projection_5_tables_full.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/5 Path Query/chain_decomposition_no_projection_5_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/chain_decomposition_no_projection_5_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/5 Path Query/chain_decomposition_no_projection_5_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/chain_decomposition_no_projection_5_tables.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/5 Path Query/chain_decomposition_no_projection_5_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/5 Path Query/decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/5 Path Query/decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/5 Path Query/decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/decomposition_no_projection_5_tables_full.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/5 Path Query/decomposition_no_projection_5_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/decomposition_no_projection_5_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/5 Path Query/decomposition_no_projection_5_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/decomposition_no_projection_5_tables.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/5 Path Query/decomposition_no_projection_5_tables"
    # },

    # ---- 5 Path Query - cit-HepTh ----
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/baseline_1_table.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/5 Path Query/baseline_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/baseline_5_tables.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/5 Path Query/baseline_5_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/chain_decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/5 Path Query/chain_decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/chain_decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/5 Path Query/chain_decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/chain_decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/5 Path Query/chain_decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/chain_decomposition_no_projection_5_tables_full.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/5 Path Query/chain_decomposition_no_projection_5_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/chain_decomposition_no_projection_5_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/5 Path Query/chain_decomposition_no_projection_5_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/chain_decomposition_no_projection_5_tables.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/5 Path Query/chain_decomposition_no_projection_5_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/5 Path Query/decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/5 Path Query/decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/5 Path Query/decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/decomposition_no_projection_5_tables_full.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/5 Path Query/decomposition_no_projection_5_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/decomposition_no_projection_5_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/5 Path Query/decomposition_no_projection_5_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/5 Path Query/decomposition_no_projection_5_tables.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/5 Path Query/decomposition_no_projection_5_tables"
    # },


    # ---- Cyclic Query 1 - soc-Epinions1 ----
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/baseline_1_table.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 1/baseline_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/baseline_9_tables.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 1/baseline_9_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/chain_decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 1/chain_decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/chain_decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 1/chain_decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/chain_decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 1/chain_decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/chain_decomposition_no_projection_9_tables_full.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 1/chain_decomposition_no_projection_9_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/chain_decomposition_no_projection_9_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 1/chain_decomposition_no_projection_9_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/chain_decomposition_no_projection_9_tables.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 1/chain_decomposition_no_projection_9_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 1/decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 1/decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 1/decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/decomposition_no_projection_9_tables_full.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 1/decomposition_no_projection_9_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/decomposition_no_projection_9_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 1/decomposition_no_projection_9_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/decomposition_no_projection_9_tables.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 1/decomposition_no_projection_9_tables"
    # },

    # ---- Cyclic Query 1 - p2p-Gnutella31 ----
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/baseline_1_table.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 1/baseline_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/baseline_9_tables.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 1/baseline_9_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/chain_decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 1/chain_decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/chain_decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 1/chain_decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/chain_decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 1/chain_decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/chain_decomposition_no_projection_9_tables_full.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 1/chain_decomposition_no_projection_9_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/chain_decomposition_no_projection_9_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 1/chain_decomposition_no_projection_9_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/chain_decomposition_no_projection_9_tables.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 1/chain_decomposition_no_projection_9_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 1/decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 1/decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 1/decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/decomposition_no_projection_9_tables_full.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 1/decomposition_no_projection_9_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/decomposition_no_projection_9_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 1/decomposition_no_projection_9_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/decomposition_no_projection_9_tables.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 1/decomposition_no_projection_9_tables"
    # },

    # ---- Cyclic Query 1 - cit-HepTh ----
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/baseline_1_table.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 1/baseline_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/baseline_9_tables.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 1/baseline_9_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/chain_decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 1/chain_decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/chain_decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 1/chain_decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/chain_decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 1/chain_decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/chain_decomposition_no_projection_9_tables_full.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 1/chain_decomposition_no_projection_9_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/chain_decomposition_no_projection_9_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 1/chain_decomposition_no_projection_9_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/chain_decomposition_no_projection_9_tables.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 1/chain_decomposition_no_projection_9_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 1/decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 1/decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 1/decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/decomposition_no_projection_9_tables_full.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 1/decomposition_no_projection_9_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/decomposition_no_projection_9_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 1/decomposition_no_projection_9_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 1/decomposition_no_projection_9_tables.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 1/decomposition_no_projection_9_tables"
    # },


    # ---- Cyclic Query 2 - soc-Epinions1 ----
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/baseline_1_table.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 2/baseline_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/baseline_8_tables.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 2/baseline_8_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/chain_decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 2/chain_decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/chain_decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 2/chain_decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/chain_decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 2/chain_decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/chain_decomposition_no_projection_8_tables_full.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 2/chain_decomposition_no_projection_8_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/chain_decomposition_no_projection_8_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 2/chain_decomposition_no_projection_8_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/chain_decomposition_no_projection_8_tables.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 2/chain_decomposition_no_projection_8_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 2/decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 2/decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 2/decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/decomposition_no_projection_8_tables_full.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 2/decomposition_no_projection_8_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/decomposition_no_projection_8_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 2/decomposition_no_projection_8_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/decomposition_no_projection_8_tables.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 2/decomposition_no_projection_8_tables"
    # },

    # ---- Cyclic Query 2 - p2p-Gnutella31 ----
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/baseline_1_table.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 2/baseline_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/baseline_8_tables.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 2/baseline_8_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/chain_decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 2/chain_decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/chain_decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 2/chain_decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/chain_decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 2/chain_decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/chain_decomposition_no_projection_8_tables_full.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 2/chain_decomposition_no_projection_8_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/chain_decomposition_no_projection_8_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 2/chain_decomposition_no_projection_8_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/chain_decomposition_no_projection_8_tables.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 2/chain_decomposition_no_projection_8_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 2/decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 2/decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 2/decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/decomposition_no_projection_8_tables_full.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 2/decomposition_no_projection_8_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/decomposition_no_projection_8_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 2/decomposition_no_projection_8_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/decomposition_no_projection_8_tables.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 2/decomposition_no_projection_8_tables"
    # },

    # ---- Cyclic Query 2 - cit-HepTh ----
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/baseline_1_table.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 2/baseline_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/baseline_8_tables.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 2/baseline_8_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/chain_decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 2/chain_decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/chain_decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 2/chain_decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/chain_decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 2/chain_decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/chain_decomposition_no_projection_8_tables_full.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 2/chain_decomposition_no_projection_8_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/chain_decomposition_no_projection_8_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 2/chain_decomposition_no_projection_8_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/chain_decomposition_no_projection_8_tables.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 2/chain_decomposition_no_projection_8_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 2/decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 2/decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 2/decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/decomposition_no_projection_8_tables_full.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 2/decomposition_no_projection_8_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/decomposition_no_projection_8_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 2/decomposition_no_projection_8_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 2/decomposition_no_projection_8_tables.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 2/decomposition_no_projection_8_tables"
    # },


    # ---- Cyclic Query 3 - soc-Epinions1 ----
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 3/baseline_1_table.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 3/baseline_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 3/baseline_5_tables.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 3/baseline_5_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 3/chain_decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 3/chain_decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 3/chain_decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 3/chain_decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 3/chain_decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 3/chain_decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 3/chain_decomposition_no_projection_5_tables_full.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 3/chain_decomposition_no_projection_5_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 3/chain_decomposition_no_projection_5_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 3/chain_decomposition_no_projection_5_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 3/chain_decomposition_no_projection_5_tables.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 3/chain_decomposition_no_projection_5_tables"
    # },

    # ---- Cyclic Query 3 - p2p-Gnutella31 ----
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 3/baseline_1_table.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 3/baseline_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 3/baseline_5_tables.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 3/baseline_5_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 3/chain_decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 3/chain_decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 3/chain_decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 3/chain_decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 3/chain_decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 3/chain_decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 3/chain_decomposition_no_projection_5_tables_full.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 3/chain_decomposition_no_projection_5_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 3/chain_decomposition_no_projection_5_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 3/chain_decomposition_no_projection_5_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 3/chain_decomposition_no_projection_5_tables.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 3/chain_decomposition_no_projection_5_tables"
    # },

    # ---- Cyclic Query 3 - cit-HepTh ----
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 3/baseline_1_table.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 3/baseline_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 3/baseline_5_tables.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 3/baseline_5_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 3/chain_decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 3/chain_decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 3/chain_decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 3/chain_decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 3/chain_decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 3/chain_decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 3/chain_decomposition_no_projection_5_tables_full.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 3/chain_decomposition_no_projection_5_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 3/chain_decomposition_no_projection_5_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 3/chain_decomposition_no_projection_5_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 3/chain_decomposition_no_projection_5_tables.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 3/chain_decomposition_no_projection_5_tables"
    # },


    # ---- Cyclic Query 4 - soc-Epinions1 ----
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/baseline_1_table.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 4/baseline_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/baseline_6_tables.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 4/baseline_6_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/chain_decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 4/chain_decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/chain_decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 4/chain_decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/chain_decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 4/chain_decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/chain_decomposition_no_projection_6_tables_full.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 4/chain_decomposition_no_projection_6_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/chain_decomposition_no_projection_6_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 4/chain_decomposition_no_projection_6_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/chain_decomposition_no_projection_6_tables.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 4/chain_decomposition_no_projection_6_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 4/decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 4/decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 4/decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/decomposition_no_projection_6_tables_full.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 4/decomposition_no_projection_6_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/decomposition_no_projection_6_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 4/decomposition_no_projection_6_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/decomposition_no_projection_6_tables.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 4/decomposition_no_projection_6_tables"
    # },

    # ---- Cyclic Query 4 - p2p-Gnutella31 ----
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/baseline_1_table.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 4/baseline_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/baseline_6_tables.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 4/baseline_6_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/chain_decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 4/chain_decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/chain_decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 4/chain_decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/chain_decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 4/chain_decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/chain_decomposition_no_projection_6_tables_full.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 4/chain_decomposition_no_projection_6_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/chain_decomposition_no_projection_6_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 4/chain_decomposition_no_projection_6_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/chain_decomposition_no_projection_6_tables.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 4/chain_decomposition_no_projection_6_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 4/decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 4/decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 4/decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/decomposition_no_projection_6_tables_full.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 4/decomposition_no_projection_6_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/decomposition_no_projection_6_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 4/decomposition_no_projection_6_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/decomposition_no_projection_6_tables.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 4/decomposition_no_projection_6_tables"
    # },

    # ---- Cyclic Query 4 - cit-HepTh ----
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/baseline_1_table.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 4/baseline_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/baseline_6_tables.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 4/baseline_6_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/chain_decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 4/chain_decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/chain_decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 4/chain_decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/chain_decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 4/chain_decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/chain_decomposition_no_projection_6_tables_full.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 4/chain_decomposition_no_projection_6_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/chain_decomposition_no_projection_6_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 4/chain_decomposition_no_projection_6_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/chain_decomposition_no_projection_6_tables.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 4/chain_decomposition_no_projection_6_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 4/decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 4/decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 4/decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/decomposition_no_projection_6_tables_full.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 4/decomposition_no_projection_6_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/decomposition_no_projection_6_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 4/decomposition_no_projection_6_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 4/decomposition_no_projection_6_tables.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 4/decomposition_no_projection_6_tables"
    # },


    # ---- Cyclic Query 5 - soc-Epinions1 ----
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/baseline_1_table.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 5/baseline_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/baseline_5_tables.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 5/baseline_5_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/chain_decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 5/chain_decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/chain_decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 5/chain_decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/chain_decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 5/chain_decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/chain_decomposition_no_projection_5_tables_full.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 5/chain_decomposition_no_projection_5_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/chain_decomposition_no_projection_5_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 5/chain_decomposition_no_projection_5_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/chain_decomposition_no_projection_5_tables.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 5/chain_decomposition_no_projection_5_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 5/decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 5/decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 5/decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/decomposition_no_projection_5_tables_full.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 5/decomposition_no_projection_5_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/decomposition_no_projection_5_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 5/decomposition_no_projection_5_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/decomposition_no_projection_5_tables.sql",
    #     "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #     "trials": 3,
    #     "output-dir": f"results/soc-Epinions1/Cyclic Query 5/decomposition_no_projection_5_tables"
    # },

    # ---- Cyclic Query 5 - p2p-Gnutella31 ----
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/baseline_1_table.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 5/baseline_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/baseline_5_tables.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 5/baseline_5_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/chain_decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 5/chain_decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/chain_decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 5/chain_decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/chain_decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 5/chain_decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/chain_decomposition_no_projection_5_tables_full.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 5/chain_decomposition_no_projection_5_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/chain_decomposition_no_projection_5_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 5/chain_decomposition_no_projection_5_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/chain_decomposition_no_projection_5_tables.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 5/chain_decomposition_no_projection_5_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 5/decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 5/decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 5/decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/decomposition_no_projection_5_tables_full.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 5/decomposition_no_projection_5_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/decomposition_no_projection_5_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 5/decomposition_no_projection_5_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/decomposition_no_projection_5_tables.sql",
    #     "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #     "trials": 3,
    #     "output-dir": f"results/p2p-Gnutella31/Cyclic Query 5/decomposition_no_projection_5_tables"
    # },

    # ---- Cyclic Query 5 - cit-HepTh ----
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/baseline_1_table.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 5/baseline_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/baseline_5_tables.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 5/baseline_5_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/chain_decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 5/chain_decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/chain_decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 5/chain_decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/chain_decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 5/chain_decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/chain_decomposition_no_projection_5_tables_full.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 5/chain_decomposition_no_projection_5_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/chain_decomposition_no_projection_5_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 5/chain_decomposition_no_projection_5_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/chain_decomposition_no_projection_5_tables.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 5/chain_decomposition_no_projection_5_tables"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/decomposition_no_projection_1_table_full.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 5/decomposition_no_projection_1_table_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/decomposition_no_projection_1_table_faq.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 5/decomposition_no_projection_1_table_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/decomposition_no_projection_1_table.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 5/decomposition_no_projection_1_table"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/decomposition_no_projection_5_tables_full.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 5/decomposition_no_projection_5_tables_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/decomposition_no_projection_5_tables_faq.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 5/decomposition_no_projection_5_tables_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Cyclic Query 5/decomposition_no_projection_5_tables.sql",
    #     "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #     "trials": 3,
    #     "output-dir": f"results/cit-HepTh/Cyclic Query 5/decomposition_no_projection_5_tables"
    # },


    # ---- Cyclic Query 6 - soc-Epinions1 ----
    #  {
    #      "pipeline-sql-path": f"pipelines/Cyclic Query 6/baseline_1_table.sql",
    #      "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #      "trials": 3,
    #      "output-dir": f"results/soc-Epinions1/Cyclic Query 6/baseline_1_table"
    #  },
    #  {
    #      "pipeline-sql-path": f"pipelines/Cyclic Query 6/baseline_4_tables.sql",
    #      "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #      "trials": 3,
    #      "output-dir": f"results/soc-Epinions1/Cyclic Query 6/baseline_4_tables"
    #  },
    #  {
    #      "pipeline-sql-path": f"pipelines/Cyclic Query 6/chain_decomposition_no_projection_1_table_full.sql",
    #      "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #      "trials": 3,
    #      "output-dir": f"results/soc-Epinions1/Cyclic Query 6/chain_decomposition_no_projection_1_table_full"
    #  },
    #  {
    #      "pipeline-sql-path": f"pipelines/Cyclic Query 6/chain_decomposition_no_projection_1_table_faq.sql",
    #      "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #      "trials": 3,
    #      "output-dir": f"results/soc-Epinions1/Cyclic Query 6/chain_decomposition_no_projection_1_table_faq"
    #  },
    #  {
    #      "pipeline-sql-path": f"pipelines/Cyclic Query 6/chain_decomposition_no_projection_1_table.sql",
    #      "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #      "trials": 3,
    #      "output-dir": f"results/soc-Epinions1/Cyclic Query 6/chain_decomposition_no_projection_1_table"
    #  },
    #  {
    #      "pipeline-sql-path": f"pipelines/Cyclic Query 6/chain_decomposition_no_projection_4_tables_full.sql",
    #      "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #      "trials": 3,
    #      "output-dir": f"results/soc-Epinions1/Cyclic Query 6/chain_decomposition_no_projection_4_tables_full"
    #  },
    #  {
    #      "pipeline-sql-path": f"pipelines/Cyclic Query 6/chain_decomposition_no_projection_4_tables_faq.sql",
    #      "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #      "trials": 3,
    #      "output-dir": f"results/soc-Epinions1/Cyclic Query 6/chain_decomposition_no_projection_4_tables_faq"
    #  },
    #  {
    #      "pipeline-sql-path": f"pipelines/Cyclic Query 6/chain_decomposition_no_projection_4_tables.sql",
    #      "dataset-path": f"data/snap_data/soc-Epinions1.csv",
    #      "trials": 3,
    #      "output-dir": f"results/soc-Epinions1/Cyclic Query 6/chain_decomposition_no_projection_4_tables"
    #  },

    # ---- Cyclic Query 6 - p2p-Gnutella31 ----
    #  {
    #      "pipeline-sql-path": f"pipelines/Cyclic Query 6/baseline_1_table.sql",
    #      "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #      "trials": 3,
    #      "output-dir": f"results/p2p-Gnutella31/Cyclic Query 6/baseline_1_table"
    #  },
    #  {
    #      "pipeline-sql-path": f"pipelines/Cyclic Query 6/baseline_4_tables.sql",
    #      "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #      "trials": 3,
    #      "output-dir": f"results/p2p-Gnutella31/Cyclic Query 6/baseline_4_tables"
    #  },
    #  {
    #      "pipeline-sql-path": f"pipelines/Cyclic Query 6/chain_decomposition_no_projection_1_table_full.sql",
    #      "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #      "trials": 3,
    #      "output-dir": f"results/p2p-Gnutella31/Cyclic Query 6/chain_decomposition_no_projection_1_table_full"
    #  },
    #  {
    #      "pipeline-sql-path": f"pipelines/Cyclic Query 6/chain_decomposition_no_projection_1_table_faq.sql",
    #      "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #      "trials": 3,
    #      "output-dir": f"results/p2p-Gnutella31/Cyclic Query 6/chain_decomposition_no_projection_1_table_faq"
    #  },
    #  {
    #      "pipeline-sql-path": f"pipelines/Cyclic Query 6/chain_decomposition_no_projection_1_table.sql",
    #      "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #      "trials": 3,
    #      "output-dir": f"results/p2p-Gnutella31/Cyclic Query 6/chain_decomposition_no_projection_1_table"
    #  },
    #  {
    #      "pipeline-sql-path": f"pipelines/Cyclic Query 6/chain_decomposition_no_projection_4_tables_full.sql",
    #      "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #      "trials": 3,
    #      "output-dir": f"results/p2p-Gnutella31/Cyclic Query 6/chain_decomposition_no_projection_4_tables_full"
    #  },
    #  {
    #      "pipeline-sql-path": f"pipelines/Cyclic Query 6/chain_decomposition_no_projection_4_tables_faq.sql",
    #      "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #      "trials": 3,
    #      "output-dir": f"results/p2p-Gnutella31/Cyclic Query 6/chain_decomposition_no_projection_4_tables_faq"
    #  },
    #  {
    #      "pipeline-sql-path": f"pipelines/Cyclic Query 6/chain_decomposition_no_projection_4_tables.sql",
    #      "dataset-path": f"data/snap_data/p2p-Gnutella31.csv",
    #      "trials": 3,
    #      "output-dir": f"results/p2p-Gnutella31/Cyclic Query 6/chain_decomposition_no_projection_4_tables"
    #  },

    # ---- Cyclic Query 6 - cit-HepTh ----
    #  {
    #      "pipeline-sql-path": f"pipelines/Cyclic Query 6/baseline_1_table.sql",
    #      "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #      "trials": 3,
    #      "output-dir": f"results/cit-HepTh/Cyclic Query 6/baseline_1_table"
    #  },
    #  {
    #      "pipeline-sql-path": f"pipelines/Cyclic Query 6/baseline_4_tables.sql",
    #      "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #      "trials": 3,
    #      "output-dir": f"results/cit-HepTh/Cyclic Query 6/baseline_4_tables"
    #  },
    #  {
    #      "pipeline-sql-path": f"pipelines/Cyclic Query 6/chain_decomposition_no_projection_1_table_full.sql",
    #      "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #      "trials": 3,
    #      "output-dir": f"results/cit-HepTh/Cyclic Query 6/chain_decomposition_no_projection_1_table_full"
    #  },
    #  {
    #      "pipeline-sql-path": f"pipelines/Cyclic Query 6/chain_decomposition_no_projection_1_table_faq.sql",
    #      "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #      "trials": 3,
    #      "output-dir": f"results/cit-HepTh/Cyclic Query 6/chain_decomposition_no_projection_1_table_faq"
    #  },
    #  {
    #      "pipeline-sql-path": f"pipelines/Cyclic Query 6/chain_decomposition_no_projection_1_table.sql",
    #      "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #      "trials": 3,
    #      "output-dir": f"results/cit-HepTh/Cyclic Query 6/chain_decomposition_no_projection_1_table"
    #  },
    #  {
    #      "pipeline-sql-path": f"pipelines/Cyclic Query 6/chain_decomposition_no_projection_4_tables_full.sql",
    #      "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #      "trials": 3,
    #      "output-dir": f"results/cit-HepTh/Cyclic Query 6/chain_decomposition_no_projection_4_tables_full"
    #  },
    #  {
    #      "pipeline-sql-path": f"pipelines/Cyclic Query 6/chain_decomposition_no_projection_4_tables_faq.sql",
    #      "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #      "trials": 3,
    #      "output-dir": f"results/cit-HepTh/Cyclic Query 6/chain_decomposition_no_projection_4_tables_faq"
    #  },
    #  {
    #      "pipeline-sql-path": f"pipelines/Cyclic Query 6/chain_decomposition_no_projection_4_tables.sql",
    #      "dataset-path": f"data/snap_data/cit-HepTh.csv",
    #      "trials": 3,
    #      "output-dir": f"results/cit-HepTh/Cyclic Query 6/chain_decomposition_no_projection_4_tables"
    #  },


    # ---- Acyclic Query 1 - IMDB ----
    # {
    #     "pipeline-sql-path": f"pipelines/Acyclic Query 1/baseline.sql",
    #     "dataset-path": f"data/imdb_data",
    #     "trials": 3,
    #     "output-dir": f"results/imdb/Acyclic Query 1/baseline"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Acyclic Query 1/chain_decomposition_full.sql",
    #     "dataset-path": f"data/imdb_data",
    #     "trials": 3,
    #     "output-dir": f"results/imdb/Acyclic Query 1/chain_decomposition_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Acyclic Query 1/chain_decomposition_faq.sql",
    #     "dataset-path": f"data/imdb_data",
    #     "trials": 3,
    #     "output-dir": f"results/imdb/Acyclic Query 1/chain_decomposition_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Acyclic Query 1/chain_decomposition_no_projection_full.sql",
    #     "dataset-path": f"data/imdb_data",
    #     "trials": 3,
    #     "output-dir": f"results/imdb/Acyclic Query 1/chain_decomposition_no_projection_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Acyclic Query 1/chain_decomposition_no_projection_faq.sql",
    #     "dataset-path": f"data/imdb_data",
    #     "trials": 3,
    #     "output-dir": f"results/imdb/Acyclic Query 1/chain_decomposition_no_projection_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Acyclic Query 1/chain_decomposition_no_projection.sql",
    #     "dataset-path": f"data/imdb_data",
    #     "trials": 3,
    #     "output-dir": f"results/imdb/Acyclic Query 1/chain_decomposition_no_projection"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Acyclic Query 1/chain_decomposition.sql",
    #     "dataset-path": f"data/imdb_data",
    #     "trials": 3,
    #     "output-dir": f"results/imdb/Acyclic Query 1/chain_decomposition"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Acyclic Query 1/decomposition_full.sql",
    #     "dataset-path": f"data/imdb_data",
    #     "trials": 3,
    #     "output-dir": f"results/imdb/Acyclic Query 1/decomposition_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Acyclic Query 1/decomposition_faq.sql",
    #     "dataset-path": f"data/imdb_data",
    #     "trials": 3,
    #     "output-dir": f"results/imdb/Acyclic Query 1/decomposition_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Acyclic Query 1/decomposition_no_projection_full.sql",
    #     "dataset-path": f"data/imdb_data",
    #     "trials": 3,
    #     "output-dir": f"results/imdb/Acyclic Query 1/decomposition_no_projection_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Acyclic Query 1/decomposition_no_projection_faq.sql",
    #     "dataset-path": f"data/imdb_data",
    #     "trials": 3,
    #     "output-dir": f"results/imdb/Acyclic Query 1/decomposition_no_projection_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Acyclic Query 1/decomposition_no_projection.sql",
    #     "dataset-path": f"data/imdb_data",
    #     "trials": 3,
    #     "output-dir": f"results/imdb/Acyclic Query 1/decomposition_no_projection"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Acyclic Query 1/decomposition.sql",
    #     "dataset-path": f"data/imdb_data",
    #     "trials": 3,
    #     "output-dir": f"results/imdb/Acyclic Query 1/decomposition"
    # },

    # ---- Acyclic Query 2 - IMDB ----
    # {
    #     "pipeline-sql-path": f"pipelines/Acyclic Query 2/baseline.sql",
    #     "dataset-path": f"data/imdb_data",
    #     "trials": 3,
    #     "output-dir": f"results/imdb/Acyclic Query 2/baseline"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Acyclic Query 2/chain_decomposition_full.sql",
    #     "dataset-path": f"data/imdb_data",
    #     "trials": 3,
    #     "output-dir": f"results/imdb/Acyclic Query 2/chain_decomposition_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Acyclic Query 2/chain_decomposition_faq.sql",
    #     "dataset-path": f"data/imdb_data",
    #     "trials": 3,
    #     "output-dir": f"results/imdb/Acyclic Query 2/chain_decomposition_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Acyclic Query 2/chain_decomposition_no_projection_full.sql",
    #     "dataset-path": f"data/imdb_data",
    #     "trials": 3,
    #     "output-dir": f"results/imdb/Acyclic Query 2/chain_decomposition_no_projection_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Acyclic Query 2/chain_decomposition_no_projection_faq.sql",
    #     "dataset-path": f"data/imdb_data",
    #     "trials": 3,
    #     "output-dir": f"results/imdb/Acyclic Query 2/chain_decomposition_no_projection_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Acyclic Query 2/chain_decomposition_no_projection.sql",
    #     "dataset-path": f"data/imdb_data",
    #     "trials": 3,
    #     "output-dir": f"results/imdb/Acyclic Query 2/chain_decomposition_no_projection"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Acyclic Query 2/chain_decomposition.sql",
    #     "dataset-path": f"data/imdb_data",
    #     "trials": 3,
    #     "output-dir": f"results/imdb/Acyclic Query 2/chain_decomposition"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Acyclic Query 2/decomposition_full.sql",
    #     "dataset-path": f"data/imdb_data",
    #     "trials": 3,
    #     "output-dir": f"results/imdb/Acyclic Query 2/decomposition_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Acyclic Query 2/decomposition_faq.sql",
    #     "dataset-path": f"data/imdb_data",
    #     "trials": 3,
    #     "output-dir": f"results/imdb/Acyclic Query 2/decomposition_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Acyclic Query 2/decomposition_no_projection_full.sql",
    #     "dataset-path": f"data/imdb_data",
    #     "trials": 3,
    #     "output-dir": f"results/imdb/Acyclic Query 2/decomposition_no_projection_full"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Acyclic Query 2/decomposition_no_projection_faq.sql",
    #     "dataset-path": f"data/imdb_data",
    #     "trials": 3,
    #     "output-dir": f"results/imdb/Acyclic Query 2/decomposition_no_projection_faq"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Acyclic Query 2/decomposition_no_projection.sql",
    #     "dataset-path": f"data/imdb_data",
    #     "trials": 3,
    #     "output-dir": f"results/imdb/Acyclic Query 2/decomposition_no_projection"
    # },
    # {
    #     "pipeline-sql-path": f"pipelines/Acyclic Query 2/decomposition.sql",
    #     "dataset-path": f"data/imdb_data",
    #     "trials": 3,
    #     "output-dir": f"results/imdb/Acyclic Query 2/decomposition"
    # },

]

def run_experiments():
    overview_file = "OVERVIEW.csv"
    if not os.path.exists(overview_file):
        with open(overview_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "ID", "Dataset", "Variant", "Status", "Duration_Min"])

    for exp in EXPERIMENTS:
        subprocess.run(["docker", "compose", "down", "-v"], check=False)
        subprocess.run(["docker", "system", "prune", "-f"], check=False)

        scratch_dir = "/local/scratch/emumic/feldera_storage"

        # Docker deletes folder as root to bypass password prompt
        subprocess.run([
            "docker", "run", "--rm", "-v", "/local/scratch/emumic:/mnt", "ubuntu", 
            "rm", "-rf", "/mnt/feldera_storage"
        ], check=False)

        # Create and unlock folder for feldera
        subprocess.run(["mkdir", "-p", scratch_dir], check=False)
        subprocess.run(["chmod", "777", scratch_dir], check=False)

        subprocess.run(["docker", "compose", "up", "-d"], check=False)
        time.sleep(30)

        cmd = ["python", "experiment.py"]

        for key, value in exp.items():
            cmd.append(f"--{key}")
            cmd.append(str(value))

        start_time = time.perf_counter()

        try:
            subprocess.run(cmd, timeout= 60 * 60 * 15, check=True)
            status = "COMPLETED"
        except subprocess.TimeoutExpired:
            status = "TIMEOUT"
        except subprocess.CalledProcessError:
            status = "CRASHED"
        except Exception as e:
            print(f"ERROR: {e}")
            status = "ERROR"

        duration_min = round((time.perf_counter() - start_time) / 60, 2)

        with open(overview_file, "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    os.path.basename(os.path.dirname(exp["pipeline-sql-path"])),
                    os.path.basename(exp["dataset-path"]),
                    os.path.basename(exp["pipeline-sql-path"]),
                    status,
                    duration_min,
                ])
            
        print(f"[{datetime.datetime.now()}] FINISHED: {status} in {duration_min}min")
            
        time.sleep(30)


if __name__ == "__main__":
    run_experiments()