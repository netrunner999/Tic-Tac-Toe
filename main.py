import sys
import random
import asyncio
from qasync import QEventLoop
import websockets
import logging
import traceback
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox
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
    QGraphicsOpacityEffect,
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
)

import threading

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("game.log")],
)
logger = logging.getLogger(__name__)


class SciFiButton(QPushButton):
    def __init__(self, text, parent=None):
        """
        Initializes a custom Sci-Fi styled button with specific font and size settings.
        """
        super().__init__(text, parent)
        self.setFont(QFont("Orbitron", 14, QFont.Weight.Bold))
        self.setMinimumSize(60, 60)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)


class MainMenu(QMainWindow):
    def __init__(self):
        """
        Initializes the main menu window and sets up the UI components.
        """
        super().__init__()
        logger.info("Initializing main menu")
        self.initUI()
        self.set_background()

    def initUI(self):
        """
        Sets up the main menu UI, including title, input fields, and buttons.
        """
        self.setWindowTitle("Cyber Tic Tac Toe")
        self.setFixedSize(600, 650)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 20, 40, 20)
        central_widget.setLayout(layout)

        title = QLabel("CYBER TIC TAC TOE")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Orbitron", 32, QFont.Weight.Bold))

        input_layout = QVBoxLayout()

        self.player_x_input = QLineEdit()
        self.player_x_input.setPlaceholderText("Player X")
        self.player_x_input.setStyleSheet(
            """
            QLineEdit {
                background: rgba(30, 30, 60, 200);
                border: 2px solid #00ffff;
                border-radius: 10px;
                padding: 10px;
                color: #00ffff;
                font: 16px Orbitron;
            }
        """
        )

        self.player_o_input = QLineEdit()
        self.player_o_input.setPlaceholderText("Player O")
        self.player_o_input.setStyleSheet(self.player_x_input.styleSheet())

        input_layout.addWidget(QLabel("Player X Name:"))
        input_layout.addWidget(self.player_x_input)
        self.player_o_label = QLabel("Player O Name:")
        input_layout.addWidget(self.player_o_label)
        input_layout.addWidget(self.player_o_input)

        self.size_combobox = QComboBox()
        self.size_combobox.addItems(["3x3 (Classic)", "9x9 (Extended)"])
        self.size_combobox.setStyleSheet(
            """
            QComboBox {
                background-color: rgba(30, 30, 60, 200);
                border: 2px solid #00ffff;
                border-radius: 10px;
                padding: 10px;
                color: #00ffff;
                font: 16px Orbitron;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: black;
                border: 2px solid #00ffff;
                border-radius: 10px;
                padding: 10px;
                font: 16px Orbitron;
            }
            """)

        self.mode_combobox = QComboBox()
        self.mode_combobox.setStyleSheet(self.size_combobox.styleSheet())

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("IP хоста (например: ws://127.0.0.1:8765)")
        self.ip_input.setStyleSheet(self.player_x_input.styleSheet())
        self.ip_input.hide()
        layout.addWidget(self.ip_input)

        start_btn = SciFiButton("Start Game")
        start_btn.clicked.connect(self.start_game)
        start_btn.setStyleSheet(
            """
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
        """
        )

        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addLayout(input_layout)
        layout.addSpacing(10)
        layout.addWidget(QLabel("Select Board Size:"))
        layout.addWidget(self.size_combobox)
        layout.addSpacing(10)
        layout.addWidget(QLabel("Game Mode:"))
        layout.addWidget(self.mode_combobox)
        layout.addStretch()
        layout.addWidget(start_btn)

        self.mode_combobox.addItems(
            ["Оффлайн игра", "Онлайн - хост", "Онлайн - клиент"]
        )
        self.mode_combobox.currentIndexChanged.connect(self.update_input_fields)

    def set_background(self):
        """
        Sets the gradient background for the main menu.
        """
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor(10, 10, 30))
        gradient.setColorAt(1.0, QColor(30, 10, 40))

        palette = self.palette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setPalette(palette)

    def update_input_fields(self):
        mode = self.mode_combobox.currentText()
        is_online = "Онлайн" in mode

        if is_online:
            self.ip_input.show() if mode == "Онлайн - клиент" else self.ip_input.hide()
            self.size_combobox.setEnabled(False)
            self.size_combobox.setCurrentIndex(0)  # Устанавливаем 3x3 для онлайн игры
            self.player_o_input.hide()
            self.player_o_label.hide()
            self.player_x_input.setPlaceholderText("Ваше имя")
        else:
            self.ip_input.hide()
            self.size_combobox.setEnabled(True)
            self.player_o_input.show()
            self.player_o_label.show()
            self.player_x_input.setPlaceholderText("Player X")

    def start_game(self):
        try:
            mode = self.mode_combobox.currentText()
            is_online = "Онлайн" in mode
            board_size = (
                3
                if is_online
                else (3 if "3x3" in self.size_combobox.currentText() else 9)
            )
            player_name = self.player_x_input.text() or "Player"
            logger.info(
                f"Starting game - Mode: {mode}, Board size: {board_size}, Player: {player_name}"
            )

            if mode == "Оффлайн игра":
                player_o = self.player_o_input.text() or "Player O"
                logger.info(
                    f"Starting offline game with players: {player_name} vs {player_o}"
                )
                self.game_window = GameWindow(
                    board_size, player_name, player_o, mode="offline"
                )
                self.game_window.show()
                self.hide()

            elif mode == "Онлайн - хост":
                logger.info("Starting online game as host")
                from server import start_server

                server_thread = threading.Thread(target=start_server)
                server_thread.daemon = True
                server_thread.start()

                self.game_window = GameWindow(
                    board_size, player_name, None, mode="host"
                )
                self.game_window.show()
                self.hide()

            elif mode == "Онлайн - клиент":
                logger.info("Starting online game as client")

                ip = self.ip_input.text().strip()
                if not ip:
                    raise ValueError("Не введён IP адрес")

                self.game_window = GameWindow(
                    board_size, player_name, None, mode="client", server_ip=ip
                )
                self.game_window.show()
                self.hide()

        except Exception as e:
            logger.error(f"Error starting game: {str(e)}")
            logger.error(traceback.format_exc())
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Произошла ошибка при запуске игры:\n{e}",
            )


class GameWindow(QMainWindow):
    def __init__(self, board_size, player_x, player_o, mode="offline", server_ip=None):
        """
        Initializes the game window with the specified board size and player names.
        """
        super().__init__()
        logger.info(
            f"Initializing game window - Mode: {mode}, Board size: {board_size}"
        )
        self.players = {"X": player_x, "O": player_o}
        self.mode = mode
        self.client = None
        self.symbol = None
        self.server_ip = server_ip
        self.current_player = "X"
        self.game_active = mode == "offline"

        if mode in ("host", "offline"):
            self.board_size = board_size
            self.required_to_win = 3 if board_size == 3 else 5
        else:
            self.board_size = 3
            self.required_to_win = 3

        self.board = [
            [None for _ in range(self.board_size)] for _ in range(self.board_size)
        ]

        self.setWindowTitle("Cyber Tic Tac Toe")
        self.setMinimumSize(
            800 if self.board_size == 9 else 600, 850 if self.board_size == 9 else 700
        )

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")

        central_widget = QWidget()
        self.setCentralWidget(scroll)
        scroll.setWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.title_label = QLabel("Cyber Tic Tac Toe")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont("Orbitron", 28, QFont.Weight.Bold))

        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        self.buttons = [
            [SciFiButton("") for _ in range(self.board_size)]
            for _ in range(self.board_size)
        ]

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
                # Кнопки активны сразу в оффлайн режиме
                button.setEnabled(mode == "offline")
                self.grid.addWidget(button, row, col)

        control_layout = QHBoxLayout()

        new_game_btn = SciFiButton("New Game")
        new_game_btn.setStyleSheet(
            """
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
        """
        )
        new_game_btn.clicked.connect(self.reset_game)

        menu_btn = SciFiButton("Go to Main Menu")
        menu_btn.setStyleSheet(new_game_btn.styleSheet())
        menu_btn.clicked.connect(self.return_to_menu)

        control_layout.addWidget(new_game_btn)
        control_layout.addWidget(menu_btn)

        main_layout.addWidget(self.title_label)
        main_layout.addLayout(self.grid)
        main_layout.addLayout(control_layout)

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

        self.update_title()

        if mode in ("host", "client"):
            try:
                from client import GameClient

                host = self.server_ip or "localhost"
                logger.info(f"Initializing client with host: {host}")
                self.client = GameClient(
                    host,
                    callbacks={
                        "on_assign": self.assign_symbol,
                        "on_start": self.online_start,
                        "on_state_update": self.handle_state_update,
                        "on_game_end": self.handle_game_end,
                        "on_error": self.handle_error,
                    },
                )

                if self.client.connect():
                    logger.info("Successfully connected to server")
                else:
                    raise Exception("Failed to connect to server")

            except Exception as e:
                logger.error(f"Error initializing client: {str(e)}")
                logger.error(traceback.format_exc())
                QMessageBox.critical(
                    self,
                    "Ошибка",
                    f"Ошибка инициализации клиента:\n{e}",
                )
                self.close()

    def handle_state_update(self, state):
        """Обработка обновления состояния игры от сервера"""
        logger.info(f"Received state update: {state}")
        self.game_state = state
        self.board = state["board"]
        self.current_player = state["current_player"]
        self.game_active = state["game_active"]

        for row in range(self.board_size):
            for col in range(self.board_size):
                self.buttons[row][col].setText(self.board[row][col] or "")
                self.buttons[row][col].setEnabled(
                    self.game_active
                    and self.board[row][col] is None
                    and self.symbol == self.current_player
                )

        self.update_title()

    def handle_error(self, message):
        """Обработка ошибок от сервера"""
        logger.error(f"Server error: {message}")
        QMessageBox.critical(self, "Ошибка сервера", message)
        self.close()

    def assign_symbol(self, symbol):
        self.symbol = symbol
        self.players[symbol] = self.players["X"]
        logger.info(f"Assigned symbol: {symbol}")
        self.update_title()

    def online_start(self):
        self.board = [
            [None for _ in range(self.board_size)] for _ in range(self.board_size)
        ]
        self.current_player = "X"
        self.game_active = True
        logger.info("Game started")
        self.update_title()
        for row in self.buttons:
            for button in row:
                button.setText("")
                button.setEnabled(True)

    def handle_game_end(self, reason, state=None):
        """Обработка окончания игры"""
        self.game_active = False
        logger.info(f"Game ended: {reason}")
        if state:
            self.game_state = state
            self.board = state["board"]
            for row in range(self.board_size):
                for col in range(self.board_size):
                    self.buttons[row][col].setText(self.board[row][col] or "")
                    logger.info(
                        f"Updating button at {row},{col} with {self.board[row][col]}"
                    )
        self.title_label.setText(f"Game Over: {reason.replace('X', '&#88;')}")
        for row in self.buttons:
            for button in row:
                button.setEnabled(False)

        self.title_label.setText(f"Game Over: {reason}")
        for row in self.buttons:
            for button in row:
                button.setEnabled(False)

    def make_move(self, row, col):
        try:
            if not self.game_active:
                logger.warning("Attempted to make move while game is not active")
                return

            if self.board[row][col]:
                logger.warning(f"Cell already occupied: row={row}, col={col}")
                return

            if self.mode != "offline" and self.symbol != self.current_player:
                logger.warning("Not player's turn")
                return

            logger.info(
                f"Making move - row: {row}, col: {col}, player: {self.current_player}"
            )

            if self.mode == "offline":
                self.board[row][col] = self.current_player
                self.buttons[row][col].setText(self.current_player)
                self.buttons[row][col].setEnabled(False)

                if self.check_winner(row, col):
                    self.game_active = False
                    logger.info(f"Game won by {self.current_player}")
                    self.handle_game_end(f"{self.players[self.current_player]} wins!")
                elif self.check_draw():
                    self.game_active = False
                    logger.info("Game ended in draw")
                    self.handle_game_end("Draw!")
                else:
                    self.current_player = "O" if self.current_player == "X" else "X"
                    logger.info(f"Turn switched to {self.current_player}")
                    self.update_title()
            else:
                if self.client and self.client.send_move(row, col):
                    logger.info("Move sent to server")
                else:
                    logger.error("Failed to send move to server")
                    QMessageBox.critical(
                        self, "Ошибка", "Не удалось отправить ход на сервер"
                    )

        except Exception as e:
            logger.error(f"Error making move: {str(e)}")
            logger.error(traceback.format_exc())
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Произошла ошибка при выполнении хода:\n{e}",
            )

    def check_winner(self, last_row, last_col):
        """
        Checks if the current player has won the game after their last move.
        """
        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1),
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
        """
        Checks if the game has ended in a draw.
        """
        return all(cell is not None for row in self.board for cell in row)

    def update_title(self):
        if self.mode != "offline":
            if not self.game_active:
                self.title_label.setText("Waiting for connection...")
                for row in self.buttons:
                    for button in row:
                        button.setEnabled(False)
            elif self.symbol == self.current_player:
                self.title_label.setText(f"{self.players[self.current_player].replace('X', '&#88;')}'s Turn")
                for row in self.buttons:
                    for button in row:
                        button.setEnabled(True)
            else:
                self.title_label.setText("Opponent's Turn")
                for row in self.buttons:
                    for button in row:
                        button.setEnabled(False)
        else:
            player_name = self.players[self.current_player].replace('X', '&#88;')
            self.title_label.setText(f"{player_name}'s Turn")
            for row in self.buttons:
                for button in row:
                    button.setEnabled(True)

    def reset_game(self):
        if self.mode != "offline":
            if self.client:
                self.client.send_reset()
            return

        self.current_player = random.choice(["X", "O"])
        self.board = [
            [None for _ in range(self.board_size)] for _ in range(self.board_size)
        ]
        self.game_active = True
        self.update_title()
        for row in self.buttons:
            for button in row:
                button.setText("")
                button.setEnabled(True)

    def return_to_menu(self):
        """
        Returns to the main menu and closes the game window.
        """
        self.menu = MainMenu()
        self.menu.show()
        self.close()

    def closeEvent(self, event):
        try:
            logger.info("Closing game window")
            if self.client:
                logger.info("Closing client connection")
                self.client.close()
            super().closeEvent(event)
        except Exception as e:
            logger.error(f"Error closing window: {str(e)}")
            logger.error(traceback.format_exc())
            event.accept()

    def set_background(self):
        """
        Sets the gradient background for the game window.
        """
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor(10, 10, 30))
        gradient.setColorAt(1.0, QColor(30, 10, 40))

        palette = self.palette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setPalette(palette)


if __name__ == "__main__":
    """
    Entry point of the application. Initializes and starts the main menu.
    """
    try:
        logger.info("Starting application")
        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon("./img/logo.png"))
        app.setStyleSheet(
            """
        * {
            color: #00ffff;
            font-family: 'Orbitron';
        }
        QLabel {
            background: transparent;
        }
        """
        )

        loop = QEventLoop(app)
        asyncio.set_event_loop(loop)

        menu = MainMenu()
        menu.show()

        with loop:
            loop.run_forever()

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        logger.error(traceback.format_exc())
        sys.exit(1)
