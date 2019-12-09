import sys
import logging
import rds_config
import pymysql

rds_host = "database-2.ctr9yzjpib8v.us-east-1.rds.amazonaws.com"
conn = pymysql.connect(rds_host, user=rds_config.db_username, passwd=rds_config.db_password, db=rds_config.db_name, connect_timeout=5)

anon = 'Anonymous'

def add_survey(login, yaml_tmpl):
    with conn.cursor() as cur:
        cur.execute(f'''
            insert into survey (login, yaml) values("%s", "%s");
            ''' % (login, yaml_tmpl))
        conn.commit()

def get_last_survey():
    with conn.cursor() as cur:
        cur.execute(f'''
            select id from survey where
            id = (select max(id) from survey);
            ''')
        ret = cur.fetchall()
        conn.commit()
        return ret[0][0]

def get_survey_yaml(survey_id):
    with conn.cursor() as cur:
        cur.execute(f'''
            select yaml from survey where id = %s;
            ''' % survey_id)
        ret = cur.fetchall()
        conn.commit()
        return ret[0][0]

def get_survey_res(survey_id):
    with conn.cursor() as cur:
        cur.execute(f'''
            select * from survey_res where survey_id = %s;
            ''' % str(survey_id))
        ret = cur.fetchall()
        conn.commit()
        return ret

def add_survey_res(survey_id, login, var_val_map_str):
    with conn.cursor() as cur:
        cur.execute(f'''
            insert into survey_res (survey_id, login, var_val_map)
            values ("%s", "%s", "%s");
            ''' % (survey_id, login, var_val_map_str))
        conn.commit()
