import sys
import logging
import rds_config
import pymysql
import random
import string

conn = pymysql.connect(rds_config.rds_host, user=rds_config.db_username, passwd=rds_config.db_password, db=rds_config.db_name, connect_timeout=5)

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

def get_login_by_cookie(cookie):
#consider logout - we cannot clean cookies
    if cookie == '':
        return anon

    with conn.cursor() as cur:
        rows_cnt = cur.execute(f'''
            select login from cookie where cookie = '%s';
            ''' % str(cookie))
        if (rows_cnt > 0):
            ret = cur.fetchall()
            conn.commit()
            return ret[0][0]
        else:
            return anon

def is_login_data_correct(login, password):
    with conn.cursor() as cur:
        rows_cnt = cur.execute(f'''
                            select * from user where
                            (login = '%s' and passwd = '%s');
                            ''' % (login, password))
        if (rows_cnt > 0):
            return True
        else:
            return False

def login_exist(login):
    with conn.cursor() as cur:
        rows_cnt = cur.execute(f'''
                            select * from user where
                            (login = '%s');
                            ''' % login)
        if (rows_cnt > 0):
            return True
        else:
            return False


def add_cookie(login):
    N = 15 
    cookie = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

    with conn.cursor() as cur:
        cur.execute(f'''
            insert into cookie (cookie, login) values("%s", "%s");
            ''' % (cookie, login))
        conn.commit()
        return cookie

def is_login_already_created(login):
    with conn.cursor() as cur:
        rows_cnt = cur.execute(f'''
                            select * from user where (login = '%s');
                            ''' % login)
        if (rows_cnt > 0):
            return True
        else:
            return False

def add_user(login, password):
    if is_login_already_created(login): 
        return {'ok_signup': False,
                'err_message': f'''Login %s is already created!''' % login }

    with conn.cursor() as cur:
        cur.execute(f'''
            insert into user (login, passwd) values("%s", "%s");
            ''' % (login, password))
        conn.commit()
        return {'ok_signup' : True }


def add_survey_res(survey_id, login, var_val_map_str):
    with conn.cursor() as cur:
        cur.execute(f'''
            insert into survey_res (survey_id, login, var_val_map)
            values ("%s", "%s", "%s");
            ''' % (survey_id, login, var_val_map_str))
        conn.commit()
