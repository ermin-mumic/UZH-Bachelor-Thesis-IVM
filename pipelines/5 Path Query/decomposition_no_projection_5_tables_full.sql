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
SELECT DISTINCT B
FROM CHILD_1_Q;

-- Child Bag 2.
CREATE MATERIALIZED VIEW CHILD_2_Q AS
SELECT R5.E AS E, R5.F AS F
FROM R5;

CREATE MATERIALIZED VIEW CHILD_2_P AS
SELECT DISTINCT E
FROM CHILD_2_Q;

-- Child Bag 3.
CREATE MATERIALIZED VIEW CHILD_3_Q AS
SELECT R2.B AS B, R2.C AS C
FROM R2
JOIN CHILD_1_P ON CHILD_1_P.B = R2.B;

CREATE MATERIALIZED VIEW CHILD_3_P AS
SELECT DISTINCT C
FROM CHILD_3_Q;

-- Child Bag 4.
CREATE MATERIALIZED VIEW CHILD_4_Q AS
SELECT R4.D AS D, R4.E AS E
FROM R4
JOIN CHILD_2_P ON CHILD_2_P.E = R4.E;

CREATE MATERIALIZED VIEW CHILD_4_P AS
SELECT DISTINCT D
FROM CHILD_4_Q;

-- Root Bag.
CREATE MATERIALIZED VIEW ROOT_Q AS
SELECT R3.C AS C, R3.D AS D
FROM R3
JOIN CHILD_3_P ON CHILD_3_P.C = R3.C
JOIN CHILD_4_P ON CHILD_4_P.D = R3.D;

-- Result.
CREATE MATERIALIZED VIEW RESULT AS
SELECT CHILD_1_Q.A AS A, CHILD_1_Q.B AS B, ROOT_Q.C AS C, ROOT_Q.D AS D, CHILD_2_Q.E AS E, CHILD_2_Q.F AS F
FROM ROOT_Q
JOIN CHILD_4_Q ON CHILD_4_Q.D = ROOT_Q.D
JOIN CHILD_3_Q ON CHILD_3_Q.C = ROOT_Q.C
JOIN CHILD_2_Q ON CHILD_2_Q.E = CHILD_4_Q.E
JOIN CHILD_1_Q ON CHILD_1_Q.B = CHILD_3_Q.B;
