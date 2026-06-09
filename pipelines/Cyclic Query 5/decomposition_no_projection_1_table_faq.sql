-- Template.
CREATE TABLE EDGES (
    src bigint,
    tgt bigint
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
SELECT R1.A AS A, R1.B AS B, R5.E AS E
FROM EDGES AS R1(A, B)
JOIN EDGES AS R5(A, E) ON R1.A = R5.A;

CREATE MATERIALIZED VIEW CHILD_1_P AS
SELECT B, E, COUNT(*) AS COUNT_C1
FROM CHILD_1_Q
GROUP BY B, E;

-- Child Bag 2.
CREATE MATERIALIZED VIEW CHILD_2_Q AS
SELECT R3.C AS C, R3.D AS D, R4.E AS E
FROM EDGES AS R3(C, D)
JOIN EDGES AS R4(D, E) ON R3.D = R4.D;

CREATE MATERIALIZED VIEW CHILD_2_P AS
SELECT C, E, COUNT(*) AS COUNT_C2
FROM CHILD_2_Q
GROUP BY C, E;

-- Root Bag.
CREATE MATERIALIZED VIEW ROOT_Q AS
SELECT R2.B AS B, R2.C AS C, CHILD_1_P.E AS E, COUNT_C1, COUNT_C2
FROM EDGES AS R2(B, C)
JOIN CHILD_1_P ON CHILD_1_P.B = R2.B 
JOIN CHILD_2_P ON CHILD_2_P.C = R2.C AND CHILD_2_P.E = CHILD_1_P.E;

-- Result.
CREATE MATERIALIZED VIEW RESULT AS
SELECT SUM(COUNT_C1 * COUNT_C2) AS total_count
FROM ROOT_Q;

