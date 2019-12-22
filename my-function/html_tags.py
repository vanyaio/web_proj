import q_params
import survey
import user
import conf

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
                <form action="./prod" method="get">
                  <input type="hidden" name="%s" value="1">
                  <input type="submit" value="Logout">
                </form>
                <form action="./prod" method="get">
                  <input type="hidden" name="" value="">
                  <input type="submit" value="Go to main menu">
                </form>
                ''' % (user.login, q_params.get_login_page, q_params.get_signup_page, q_params.logout)
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
                    Type your survey template. Example below
                    results in the following survey <br>
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
            <br>
            <form action="./prod" method="get">
              <input type="hidden" name="%s" value="1">
              <input type="submit" value="Log in with google">
            </form>
            
            ''' % (q_params.login, q_params.password, q_params.do_login, q_params.get_google_login_page)

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
        Your survey is created!<br>
        <a href="%s?%s=%s">Link</a>
        ''' % (conf.api_url, q_params.get_survey, str(added_survey))
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

google_login_page = f'''
<html lang="en">
  <head>
    <meta name="google-signin-scope" content="profile email">
    <meta name="google-signin-client_id" 
      content="1069669795497-ifvno18k8plqe1rdumnjls437oehl0ke.apps.googleusercontent.com">
    <script src="https://apis.google.com/js/platform.js" async defer></script>
  </head>
  <body>
    <div class="g-signin2" data-onsuccess="onSignIn" data-theme="dark"></div>
    <p id="content"></p>

    <form action="./prod" method="get">
      <input type="hidden" name="%s" value="1">
      <textarea name="%s" cols="50" rows="40"></textarea>
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
        request.open("GET","https://ogunh8f1ck.execute-api.us-east-1.amazonaws.com/prod", true);
        request.setRequestHeader("Authorization", id_token);
        request.onload = function() {{
          var text = request.responseText;
          document.getElementById("content").innerHTML = id_token;
        }};
        request.send(); 
      }}
    </script>
  </body>
</html>
''' % (q_params.do_login_google, q_params.google_token)
