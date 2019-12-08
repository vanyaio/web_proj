import json
import db_queries
import html_tags
import q_params
import survey
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def create_by_yaml(yaml_str):
    str1 = yaml_str.replace("\r", "")
    str2 = str1.replace('"', '\\"')
    db_queries.add_survey(db_queries.anon, str2);
    added_survey = db_queries.get_last_survey()

    logger.info(added_survey)

    return html_tags.create_by_yaml(added_survey)
    #  logger.info(yaml_str.count('\n'))
    #  logger.info(yaml_str.count('\r'))
    #  logger.info(len(yaml_str.splitlines()))
    #  return html_tags.create_by_yaml(10)

def get_survey(survey_id):
    logger.info(survey_id)
    yaml_str = db_queries.get_survey_yaml(survey_id)
    return html_tags.get_survey(yaml_str, survey_id)

def get_survey_res(survey_id):
    res_raws = db_queries.get_survey_res(survey_id)
    survey_yaml_str = db_queries.get_survey_yaml(survey_id)
    html_str = ''
    for res in res_raws:
        var_val_map = survey.get_var_val_map_from_str(res['var_val_map'])
        html_str += survey.get_html_survey_res(var_val_map, survey_yaml_str)
    return html_tags.get_survey_res(html_str)

def submit_survey(q_string):
    var_val_map_str = survey.get_var_val_str_from_map(q_string)
    db_queries.add_survey_res(q_string[q_params.survey_id_str], db_queries.anon, var_val_map_str)
    return html_tags.submit_survey(q_string[q_params.survey_id_str])

def lambda_handler(event, context):
    ret = {}
    ret['statusCode'] = 200
    ret['headers'] = {
        'Content-Type': 'text/html'
    }

    #actually that's mapping
    q_string = event["queryStringParameters"]

    if q_string is None:
        ret['body'] = html_tags.main_menu
        return ret
    elif q_params.create_survey in q_string:
        ret['body'] = html_tags.create_survey
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
