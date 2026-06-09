-- The TPC-H Schema.
CREATE TABLE PART (
    PARTKEY bigint not null,
    P_NAME varchar(55),
    P_MFGR char(25),
    P_BRAND char(10),
    P_TYPE varchar(25),
    P_SIZE integer,
    P_CONTAINER char(10),
    P_RETAILPRICE decimal(12,2),
    P_COMMENT varchar(23),
    PRIMARY KEY (PARTKEY)
) WITH ('materialized' = 'true');

CREATE TABLE SUPPLIER (
    SUPPKEY bigint not null,
    S_NAME char(25),
    S_ADDRESS varchar(40),
    S_NATIONKEY bigint not null,
    S_PHONE char(15),
    S_ACCTBAL decimal(12,2),
    S_COMMENT varchar(101),
    PRIMARY KEY (SUPPKEY)
) WITH (
    'connectors' = '[{
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/{{FILE_PATH}}/supplier.csv"
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

CREATE TABLE PARTSUPP (
    PARTKEY bigint not null,
    SUPPKEY bigint not null,
    PS_AVAILQTY integer,
    PS_SUPPLYCOST decimal(12,2),
    PS_COMMENT varchar(199),
    PRIMARY KEY (PARTKEY, SUPPKEY)
) WITH ('materialized' = 'true');

CREATE TABLE CUSTOMER (
    CUSTKEY bigint not null,
    C_NAME varchar(25),
    C_ADDRESS varchar(40),
    C_NATIONKEY bigint not null,
    C_PHONE char(15),
    C_ACCTBAL decimal(12,2),
    C_MKTSEGMENT char(10),
    C_COMMENT varchar(117),
    PRIMARY KEY (CUSTKEY)
) WITH (
    'connectors' = '[{
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/{{FILE_PATH}}/customer.csv"
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

CREATE TABLE ORDERS (
    ORDERKEY bigint not null,
    CUSTKEY bigint not null,
    O_ORDERSTATUS char(1),
    O_TOTALPRICE decimal(12,2),
    O_ORDERDATE date,
    O_ORDERPRIORITY char(15),
    O_CLERK char(15),
    O_SHIPPRIORITY integer,
    O_COMMENT varchar(79),
    PRIMARY KEY (ORDERKEY)
) WITH (
    'connectors' = '[{
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/{{FILE_PATH}}/orders.csv"
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

CREATE TABLE LINEITEM (
    ORDERKEY bigint not null,
    PARTKEY bigint not null,
    SUPPKEY bigint not null,
    L_LINENUMBER integer not null,
    L_QUANTITY decimal(12,2),
    L_EXTENDEDPRICE decimal(12,2),
    L_DISCOUNT decimal(12,2),
    L_TAX decimal(12,2),
    L_RETURNFLAG char(1),
    L_LINESTATUS char(1),
    L_SHIPDATE date,
    L_COMMITDATE date,
    L_RECEIPTDATE date,
    L_SHIPINSTRUCT char(25),
    L_SHIPMODE char(10),
    L_COMMENT varchar(44),
    PRIMARY KEY (ORDERKEY, L_LINENUMBER)
) WITH (
    'connectors' = '[{
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/{{FILE_PATH}}/lineitem.csv"
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

CREATE TABLE NATION (
    NATIONKEY bigint not null,
    N_NAME char(25),
    REGIONKEY bigint not null,
    N_COMMENT varchar(152),
    PRIMARY KEY (NATIONKEY)
) WITH (
    'connectors' = '[{
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/{{FILE_PATH}}/nation.csv"
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

CREATE TABLE REGION (
    REGIONKEY bigint not null,
    R_NAME char(25),
    R_COMMENT varchar(152),
    PRIMARY KEY (REGIONKEY)
) WITH ('materialized' = 'true');

-- Child Bag 1.
CREATE MATERIALIZED VIEW CHILD_1_Q AS
SELECT *
FROM (   SELECT 
                NATIONKEY AS S_NATIONKEY,
                N_NAME AS N_S_NAME,
                REGIONKEY AS N_S_REGIONKEY,
                N_COMMENT AS N_S_COMMENT
        FROM NATION AS NATION_S
)
JOIN (
    SELECT DISTINCT S_NATIONKEY
    FROM SUPPLIER
)
USING (S_NATIONKEY);

CREATE MATERIALIZED VIEW CHILD_1_P AS
SELECT S_NATIONKEY, COUNT(*) AS COUNT_C1
FROM CHILD_1_Q
GROUP BY S_NATIONKEY;

-- Child Bag 2.
CREATE MATERIALIZED VIEW CHILD_2_Q AS
SELECT * 
FROM SUPPLIER
JOIN (
    SELECT DISTINCT SUPPKEY
    FROM LINEITEM
)
USING (SUPPKEY)
JOIN (
    SELECT DISTINCT S_NATIONKEY
    FROM (   SELECT 
                NATIONKEY AS S_NATIONKEY,
                N_NAME AS N_S_NAME,
                REGIONKEY AS N_S_REGIONKEY,
                N_COMMENT AS N_S_COMMENT
        FROM NATION AS NATION_S
))
USING (S_NATIONKEY)
JOIN CHILD_1_P USING (S_NATIONKEY);

CREATE MATERIALIZED VIEW CHILD_2_P AS
SELECT SUPPKEY, SUM(COUNT_C1) AS COUNT_C2
FROM CHILD_2_Q
GROUP BY SUPPKEY;

-- Child Bag 3.
CREATE MATERIALIZED VIEW CHILD_3_Q AS
SELECT *
FROM (   SELECT 
                NATIONKEY AS C_NATIONKEY,
                N_NAME AS N_C_NAME,
                REGIONKEY AS N_C_REGIONKEY,
                N_COMMENT AS N_C_COMMENT
        FROM NATION AS NATION_C
)
JOIN (
    SELECT DISTINCT C_NATIONKEY
    FROM CUSTOMER
)
USING (C_NATIONKEY);

CREATE MATERIALIZED VIEW CHILD_3_P AS
SELECT C_NATIONKEY, COUNT(*) AS COUNT_C3
FROM CHILD_3_Q
GROUP BY C_NATIONKEY;

-- Child Bag 4.
CREATE MATERIALIZED VIEW CHILD_4_Q AS
SELECT *
FROM CUSTOMER
JOIN (
    SELECT DISTINCT CUSTKEY
    FROM ORDERS
)
USING (CUSTKEY)
JOIN (
    SELECT DISTINCT C_NATIONKEY
    FROM (   SELECT 
                NATIONKEY AS C_NATIONKEY,
                N_NAME AS N_C_NAME,
                REGIONKEY AS N_C_REGIONKEY,
                N_COMMENT AS N_C_COMMENT
        FROM NATION AS NATION_C
))
USING (C_NATIONKEY)
JOIN CHILD_3_P USING (C_NATIONKEY);

CREATE MATERIALIZED VIEW CHILD_4_P AS
SELECT CUSTKEY, SUM(COUNT_C3) AS COUNT_C4
FROM CHILD_4_Q
GROUP BY CUSTKEY;

-- Child Bag 5.
CREATE MATERIALIZED VIEW CHILD_5_Q AS
SELECT *
FROM ORDERS
JOIN (
    SELECT DISTINCT ORDERKEY
    FROM LINEITEM
)
USING (ORDERKEY)
JOIN (
    SELECT DISTINCT CUSTKEY
    FROM CUSTOMER
)
USING (CUSTKEY)
JOIN CHILD_4_P USING (CUSTKEY);

CREATE MATERIALIZED VIEW CHILD_5_P AS
SELECT ORDERKEY, SUM(COUNT_C4) AS COUNT_C5
FROM CHILD_5_Q
GROUP BY ORDERKEY;

-- Root Bag.
CREATE MATERIALIZED VIEW ROOT_Q AS
SELECT *
FROM LINEITEM
JOIN (
    SELECT DISTINCT ORDERKEY
    FROM ORDERS
)
USING (ORDERKEY)
JOIN (
    SELECT DISTINCT SUPPKEY
    FROM SUPPLIER
)
USING (SUPPKEY)
JOIN CHILD_2_P USING (SUPPKEY)
JOIN CHILD_5_P USING (ORDERKEY);

-- Result.
CREATE MATERIALIZED VIEW RESULT AS
SELECT SUM(COUNT_C2 * COUNT_C5) AS total_count
FROM ROOT_Q;


