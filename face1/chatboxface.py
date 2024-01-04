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
        text_edit_color = QColor("Black")  
        self.textEdit.setFont(text_edit_font)
        self.textEdit.setTextColor(text_edit_color)
        list_view_font = QFont("Times New Roman", 13)  
        list_view_color = QColor("Orange")  

        self.listView.setFont(list_view_font)
        self.listView.setStyleSheet(f"color: {list_view_color.name()}")  
        self.predefined_responses = {
    "cách sử dụng phần mềm": "\nBước 1: Mở ứng dụng Nhận Diện Khuôn Mặt\nBước 2: Đăng Nhập bằng Việc Đưa mặt vào\nBước 3: Nhấn Vào Bổ Sung Người Để Thêm\n Bước 4 Nhập thông tin và chụp hình sau đó quét mặt\n Bước 5 Vào CAMERA để xem người Đó ",
    "yêu cầu hỗ trợ kỹ thuật": "\nĐể nhận hỗ trợ kỹ thuật, \nvui lòng liên hệ đường dây nóng: 0523125184\n Hổ Trợ: Nguyễn Nhật Huy"
   
        }

    def send_message(self):
        user_input = self.textEdit.toPlainText()
        if user_input.strip() != "":   
            if user_input in self.predefined_responses:
                response = self.predefined_responses[user_input]
            else:
               
                response = self.generate_openai_response(user_input)        
                
            you_item = QStandardItem("You: " + user_input)
            you_item.setFont(QFont("Times New Roman", 13))
            you_item.setForeground(QColor("white"))
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