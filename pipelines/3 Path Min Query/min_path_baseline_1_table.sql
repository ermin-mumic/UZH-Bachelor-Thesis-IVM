-- Template.
CREATE TABLE EDGES (
    src bigint,
    tgt bigint,
    cost int
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

-- 3 Path Min Query.
CREATE MATERIALIZED VIEW RESULT AS
SELECT R1.A AS A, MIN(R1_C + R2_C + R3_C) AS MIN_COST
FROM EDGES AS R1(A, B, R1_C)
JOIN EDGES AS R2(B, C, R2_C) ON R1.B = R2.B
JOIN EDGES AS R3(C, D, R3_C) ON R3.C = R2.C
GROUP BY R1.A;