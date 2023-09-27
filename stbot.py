
import Constants
import sys
import openai
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QTextEdit
)

openai.api_key = Constants.API_KEY


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.logo_label = QLabel()
        self.logo_pixmap = QPixmap('michaelajayi.jpg').scaled(
            500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(self.logo_pixmap)

        self.input_label = QLabel('Ask Something')
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText('Type here...')
        self.answer_label = QLabel('Answer:')
        self.answer_field = QTextEdit()
        self.answer_field.setReadOnly(True)
        self.sumbit_button = QPushButton('Sumbit')
        self.sumbit_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2F3540;
                border: none;
                color: white;
                padding: 15px 32px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 25px;
                }
            QpushButton:hover {
                background-color: #3e8e41;
                }
                """

        )
        self.recommended_questions_group = QGroupBox('Recommended Questions')
        self.recommended_questions_layout = QVBoxLayout()
        self.recommended_questions = ["What is the four corner opposition?",
                                      "How do I become a better storyteller?", "What are some popular ways to get better at writting?"]
        self.question_buttons = []

        # Create a layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(50)
        layout.setAlignment(Qt.AlignCenter)

        # Add Logo
        layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)

        # Add Input Field and Sumbit Button
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.sumbit_button)
        layout.addLayout(input_layout)

        # Add Answer Field
        layout.addWidget(self.answer_label)
        layout.addWidget(self.answer_field)

        # add the recommended questions buttons
        for question in self.recommended_questions:
            button = QPushButton(question)
            button.setStyleSheet(
                """
                QPushButton {
                    background-color: #FFFFFF:
                    border: 2px solid #00AEFF;
                    colour: #00AEFF;
                    padding: 10px 20px;
                    font-size: 30px;
                    font-weight: bold;
                    border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: #00AEFF;
                        color: #FFFFFF;
                        }"""
            )
            button.clicked.connect(
                lambda _, q=question: self.input_field.setText(q))
            self.recommended_questions_layout.addWidget(button)
            self.question_buttons.append(button)
        self.recommended_questions_group.setLayout(
            self.recommended_questions_layout)
        layout.addWidget(self.recommended_questions_group)

        # Set the layout
        self.setLayout(layout)

        # Set the window properties
        self.setWindowTitle('Storyteller Writer Advisor Bot')
        self.setGeometry(200, 200, 600, 600)

        # Connect the submit button to the function which queries OpenAI's API
        self.sumbit_button.clicked.connect(self.get_answer)

    def get_answer(self):
        question = self.input_field.text()

        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a Storyteller expert. Answer the follwing questions in a concise way or with bullet points."},
                {"role": "user", "content": "What is the four corner opposition?"},
                {"role": "assistant", "content": "A story structure writing technique that draws the lines between four leading charcters conflicts."},
                {"role": "user", "content": f'{question}'}],
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=1
        )

        answer = completion.choices[0].message.content

        self.answer_field.setText(answer)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
