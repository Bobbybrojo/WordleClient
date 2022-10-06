import json
import socket
import ssl
from word_manager import WordManager


# Represents an object that plays Wordle by communicating with a server
class WordlePlayer:

    def __init__(self, host, port, user, use_tls):
        self.host = host
        self.port = port
        self.id = None

        # Setup messages to send to server
        self.helloMsg = {"type": "hello", "northeastern_username": user}
        self.guessMsg = {"type": "guess", "id": None, "word": None}

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if use_tls:
            context = ssl.create_default_context()
            context.verify_mode = ssl.CERT_REQUIRED
            context.load_default_certs()
            self.socket = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=self.host)


        self.word_manager = WordManager()
        self.game_data = {}

    # Starts the game of Wordle with the server (connects and sends start message)
    def play(self):
        self.socket.connect((self.host, self.port))
        self.__send(self.helloMsg)
        self.process_server_message(self.__receive())


    # Processes messages received from the server and continues playing given the new data
    def process_server_message(self, message):
        msg = json.loads(message.decode().strip("\n"))
        if msg["type"] == "start":
            self.id = msg["id"]

            # Makes the first guess of the game
            self.guessMsg["id"] = self.id
            self.guessMsg["word"] = "crane"
            self.__send(self.guessMsg)
            self.process_server_message(self.__receive())
        if msg["type"] == "retry":
            self.game_data = msg["guesses"]
            guess = self.game_data[-1]
            for x in range(5):
                self.word_manager.add_letter(guess["word"][x:x+1], guess["marks"][x], x)
            self.word_manager.filter_words()  # filter out bad words based on data back from server

            # send the next guess to the server by getting a valid word from the word list
            self.guessMsg["word"] = self.word_manager.get_word()
            self.__send(self.guessMsg)
            self.process_server_message(self.__receive())  # recursively process the server's message
        if msg["type"] == "bye":
            print(msg["flag"])
        if msg["type"] == "error":
            print(msg["message"])

    # Sends a message to the server
    # Messages are formatted as Python dictionaries
    def __send(self, msg):
        self.socket.send(json.dumps(msg).encode() + "\n".encode())

    # Receives a complete message from the server and returns it
    def __receive(self):
        msg = self.socket.recv(1024)
        while not msg.decode().endswith('\n'):
            msg += self.socket.recv(1024)

        return msg
