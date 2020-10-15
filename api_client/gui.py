from PyQt5.QtWidgets import QMainWindow
from api_client.interface import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QListWidgetItem
import requests
import json


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.button_login.clicked.connect(self.display_main)
        self.button_send_question.clicked.connect(self.send_data)
        self.button_update_answers.clicked.connect(self.get_all_answers)
        self.user = ""

    def display_main(self):
        if str(self.text_user_id.text()) == "":
            self.text_user_id.setText("Input UserName")
            return 0
        if len(self.text_user_id.text()) < 3:
            self.text_user_id.setText("UserName must be longer than 3")
            return 0
        self.user = str(self.text_user_id.text())
        self.stackedWidget.setCurrentIndex(1)

    def send_data(self):
        data = self.text_data.toPlainText()
        data.rstrip('\n')
        json_acceptable_string = data.replace("'", "\"")
        try:
            request = requests.post("https://cov-test-app.herokuapp.com/question?user="+self.user,
                                    json=json.loads(json_acceptable_string))
            self.label_send_status.setText("Data send")
            self.label_send_status.setStyleSheet('color: green')
            print("ok")
        except:
            self.label_send_status.setText("Wrong data")
            self.label_send_status.setStyleSheet('color: red')

    def get_all_answers(self):
        self.list_widget_answers.clear()
        request = requests.get("https://cov-test-app.herokuapp.com/answers?user="+self.user)
        data = request.json()
        print(data)
        for e in data:
            print("ok")
            print(e)
            item = QListWidgetItem(str(e))
            self.list_widget_answers.addItem(item)


def main():
    app = QApplication([])
    vp = MainWindow()
    vp.show()
    app.exec_()


if __name__ == '__main__':
    main()
