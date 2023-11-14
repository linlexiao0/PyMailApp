from mail_sender import MailSender
from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, world!6"

@app.route('/send',methods=['post'])
def send():
    print(request.json)
    mail_host = request.json.get("mail_host").strip() 
    mail_user = request.json.get("mail_user").strip() 
    mail_pass = request.json.get("mail_pass").strip()
    sender_email = request.json.get("sender_email").strip() 
    sender_nickname = request.json.get("sender_nickname").strip() 
    receivers = request.json.get("receivers").strip() 
    subject = request.json.get("subject").strip() 
    msg = request.json.get("msg").strip() 
    
    if mail_host and mail_user and mail_pass and sender_email and sender_nickname and receivers and subject and msg:
        try:
            sender = MailSender(mail_host,mail_user,mail_pass,sender_email,sender_nickname)
        except Exception as e:
            return json.dumps({"version":"1.0.0","code": 2002, "msg": "登录失败！请检查用户名和密码"})
        
        sender.sendHTMLText([receivers],subject,msg)
        return json.dumps({"version":"1.0.0","code": 200, "msg": "发送成功"})

    else:
        return json.dumps({"version":"1.0.0","code": 2001, "msg": "信息不能为空！"})

if __name__=='__main__':
    app.run("0.0.0.0")

