from verify_email import verify_email


def check(email):
    v = verify_email(email)
    print(v)

e_mail=input("请输入电子邮件地址：")

check(e_mail)