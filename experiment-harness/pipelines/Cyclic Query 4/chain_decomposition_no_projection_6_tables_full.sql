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
SELECT DISTINCT B, F
FROM CHILD_1_Q;

-- Child Bag 2.
CREATE MATERIALIZED VIEW CHILD_2_Q AS
SELECT R2.B AS B, R2.C AS C, CHILD_1_P.F AS F
FROM R2
JOIN CHILD_1_P ON CHILD_1_P.B = R2.B;

CREATE MATERIALIZED VIEW CHILD_2_P AS
SELECT DISTINCT C, F
FROM CHILD_2_Q;

-- Child Bag 3.
CREATE MATERIALIZED VIEW CHILD_3_Q AS
SELECT R3.C AS C, R3.D AS D, CHILD_2_P.F AS F
FROM R3
JOIN CHILD_2_P ON CHILD_2_P.C = R3.C;

CREATE MATERIALIZED VIEW CHILD_3_P AS
SELECT DISTINCT D, F
FROM CHILD_3_Q;

-- Root Bag.
CREATE MATERIALIZED VIEW ROOT_Q AS
SELECT R4.D AS D, R5.E AS E, R5.F AS F
FROM R4
JOIN R5 ON R5.E = R4.E
JOIN CHILD_3_P ON CHILD_3_P.D = R4.D AND CHILD_3_P.F = R5.F;

-- Result.
CREATE MATERIALIZED VIEW RESULT AS
SELECT CHILD_1_Q.A AS A, CHILD_1_Q.B AS B, CHILD_2_Q.C AS C, ROOT_Q.D AS D, ROOT_Q.E AS E, ROOT_Q.F AS F
FROM ROOT_Q
JOIN CHILD_3_Q ON ROOT_Q.D = CHILD_3_Q.D AND ROOT_Q.F = CHILD_3_Q.F
JOIN CHILD_2_Q ON CHILD_3_Q.C = CHILD_2_Q.C AND CHILD_3_Q.F = CHILD_2_Q.F AND (CHILD_2_Q.F = ROOT_Q.F)
JOIN CHILD_1_Q ON CHILD_2_Q.B = CHILD_1_Q.B AND CHILD_2_Q.F = CHILD_1_Q.F AND (CHILD_1_Q.F = ROOT_Q.F) AND (CHILD_1_Q.F = CHILD_3_Q.F);


