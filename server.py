import socket
import threading
import json
import logging
import sys

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("game.log")],
)
logger = logging.getLogger(__name__)


class GameServer:
    def __init__(self, host="0.0.0.0", port=8765):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        self.game_state = {
            "board": [[None for _ in range(3)] for _ in range(3)],
            "current_player": "X",
            "game_active": False,
            "players": {"X": None, "O": None},
        }
        self.lock = threading.Lock()

    def start(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(2)
            logger.info(f"Server started on {self.host}:{self.port}")

            while True:
                client_socket, address = self.server_socket.accept()
                logger.info(f"New connection from {address}")

                if len(self.clients) >= 2:
                    logger.warning(
                        f"Connection rejected from {address} - maximum clients reached"
                    )
                    client_socket.send(
                        json.dumps(
                            {"type": "error", "message": "Maximum clients reached"}
                        ).encode()
                    )
                    client_socket.close()
                    continue

                client_thread = threading.Thread(
                    target=self.handle_client, args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()

        except Exception as e:
            logger.error(f"Server error: {str(e)}")
            if self.server_socket:
                self.server_socket.close()

    def handle_client(self, client_socket, address):
        try:
            # Назначаем символ игроку
            with self.lock:
                if len(self.clients) == 0:
                    symbol = "X"
                else:
                    symbol = "O"
                self.clients.append((client_socket, symbol))
                self.game_state["players"][symbol] = address[0]

            # Отправляем игроку его символ
            client_socket.send(
                json.dumps({"type": "assign", "symbol": symbol}).encode()
            )

            # Если подключились оба игрока, начинаем игру
            if len(self.clients) == 2:
                self.game_state["game_active"] = True
                for client, _ in self.clients:
                    client.send(
                        json.dumps({"type": "start", "state": self.game_state}).encode()
                    )

            # Основной цикл обработки сообщений от клиента
            while True:
                try:
                    data = client_socket.recv(1024)
                    if not data:
                        break

                    message = json.loads(data.decode())
                    logger.info(f"Received message from {address}: {message}")

                    if message["type"] == "move":
                        self.handle_move(client_socket, message)
                    elif message["type"] == "reset":
                        self.reset_game()

                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON from {address}")
                    continue
                except Exception as e:
                    logger.error(f"Error handling message from {address}: {str(e)}")
                    break

        except Exception as e:
            logger.error(f"Error handling client {address}: {str(e)}")
        finally:
            self.remove_client(client_socket)
            client_socket.close()

    def handle_move(self, client_socket, message):
        with self.lock:
            row, col = message["row"], message["col"]
            symbol = next(s for c, s in self.clients if c == client_socket)

            if not self.game_state["game_active"]:
                return

            if self.game_state["current_player"] != symbol:
                return

            if self.game_state["board"][row][col] is not None:
                return

            self.game_state["board"][row][col] = symbol
            self.game_state["current_player"] = "O" if symbol == "X" else "X"

            # Сначала отправляем обновление состояния
            for client, _ in self.clients:
                client.send(
                    json.dumps(
                        {"type": "state_update", "state": self.game_state}
                    ).encode()
                )

            # Затем проверяем победу или ничью
            if self.check_winner(row, col):
                self.game_state["game_active"] = False
                # Отправляем финальное состояние с победой
                for client, _ in self.clients:
                    client.send(
                        json.dumps(
                            {
                                "type": "game_end",
                                "reason": f"{symbol} wins",
                                "state": self.game_state,
                            }
                        ).encode()
                    )
            elif self.check_draw():
                self.game_state["game_active"] = False
                # Отправляем финальное состояние с ничьей
                for client, _ in self.clients:
                    client.send(
                        json.dumps(
                            {
                                "type": "game_end",
                                "reason": "draw",
                                "state": self.game_state,
                            }
                        ).encode()
                    )

    def check_winner(self, last_row, last_col):
        symbol = self.game_state["board"][last_row][last_col]
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for dr, dc in directions:
            count = 1
            for step in [-1, 1]:
                r, c = last_row, last_col
                while True:
                    r += dr * step
                    c += dc * step
                    if 0 <= r < 3 and 0 <= c < 3:
                        if self.game_state["board"][r][c] == symbol:
                            count += 1
                        else:
                            break
                    else:
                        break
            if count >= 3:
                return True
        return False

    def check_draw(self):
        return all(cell is not None for row in self.game_state["board"] for cell in row)

    def reset_game(self):
        with self.lock:
            self.game_state["board"] = [[None for _ in range(3)] for _ in range(3)]
            self.game_state["current_player"] = "X"
            self.game_state["game_active"] = True
            for client, _ in self.clients:
                client.send(
                    json.dumps({"type": "start", "state": self.game_state}).encode()
                )

    def remove_client(self, client_socket):
        with self.lock:
            for i, (client, symbol) in enumerate(self.clients):
                if client == client_socket:
                    self.clients.pop(i)
                    self.game_state["players"][symbol] = None
                    break

            # Если остался только один клиент, сбрасываем игру
            if len(self.clients) == 1:
                self.game_state["game_active"] = False
                remaining_client, _ = self.clients[0]
                remaining_client.send(
                    json.dumps(
                        {
                            "type": "game_end",
                            "reason": "opponent_disconnected",
                            "state": self.game_state,
                        }
                    ).encode()
                )


def start_server():
    server = GameServer()
    server.start()


if __name__ == "__main__":
    start_server()
