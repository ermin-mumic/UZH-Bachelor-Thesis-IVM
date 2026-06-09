-- Template.
CREATE TABLE R1 (
    A bigint,
    B bigint
) WITH (
    'materialized' = 'true',
    'connectors' = '[{
        "name": "R1_connector",
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

CREATE TABLE R2 (
    B bigint,
    C bigint
) WITH (
    'materialized' = 'true',
    'connectors' = '[{
        "name": "R2_connector",
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

CREATE TABLE R3 (
    C bigint,
    D bigint
) WITH (
    'materialized' = 'true',
    'connectors' = '[{
        "name": "R3_connector",
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

CREATE TABLE R4 (
    D bigint,
    E bigint
) WITH (
    'materialized' = 'true',
    'connectors' = '[{
        "name": "R4_connector",
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

CREATE TABLE R5 (
    E bigint,
    F bigint
) WITH (
    'materialized' = 'true',
    'connectors' = '[{
        "name": "R5_connector",
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

CREATE TABLE R6 (
    A bigint,
    F bigint
) WITH (
    'materialized' = 'true',
    'connectors' = '[{
        "name": "R6_connector",
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
SELECT R1.A AS A, R1.B AS B, R6.F AS F
FROM R1
JOIN R6 ON R1.A = R6.A;

CREATE MATERIALIZED VIEW CHILD_1_P AS
SELECT B, F, COUNT(*) AS COUNT_C1
FROM CHILD_1_Q
GROUP BY B, F;

-- Child Bag 2.
CREATE MATERIALIZED VIEW CHILD_2_Q AS
SELECT R2.B AS B, R2.C AS C, CHILD_1_P.F AS F, COUNT_C1
FROM R2
JOIN CHILD_1_P ON CHILD_1_P.B = R2.B;

CREATE MATERIALIZED VIEW CHILD_2_P AS
SELECT C, F, SUM(COUNT_C1) AS COUNT_C2
FROM CHILD_2_Q
GROUP BY C, F;

-- Child Bag 3.
CREATE MATERIALIZED VIEW CHILD_3_Q AS
SELECT R3.C AS C, R3.D AS D, CHILD_2_P.F AS F, COUNT_C2
FROM R3
JOIN CHILD_2_P ON CHILD_2_P.C = R3.C;

CREATE MATERIALIZED VIEW CHILD_3_P AS
SELECT D, F, SUM(COUNT_C2) AS COUNT_C3
FROM CHILD_3_Q
GROUP BY D, F;

-- Root Bag.
CREATE MATERIALIZED VIEW ROOT_Q AS
SELECT R4.D AS D, R5.E AS E, R5.F AS F, COUNT_C3
FROM R4
JOIN R5 ON R5.E = R4.E
JOIN CHILD_3_P ON CHILD_3_P.D = R4.D AND CHILD_3_P.F = R5.F;

-- Result.
CREATE MATERIALIZED VIEW RESULT AS
SELECT SUM(COUNT_C3) AS total_count
FROM ROOT_Q;


