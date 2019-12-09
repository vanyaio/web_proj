import json

def lambda_handler(event, context):
    ret = {}
    ret['statusCode'] = 200
    ret['headers'] = {
        'Content-Type': 'text/html',
        'Set-Cookie': 'cookiearehere'
    }

    if 'cookie' in event['headers']:
        ret['body'] = event['headers']['cookie'] 
    else:
        ret['body'] = 'no cookies <br>'
        ret['body'] += json.dumps(event)

    return ret
