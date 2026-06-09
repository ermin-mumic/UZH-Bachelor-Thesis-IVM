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

CREATE TABLE R7 (
    A bigint,
    E bigint
) WITH (
    'materialized' = 'true',
    'connectors' = '[{
        "name": "R7_connector",
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

CREATE TABLE R9 (
    B bigint,
    D bigint
) WITH (
    'materialized' = 'true',
    'connectors' = '[{
        "name": "R9_connector",
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
FROM R1
JOIN R7 ON R1.A = R7.A;

CREATE MATERIALIZED VIEW CHILD_1_P AS
SELECT B, E, COUNT(*) AS COUNT_C1
FROM CHILD_1_Q
GROUP BY B, E;

-- Root Bag.
CREATE MATERIALIZED VIEW ROOT_Q AS
SELECT R9.B AS B, R9.D AS D, R4.E AS E, COUNT_C1
FROM R4
JOIN R9 ON R4.D = R9.D
JOIN CHILD_1_P ON CHILD_1_P.B = R9.B AND CHILD_1_P.E = R4.E;

-- Result.
CREATE MATERIALIZED VIEW RESULT AS
SELECT SUM(COUNT_C1) AS total_count
FROM ROOT_Q;