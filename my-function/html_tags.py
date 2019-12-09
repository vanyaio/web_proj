import q_params
import survey

def wrap_tag(tag):
    html_begin = f'''
                <html>
                <header><title>Public Survey</title></header>
                <body>
                '''
    html_end = f'''
                </body>
                </html>
                '''
    return  html_begin + tag + html_end

main_menu = f'''
                <form action="./prod" method="get">
                  <input type="hidden" name="%s" value="1">
                  <input type="submit" value="Create survey">
                </form>
            ''' % q_params.create_survey
main_menu = wrap_tag(main_menu)

create_survey = f'''
                <form action="./prod" method="get">
                  <textarea name="%s" cols="50" rows="80"></textarea>
                  <input type="submit" value="Submit">
                </form>
                ''' % q_params.create_by_yaml 

create_survey = wrap_tag(create_survey)

def create_by_yaml(added_survey):
    html_str = f'''
        Your survey is created!
        Link: /prod?%s=%s
        ''' % (q_params.get_survey, str(added_survey))
    return wrap_tag(html_str)

def get_survey(yaml_str, survey_id):
    html_str = f'''
                    <form action="./prod" method="get">
                      <input type="hidden" name="%s" value="%s">
                      <input type="submit" value="See survey results">
                    </form>
                ''' % (q_params.get_survey_res, str(survey_id))
    html_str += survey.get_html_survey_from_yaml_str(yaml_str, "./prod", survey_id)
    return wrap_tag(html_str)

def submit_survey(survey_id):
    html_str = 'Successful submit! <br>'
    html_str += f'''
                    <form action="./prod" method="get">
                      <input type="hidden" name="%s" value="%s">
                      <input type="submit" value="See survey results">
                    </form>
                ''' % (q_params.get_survey_res, str(survey_id))
    return wrap_tag(html_str)

def get_survey_res(html_surveys_list_str):
    return wrap_tag(html_surveys_list_str)
