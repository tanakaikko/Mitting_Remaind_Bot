import remainder,time

fig = True
figjag = input("今日からメールを送りますか？(Y/n)：")
if figjag == "y" or figjag == "Y":
    fig = True
else:
    fig = False
remainder.get_pas()

while True:
    print("judgement!",fig)
    fig = remainder.main(fig)
    time.sleep(60*3)