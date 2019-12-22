import yaml
import q_params
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

def parse_yaml_string(ys):
    fd = StringIO(ys)
    dct = yaml.load(fd, Loader=yaml.FullLoader)
    return dct

def get_html_survey_from_yaml_str(survey_str, form_action, survey_id):
    name_cnt = 1
    html_str = f'''<form action="%s" method="get">''' % form_action
    yaml_dict = parse_yaml_string(survey_str)
    for item in yaml_dict:
        if (item['type'] == 'desc'):
            html_str += '\n' + item['desc'] + '<br>'
        elif (item['type'] == 'radio'):
            name = 'name' + str(name_cnt)
            name_cnt += 1
            opts = item['opts']
            for opt in opts:
                html_str += f'''
<input type="%s" name="%s" value="%s"> %s <br> ''' % ('radio',name,opt['val'],opt['desc'])
        elif (item['type'] == 'text'):
            name = 'name' + str(name_cnt)
            name_cnt += 1
            html_str += f'''
<input type="text" name="%s"> <br>
            ''' % name

    html_str += f'''\n<input type="hidden" name="%s" value="1">''' % q_params.submit_survey
    html_str += f'''\n<input type="hidden" name="%s" value="%s">''' % (q_params.survey_id_str, str(survey_id))
    html_str += '\n<input type="submit" class="submit" value="Submit">'
    html_str += "\n</form>"
    return html_str

def get_html_survey_res(var_val_map, survey_str):
    name_cnt = 1
    html_str = f'''<form action="" method="get">'''
    yaml_dict = parse_yaml_string(survey_str)
    for item in yaml_dict:
        if (item['type'] == 'desc'):
            html_str += '\n' + item['desc'] + '<br>'
        elif (item['type'] == 'radio'):
            name = 'name' + str(name_cnt)
            name_cnt += 1
            opts = item['opts']
            for opt in opts:
                checked = ''
                if (var_val_map[name] == opt['val']):
                    checked = 'checked'
                html_str += f'''
<input type="%s" name="%s" value="%s" %s> %s <br> ''' % ('radio',name,opt['val'],checked,opt['desc'])
        elif (item['type'] == 'text'):
            name = 'name' + str(name_cnt)
            name_cnt += 1
            html_str += f'''
<input type="text" value="%s" > <br> ''' % var_val_map[name] 

    html_str += "\n</form>"
    return html_str

def get_var_val_map_from_str(str):
    return dict(item.split('=') for item in str.replace('"', '').split()) 

def get_var_val_str_from_map(q_string):
    var_val_str = ''
    for param in q_string:
        if param[:4] == 'name':
            var_val_str += f''' %s=\\"%s\\"''' % (param, q_string[param])
    return var_val_str

if __name__ == "__main__":
    ys = f'''
- type: desc
  desc: "Your name?"
- type: text
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
    '''

    print(get_html_survey_from_yaml_str(ys, "./prod", 10))
    print(get_html_survey_res({'name1' : 'male', 'name2' : 'mers'}, ys))
    print('----')
    str1 = ' name1="male" name2="mers" '
    dc = get_var_val_map_from_str(str1)
    print(str(dc))
    print(get_html_survey_res(dc, ys))
    print('----')
    print(get_var_val_str_from_map({'name1' : 'male', 'name2' : 'mers'}))
