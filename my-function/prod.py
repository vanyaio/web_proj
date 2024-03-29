from __future__ import print_function
import json
import db_queries
import html_tags
import q_params
import survey
import logging
import user
from google.auth.transport import requests
from google.oauth2 import id_token
import boto3
import conf

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sns = boto3.client('sns')

def create_by_yaml(yaml_str):
    str1 = yaml_str.replace("\r", "")
    str2 = str1.replace('"', '\\"')
    db_queries.add_survey(user.login, str2);
    added_survey = db_queries.get_last_survey()

    logger.info(added_survey)
    #sns.publish(PhoneNumber = conf.admin_number, Message=f'''Added new survey id %s''' % str(added_survey))

    return html_tags.create_by_yaml(added_survey)

def get_survey(survey_id):
    logger.info(survey_id)
    yaml_str = db_queries.get_survey_yaml(survey_id)
    return html_tags.get_survey(yaml_str, survey_id)

def get_survey_res(survey_id):
    res_raws = db_queries.get_survey_res(survey_id)
    survey_yaml_str = db_queries.get_survey_yaml(survey_id)
    html_str = ''
    for res in res_raws:
        var_val_map = survey.get_var_val_map_from_str(res[2])
        login = res[1]
        #  html_str += str(login) + " <br>"
        html_str += html_tags.user_link(login) 
        html_str += survey.get_html_survey_res(var_val_map, survey_yaml_str)
    return html_tags.get_survey_res(html_str)

def submit_survey(q_string):
    var_val_map_str = survey.get_var_val_str_from_map(q_string)
    db_queries.add_survey_res(q_string[q_params.survey_id_str], user.login, var_val_map_str)
    return html_tags.submit_survey(q_string[q_params.survey_id_str])

ok_login = 'ok_login'
cookie = 'cookie'
def do_login(login, password):
    status = {}
    status[ok_login] = db_queries.is_login_data_correct(login, password)
    if not status[ok_login]:
        return status
    status[cookie] = db_queries.add_cookie(login)
    return status

def do_signup(login, password):
    status = db_queries.add_user(login, password)
    return status

def do_login_google(token): 
    status = {}
    try:
        idInformation = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            f'''%s.apps.googleusercontent.com''' % conf.google_token)
        logger.info(idInformation)
 
        if idInformation['iss'] not in ['accounts.google.com', 
            'https://accounts.google.com']:
            status[ok_login] = False 
            return status
 
        # Get principalId from idInformation
        status[ok_login] = True 
        #  google_login = idInformation['sub']
        #  google_login = idInformation['name']
        google_login = idInformation['email']
        if (not db_queries.login_exist(google_login)):
            db_queries.add_user(google_login, 'SecretGooglePassword')
        status[cookie] = db_queries.add_cookie(google_login)
        return status
 
    except ValueError as err:
        status[ok_login] = False 
        return status

def get_user_surveys(login):
    surveys = db_queries.get_user_surveys(login)
    return html_tags.get_user_surveys(login, surveys)

def lambda_handler(event, context):
    ret = {}
    ret['statusCode'] = 200
    ret['headers'] = {
        'Content-Type': 'text/html'
    }

    #  logger.info(event['headers']['cookie'])
    user.get_current_user(event)
    #  logger.info(user.login)
    #actually that's mapping
    q_string = event["queryStringParameters"]

    if q_string is None:
        ret['body'] = html_tags.main_menu()
        return ret
    elif q_params.get_login_page in q_string:
        ret['body'] = html_tags.login_page
        return ret
    elif q_params.get_google_login_page in q_string:
        ret['body'] = html_tags.google_login_page
        return ret
    elif q_params.logout in q_string:
        ret['headers']['Set-Cookie'] = ''
        user.login = db_queries.anon
        ret['body'] = html_tags.main_menu()
        return ret
    elif q_params.get_signup_page in q_string:
        ret['body'] = html_tags.signup_page
        return ret
    elif q_params.do_login in q_string:
        login_status = do_login(q_string[q_params.login], q_string[q_params.password])
        if (login_status[ok_login]):
            ret['headers']['Set-Cookie'] = login_status[cookie] 
            user.get_current_user(None, login_status[cookie])
            ret['body'] = html_tags.main_menu()
            return ret
        else:
            ret['body'] = html_tags.fail_login()
            return ret
    elif q_params.do_login_google in q_string: #copypaste from above
        login_status = do_login_google(q_string[q_params.google_token])
        if (login_status[ok_login]):
            ret['headers']['Set-Cookie'] = login_status[cookie] 
            user.get_current_user(None, login_status[cookie])
            ret['body'] = html_tags.main_menu()
            return ret
        else:
            ret['body'] = html_tags.fail_login()
            return ret
    elif q_params.do_signup in q_string:
        signup_status = do_signup(q_string[q_params.login], q_string[q_params.password])
        ret['body'] = html_tags.signup_res(q_string[q_params.login], signup_status)
        return ret
    elif q_params.create_survey in q_string:
        ret['body'] = html_tags.create_survey()
        #  ret['body'] = str(type(event)) + "<br>" + str(event) + "<br>" + "keke"
        return ret
    elif q_params.create_by_yaml in q_string:
        ret['body'] = create_by_yaml(q_string[q_params.create_by_yaml])
        return ret
    elif q_params.get_survey in q_string:
        ret['body'] = get_survey(q_string[q_params.get_survey])
        return ret
    elif q_params.submit_survey in q_string:
        ret['body'] = submit_survey(q_string)
        return ret
    elif q_params.get_survey_res in q_string:
        ret['body'] = get_survey_res(q_string[q_params.get_survey_res])
        return ret
    elif q_params.get_user_surveys in q_string:
        ret['body'] = get_user_surveys(q_string[q_params.login])
        return ret
    elif q_params.get_user_info in q_string:
        ret['body'] = html_tags.get_user_info(q_string[q_params.login])
        return ret
