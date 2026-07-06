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

-- 5 Path Query.
CREATE MATERIALIZED VIEW RESULT AS
SELECT R1.A AS A, R1.B AS B, R3.C AS C, R3.D AS D, R5.E AS E, R5.F AS F
FROM EDGES AS R1(A, B)
JOIN EDGES AS R2(B, C) ON R1.B = R2.B
JOIN EDGES AS R3(C, D) ON R3.C = R2.C
JOIN EDGES AS R4(D, E) ON R4.D = R3.D
JOIN EDGES AS R5(E, F) ON R5.E = R4.E;