import smtplib
from email.mime.text import MIMEText
from email.header import Header

class MailSender:
    def __init__(self, mail_host:str, mail_user:str, mail_pass:str,
                sender_email:str, sender_nickname:str):
        """创建一个MailSender实例

        Args:
            mail_host (str): 邮箱提供商的地址，比如 smtp.163.com

            mail_user (str): 你的邮箱用户名，比如 foo

            mail_pass (str): 你的邮箱访问密钥

            sender (str): 你的邮箱地址，比如 foo@bar.com

            sendernickname (str): 你的昵称，比如 mynickname
        """        

        # print("get=",mail_host,mail_user,mail_pass,sender_email,sender_nickname,sep='\n')

        self.mail_host = mail_host
        self.mail_user = mail_user
        self.mail_pass = mail_pass
        self.sender_email = sender_email
        self.sender_nickname = sender_nickname

        self.smtp_obj = smtplib.SMTP() 
        self.smtp_obj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        self.smtp_obj.login(mail_user,mail_pass) 

    def sendPlainText(self, receivers:list, subject:str, msg: str):
        data = MIMEText(msg, 'plain', 'utf-8')
        data['From'] = Header(f"{self.sender_nickname} <{self.sender_email}>")
        data['To'] =  Header(';'.join(receivers))
        data['Subject'] = Header(subject, 'utf-8')

        self.smtp_obj.sendmail(self.sender_email, receivers, data.as_string())
        
    def sendHTMLText(self, receivers:list, subject:str, msgHTML: str):
        data = MIMEText(msgHTML, 'html', 'utf-8')
        data['From'] = Header(f"{self.sender_nickname} <{self.sender_email}>")
        data['To'] =  Header(';'.join(receivers))
        data['Subject'] = Header(subject, 'utf-8')

        self.smtp_obj.sendmail(self.sender_email, receivers, data.as_string())
    
if __name__ == "__main__":
    mail_sender = MailSender("smtp.163.com","linlexiao2007","",
                        "linlexiao2007@163.com","linlexiao")
    
    # mail_sender.sendPlainText(["2623459403@qq.com"],"你好！","邮件测试（这是正文）")

    mail_sender.sendHTMLText(["2623459403@qq.com"],"你好！",
                             """
                             <h1>邮件测试（这是正文）</h1> <p>测试段落</p> <a href="bing.com">超链接</a>
                             """
    )


