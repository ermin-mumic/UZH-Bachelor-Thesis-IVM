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
SELECT R2.B AS B, R3.C AS C, R4.D AS D
FROM EDGES AS R2(B, C)
JOIN EDGES AS R3(C, D) ON R2.C = R3.C
JOIN EDGES AS R4(B, D) ON R4.B = R2.B AND R4.D = R3.D;

CREATE MATERIALIZED VIEW CHILD_1_P AS
SELECT B, D
FROM CHILD_1_Q;

-- Root Bag.
CREATE MATERIALIZED VIEW RESULT AS
SELECT R1.A AS A, R4.B AS B, R5.D AS D
FROM EDGES AS R1(A, B)
JOIN EDGES AS R4(B, D) ON R4.B = R1.B
JOIN EDGES AS R5(A, D) ON R5.A = R1.A AND R5.D = R4.D
JOIN CHILD_1_P ON CHILD_1_P.B = R4.B AND (CHILD_1_P.B = R1.B) AND CHILD_1_P.D = R5.D AND (CHILD_1_P.D = R4.D);