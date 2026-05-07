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
    A bigint,
    E bigint
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
SELECT R1.A AS A, R1.B AS B, R5.E AS E
FROM R1
JOIN R5 ON R1.A = R5.A;

CREATE MATERIALIZED VIEW CHILD_1_P AS
SELECT B, E
FROM CHILD_1_Q;

-- Child Bag 2.
CREATE MATERIALIZED VIEW CHILD_2_Q AS
SELECT R2.B AS B, R2.C AS C, CHILD_1_P.E AS E
FROM R2
JOIN CHILD_1_P ON CHILD_1_P.B = R2.B;

CREATE MATERIALIZED VIEW CHILD_2_P AS
SELECT C, E
FROM CHILD_2_Q;

-- Root Bag.
CREATE MATERIALIZED VIEW ROOT_Q AS
SELECT R3.C AS C, R3.D AS D, R4.E AS E
FROM R3
JOIN R4 ON R3.D = R4.D
JOIN CHILD_2_P ON CHILD_2_P.C = R3.C AND CHILD_2_P.E = R4.E;

-- Result.
CREATE MATERIALIZED VIEW RESULT AS
SELECT CHILD_1_Q.A AS A, CHILD_1_Q.B AS B, ROOT_Q.C AS C, ROOT_Q.D AS D, ROOT_Q.E AS E
FROM ROOT_Q
JOIN CHILD_2_Q ON ROOT_Q.C = CHILD_2_Q.C AND ROOT_Q.E = CHILD_2_Q.E
JOIN CHILD_1_Q ON CHILD_2_Q.B = CHILD_1_Q.B AND CHILD_2_Q.E = CHILD_1_Q.E AND (CHILD_1_Q.E = ROOT_Q.E);
