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
SELECT R1.A AS A, R1.B AS B, R7.E AS E
FROM EDGES AS R1(A, B)
JOIN EDGES AS R7(A, E) ON R1.A = R7.A;

CREATE MATERIALIZED VIEW CHILD_1_P AS
SELECT DISTINCT B, E
FROM CHILD_1_Q;

-- Root Bag.
CREATE MATERIALIZED VIEW ROOT_Q AS
SELECT R9.B AS B, R9.D AS D, R4.E AS E
FROM EDGES AS R4(D, E)
JOIN EDGES AS R9(B, D) ON R4.D = R9.D
JOIN CHILD_1_P ON CHILD_1_P.B = R9.B AND CHILD_1_P.E = R4.E;

-- Result.
CREATE MATERIALIZED VIEW RESULT AS
SELECT CHILD_1_Q.A AS A, CHILD_1_Q.B AS B, ROOT_Q.D AS D, ROOT_Q.E AS E
FROM ROOT_Q
JOIN CHILD_1_Q ON CHILD_1_Q.B = ROOT_Q.B AND CHILD_1_Q.E = ROOT_Q.E;
