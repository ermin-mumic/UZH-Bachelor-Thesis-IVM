-- Template.
CREATE TABLE R1 (
    A bigint,
    B bigint,
    R1_C int
) WITH (
    'materialized' = 'true',
    'connectors' = '[{
        "name": "R1_connector",
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/{{FILE_PATH}}"
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
    C bigint,
    R2_C int
) WITH (
    'materialized' = 'true',
    'connectors' = '[{
        "name": "R2_connector",
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/{{FILE_PATH}}"
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
    D bigint,
    R3_C int
) WITH (
    'materialized' = 'true',
    'connectors' = '[{
        "name": "R3_connector",
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/{{FILE_PATH}}"
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

-- 3 Path Min Query.
CREATE MATERIALIZED VIEW RESULT AS
SELECT R1.A AS A, MIN(R1_C + R2_C + R3_C) AS MIN_COST
FROM R1
JOIN R2 ON R1.B = R2.B
JOIN R3 ON R3.C = R2.C
GROUP BY R1.A;
