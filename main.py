import sys
import random

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QGridLayout,
    QLabel,
    QVBoxLayout,
    QGraphicsOpacityEffect,
)

from PyQt6.QtCore import (
    Qt,
    QPropertyAnimation,
    QEasingCurve,
    QTimer,
)

from PyQt6.QtGui import (
    QFont,
    QColor,
    QLinearGradient,
    QBrush,
    QPalette,
    QIcon,
)

class SciFiButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumSize(100, 100)
        self.setFont(QFont("Arial", 24, QFont.Weight.Bold))

class TicTacToe(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.current_player = random.choice(["X", "O"])
        self.board = [["" for _ in range(3)] for _ in range(3)]

        # Set up opacity effect and animation
        self.opacity_effect = QGraphicsOpacityEffect(self.title_label)
        self.title_label.setGraphicsEffect(self.opacity_effect)

        self.title_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.title_anim.setDuration(1500)
        self.title_anim.setStartValue(0.3)
        self.title_anim.setEndValue(1.0)
        self.title_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.title_anim.setLoopCount(-1)
        self.title_anim.start()

    def initUI(self):
        self.setWindowTitle("Cyber Tic Tac Toe")
        self.setFixedSize(600, 700)

        # Set icon for the app
        self.setWindowIcon(QIcon("./img/logo.png"))

        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Title label with gradient effect
        self.title_label = QLabel("Tic Tac Toe")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont("Orbitron", 32, QFont.Weight.Bold))


        # Create gradient effect
        gradient = QLinearGradient(0, 0, 0, 1)
        gradient.setColorAt(0.0, QColor(0, 255, 255))
        gradient.setColorAt(1.0, QColor(255, 0, 255))
        gradient.setCoordinateMode(QLinearGradient.CoordinateMode.ObjectMode)

        palette = self.title_label.palette()
        palette.setBrush(QPalette.ColorRole.WindowText, QBrush(gradient))
        self.title_label.setPalette(palette)

        # Game board
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.buttons = [[SciFiButton("") for _ in range(3)] for _ in range(3)]

        for row in range(3):
            for col in range(3):
                button = self.buttons[row][col]
                button.setStyleSheet(
                    """
                    SciFiButton {
                        background-color: rgba(30, 30, 60, 200);
                        color: #00ffff;
                        border: 2px solid #00ffff;
                        border-radius: 15px;
                    }
                    SciFiButton:hover {
                        background-color: rgba(50, 50, 100, 200);
                        border: 2px solid #ff00ff;
                    }
                """
                )
                button.clicked.connect(lambda _, r=row, c=col: self.make_move(r, c))
                self.grid.addWidget(button, row, col)

        # Reset button
        reset_btn = SciFiButton("New Game")
        reset_btn.setStyleSheet(
            """
            SciFiButton {
                background-color: rgba(255, 0, 255, 100);
                color: white;
                border: 2px solid #00ffff;
                border-radius: 15px;
                padding: 15px;
            }
            SciFiButton:hover {
                background-color: rgba(255, 0, 255, 150);
            }
        """
        )
        reset_btn.clicked.connect(self.reset_game)

        # Add widgets to main layout
        main_layout.addWidget(self.title_label)
        main_layout.addLayout(self.grid)
        main_layout.addWidget(reset_btn)

        # Set background
        self.set_background()

    def set_background(self):
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor(10, 10, 30))
        gradient.setColorAt(1.0, QColor(30, 10, 40))

        palette = self.palette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setPalette(palette)

    def make_move(self, row, col):
        button = self.buttons[row][col]
        if not self.board[row][col]:
            button.setText(self.current_player)
            self.board[row][col] = self.current_player

            # Flash animation using style sheets
            original_style = button.styleSheet()
            button.setStyleSheet(original_style + "color: #ff00ff;")
            QTimer.singleShot(200, lambda: button.setStyleSheet(original_style))

            if self.check_winner():
                self.show_winner()
            elif self.check_draw():
                self.show_draw()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        # Check rows, columns, and diagonals
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return True
        return False

    def check_draw(self):
        return all(cell != "" for row in self.board for cell in row)

    def show_winner(self):
        for row in self.buttons:
            for button in row:
                button.setEnabled(False)
        self.title_label.setText(f"PLAYER {self.current_player} WINS!")

    def show_draw(self):
        self.title_label.setText("DRAW!")

    def reset_game(self):
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.title_label.setText("Tic Tac Toe")
        for row in self.buttons:
            for button in row:
                button.setText("")
                button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./img/logo.png"))

    # Set global style
    app.setStyleSheet(
        """
        * {
            color: #00ffff;
            font-family: 'Orbitron';
        }
        QMainWindow {
            background-color: #0a0a1a;
        }
    """
    )

    game = TicTacToe()
    game.show()
    sys.exit(app.exec())
