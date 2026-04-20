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
SELECT R2.B AS B, R3.C AS C, R9.D AS D
FROM EDGES AS R2(B, C)
JOIN EDGES AS R3(C, D) ON R2.C = R3.C
JOIN EDGES AS R9(B, D) ON R9.B = R2.B AND R9.D = R3.D;

CREATE MATERIALIZED VIEW CHILD_1_P AS
SELECT B, D
FROM CHILD_1_Q;

-- Child Bag 2.
CREATE MATERIALIZED VIEW CHILD_2_Q AS
SELECT R1.A AS A, R9.B AS B, R8.D AS D
FROM EDGES AS R1(A, B)
JOIN EDGES AS R8(A, D) ON R1.A = R8.A
JOIN EDGES AS R9(B, D) ON R8.D = R9.D AND R9.B = R1.B
JOIN CHILD_1_P ON CHILD_1_P.B = R9.B AND (CHILD_1_P.B = R1.B) AND CHILD_1_P.D = R9.D AND (CHILD_1_P.D = R8.D);

CREATE MATERIALIZED VIEW CHILD_2_P AS
SELECT A, D
FROM CHILD_2_Q;

-- Child Bag 3.
CREATE MATERIALIZED VIEW CHILD_3_Q AS
SELECT R7.A AS A, R8.D AS D, R7.E AS E
FROM EDGES AS R4(D, E)
JOIN EDGES AS R7(A, E) ON R4.E = R7.E
JOIN EDGES AS R8(A, D) ON R8.A = R7.A AND R8.D = R4.D
JOIN CHILD_2_P ON CHILD_2_P.A = R8.A AND (CHILD_2_P.A = R7.A) AND CHILD_2_P.D = R8.D AND (CHILD_2_P.D = R4.D);

CREATE MATERIALIZED VIEW CHILD_3_P AS
SELECT A, E
FROM CHILD_3_Q;

-- Root Bag.
CREATE MATERIALIZED VIEW ROOT_Q AS
SELECT R7.A AS A, R5.E AS E, R6.F AS F
FROM EDGES AS R5(E, F)
JOIN EDGES AS R6(A, F) ON R5.F = R6.F
JOIN EDGES AS R7(A, E) ON R7.A = R6.A AND R7.E = R5.E
JOIN CHILD_3_P ON CHILD_3_P.A = R7.A AND (CHILD_3_P.A = R6.A) AND CHILD_3_P.E = R7.E AND (CHILD_3_P.E = R5.E);


