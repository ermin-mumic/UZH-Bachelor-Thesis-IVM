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

-- Child Bag 1.
CREATE MATERIALIZED VIEW CHILD_1_Q AS
SELECT *
FROM R1;

CREATE MATERIALIZED VIEW CHILD_1_P AS
SELECT DISTINCT B
FROM CHILD_1_Q;

-- Child Bag 2.
CREATE MATERIALIZED VIEW CHILD_2_Q AS
SELECT *
FROM R3;

CREATE MATERIALIZED VIEW CHILD_2_P AS
SELECT DISTINCT C
FROM CHILD_2_Q;

-- Root Bag.
CREATE MATERIALIZED VIEW RESULT AS
SELECT R2.B AS B, R2.C AS C, R2_C as MIN_COST
FROM R2
JOIN CHILD_1_P ON CHILD_1_P.B = R2.B
JOIN CHILD_2_P ON CHILD_2_P.C = R2.C;

