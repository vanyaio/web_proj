import json
import db_queries
import html_tags
import q_params

def create_by_yaml(yaml_str):
    db_queries.survey_add(db_queries.anon, yaml_str);
    added_survey = db_queries.get_last_survey()
    return html_tags.create_by_yaml(added_survey)

def get_survey(survey_id):
    yaml_str = db_queries.get_survey_yaml(survey_id)
    return html_tags.get_survey(yaml_str)

def get_survey_res(servey_id):
    
def lambda_handler(event, context):
    ret = {}
    ret['statusCode'] = 200
    ret['headers'] = {
        'Content-Type': 'text/html'
    }

    q_string = event["queryStringParameters"]

    if q_string is None:
        ret['body'] = html_tags.main_menu
        return ret
    elif q_params.create_survey in q_string:
        ret['body'] = html_tags.create_survey
        return ret
    elif q_pamars.create_by_yaml in q_string:
        ret['body'] = create_by_yaml(q_string[q_params.create_by_yaml])
        return ret
    elif q_params.get_survey in q_string:
        ret['body'] = get_survey(q_string[q_params.get_survey])
        return ret
    elif q_params.get_survey_res in q_string:
        ret['body'] = get_survey_res(q_string[q_params.get_survey_res])
        return ret
