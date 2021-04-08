import sys
from db.db import Database
from encryption.encryption import Encryption
from config.config import dbname, host, port, user, password
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit
import pyperclip

f = Encryption()
db = Database(dbname, host, port, user, password)


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle('Password Manager')
        self.setGeometry(650, 350, 720, 300)

        self.login = QtWidgets.QLabel(self)
        self.password = QtWidgets.QLabel(self)

        self.error = QtWidgets.QLabel(self)

        self.search = QTextEdit(self)
        self.search.move(10, 125)
        self.search.setFixedSize(200, 30)

        self.btn = QtWidgets.QPushButton(self)
        self.btn.move(10, 160)
        self.btn.setText('Найти')
        self.btn.adjustSize()
        self.btn.clicked.connect(self.get_password)

        self.btn_CopyLogin = QtWidgets.QPushButton(self)
        self.btn_CopyLogin.hide()

        self.btn_CopyPassword = QtWidgets.QPushButton(self)
        self.btn_CopyPassword.hide()

        self.name = QTextEdit(self)
        self.name.move(450, 30)
        self.name.setFixedSize(200, 30)
        self.name.setPlaceholderText('Название сайта')

        self.url = QTextEdit(self)
        self.url.move(450, 70)
        self.url.setFixedSize(200, 30)
        self.url.setPlaceholderText('Ссылка')

        self.loginAdd = QTextEdit(self)
        self.loginAdd.move(450, 110)
        self.loginAdd.setFixedSize(200, 30)
        self.loginAdd.setPlaceholderText('Логин')

        self.passwordAdd = QTextEdit(self)
        self.passwordAdd.move(450, 150)
        self.passwordAdd.setFixedSize(200, 30)
        self.passwordAdd.setPlaceholderText('Пароль')

        self.btnAdd = QtWidgets.QPushButton(self)
        self.btnAdd.move(450, 200)
        self.btnAdd.setText('Добавить')
        self.btnAdd.adjustSize()
        self.btnAdd.clicked.connect(self.add_password)

    def get_password(self):
        name = self.search.toPlainText()
        data = db.get_password(name)
        if data:
            for i in data:
                self.login.setText(f'Логин: {i["login"]}')
                self.password.setText(f'Пароль: {f.decrypt(i["password"])}')
            self.error.hide()

            self.login.show()
            self.login.move(10, 80)
            self.login.adjustSize()

            self.password.show()
            self.password.move(10, 100)
            self.password.adjustSize()

            self.btn_CopyLogin.show()
            self.btn_CopyLogin.move(300, 75)
            self.btn_CopyLogin.setText('Копировать логин')
            self.btn_CopyLogin.adjustSize()
            self.btn_CopyLogin.clicked.connect(self.copy_login)

            self.btn_CopyPassword.show()
            self.btn_CopyPassword.move(300, 105)
            self.btn_CopyPassword.setText('Копировать пароль')
            self.btn_CopyPassword.adjustSize()
            self.btn_CopyPassword.clicked.connect(self.copy_password)
        else:
            self.login.hide()
            self.password.hide()
            self.btn_CopyPassword.hide()
            self.btn_CopyLogin.hide()
            self.error.show()
            self.error.move(10, 50)
            self.error.setText('Не удалось найти ')

    def copy_login(self):
        name = self.search.toPlainText()
        login = db.get_password(name)
        for i in login:
            pyperclip.copy(i['login'])

    def copy_password(self):
        name = self.search.toPlainText()
        password = db.get_password(name)
        for i in password:
            pyperclip.copy(f.decrypt(i['password']))

    def add_password(self):
        name = self.name.toPlainText()
        url = self.url.toPlainText()
        login = self.loginAdd.toPlainText()
        password = self.passwordAdd.toPlainText()

        self.name.setText('')
        self.url.setText('')
        self.loginAdd.setText('')
        self.passwordAdd.setText('')

        if(db.get_password(name)):
            print('уже существует')
        else:
            db.add_password(name, url, login, f.encrypt(password))


def main():
    app = QApplication(sys.argv)
    window = Window()

    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()