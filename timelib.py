import datetime,json,gspread
#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials 
import smtplib, ssl
from email.mime.text import MIMEText

def weekly_list(N):
    out_list = []
    for i in range(N):
        date_N_days_ago = datetime.datetime.now() - datetime.timedelta(days=i)
        out_list.append(date_N_days_ago)
    return out_list

def get_json_list(json_name):
    with open(json_name) as f:
        para_list = json.load(f)
    return para_list

def spreadsheet_func():#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
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

def get_cell():
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
    return import_value_list

def sent_mail():
    # 以下にGmailの設定を書き込む★ --- (*1)
    gmail_account = "s17a2082ju@s.chibakoudai.jp"
    gmail_password = "avtr85zd"
    # メールの送信先★ --- (*2)
    mail_to = "s17a2082ju@s.chibakoudai.jp"

    # メールデータ(MIME)の作成 --- (*3)
    subject = "メール送信テスト"
    body = "メール送信テスト"
    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["To"] = mail_to
    msg["From"] = gmail_account

    # Gmailに接続 --- (*4)
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465,
        context=ssl.create_default_context())
    server.login(gmail_account, gmail_password)
    server.send_message(msg) # メールの送信

def main():
    #Sunday Monday Tuesday Wednesday Thursday Friday Saturday

    dt_now = datetime.datetime.now()

    #Day of the week
    dw= dt_now.strftime('%A')

    #hour set
    hour = dt_now.strftime('%H')

    #minuts set
    minutes = dt_now.strftime('%M')

    num_days = 6
    list = weekly_list(num_days)

    setlist = get_json_list("time_setting.json")

    if dw == setlist["Day of the week"] and hour == str(setlist["Hour"]) and minutes == str(setlist["Minutes"]):
        pass