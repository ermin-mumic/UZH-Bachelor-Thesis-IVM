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

-- Cyclic Query 4.
CREATE MATERIALIZED VIEW BASELINE_QUERY AS
SELECT R1.A AS A, R2.B AS B, R3.C AS C, R4.D AS D, R5.E AS E, R6.F AS F
FROM EDGES AS R1(A, B)
JOIN EDGES AS R2(B, C) ON R1.B = R2.B
JOIN EDGES AS R3(C, D) ON R2.C = R3.C
JOIN EDGES AS R4(D, E) ON R3.D = R4.D
JOIN EDGES AS R5(E, F) ON R4.E = R5.E
JOIN EDGES AS R6(A, F) ON R5.F = R6.F AND R6.A = R1.A;