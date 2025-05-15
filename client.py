import socket
import json
import threading
import logging
import sys

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("game.log")],
)
logger = logging.getLogger(__name__)


class GameClient:
    def __init__(self, host, port=8765, callbacks=None):
        self.host = host
        self.port = port
        self.socket = None
        self.symbol = None
        self.callbacks = callbacks or {}
        self.connected = False
        self.receive_thread = None

    def connect(self):
        try:
            logger.info(f"Connecting to {self.host}:{self.port}")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            logger.info("Connected successfully")

            # Запускаем поток для приема сообщений
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.daemon = True
            self.receive_thread.start()

            return True
        except Exception as e:
            logger.error(f"Connection error: {str(e)}")
            if self.socket:
                self.socket.close()
            self.connected = False
            raise

    def receive_messages(self):
        try:
            while self.connected:
                try:
                    data = self.socket.recv(1024)
                    if not data:
                        logger.info("Connection closed by server")
                        break

                    message = json.loads(data.decode())
                    logger.info(f"Received message: {message}")

                    if message["type"] == "assign":
                        self.symbol = message["symbol"]
                        if "on_assign" in self.callbacks:
                            self.callbacks["on_assign"](self.symbol)

                    elif message["type"] == "start":
                        if "on_start" in self.callbacks:
                            self.callbacks["on_start"]()

                    elif message["type"] == "state_update":
                        if "on_state_update" in self.callbacks:
                            self.callbacks["on_state_update"](message["state"])

                    elif message["type"] == "game_end":
                        if "on_game_end" in self.callbacks:
                            self.callbacks["on_game_end"](
                                message["reason"], message.get("state")
                            )

                    elif message["type"] == "error":
                        logger.error(f"Server error: {message['message']}")
                        if "on_error" in self.callbacks:
                            self.callbacks["on_error"](message["message"])

                except json.JSONDecodeError:
                    logger.error("Invalid JSON received")
                    continue
                except Exception as e:
                    logger.error(f"Error processing message: {str(e)}")
                    break

        except Exception as e:
            logger.error(f"Error in receive_messages: {str(e)}")
        finally:
            self.connected = False
            if self.socket:
                self.socket.close()

    def send_move(self, row, col):
        if not self.connected:
            logger.error("Not connected to server")
            return False

        try:
            message = {"type": "move", "row": row, "col": col}
            self.socket.send(json.dumps(message).encode())
            return True
        except Exception as e:
            logger.error(f"Error sending move: {str(e)}")
            return False

    def send_reset(self):
        if not self.connected:
            logger.error("Not connected to server")
            return False

        try:
            message = {"type": "reset"}
            self.socket.send(json.dumps(message).encode())
            return True
        except Exception as e:
            logger.error(f"Error sending reset: {str(e)}")
            return False

    def close(self):
        self.connected = False
        if self.socket:
            self.socket.close()
