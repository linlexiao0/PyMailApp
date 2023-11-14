from mail_sender import MailSender
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

class LabelLineEdit(QWidget):
    def __init__(self, text, parent = None):
        super().__init__(parent)
        self.main_layout = QHBoxLayout(self)
        self.label = QLabel(text,self)
        self.line_edit = QLineEdit(self)
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.line_edit)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.main_layout)

    def text(self, *args):
        return self.line_edit.text(*args)

    def setText(self, *args):
        return self.line_edit.setText(*args)
    
    def setEchoMode(self, *args):
        return self.line_edit.setEchoMode(*args)

    def setPlaceholderText(self, *args):
        return self.line_edit.setPlaceholderText(*args)

class MailWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setMinimumWidth(500)
        
        self.setWindowTitle("发送邮件")

        self.main_layout = QVBoxLayout()

        self.edit_mail_host = LabelLineEdit("邮箱服务器",self)
        self.edit_mail_host.setPlaceholderText("例如：smtp.163.com")
        self.main_layout.addWidget(self.edit_mail_host)

        self.edit_mail_user = LabelLineEdit("邮箱用户名：",self)
        self.edit_mail_user.setPlaceholderText("@前面的部分")
        self.main_layout.addWidget(self.edit_mail_user)
        
        self.edit_mail_pass = LabelLineEdit("邮箱授权码：",self)
        self.edit_mail_pass.setPlaceholderText("你的授权码")
        self.edit_mail_pass.setEchoMode(QLineEdit.Password)
        self.main_layout.addWidget(self.edit_mail_pass)
 
        self.edit_sender_email = LabelLineEdit("发信地址：",self)
        self.edit_sender_email.setPlaceholderText("发信时发出的地址")
        self.main_layout.addWidget(self.edit_sender_email)

        self.edit_sender_nickname = LabelLineEdit("发信人昵称：",self)
        self.edit_sender_nickname.setPlaceholderText("发信时携带的昵称")
        self.main_layout.addWidget(self.edit_sender_nickname)
        

        # self.btn_login = QPushButton("登录",self)
        # self.btn_login.clicked.connect(self.login)
        # self.main_layout.addWidget(self.btn_login)

        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.main_layout.addWidget(line)

        self.edit_subject = LabelLineEdit("主题：",self)
        self.main_layout.addWidget(self.edit_subject)

        self.edit_receive = LabelLineEdit("收信人：",self)
        self.main_layout.addWidget(self.edit_receive)

        label = QLabel("正文：")
        self.main_layout.addWidget(label)
        self.edit_message = QTextEdit(self)
        self.main_layout.addWidget(self.edit_message)

        label2=QLabel("启用HTML")
        self.isHTML = QCheckBox(self)
        self.btn_send = QPushButton("发送",self)
        self.btn_send.clicked.connect(self.send)
        self.btn_send.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.hlay1 = QHBoxLayout()
        self.hlay1.addWidget(label2)
        self.hlay1.addWidget(self.isHTML)
        self.hlay1.addWidget(self.btn_send)
        self.main_layout.addLayout(self.hlay1)

        self.setLayout(self.main_layout)


        self.is_login = False
        self.mail_sender = None

    def login(self):
        try:
            self.mail_sender = MailSender(
                self.edit_mail_host.text(),
                self.edit_mail_user.text(),
                self.edit_mail_pass.text(),
                self.edit_sender_email.text(),
                self.edit_sender_nickname.text(),
            )
        except Exception as e:
            QMessageBox.critical(self, "失败", f"登陆失败，错误原因为：{e}", QMessageBox.Yes, QMessageBox.Yes)
            return False
        else:
            # QMessageBox.information(self, "成功", "登陆成功！", QMessageBox.Yes, QMessageBox.Yes)
            return True
            
    
    def send(self):
        if not self.login():
            return

        # if not self.is_login:
        #     QMessageBox.critical(self, "错误", "还未登录！", QMessageBox.Yes, QMessageBox.Yes)

        try:
            if self.isHTML.isChecked():
                self.mail_sender.sendHTMLText(
                    [self.edit_receive.text()],
                    self.edit_subject.text(),
                    self.edit_message.toPlainText(),
                )
            else:
                self.mail_sender.sendPlainText(
                    [self.edit_receive.text()],
                    self.edit_subject.text(),
                    self.edit_message.toPlainText(),
                )
        except Exception as e:
            QMessageBox.critical(self, "失败", f"登陆成功，但发送失败，错误原因为：{e}", QMessageBox.Yes, QMessageBox.Yes)

        else:
            QMessageBox.information(self, "成功", "发送成功！", QMessageBox.Yes, QMessageBox.Yes)

            

if __name__=="__main__":
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    w = MailWidget()
    w.show()
    app.exec_()