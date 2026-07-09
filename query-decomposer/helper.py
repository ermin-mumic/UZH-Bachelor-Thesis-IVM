import sqlglot

sql_schema_1 = """
        CREATE TABLE LINEITEM (
            ORDERKEY  bigint not null,
            PARTKEY   bigint not null,
            SUPPKEY   bigint not null,
            L_QUANTITY decimal(12,2),
            PRIMARY KEY (ORDERKEY)
        );

        CREATE TABLE SUPPLIER (
            SUPPKEY   bigint not null,
            NATIONKEY bigint not null,
            S_NAME    char(25),
            PRIMARY KEY (SUPPKEY)
        );

        CREATE TABLE CUSTOMER (
            CUSTKEY   bigint not null,
            NATIONKEY bigint not null,
            C_NAME    varchar(25),
            PRIMARY KEY (CUSTKEY)
        );
    """

sql_1 = """
        SELECT * FROM LINEITEM AS L
        JOIN SUPPLIER USING (SUPPKEY)
        JOIN CUSTOMER ON L.CUSTOMERKEY = CUSTOMER.CUSTOMERKEY
    """

sql_schema_3 = """
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
    NATIONKEY bigint not null,
    S_PHONE char(15),
    S_ACCTBAL decimal(12,2),
    S_COMMENT varchar(101),
    PRIMARY KEY (SUPPKEY)
) WITH ('materialized' = 'true');

CREATE TABLE PARTSUPP (
    PARTKEY bigint not null,
    SUPPKEY bigint not null,
    PS_AVAILQTY integer,
    PS_SUPPLYCOST decimal(12,2),
    PS_COMMENT varchar(199),
    PRIMARY KEY (PARTKEY, SUPPKEY)
) WITH (
    'connectors' = '[{
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/{{FILE_PATH}}/partsupp.csv"
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

CREATE TABLE CUSTOMER (
    CUSTKEY bigint not null,
    C_NAME varchar(25),
    C_ADDRESS varchar(40),
    NATIONKEY bigint not null,
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
) WITH ('materialized' = 'true');

CREATE TABLE REGION (
    REGIONKEY bigint not null,
    R_NAME char(25),
    R_COMMENT varchar(152),
    PRIMARY KEY (REGIONKEY)
) WITH ('materialized' = 'true');
    """

sql_3 = """
    CREATE MATERIALIZED VIEW RESULT AS
    SELECT COUNT(COLUMNTEST)
    FROM LINEITEM
    JOIN ORDERS USING (ORDERKEY)
    JOIN CUSTOMER USING (CUSTKEY)
    JOIN PARTSUPP USING (PARTKEY, SUPPKEY)
    WHERE (REGIONKEY > 10 OR REGIONKEY <5) AND (ORDERKEY <5 OR ORDERKEY >10);
"""

sql_schema_4 = """
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
"""

sql_4 = """
CREATE MATERIALIZED VIEW RESULT AS
SELECT R1.A AS A, R2.B AS B, R3.C AS C, R4.D AS D
FROM EDGES AS R1
JOIN EDGES AS R2(B, C) ON R1.B = R2.B
JOIN EDGES AS R3(C, D) ON R2.C = R3.C
JOIN EDGES AS R4(B, D) ON R4.D = R3.D AND R4.B = R2.B AND (R4.B = R1.B)
JOIN EDGES AS R5(A, D) ON R5.A = R1.A AND R5.D = R4.D AND (R5.D =R3.D);
"""


ast_query = sqlglot.parse_one(sql_3)
ast_schema = sqlglot.parse(sql_schema_4)
print(repr(ast_query))
#print(repr(ast_schema))

#print(ast.args.get("joins")[1].args.get("on").args)


