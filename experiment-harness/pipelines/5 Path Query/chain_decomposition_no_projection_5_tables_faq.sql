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

-- Child Bag 1.
CREATE MATERIALIZED VIEW CHILD_1_Q AS
SELECT R1.A AS A, R1.B AS B
FROM R1;

CREATE MATERIALIZED VIEW CHILD_1_P AS
SELECT B, COUNT(*) AS COUNT_C1
FROM CHILD_1_Q
GROUP BY B;

-- Child Bag 2.
CREATE MATERIALIZED VIEW CHILD_2_Q AS
SELECT R2.B AS B, R2.C AS C, COUNT_C1
FROM R2
JOIN CHILD_1_P ON CHILD_1_P.B = R2.B;

CREATE MATERIALIZED VIEW CHILD_2_P AS
SELECT C, SUM(COUNT_C1) AS COUNT_C2
FROM CHILD_2_Q
GROUP BY C;

-- Child Bag 3.
CREATE MATERIALIZED VIEW CHILD_3_Q AS
SELECT R3.C AS C, R3.D AS D, COUNT_C2
FROM R3
JOIN CHILD_2_P ON CHILD_2_P.C = R3.C;

CREATE MATERIALIZED VIEW CHILD_3_P AS
SELECT D, SUM(COUNT_C2) AS COUNT_C3
FROM CHILD_3_Q
GROUP BY D;

-- Child Bag 4.
CREATE MATERIALIZED VIEW CHILD_4_Q AS
SELECT R4.D AS D, R4.E AS E, COUNT_C3
FROM R4
JOIN CHILD_3_P ON CHILD_3_P.D = R4.D;

CREATE MATERIALIZED VIEW CHILD_4_P AS
SELECT E, SUM(COUNT_C3) AS COUNT_C4
FROM CHILD_4_Q
GROUP BY E;

-- Root Bag.
CREATE MATERIALIZED VIEW ROOT_Q AS
SELECT R5.E AS E, R5.F AS F, COUNT_C4
FROM R5
JOIN CHILD_4_P ON CHILD_4_P.E = R5.E;

-- Result.
CREATE MATERIALIZED VIEW RESULT AS
SELECT SUM(COUNT_C4) AS total_count
FROM ROOT_Q;
