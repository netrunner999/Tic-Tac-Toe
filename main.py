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
    QHBoxLayout,
    QLineEdit,
    QComboBox,
    QScrollArea,
    QSizePolicy,
    QGraphicsOpacityEffect,  # Перенесено сюда
)
from PyQt6.QtCore import (
    Qt,
    QPropertyAnimation,
    QEasingCurve,
    QTimer,
    QSize,
)
from PyQt6.QtGui import (
    QFont,
    QColor,
    QLinearGradient,
    QBrush,
    QPalette,
    QIcon,
    QPainter,
)

class SciFiButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Orbitron", 14, QFont.Weight.Bold))
        self.setMinimumSize(60, 60)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.set_background()

    def initUI(self):
        self.setWindowTitle("Cyber Tic Tac Toe")
        self.setFixedSize(600, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Title
        title = QLabel("CYBER TIC TAC TOE")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Orbitron", 32, QFont.Weight.Bold))

        # Player inputs
        input_layout = QVBoxLayout()

        self.player_x_input = QLineEdit()
        self.player_x_input.setPlaceholderText("Player X")
        self.player_x_input.setStyleSheet("""
            QLineEdit {
                background: rgba(30, 30, 60, 200);
                border: 2px solid #00ffff;
                border-radius: 10px;
                padding: 10px;
                color: #00ffff;
                font: 16px Orbitron;
            }
        """)

        self.player_o_input = QLineEdit()
        self.player_o_input.setPlaceholderText("Player O")
        self.player_o_input.setStyleSheet(self.player_x_input.styleSheet())

        input_layout.addWidget(QLabel("Player X Name:"))
        input_layout.addWidget(self.player_x_input)
        input_layout.addWidget(QLabel("Player O Name:"))
        input_layout.addWidget(self.player_o_input)

        # Board size selector
        self.size_combobox = QComboBox()
        self.size_combobox.addItems(["3x3 (Classic)", "9x9 (Extended)"])
        self.size_combobox.setStyleSheet("""
            QComboBox {
                background: rgba(30, 30, 60, 200);
                border: 2px solid #00ffff;
                border-radius: 10px;
                padding: 10px;
                color: #00ffff;
                font: 16px Orbitron;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)

        # Start button
        start_btn = SciFiButton("Start Game")
        start_btn.clicked.connect(self.start_game)
        start_btn.setStyleSheet("""
            SciFiButton {
                background: rgba(255, 0, 255, 100);
                border: 2px solid #00ffff;
                border-radius: 15px;
                padding: 20px;
                color: white;
            }
            SciFiButton:hover {
                background: rgba(255, 0, 255, 150);
            }
        """)

        layout.addWidget(title)
        layout.addLayout(input_layout)
        layout.addWidget(QLabel("Select Board Size:"))
        layout.addWidget(self.size_combobox)
        layout.addStretch()
        layout.addWidget(start_btn)

    def set_background(self):
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor(10, 10, 30))
        gradient.setColorAt(1.0, QColor(30, 10, 40))

        palette = self.palette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setPalette(palette)

    def start_game(self):
        size_text = self.size_combobox.currentText()
        board_size = 3 if "3x3" in size_text else 9

        player_x = self.player_x_input.text() or "Player X"
        player_o = self.player_o_input.text() or "Player O"

        self.game_window = GameWindow(board_size, player_x, player_o)
        self.game_window.show()
        self.hide()

class GameWindow(QMainWindow):
    def __init__(self, board_size, player_x, player_o):
        super().__init__()
        self.board_size = board_size
        self.players = {
            "X": player_x,
            "O": player_o
        }
        self.required_to_win = 3 if board_size == 3 else 5
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Cyber Tic Tac Toe")
        self.setMinimumSize(800 if self.board_size == 9 else 600,
                          850 if self.board_size == 9 else 700)

        # Central widget with scroll area for large boards
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")

        central_widget = QWidget()
        self.setCentralWidget(scroll)
        scroll.setWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Title
        self.title_label = QLabel("Tic Tac Toe")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont("Orbitron", 28, QFont.Weight.Bold))

        # Game board
        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        self.buttons = [[SciFiButton("") for _ in range(self.board_size)]
                      for _ in range(self.board_size)]

        button_style = """
            SciFiButton {
                background-color: rgba(30, 30, 60, 200);
                color: #00ffff;
                border: 2px solid #00ffff;
                border-radius: 8px;
                min-width: 60px;
                min-height: 60px;
            }
            SciFiButton:hover {
                background-color: rgba(50, 50, 100, 200);
                border: 2px solid #ff00ff;
            }
        """

        for row in range(self.board_size):
            for col in range(self.board_size):
                button = self.buttons[row][col]
                button.setStyleSheet(button_style)
                button.clicked.connect(lambda _, r=row, c=col: self.make_move(r, c))
                self.grid.addWidget(button, row, col)

        # Control buttons
        control_layout = QHBoxLayout()

        new_game_btn = SciFiButton("New Game")
        new_game_btn.setStyleSheet("""
            SciFiButton {
                background: rgba(255, 0, 255, 100);
                border: 2px solid #00ffff;
                border-radius: 15px;
                padding: 15px;
                color: white;
            }
            SciFiButton:hover {
                background: rgba(255, 0, 255, 150);
            }
        """)
        new_game_btn.clicked.connect(self.reset_game)

        menu_btn = SciFiButton("Go To Menu")
        menu_btn.setStyleSheet(new_game_btn.styleSheet())
        menu_btn.clicked.connect(self.return_to_menu)

        control_layout.addWidget(new_game_btn)
        control_layout.addWidget(menu_btn)

        # Add widgets to layout
        main_layout.addWidget(self.title_label)
        main_layout.addLayout(self.grid)
        main_layout.addLayout(control_layout)

        # Game state
        self.current_player = random.choice(["X", "O"])
        self.board = [[None for _ in range(self.board_size)]
                    for _ in range(self.board_size)]

        # Animation setup
        self.opacity_effect = QGraphicsOpacityEffect(self.title_label)
        self.title_label.setGraphicsEffect(self.opacity_effect)

        self.title_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.title_anim.setDuration(1500)
        self.title_anim.setStartValue(0.3)
        self.title_anim.setEndValue(1.0)
        self.title_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.title_anim.setLoopCount(-1)
        self.title_anim.start()

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

            # Animate the move
            original_style = button.styleSheet()
            button.setStyleSheet(original_style + "color: #ff00ff;")
            QTimer.singleShot(200, lambda: button.setStyleSheet(original_style))

            if self.check_winner(row, col):
                self.show_winner()
            elif self.check_draw():
                self.show_draw()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.update_title()

    def check_winner(self, last_row, last_col):
        directions = [
            (0, 1),  # horizontal
            (1, 0),  # vertical
            (1, 1),  # diagonal down
            (1, -1), # diagonal up
        ]

        for dr, dc in directions:
            count = 1
            for step in [-1, 1]:
                r, c = last_row, last_col
                while True:
                    r += dr * step
                    c += dc * step
                    if 0 <= r < self.board_size and 0 <= c < self.board_size:
                        if self.board[r][c] == self.current_player:
                            count += 1
                        else:
                            break
                    else:
                        break
            if count >= self.required_to_win:
                return True
        return False

    def check_draw(self):
        return all(cell is not None for row in self.board for cell in row)

    def show_winner(self):
        for row in self.buttons:
            for button in row:
                button.setEnabled(False)
        winner_name = self.players[self.current_player]
        self.title_label.setText(f"{winner_name} WINS!")

    def show_draw(self):
        self.title_label.setText("DRAW!")

    def update_title(self):
        player_name = self.players[self.current_player]
        self.title_label.setText(f"{player_name}'s Turn")

    def reset_game(self):
        self.current_player = random.choice(["X", "O"])
        self.board = [[None for _ in range(self.board_size)]
                     for _ in range(self.board_size)]
        self.update_title()
        for row in self.buttons:
            for button in row:
                button.setText("")
                button.setEnabled(True)

    def return_to_menu(self):
        self.menu = MainMenu()
        self.menu.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./img/logo.png"))
    app.setStyleSheet("""
        * {
            color: #00ffff;
            font-family: 'Orbitron';
        }
        QLabel {
            background: transparent;
        }
    """)

    menu = MainMenu()
    menu.show()
    sys.exit(app.exec())
