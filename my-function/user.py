import db_queries
login = ''

def get_current_user(event, cookie=None):
#consider logout - we cannot clean cookies
    global login

    if cookie is not None:
        login = db_queries.get_login_by_cookie(cookie)
        return

    if 'cookie' in event['headers']:
        ck = event['headers']['cookie']
        ck = ck.split(';')
        ck = ck[-1].split()
        login = db_queries.get_login_by_cookie(ck[0])
        return
    else:
        login = db_queries.anon
        return
