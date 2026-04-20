-- The soc-Epinions1 Schema.
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

-- Child Bag 1.
CREATE MATERIALIZED VIEW CHILD_1_Q AS
SELECT R1.A AS A, R1.B AS B, R6.F AS F
FROM EDGES AS R1(A, B)
JOIN EDGES AS R6(A, F) ON R1.A = R6.A;

CREATE MATERIALIZED VIEW CHILD_1_P AS
SELECT B, F
FROM CHILD_1_Q;

-- Child Bag 2.
CREATE MATERIALIZED VIEW CHILD_2_Q AS
SELECT R2.B AS B, R2.C AS C, CHILD_1_P.F AS F
FROM EDGES AS R2(B, C)
JOIN CHILD_1_P ON CHILD_1_P.B = R2.B;

CREATE MATERIALIZED VIEW CHILD_2_P AS
SELECT C, F
FROM CHILD_2_Q;

-- Child Bag 3.
CREATE MATERIALIZED VIEW CHILD_3_Q AS
SELECT R3.C AS C, R3.D AS D, CHILD_2_P.F AS F
FROM EDGES AS R3(C, D)
JOIN CHILD_2_P ON CHILD_2_P.C = R3.C;

CREATE MATERIALIZED VIEW CHILD_3_P AS
SELECT D, F
FROM CHILD_3_Q;

-- Root Bag.
CREATE MATERIALIZED VIEW ROOT_Q AS
SELECT R4.D AS D, R5.E AS E, R5.F AS F
FROM EDGES AS R4(D, E)
JOIN EDGES AS R5(E, F) ON R5.E = R4.E
JOIN CHILD_3_P ON CHILD_3_P.D = R4.D AND CHILD_3_P.F = R5.F;


