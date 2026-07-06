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

-- Cyclic Query 1.
CREATE MATERIALIZED VIEW RESULT AS
SELECT R1.A AS A, R2.B AS B, R3.C AS C, R4.D AS D, R5.E AS E, R6.F AS F
FROM EDGES AS R1(A, B)
JOIN EDGES AS R2(B, C) ON R1.B = R2.B
JOIN EDGES AS R3(C, D) ON R2.C = R3.C
JOIN EDGES AS R4(D, E) ON R3.D = R4.D
JOIN EDGES AS R5(E, F) ON R4.E = R5.E
JOIN EDGES AS R6(A, F) ON R5.F = R6.F AND R6.A = R1.A
JOIN EDGES AS R7(A, E) ON R7.A = R6.A AND (R7.A = R1.A) AND R7.E = R5.E AND (R7.E = R4.E)
JOIN EDGES AS R8(A, D) ON R8.A = R7.A AND (R8.A = R6.A) AND (R8.A = R1.A) AND R8.D = R4.D AND (R8.D = R3.D)
JOIN EDGES AS R9(B, D) ON R9.B = R2.B AND (R9.B = R1.B) AND R9.D = R8.D AND (R9.D = R4.D) AND (R9.D = R3.D);