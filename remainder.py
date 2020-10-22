import datetime,json,gspread
#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials 
import smtplib, ssl, getpass,emailtxt
from email.mime.text import MIMEText

#global password val
password = ""

#weekly list get
def weekly_list(N):
    out_list = []
    for i in range(N):
        date_N_days_ago = datetime.datetime.now() - datetime.timedelta(days=i)
        out_list.append(date_N_days_ago)
    return out_list

#json data get
def get_json_list(json_name):
    with open(json_name) as f:
        para_list = json.load(f)
    return para_list

#spreadsheet get cell
def get_cell(keyjson,SPREADSHEET_KEY):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    #認証情報設定
    #ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
    credentials = ServiceAccountCredentials.from_json_keyfile_name(keyjson, scope)

    #OAuth2の資格情報を使用してGoogle APIにログインします。
    gc = gspread.authorize(credentials)

    #共有設定したスプレッドシートのシート1を開く
    worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

    import_value = 'null'
    i = 1
    import_value_list = []
    #Rows and columns
    while import_value != '':
        import_value_list.append([])
        for columns in ['A','B','C','D']:
            selectedcell = columns + str(i)
            import_value = worksheet.acell(selectedcell).value
            import_value_list[i-1].append(import_value)
        i = i + 1

    return import_value_list

#sent mail
def sent_mail(gmail_account,gmail_password,msg):
    # Gmailに接続 --- (*4)
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465,
        context=ssl.create_default_context())
    server.login(gmail_account, gmail_password)
    server.send_message(msg) # メールの送信

#password get
def get_pas():
    global password
    password = getpass.getpass()

#main def
def main(fig):
    #Sunday Monday Tuesday Wednesday Thursday Friday Saturday
    dt_now = datetime.datetime.now()
    
    #Day of the weekavtr85zd
    dw= dt_now.strftime('%A')

    #hour set
    hour = dt_now.strftime('%H')

    #minuts set
    minutes = dt_now.strftime('%M')

    print(dt_now.strftime('%Y/%m/%d(%A) %H:%M'))
    num_days = 6
    weeklist = weekly_list(num_days)

    setlist = get_json_list("time_setting.json")

    if dw == setlist["Day of the week"]:
        if int(hour) >= setlist["Hour"] and int(minutes) >= setlist["Minutes"] and fig:
            print('sent email standby')
            output_data = get_cell(setlist["keyjson"],setlist["SPREADSHEET_KEY"])
            sent_list = []
            #内容があるかサーチ
            i = 1
            while output_data[i][0] != '':
                for j in range(6):
                    ok_day = weeklist[j].strftime('%Y/%m/%d')
                    if ok_day in output_data[i][0]:
                        sent_list.append(output_data[i][1])
                i = i + 1
            msg_list = ''
            for name in sent_list:
                msg_list = msg_list + name + ","
            
            today_data = datetime.datetime.now() + datetime.timedelta(days=setlist["Today"])
            nest_week = datetime.datetime.now() + datetime.timedelta(days=(7+setlist["Today"]))
            tmp_msg = emailtxt.mail_setting(today_data.strftime('%Y/%m/%d(%A)'),nest_week.strftime('%Y/%m/%d(%A)'),msg_list,sent_list != [])
            msg = MIMEText(tmp_msg)
            msg["Subject"]  = "{0}の進捗報告会について".format(today_data.strftime('%Y/%m/%d(%A)'))
            msg["From"] = setlist["From_email"]
            msg["To"] = setlist["To_email"]
            
            try:    
                sent_mail(setlist["From_email"],password,msg)
                print('sent email!')
            except:
                print('miss sent email')

            return False
        else:
            pass
    else:
        return True