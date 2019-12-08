import json

def lambda_handler(event, context):
    ret = {}
    ret['statusCode'] = 200
    ret['headers'] = {
        'Content-Type': 'text/html'
    }

    q_string = event["queryStringParameters"]

    if q_string is None:
        ret['body'] = ""
        return ret

    if ('show' in q_string):
        body_str = f'''
                <html>
                <header><title>This is title</title></header>
                <body>
                Hello world Show %s <br>
                and all is %s
                </body>
                </html>
                    ''' % (q_string['show'], str(q_string)) 
    else:
        body_str = f'''
            <html>
                <header><title>This is title</title></header>
            <body>
                Hello world
                <form action="./prod" method="get">
                  First name: <input type="text" name="show"><br>
                  <input type="checkbox" name="v1" value="Bike"> I have a bike<br>
                  <input type="checkbox" name="v2" value="Car" checked> I have a car<br>
                  Gender? <br>
                  <input type="radio" name="gender" value="male" checked> Male<br>
                  <input type="radio" name="gender" value="female"> Female<br>
                  <input type="radio" name="gender" value="other"> Other<br><br>
                  <input type="submit" value="Submit">
                </form>
            </body>
            </html>
                    '''

    ret['body'] = body_str

    return ret
