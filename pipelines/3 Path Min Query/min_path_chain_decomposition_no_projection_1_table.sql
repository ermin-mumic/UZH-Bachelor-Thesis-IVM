-- Template.
CREATE TABLE EDGES (
    src bigint,
    tgt bigint,
    cost int
) WITH (
    'materialized' = 'true',
    'connectors' = '[{
        "name": "Edges_connector",
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
FROM EDGES AS R1(A, B, R1_C);

CREATE MATERIALIZED VIEW CHILD_1_P AS
SELECT DISTINCT B
FROM CHILD_1_Q;

-- Child Bag 2.
CREATE MATERIALIZED VIEW CHILD_2_Q AS
SELECT R2.B AS B, R2.C AS C, R2_C
FROM EDGES AS R2(B, C, R2_C)
JOIN CHILD_1_P ON CHILD_1_P.B = R2.B;

CREATE MATERIALIZED VIEW CHILD_2_P AS
SELECT DISTINCT C
FROM CHILD_2_Q;

-- Root Bag.
CREATE MATERIALIZED VIEW RESULT AS
SELECT R3.C AS C, R3.D AS D, R3_C AS MIN_COST
FROM EDGES AS R3(C, D, R3_C)
JOIN CHILD_2_P ON CHILD_2_P.C = R3.C;
