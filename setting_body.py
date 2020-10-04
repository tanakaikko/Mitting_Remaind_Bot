from email.mime.text import MIMEText


subject,body = "",""
body1 = """
    ※自動送信です．
    佐藤研究室の皆様
    
    平素よりお世話になっております．
    佐藤研究室の田中です．
"""
def body_setting(today,naxtday,namelist,yesorno):
    global subject,body
    subject = today + "の進捗報告会について"
    body2_1 = """
    https://docs.google.com/spreadsheets/d/1TSiFA-ZrAvkGtg363fHp6tY9iRae0QllGst5TTkdPX8/edit?usp=sharing
    上記のスプレッドシートの通り，今週進捗発表希望者がいなかったため，
    今週{0}の進捗報告会は，お休みとさせていただきます．
    """.format(today)

    body2_2 = """
    https://docs.google.com/spreadsheets/d/1TSiFA-ZrAvkGtg363fHp6tY9iRae0QllGst5TTkdPX8/edit?usp=sharing
    上記のスプレッドシートの通り，
    {1}
    が報告を希望されたので，今週{0}の進捗報告会は開催となります．

    """.format(today, namelist)

    body3 = """
    なお，来週{0} の進捗報告会希望の方は，
    以下の通りに，希望届を提出してください．

    ※いつかのメールの内容
    https://forms.gle/AEWTkZ4VeHUAw9G58
    ↑のフォームに回答していただき，田中から全体に開催のご連絡をする形にいたします．
    フォームは，使いまわしますので卒業まで上記のURLから申請してください．
    また，以下にフォーム利用の注意点について，記載いたします．

    ＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊
    このフォームは，毎週水曜日の朝9:00に締め切り，その後の回答は翌週の進捗報告会への希望と判断いたします．
    日・月・火・水・木・金・土
    → → → → →→｜→ → → → → 
         ↑ 　　   　  ↑
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

msg = MIMEText(body)
msg["Subject"] = subject