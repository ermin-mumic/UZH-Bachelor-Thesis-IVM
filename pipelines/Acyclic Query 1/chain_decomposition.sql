-- The IMDB Schema.
CREATE TABLE aka_name (
    an_id integer NOT NULL PRIMARY KEY,
    an_person_id integer NOT NULL,
    an_name character varying,
    an_imdb_index character varying(3),
    an_name_pcode_cf character varying(11),
    an_name_pcode_nf character varying(11),
    an_surname_pcode character varying(11),
    an_md5sum character varying(65)
) WITH ('materialized' = 'true');

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
    ci_person_id integer NOT NULL,
    ci_movie_id integer NOT NULL,
    ci_person_role_id integer,
    ci_note character varying,
    ci_nr_order integer,
    ci_role_id integer NOT NULL
) WITH ('materialized' = 'true');

CREATE TABLE char_name (
    chn_id integer NOT NULL PRIMARY KEY,
    chn_name character varying NOT NULL,
    chn_imdb_index character varying(2),
    chn_imdb_id integer,
    chn_name_pcode_nf character varying(5),
    chn_surname_pcode character varying(5),
    chn_md5sum character varying(32)
) WITH ('materialized' = 'true');

CREATE TABLE comp_cast_type (
    cct_id integer NOT NULL PRIMARY KEY,
    cct_kind character varying(32) NOT NULL
) WITH ('materialized' = 'true');

CREATE TABLE company_name (
    cn_id integer NOT NULL PRIMARY KEY,
    cn_name character varying NOT NULL,
    cn_country_code character varying(6),
    cn_imdb_id integer,
    cn_name_pcode_nf character varying(5),
    cn_name_pcode_sf character varying(5),
    cn_md5sum character varying(32)
) WITH ('materialized' = 'true');

CREATE TABLE company_type (
    company_type_id integer NOT NULL PRIMARY KEY,
    ct_kind character varying(32)
) WITH (
    'connectors' = '[{
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/{{FILE_PATH}}/company_type.csv"
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
    mc_company_id integer NOT NULL,
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
) WITH (
    'connectors' = '[{
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/{{FILE_PATH}}/movie_info_idx.csv"
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
    n_id integer NOT NULL PRIMARY KEY,
    n_name character varying NOT NULL,
    n_imdb_index character varying(9),
    n_imdb_id integer,
    n_gender character varying(1),
    n_name_pcode_cf character varying(5),
    n_name_pcode_nf character varying(5),
    n_surname_pcode character varying(5),
    n_md5sum character varying(32)
) WITH ('materialized' = 'true');

CREATE TABLE role_type (
    rt_id integer NOT NULL PRIMARY KEY,
    rt_role character varying(32) NOT NULL
) WITH ('materialized' = 'true');

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
    mi_movie_id integer NOT NULL,
    mi_info_type_id integer NOT NULL,
    mi_info character varying NOT NULL,
    mi_note character varying
) WITH ('materialized' = 'true');

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
FROM title
JOIN (
    SELECT DISTINCT movie_id
    FROM movie_companies
)
USING (movie_id)
JOIN (
    SELECT DISTINCT movie_id
    FROM movie_info_idx
)
USING (movie_id);

CREATE MATERIALIZED VIEW CHILD_1_P AS
SELECT DISTINCT movie_id
FROM CHILD_1_Q;

-- Child Bag 2.
CREATE MATERIALIZED VIEW CHILD_2_Q AS
SELECT *
FROM company_type
JOIN (
    SELECT DISTINCT company_type_id
    FROM movie_companies
)
USING (company_type_id);

CREATE MATERIALIZED VIEW CHILD_2_P AS
SELECT DISTINCT company_type_id
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
    FROM movie_info_idx
)
USING (movie_id)
JOIN (
    SELECT DISTINCT company_type_id
    FROM company_type
)
USING (company_type_id)
JOIN CHILD_1_P USING (movie_id)
JOIN CHILD_2_P USING (company_type_id);

CREATE MATERIALIZED VIEW CHILD_3_P AS
SELECT DISTINCT movie_id
FROM CHILD_3_Q;

--Child Bag 4.
CREATE MATERIALIZED VIEW CHILD_4_Q AS
SELECT *
FROM movie_info_idx
JOIN (
    SELECT DISTINCT movie_id
    FROM title
)
USING (movie_id)
JOIN (
    SELECT DISTINCT movie_id
    FROM movie_companies
)
USING (movie_id)
JOIN (
    SELECT DISTINCT info_type_id
    FROM info_type
)
USING (info_type_id)
JOIN CHILD_3_P USING (movie_id);

CREATE MATERIALIZED VIEW CHILD_4_P AS
SELECT DISTINCT info_type_id
FROM CHILD_4_Q;

-- Root Bag.
CREATE MATERIALIZED VIEW RESULT AS
SELECT *
FROM info_type
JOIN (
    SELECT DISTINCT info_type_id
    FROM movie_info_idx
)
USING (info_type_id)
JOIN CHILD_4_P USING (info_type_id);



