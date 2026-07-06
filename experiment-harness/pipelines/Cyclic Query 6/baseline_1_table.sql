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

-- Cyclic Query 6.
CREATE MATERIALIZED VIEW RESULT AS
SELECT R1.A AS A, R9.B AS B, R4.D AS D, R7.E AS E
FROM EDGES AS R1(A, B)
JOIN EDGES AS R9(B, D) ON R1.B = R9.B
JOIN EDGES AS R7(A, E) ON R7.A = R1.A
JOIN EDGES AS R4(D, E) ON R4.D = R9.D AND R4.E = R7.E;