import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListView, QTextEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor,QFont
from Chatbox import Ui_MainWindow
import openai
from PyQt5.QtGui import QStandardItem, QStandardItemModel

class ChatMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.send_message)
        openai.api_key = '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'
        self.model = QStandardItemModel()
        self.listView.setModel(self.model)


        greeting = "Nhân Viên: Xin chào! Tôi Là Nhân Viên Ảo của Phần Mềm\n Nếu có Thắc Mắc Gì Về CAMERA Hãy Liên Hệ \n SDT:0523125184"
        self.model.appendRow(QStandardItem(greeting))
        text_edit_font = QFont("Times New Roman", 13)  
        text_edit_color = QColor("black")  
        self.textEdit.setFont(text_edit_font)
        self.textEdit.setTextColor(text_edit_color)
        list_view_font = QFont("Times New Roman", 13)  
        list_view_color = QColor("red")  

        self.listView.setFont(list_view_font)
        self.listView.setStyleSheet(f"color: {list_view_color.name()}")  


    def send_message(self):
        user_input = self.textEdit.toPlainText()
        if user_input.strip() != "":           
            response = self.generate_openai_response(user_input)        
            you_item = QStandardItem("You: " + user_input)
            you_item.setFont(QFont("Times New Roman", 13))
            you_item.setForeground(QColor("black"))
            self.model.appendRow(you_item)

            bot_item = QStandardItem("Nhân Viên: " + response)
            self.model.appendRow(bot_item)
            index = self.model.indexFromItem(self.model.item(self.model.rowCount() - 1))
            self.listView.scrollTo(index)
            self.textEdit.clear()

    def generate_openai_response(self, user_input):

        prompt = f"Question: {user_input}\nAnswer:"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=150
        )
        return response['choices'][0]['text'].strip()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ChatMainWindow()
    main_window.show()
    sys.exit(app.exec_())
