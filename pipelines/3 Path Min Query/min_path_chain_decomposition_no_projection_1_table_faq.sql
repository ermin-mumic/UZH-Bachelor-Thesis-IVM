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
SELECT A, B, MIN(R1_C) AS COUNT_C1
FROM CHILD_1_Q
GROUP BY A, B;

-- Child Bag 2.
CREATE MATERIALIZED VIEW CHILD_2_Q AS
SELECT CHILD_1_P.A AS A, R2.B AS B, R2.C AS C, R2_C, COUNT_C1
FROM EDGES AS R2(B, C, R2_C)
JOIN CHILD_1_P ON CHILD_1_P.B = R2.B;

CREATE MATERIALIZED VIEW CHILD_2_P AS
SELECT A, C, MIN(COUNT_C1 + R2_C) AS COUNT_C2
FROM CHILD_2_Q
GROUP BY A, C;

-- Root Bag.
CREATE MATERIALIZED VIEW ROOT_Q AS
SELECT CHILD_2_P.A AS A, R3.C AS C, R3.D AS D, R3_C, COUNT_C2
FROM EDGES AS R3(C, D, R3_C)
JOIN CHILD_2_P ON CHILD_2_P.C = R3.C;

-- Result.
CREATE MATERIALIZED VIEW RESULT AS
SELECT A, MIN(R3_C + COUNT_C2) AS MIN_COST
FROM ROOT_Q
GROUP BY A;