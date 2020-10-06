import datetime,json,gspread
#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials 
import smtplib, ssl, getpass
from email.mime.text import MIMEText


password = ""

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
    credentials = ServiceAccountCredentials.from_json_keyfile_name('example.json', scope)

    #OAuth2の資格情報を使用してGoogle APIにログインします。
    gc = gspread.authorize(credentials)

    #共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
    SPREADSHEET_KEY = 'key'

    #共有設定したスプレッドシートのシート1を開く
    worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

    return worksheet

def get_cell():
    worksheet = spreadsheet_func()

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

def sent_mail(gmail_account,gmail_password,msg):
    # Gmailに接続 --- (*4)
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465,
        context=ssl.create_default_context())
    server.login(gmail_account, gmail_password)
    server.send_message(msg) # メールの送信

def body_setting(today,naxtday,namelist,yesorno):
    body1 = """
※自動送信です．
tttの皆様

平素よりお世話になっております．
tttのnameです．
"""
    subject = today + "の進捗報告会について"
    body2_1 = """

上記のスプレッドシートの通り，今週進捗発表希望者がいなかったため，
今週{0}の進捗報告会は，お休みとさせていただきます．
""".format(today)

    body2_2 = """

上記のスプレッドシートの通り，
{1}
が報告を希望されたので，今週{0}の進捗報告会は開催となります．

""".format(today, namelist)

    body3 = """
なお，来週{0} の進捗報告会希望の方は，
以下の通りに，希望届を提出してください．

※いつかのメールの内容

↑のフォームに回答していただき，田中から全体に開催のご連絡をする形にいたします．
フォームは，使いまわしますので卒業まで上記のURLから申請してください．
また，以下にフォーム利用の注意点について，記載いたします．

＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊
このフォームは，毎週水曜日の朝9:00に締め切り，その後の回答は翌週の進捗報告会への希望と判断いたします．
日・月・火・水・木・金・土
→ → → → →  →｜→  →  →  →  → 
        ↑ 　　      ↑
この範囲の回答は，  ↑　
今週の金曜日の希望  ↑
    　　　　　　　この範囲は，翌週の金曜日の希望と判断いたします．

※人数多数の場合，2週に分けて発表いたします．
※人数多数の場合，2週に分けて発表いたします．
＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊

それでは，失礼いたします．
""".format(naxtday)

    if yesorno:
        body = body1 + body2_2 + body3
    else:
        body = body1 + body2_1 + body3

    return [subject,body]

def get_pas():
    global password
    password = getpass.getpass()

def main(fig):
    #Sunday Monday Tuesday Wednesday Thursday Friday Saturday
    dt_now = datetime.datetime.now()
    
    #Day of the weekavtr85zd
    dw= dt_now.strftime('%A')

    #hour set
    hour = dt_now.strftime('%H')

    #minuts set
    minutes = dt_now.strftime('%M')

    print(int(hour),int(minutes))
    num_days = 6
    weeklist = weekly_list(num_days)

    setlist = get_json_list("time_setting.json")

    if dw == setlist["Day of the week"]:
        if int(hour) >= setlist["Hour"] and int(minutes) >= setlist["Minutes"] and fig:
            output_data = get_cell()
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

            listout = body_setting(today_data.strftime('%Y/%m/%d(%A)'),nest_week.strftime('%Y/%m/%d(%A)'),msg_list,sent_list is not None)
            msg = MIMEText(listout[1])
            msg["Subject"] = listout[0]
            msg["From"] = setlist["From_email"]
            msg["To"] = setlist["To_email"]
            sent_mail(setlist["From_email"],password,msg)
            
        return False

    else:
        return True