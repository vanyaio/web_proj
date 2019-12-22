import q_params
import survey
import user
import conf

css = """
@import url("https://fonts.googleapis.com/css?family=Josefin+Sans:700|Roboto:300");

body{
    font-family: 'Roboto', sans-serif;
    font-weight: 300;
    background-color: rgb(247, 247, 247);   
    width: 800px;
    margin: 60px auto;
    
}

input {
    border: none; 
}

input:focus {
    outline-width: none; 
}

input:hover{
    outline-style: solid;
    outline-color: paleturquoise;    
}

.log{
    font-family: 'Roboto', sans-serif;
    font-weight: 300;
    font-size:27px;
}


.input {
    width: 100%;
    font-family: 'Roboto';
    font-weight: 300;
    font-size:27px;
    
    background-color: rgb(248, 248, 248);
    display: inline;
}


.input-container{
    padding: 9px 14px;
    border: 1px rgb(230, 230, 230) solid;
    border-radius: 4px;
    display: inline;
    background-color: rgb(248, 248, 248);
    margin-bottom: 20px;
    
}

.submit{
    font-family: 'Roboto', sans-serif;
    font-weight: 300;
    font-size:17px;
    border: 1px rgb(230, 230, 230) solid;
    box-shadow: 0px 0px 30px rgba(0, 0, 0, .08);
    margin-bottom: 20px;
    width: 150px;
    padding: 9px 14px;
    background-color: rgb(243, 247, 255);
    border-radius: 4px;
    box-shadow: 0px 0px 30px rgba(0, 0, 0, .05);
    
    
}

.submit-log{
    font-family: 'Roboto', sans-serif;
    font-weight: 300;
    font-size:27px;
    border: 1px rgb(230, 230, 230) solid;
    box-shadow: 0px 0px 30px rgba(0, 0, 0, .08);
    margin-bottom: 20px;
    width: 250px;
    padding: 9px 14px;
    background-color: rgb(243, 247, 255);
    border-radius: 4px;
    box-shadow: 0px 0px 30px rgba(0, 0, 0, .05);
    
    
}


form{
    display:inline;
}

textarea{
    font-family: 'Roboto', sans-serif;
    font-weight: 300;
    padding-left: 15px;
}
"""

def wrap_tag(tag):
    html_begin = f'''
                <html>
                <header><title>Public Survey</title></header>
                <style>
                %s
                </style>
                <body>
                <div class="log">You are logged in as %s</div> <br>
                <form action="./prod" method="get">
                  <input type="hidden" name="%s" value="1">
                  <input type="submit" class="submit" value="Switch user">
                </form>
                <form action="./prod" method="get">
                  <input type="hidden" name="%s" value="1">
                  <input type="submit" class="submit" value="Create user">
                </form>
                <form action="./prod" method="get">
                  <input type="hidden" name="%s" value="1">
                  <input type="submit" class="submit" value="Logout">
                </form>
                <form action="./prod" method="get">
                  <input type="hidden" name="" value="">
                  <input type="submit" class="submit" value="Go to main menu">
                </form>
                ''' % (css, user.login, q_params.get_login_page, q_params.get_signup_page, q_params.logout)
    html_end = f'''
                </body>
                </html>
                '''
    return  html_begin + tag + html_end

def main_menu():
    main_menu = f'''
                    <form action="./prod" method="get">
                      <input type="hidden" name="%s" value="1">
                      <input type="submit" class="submit" value="Create survey">
                    </form>
                ''' % q_params.create_survey
    main_menu = wrap_tag(main_menu)
    return main_menu

def fail_login():
    fail_login_p = f'''
                    <div class="log">  Wrong login or password! <br> </div>
                    <form action="./prod" method="get">
                      <input type="hidden" name="%s" value="1">
                      <input type="submit" class="submit" value="Create survey">
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
                  <input type="submit" class="submit" value="Create survey">
                </form>
            ''' % q_params.create_survey
    page = wrap_tag(page)
    return page

def create_survey():
    create_survey = f'''
                  <div class="log">    
                    Type your survey template. Example below
                    results in the following survey </div> <br>
                    <form action="./prod" method="get">
                        Your gender?<br>
                        <input type="radio" name="name1" value="male"> Male <br> 
                        <input type="radio" name="name1" value="female"> Female <br> 
                        Your favourite car?<br>
                        <input type="radio" name="name2" value="bmw"> BMW <br> 
                        <input type="radio" name="name2" value="mers"> Mersedes <br> 
                        <input type="hidden" name="submit_survey" value="1">
                        <input type="hidden" name="survey_id" value="24">
                    </form>
                    <br>
                    <form action="./prod" method="get">
                      <textarea name="%s" cols="40" rows="25">
- type: desc
  desc: "Your gender?"
- type: radio
  opts:
    - val: male
      desc: "Male"
    - val: female
      desc: "Female"
- type: desc
  desc: "Your favourite car?"
- type: radio
  opts:
    - val: bmw
      desc: "BMW"
    - val: mers
      desc: "Mersedes"
                      </textarea>
                      <br>
                      <input type="submit" class="submit" value="Submit">
                    </form>
                    ''' % q_params.create_by_yaml 

    create_survey = wrap_tag(create_survey)
    return create_survey

login_page = f'''
            <form  class="input" action="./prod" method="get">
              login: <input type="text" name="%s"><br>
              password: <input type="text" name="%s"><br>
              <input type="hidden" name="%s" value="1">
              <input class="submit-log" type="submit" value="Log in!">
            </form>
            <br>
            <form class="input" action="./prod" method="get">
              <input type="hidden" name="%s" value="1">
              <input  class="submit-log" type="submit" value="Log in with google">
            </form>
            
            ''' % (q_params.login, q_params.password, q_params.do_login, q_params.get_google_login_page)

signup_page = f'''
            <form action="./prod" method="get">
              login: <input type="text" name="%s"><br>
              password: <input type="text" name="%s"><br>
              <input type="hidden" name="%s" value="1">
              <input type="submit" class="submit-log" value="Add new user!">
            </form>
            ''' % (q_params.login, q_params.password, q_params.do_signup)

def create_by_yaml(added_survey):
    html_str = f'''
      <div class="log">    
        Your survey is created!<br>
        <a href="%s?%s=%s">Link</a>
      </div>
        ''' % (conf.api_url, q_params.get_survey, str(added_survey))
    return wrap_tag(html_str)

def get_user_info(login):
    html = f'''
            <br> User %s info <br>
            <form action="./prod" method="get">
              <input type="hidden" name="%s" value="1">
              <input type="hidden" name="login" value="%s">
              <input type="submit" value="Surveys created by user!">
            </form>
            ''' % (login, q_params.get_user_surveys, login)
    return wrap_tag(html)

def user_link(login):
    html_str = f'''
        <br>
        <a href="%s?%s=1&login=%s">%s</a><br>
        ''' % (conf.api_url, q_params.get_user_info, login, login)
    return html_str

def get_user_surveys(login, surveys):
    html_str = f'''<br> Surveys created by %s''' % login
    for survey in surveys:
        survey_id = survey[0]
        html_str += f'''
          <div class="log">    
            <a href="%s?%s=%s">Survey id %s</a> <br>
          </div>
            ''' % (conf.api_url, q_params.get_survey, str(survey_id), str(survey_id))
    return wrap_tag(html_str)

def get_survey(yaml_str, survey_id):
    html_str = f'''
                    <form action="./prod" method="get">
                      <input type="hidden" name="%s" value="%s">
                      <input type="submit" class="submit" value="See survey results">
                    </form>
                ''' % (q_params.get_survey_res, str(survey_id))
    html_str += survey.get_html_survey_from_yaml_str(yaml_str, "./prod", survey_id)
    return wrap_tag(html_str)

def submit_survey(survey_id):
    html_str = 'Successful submit! <br>'
    html_str += f'''
                    <form action="./prod" method="get">
                      <input type="hidden" name="%s" value="%s">
                      <input type="submit" class="submit" value="See survey results">
                    </form>
                ''' % (q_params.get_survey_res, str(survey_id))
    return wrap_tag(html_str)

def get_survey_res(html_surveys_list_str):
    return wrap_tag(html_surveys_list_str)

google_login_page = f'''
<html lang="en">
  <head>
    <meta name="google-signin-scope" content="profile email">
    <meta name="google-signin-client_id" 
      content="%s.apps.googleusercontent.com">
    <script src="https://apis.google.com/js/platform.js" async defer></script>
  </head>
  <body>
    <div class="g-signin2" data-onsuccess="onSignIn" data-theme="dark"></div>

    <form action="./prod" method="get">
      <input type="hidden" name="%s" value="1">
      <textarea name="%s" cols="50" rows="40" id="tokenField">No token provided: Sign in first</textarea>
      <br>
      <input type="submit" value="Login with this token">
    </form>

    <script>
      function onSignIn(googleUser) {{
        // Useful data for your client-side scripts:
        var profile = googleUser.getBasicProfile();
        console.log("ID: " + profile.getId()); // Don't send this directly to your server!
        console.log("Full Name: " + profile.getName());
        console.log("Given Name: " + profile.getGivenName());
        console.log("Family Name: " + profile.getFamilyName());
        console.log("Image URL: " + profile.getImageUrl());
        console.log("Email: " + profile.getEmail());
 
        // The ID token you need to pass to your backend:
        var id_token = googleUser.getAuthResponse().id_token;
        console.log("ID Token: " + id_token);
 
        var request = new XMLHttpRequest();
        request.open("GET","%s", true);
        request.setRequestHeader("Authorization", id_token);
        request.onload = function() {{
          var text = request.responseText;
          document.getElementById("tokenField").innerHTML = id_token;
        }};
        request.send(); 
      }}
    </script>
  </body>
</html>
''' % (conf.google_token, q_params.do_login_google, q_params.google_token, conf.api_url)
