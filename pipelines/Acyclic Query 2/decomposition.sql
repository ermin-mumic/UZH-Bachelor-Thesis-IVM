-- The IMDB Schema.
CREATE TABLE aka_name (
    an_id integer NOT NULL PRIMARY KEY,
    person_id integer NOT NULL,
    an_name character varying,
    an_imdb_index character varying(3),
    an_name_pcode_cf character varying(11),
    an_name_pcode_nf character varying(11),
    an_surname_pcode character varying(11),
    an_md5sum character varying(65)
) WITH (
    'connectors' = '[{
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/{{FILE_PATH}}/aka_name.csv"
            }
        },
        "format": { 
            "name": "csv",
            "config": {
                "headers": false
            }
        }
    }]'
);

CREATE TABLE aka_title (
    at_id integer NOT NULL PRIMARY KEY,
    at_movie_id integer NOT NULL,
    at_title character varying,
    at_imdb_index character varying(4),
    at_kind_id integer NOT NULL,
    at_production_year integer,
    at_phonetic_code character varying(5),
    at_episode_of_id integer,
    at_season_nr integer,
    at_episode_nr integer,
    at_note character varying(72),
    at_md5sum character varying(32)
) WITH ('materialized' = 'true');

CREATE TABLE cast_info (
    ci_id integer NOT NULL PRIMARY KEY,
    person_id integer NOT NULL,
    movie_id integer NOT NULL,
    char_id integer,
    ci_note character varying,
    ci_nr_order integer,
    role_id integer NOT NULL
) WITH (
    'connectors' = '[{
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/{{FILE_PATH}}/cast_info.csv"
            }
        },
        "format": { 
            "name": "csv",
            "config": {
                "headers": false
            }
        }
    }]'
);

CREATE TABLE char_name (
    char_id integer NOT NULL PRIMARY KEY,
    chn_name character varying NOT NULL,
    chn_imdb_index character varying(2),
    chn_imdb_id integer,
    chn_name_pcode_nf character varying(5),
    chn_surname_pcode character varying(5),
    chn_md5sum character varying(32)
) WITH (
    'connectors' = '[{
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/{{FILE_PATH}}/char_name.csv"
            }
        },
        "format": { 
            "name": "csv",
            "config": {
                "headers": false
            }
        }
    }]'
);

CREATE TABLE comp_cast_type (
    cct_id integer NOT NULL PRIMARY KEY,
    cct_kind character varying(32) NOT NULL
) WITH ('materialized' = 'true');

CREATE TABLE company_name (
    company_id integer NOT NULL PRIMARY KEY,
    cn_name character varying NOT NULL,
    cn_country_code character varying(6),
    cn_imdb_id integer,
    cn_name_pcode_nf character varying(5),
    cn_name_pcode_sf character varying(5),
    cn_md5sum character varying(32)
) WITH (
    'connectors' = '[{
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/{{FILE_PATH}}/company_name.csv"
            }
        },
        "format": { 
            "name": "csv",
            "config": {
                "headers": false
            }
        }
    }]'
);

CREATE TABLE company_type (
    company_type_id integer NOT NULL PRIMARY KEY,
    ct_kind character varying(32)
) WITH ('materialized' = 'true');

CREATE TABLE complete_cast (
    cc_id integer NOT NULL PRIMARY KEY,
    cc_movie_id integer,
    cc_subject_id integer NOT NULL,
    cc_status_id integer NOT NULL
) WITH ('materialized' = 'true');

CREATE TABLE info_type (
    info_type_id integer NOT NULL PRIMARY KEY,
    it_info character varying(32) NOT NULL
) WITH (
    'connectors' = '[{
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/{{FILE_PATH}}/info_type.csv"
            }
        },
        "format": { 
            "name": "csv",
            "config": {
                "headers": false
            }
        }
    }]'
);

CREATE TABLE keyword (
    k_id integer NOT NULL PRIMARY KEY,
    k_keyword character varying NOT NULL,
    k_phonetic_code character varying(5)
) WITH ('materialized' = 'true');

CREATE TABLE kind_type (
    kt_id integer NOT NULL PRIMARY KEY,
    kt_kind character varying(15)
) WITH ('materialized' = 'true');

CREATE TABLE link_type (
    lt_id integer NOT NULL PRIMARY KEY,
    lt_link character varying(32) NOT NULL
) WITH ('materialized' = 'true');

CREATE TABLE movie_companies (
    mc_id integer NOT NULL PRIMARY KEY,
    movie_id integer NOT NULL,
    company_id integer NOT NULL,
    company_type_id integer NOT NULL,
    mc_note character varying
) WITH (
    'connectors' = '[{
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/{{FILE_PATH}}/movie_companies.csv"
            }
        },
        "format": { 
            "name": "csv",
            "config": {
                "headers": false
            }
        }
    }]'
);

CREATE TABLE movie_info_idx (
    mii_id integer NOT NULL PRIMARY KEY,
    movie_id integer NOT NULL,
    info_type_id integer NOT NULL,
    mii_info character varying NOT NULL,
    mii_note character varying(1)
) WITH ('materialized' = 'true');

CREATE TABLE movie_keyword (
    mk_id integer NOT NULL PRIMARY KEY,
    mk_movie_id integer NOT NULL,
    mk_keyword_id integer NOT NULL
) WITH ('materialized' = 'true');

CREATE TABLE movie_link (
    ml_id integer NOT NULL PRIMARY KEY,
    ml_movie_id integer NOT NULL,
    ml_linked_movie_id integer NOT NULL,
    ml_link_type_id integer NOT NULL
) WITH ('materialized' = 'true');

CREATE TABLE name (
    person_id integer NOT NULL PRIMARY KEY,
    n_name character varying NOT NULL,
    n_imdb_index character varying(9),
    n_imdb_id integer,
    n_gender character varying(1),
    n_name_pcode_cf character varying(5),
    n_name_pcode_nf character varying(5),
    n_surname_pcode character varying(5),
    n_md5sum character varying(32)
) WITH (
    'connectors' = '[{
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/{{FILE_PATH}}/name.csv"
            }
        },
        "format": { 
            "name": "csv",
            "config": {
                "headers": false
            }
        }
    }]'
);

CREATE TABLE role_type (
    role_id integer NOT NULL PRIMARY KEY,
    rt_role character varying(32) NOT NULL
) WITH (
    'connectors' = '[{
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/{{FILE_PATH}}/role_type.csv"
            }
        },
        "format": { 
            "name": "csv",
            "config": {
                "headers": false
            }
        }
    }]'
);

CREATE TABLE title (
    movie_id integer NOT NULL PRIMARY KEY,
    t_title character varying NOT NULL,
    t_imdb_index character varying(5),
    t_kind_id integer NOT NULL,
    t_production_year integer,
    t_imdb_id integer,
    t_phonetic_code character varying(5),
    t_episode_of_id integer,
    t_season_nr integer,
    t_episode_nr integer,
    t_series_years character varying(49),
    t_md5sum character varying(32)
) WITH (
    'connectors' = '[{
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/{{FILE_PATH}}/title.csv"
            }
        },
        "format": { 
            "name": "csv",
            "config": {
                "headers": false
            }
        }
    }]'
);

CREATE TABLE movie_info (
    mi_id integer NOT NULL PRIMARY KEY,
    movie_id integer NOT NULL,
    info_type_id integer NOT NULL,
    mi_info character varying NOT NULL,
    mi_note character varying
) WITH (
    'connectors' = '[{
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/{{FILE_PATH}}/movie_info.csv"
            }
        },
        "format": { 
            "name": "csv",
            "config": {
                "headers": false
            }
        }
    }]'
);

CREATE TABLE person_info (
    pi_id integer NOT NULL PRIMARY KEY,
    pi_person_id integer NOT NULL,
    pi_info_type_id integer NOT NULL,
    pi_info character varying NOT NULL,
    pi_note character varying
) WITH ('materialized' = 'true');

-- Child Bag 1.
CREATE MATERIALIZED VIEW CHILD_1_Q AS
SELECT *
FROM company_name
JOIN (
    SELECT DISTINCT company_id
    FROM movie_companies
)
USING (company_id);

CREATE MATERIALIZED VIEW CHILD_1_P AS
SELECT DISTINCT company_id
FROM CHILD_1_Q;

-- Child Bag 2.
CREATE MATERIALIZED VIEW CHILD_2_Q AS
SELECT *
FROM info_type
JOIN (
    SELECT DISTINCT info_type_id
    FROM movie_info
)
USING (info_type_id);

CREATE MATERIALIZED VIEW CHILD_2_P AS
SELECT DISTINCT info_type_id
FROM CHILD_2_Q;

-- Child Bag 3.
CREATE MATERIALIZED VIEW CHILD_3_Q AS
SELECT *
FROM movie_companies
JOIN (
    SELECT DISTINCT movie_id
    FROM title
)
USING (movie_id)
JOIN (
    SELECT DISTINCT movie_id
    FROM movie_info
)
USING (movie_id)
JOIN (
    SELECT DISTINCT movie_id
    FROM cast_info
)
USING (movie_id)
JOIN (
    SELECT DISTINCT company_id
    FROM company_name
)
USING (company_id)
JOIN CHILD_1_P USING (company_id);

CREATE MATERIALIZED VIEW CHILD_3_P AS
SELECT DISTINCT movie_id
FROM CHILD_3_Q;

-- Child Bag 4.
CREATE MATERIALIZED VIEW CHILD_4_Q AS
SELECT *
FROM movie_info
JOIN (
    SELECT DISTINCT movie_id
    FROM movie_companies
)
USING (movie_id)
JOIN (
    SELECT DISTINCT movie_id
    FROM title
)
USING (movie_id)
JOIN (
    SELECT DISTINCT movie_id
    FROM cast_info
)
USING (movie_id)
JOIN (
    SELECT DISTINCT info_type_id
    FROM info_type
)
USING (info_type_id)
JOIN CHILD_2_P USING (info_type_id);

CREATE MATERIALIZED VIEW CHILD_4_P AS
SELECT DISTINCT movie_id
FROM CHILD_4_Q;

-- Child Bag 5.
CREATE MATERIALIZED VIEW CHILD_5_Q AS
SELECT *
FROM name
JOIN (
    SELECT DISTINCT person_id
    FROM aka_name
)
USING (person_id)
JOIN (
    SELECT DISTINCT person_id
    FROM cast_info
)
USING (person_id);

CREATE MATERIALIZED VIEW CHILD_5_P AS
SELECT DISTINCT person_id
FROM CHILD_5_Q;

--Child Bag 6.
CREATE MATERIALIZED VIEW CHILD_6_Q AS
SELECT *
FROM role_type
JOIN (
    SELECT DISTINCT role_id
    FROM cast_info
)
USING (role_id);

CREATE MATERIALIZED VIEW CHILD_6_P AS
SELECT DISTINCT role_id
FROM CHILD_6_Q;

--Child Bag 7.
CREATE MATERIALIZED VIEW CHILD_7_Q AS
SELECT *
FROM aka_name
JOIN (
    SELECT DISTINCT person_id
    FROM name
)
USING (person_id)
JOIN (
    SELECT DISTINCT person_id
    FROM cast_info
)
USING (person_id);

CREATE MATERIALIZED VIEW CHILD_7_P AS
SELECT DISTINCT person_id
FROM CHILD_7_Q;

--Child Bag 8.
CREATE MATERIALIZED VIEW CHILD_8_Q AS
SELECT *
FROM char_name
JOIN (
    SELECT DISTINCT char_id
    FROM cast_info
)
USING (char_id);

CREATE MATERIALIZED VIEW CHILD_8_P AS
SELECT DISTINCT char_id
FROM CHILD_8_Q;

--Child Bag 9.
CREATE MATERIALIZED VIEW CHILD_9_Q AS
SELECT *
FROM title
JOIN (
    SELECT DISTINCT movie_id
    FROM movie_companies
)
USING (movie_id)
JOIN (
    SELECT DISTINCT movie_id
    FROM movie_info
)
USING (movie_id)
JOIN (
    SELECT DISTINCT movie_id
    FROM cast_info
)
USING (movie_id);

CREATE MATERIALIZED VIEW CHILD_9_P AS
SELECT DISTINCT movie_id
FROM CHILD_9_Q;

--Root Bag.
CREATE MATERIALIZED VIEW RESULT AS
SELECT *
FROM cast_info
JOIN (
    SELECT DISTINCT movie_id
    FROM movie_companies
)
USING (movie_id)
JOIN (
    SELECT DISTINCT movie_id
    FROM title
)
USING (movie_id)
JOIN (
    SELECT DISTINCT movie_id
    FROM movie_info
)
USING (movie_id)
JOIN (
    SELECT DISTINCT role_id
    FROM role_type
)
USING (role_id)
JOIN (
    SELECT DISTINCT char_id
    FROM char_name
)
USING (char_id)
JOIN (
    SELECT DISTINCT person_id
    FROM aka_name
)
USING (person_id)
JOIN (
    SELECT DISTINCT person_id
    FROM name
)
USING (person_id)
JOIN CHILD_5_P USING (person_id)
JOIN CHILD_6_P USING (role_id)
JOIN CHILD_7_P USING (person_id)
JOIN CHILD_3_P USING (movie_id)
JOIN CHILD_8_P USING (char_id)
JOIN CHILD_4_P USING (movie_id)
JOIN CHILD_9_P USING (movie_id);