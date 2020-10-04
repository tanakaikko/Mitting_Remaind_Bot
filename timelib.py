import datetime,json,gspread
#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials 


#Sunday Monday Tuesday Wednesday Thursday Friday Saturday

dt_now = datetime.datetime.now()

#Day of the week
dw= dt_now.strftime('%A')

#hour set
hour = dt_now.strftime('%H')

#minuts set
minutes = dt_now.strftime('%M')

def weekly_list(N):
    out_list = []
    for i in range(N):
        date_N_days_ago = datetime.datetime.now() - datetime.timedelta(days=i)
        out_list.append(date_N_days_ago)
    return out_list

num_days = 6
list = weekly_list(num_days)

def get_json_list(json_name):
    with open(json_name) as f:
        para_list = json.load(f)
    return para_list

setlist = get_json_list("time_setting.json")

if dw == setlist["Day of the week"] and hour == str(setlist["Hour"]) and minutes == str(setlist["Minutes"]):
    pass

def spreadsheet_func():
    global import_value

    #2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    #認証情報設定
    #ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
    credentials = ServiceAccountCredentials.from_json_keyfile_name('spreadsheet-3-dcb1fdb37648.json', scope)

    #OAuth2の資格情報を使用してGoogle APIにログインします。
    gc = gspread.authorize(credentials)

    #共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
    SPREADSHEET_KEY = '1TSiFA-ZrAvkGtg363fHp6tY9iRae0QllGst5TTkdPX8'

    #共有設定したスプレッドシートのシート1を開く
    worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

    return worksheet

worksheet = spreadsheet_func()

import_value = 'null'
i = 1
import_value_list = []
#Rows and columns
while import_value is not '':
    import_value_list.append([])
    for columns in ['A','B','C','D']:
        selectedcell = columns + str(i)
        print(selectedcell)
        import_value = worksheet.acell(selectedcell).value
        import_value_list[i-1].append(import_value)
    i = i + 1
del import_value_list[-1]


