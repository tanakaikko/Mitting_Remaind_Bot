import datetime,json


dt_now = datetime.datetime.now()

print(dt_now.strftime('%Y/%m/%d/ %H:%M:%S'))


def input_json(json_name):
    with open(json_name) as f:
        para_list = json.load(f)
    x = para_list['x']
    delta = para_list['delta']
    conv = para_list['conv']