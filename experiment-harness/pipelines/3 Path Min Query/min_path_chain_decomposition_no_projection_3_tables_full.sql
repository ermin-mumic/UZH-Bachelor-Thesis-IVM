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
SELECT R2.B AS B, R2.C AS C, R2_C
FROM R2
JOIN CHILD_1_P ON CHILD_1_P.B = R2.B;

CREATE MATERIALIZED VIEW CHILD_2_P AS
SELECT DISTINCT C
FROM CHILD_2_Q;

-- Root Bag.
CREATE MATERIALIZED VIEW ROOT_Q AS
SELECT R3.C AS C, R3.D AS D, R3_C
FROM R3
JOIN CHILD_2_P ON CHILD_2_P.C = R3.C;

-- Result.
CREATE MATERIALIZED VIEW RESULT AS
SELECT CHILD_1_Q.A AS A, MIN(R1_C + R2_C + R3_C) AS MIN_COST
FROM ROOT_Q
JOIN CHILD_2_Q ON ROOT_Q.C = CHILD_2_Q.C
JOIN CHILD_1_Q ON CHILD_1_Q.B = CHILD_2_Q.B
GROUP BY CHILD_1_Q.A;
