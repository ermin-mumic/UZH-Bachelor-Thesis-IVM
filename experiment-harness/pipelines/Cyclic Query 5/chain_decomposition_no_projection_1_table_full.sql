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
SELECT DISTINCT B, E
FROM CHILD_1_Q;

-- Child Bag 2.
CREATE MATERIALIZED VIEW CHILD_2_Q AS
SELECT R2.B AS B, R2.C AS C, CHILD_1_P.E AS E
FROM EDGES AS R2(B, C)
JOIN CHILD_1_P ON CHILD_1_P.B = R2.B;

CREATE MATERIALIZED VIEW CHILD_2_P AS
SELECT DISTINCT C, E
FROM CHILD_2_Q;

-- Root Bag.
CREATE MATERIALIZED VIEW ROOT_Q AS
SELECT R3.C AS C, R3.D AS D, R4.E AS E
FROM EDGES AS R3(C, D)
JOIN EDGES AS R4(D, E) ON R3.D = R4.D
JOIN CHILD_2_P ON CHILD_2_P.C = R3.C AND CHILD_2_P.E = R4.E;

-- Result.
CREATE MATERIALIZED VIEW RESULT AS
SELECT CHILD_1_Q.A AS A, CHILD_1_Q.B AS B, ROOT_Q.C AS C, ROOT_Q.D AS D, ROOT_Q.E AS E
FROM ROOT_Q
JOIN CHILD_2_Q ON ROOT_Q.C = CHILD_2_Q.C AND ROOT_Q.E = CHILD_2_Q.E
JOIN CHILD_1_Q ON CHILD_2_Q.B = CHILD_1_Q.B AND CHILD_2_Q.E = CHILD_1_Q.E AND (CHILD_1_Q.E = ROOT_Q.E);
