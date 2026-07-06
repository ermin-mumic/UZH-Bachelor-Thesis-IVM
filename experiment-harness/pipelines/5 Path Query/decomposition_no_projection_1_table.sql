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
SELECT R1.A AS A, R1.B AS B
FROM EDGES AS R1(A, B);

CREATE MATERIALIZED VIEW CHILD_1_P AS
SELECT DISTINCT B
FROM CHILD_1_Q;

-- Child Bag 2.
CREATE MATERIALIZED VIEW CHILD_2_Q AS
SELECT R5.E AS E, R5.F AS F
FROM EDGES AS R5(E, F);

CREATE MATERIALIZED VIEW CHILD_2_P AS
SELECT DISTINCT E
FROM CHILD_2_Q;

-- Child Bag 3.
CREATE MATERIALIZED VIEW CHILD_3_Q AS
SELECT R2.B AS B, R2.C AS C
FROM EDGES AS R2(B, C)
JOIN CHILD_1_P ON CHILD_1_P.B = R2.B;

CREATE MATERIALIZED VIEW CHILD_3_P AS
SELECT DISTINCT C
FROM CHILD_3_Q;

-- Child Bag 4.
CREATE MATERIALIZED VIEW CHILD_4_Q AS
SELECT R4.D AS D, R4.E AS E
FROM EDGES AS R4(D, E)
JOIN CHILD_2_P ON CHILD_2_P.E = R4.E;

CREATE MATERIALIZED VIEW CHILD_4_P AS
SELECT DISTINCT D
FROM CHILD_4_Q;

-- Root Bag.
CREATE MATERIALIZED VIEW RESULT AS
SELECT R3.C AS C, R3.D AS D
FROM EDGES AS R3(C, D)
JOIN CHILD_3_P ON CHILD_3_P.C = R3.C
JOIN CHILD_4_P ON CHILD_4_P.D = R3.D;
