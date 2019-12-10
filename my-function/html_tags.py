import q_params
import survey
import user

def wrap_tag(tag):
    html_begin = f'''
                <html>
                <header><title>Public Survey</title></header>
                <body>
                You are logged in as %s <br>
                <form action="./prod" method="get">
                  <input type="hidden" name="%s" value="1">
                  <input type="submit" value="Switch user">
                </form>
                <form action="./prod" method="get">
                  <input type="hidden" name="%s" value="1">
                  <input type="submit" value="Create user">
                </form>
                ''' % (user.login, q_params.get_login_page, q_params.get_signup_page)
    html_end = f'''
                </body>
                </html>
                '''
    return  html_begin + tag + html_end

def main_menu():
    main_menu = f'''
                    <form action="./prod" method="get">
                      <input type="hidden" name="%s" value="1">
                      <input type="submit" value="Create survey">
                    </form>
                ''' % q_params.create_survey
    main_menu = wrap_tag(main_menu)
    return main_menu

def fail_login():
    fail_login_p = f'''
                    Wrong login or password! <br>
                    <form action="./prod" method="get">
                      <input type="hidden" name="%s" value="1">
                      <input type="submit" value="Create survey">
                    </form>
                ''' % q_params.create_survey
    fail_login_p = wrap_tag(fail_login_p)
    return fail_login_p

def signup_res(login, status):
    page = ''
    if (status['ok_signup']):
        page = f'''User %s is successfully created! <br>''' % login
    else:
        page = f'''Signup error: %s <br>''' % status['err_message']

    page += f'''
                <form action="./prod" method="get">
                  <input type="hidden" name="%s" value="1">
                  <input type="submit" value="Create survey">
                </form>
            ''' % q_params.create_survey
    page = wrap_tag(page)
    return page

def create_survey():
    create_survey = f'''
                    <form action="./prod" method="get">
                      <textarea name="%s" cols="50" rows="80"></textarea>
                      <input type="submit" value="Submit">
                    </form>
                    ''' % q_params.create_by_yaml 

    create_survey = wrap_tag(create_survey)
    return create_survey

login_page = f'''
            <form action="./prod" method="get">
              login: <input type="text" name="%s"><br>
              password: <input type="text" name="%s"><br>
              <input type="hidden" name="%s" value="1">
              <input type="submit" value="Log in!">
            </form>
            ''' % (q_params.login, q_params.password, q_params.do_login)

signup_page = f'''
            <form action="./prod" method="get">
              login: <input type="text" name="%s"><br>
              password: <input type="text" name="%s"><br>
              <input type="hidden" name="%s" value="1">
              <input type="submit" value="Add new user!">
            </form>
            ''' % (q_params.login, q_params.password, q_params.do_signup)

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
