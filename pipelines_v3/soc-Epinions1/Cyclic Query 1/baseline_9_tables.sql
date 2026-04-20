-- The soc-Epinions1 Schema.
CREATE TABLE R1 (
    A bigint,
    B bigint
) WITH (
    'materialized' = 'true',
    'connectors' = '[{
        "name": "R1_connector",
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/data/snap_data/soc-Epinions1.csv"
            }
        },
        "format": { 
            "name": "csv",
            "config": {
                "headers": true
            }
        }
    }]'
);

CREATE TABLE R2 (
    B bigint,
    C bigint
) WITH (
    'materialized' = 'true',
    'connectors' = '[{
        "name": "R2_connector",
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/data/snap_data/soc-Epinions1.csv"
            }
        },
        "format": { 
            "name": "csv",
            "config": {
                "headers": true
            }
        }
    }]'
);

CREATE TABLE R3 (
    C bigint,
    D bigint
) WITH (
    'materialized' = 'true',
    'connectors' = '[{
        "name": "R3_connector",
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/data/snap_data/soc-Epinions1.csv"
            }
        },
        "format": { 
            "name": "csv",
            "config": {
                "headers": true
            }
        }
    }]'
);

CREATE TABLE R4 (
    D bigint,
    E bigint
) WITH (
    'materialized' = 'true',
    'connectors' = '[{
        "name": "R4_connector",
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/data/snap_data/soc-Epinions1.csv"
            }
        },
        "format": { 
            "name": "csv",
            "config": {
                "headers": true
            }
        }
    }]'
);

CREATE TABLE R5 (
    E bigint,
    F bigint
) WITH (
    'materialized' = 'true',
    'connectors' = '[{
        "name": "R5_connector",
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/data/snap_data/soc-Epinions1.csv"
            }
        },
        "format": { 
            "name": "csv",
            "config": {
                "headers": true
            }
        }
    }]'
);

CREATE TABLE R6 (
    A bigint,
    F bigint
) WITH (
    'materialized' = 'true',
    'connectors' = '[{
        "name": "R6_connector",
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/data/snap_data/soc-Epinions1.csv"
            }
        },
        "format": { 
            "name": "csv",
            "config": {
                "headers": true
            }
        }
    }]'
);

CREATE TABLE R7 (
    A bigint,
    E bigint
) WITH (
    'materialized' = 'true',
    'connectors' = '[{
        "name": "R7_connector",
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/data/snap_data/soc-Epinions1.csv"
            }
        },
        "format": { 
            "name": "csv",
            "config": {
                "headers": true
            }
        }
    }]'
);

CREATE TABLE R8 (
    A bigint,
    D bigint
) WITH (
    'materialized' = 'true',
    'connectors' = '[{
        "name": "R8_connector",
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/data/snap_data/soc-Epinions1.csv"
            }
        },
        "format": { 
            "name": "csv",
            "config": {
                "headers": true
            }
        }
    }]'
);

CREATE TABLE R9 (
    B bigint,
    D bigint
) WITH (
    'materialized' = 'true',
    'connectors' = '[{
        "name": "R9_connector",
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/data/snap_data/soc-Epinions1.csv"
            }
        },
        "format": { 
            "name": "csv",
            "config": {
                "headers": true
            }
        }
    }]'
);

-- Cyclic Query 1.
CREATE MATERIALIZED VIEW BASELINE_QUERY AS
SELECT R1.A AS A, R2.B AS B, R3.C AS C, R4.D AS D, R5.E AS E, R6.F AS F
FROM R1
JOIN R2 ON R1.B = R2.B
JOIN R3 ON R2.C = R3.C
JOIN R4 ON R3.D = R4.D
JOIN R5 ON R4.E = R5.E
JOIN R6 ON R5.F = R6.F AND R6.A = R1.A
JOIN R7 ON R7.A = R6.A AND (R7.A = R1.A) AND R7.E = R5.E AND (R7.E = R4.E)
JOIN R8 ON R8.A = R7.A AND (R8.A = R6.A) AND (R8.A = R1.A) AND R8.D = R4.D AND (R8.D = R3.D)
JOIN R9 ON R9.B = R2.B AND (R9.B = R1.B) AND R9.D = R8.D AND (R9.D = R4.D) AND (R9.D = R3.D);
