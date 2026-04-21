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

CREATE TABLE R8 (
    A bigint,
    D bigint
) WITH (
    'materialized' = 'true',
    'connectors' = '[{
        "name": "R8_connector",
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
SELECT R2.B AS B, R3.C AS C, R9.D AS D
FROM R2
JOIN R3 ON R2.C = R3.C
JOIN R9 ON R9.B = R2.B AND R9.D = R3.D;

CREATE MATERIALIZED VIEW CHILD_1_P AS
SELECT B, D
FROM CHILD_1_Q;

-- Child Bag 2.
CREATE MATERIALIZED VIEW CHILD_2_Q AS
SELECT R1.A AS A, R9.B AS B, R8.D AS D
FROM R1
JOIN R8 ON R1.A = R8.A
JOIN R9 ON R8.D = R9.D AND R9.B = R1.B
JOIN CHILD_1_P ON CHILD_1_P.B = R9.B AND (CHILD_1_P.B = R1.B) AND CHILD_1_P.D = R9.D AND (CHILD_1_P.D = R8.D);

CREATE MATERIALIZED VIEW CHILD_2_P AS
SELECT A, D
FROM CHILD_2_Q;

-- Child Bag 3.
CREATE MATERIALIZED VIEW CHILD_3_Q AS
SELECT R7.A AS A, R8.D AS D, R7.E AS E
FROM R4
JOIN R7 ON R4.E = R7.E
JOIN R8 ON R8.A = R7.A AND R8.D = R4.D
JOIN CHILD_2_P ON CHILD_2_P.A = R8.A AND (CHILD_2_P.A = R7.A) AND CHILD_2_P.D = R8.D AND (CHILD_2_P.D = R4.D);

CREATE MATERIALIZED VIEW CHILD_3_P AS
SELECT A, E
FROM CHILD_3_Q;

-- Root Bag.
CREATE MATERIALIZED VIEW ROOT_Q AS
SELECT R7.A AS A, R5.E AS E, R6.F AS F
FROM R5
JOIN R6 ON R5.F = R6.F
JOIN R7 ON R7.A = R6.A AND R7.E = R5.E
JOIN CHILD_3_P ON CHILD_3_P.A = R7.A AND (CHILD_3_P.A = R6.A) AND CHILD_3_P.E = R7.E AND (CHILD_3_P.E = R5.E);


