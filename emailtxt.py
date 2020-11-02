def mail_setting(today,naxtday,namelist,jud):
    pattern1 = """
    テンプレート
""".format(namelist,today,naxtday)

    pattern2 ="""
    テンプレート
それでは，失礼いたします．
""".format(today,naxtday)

    if jud:
        return pattern1
    else:
        return pattern2
