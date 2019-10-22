import select
import socket
import threading

from game_engine import Controller
from game_engine.Jeu import Jeu

IP = "127.0.0.1"
PORT = 10000
DEBUG = False

SEPARATOR = "##-+-##"

message_recieved = []
messages_to_send = []
running_threads = {}


def send_waiting_messages(wlist):
    for message in messages_to_send:
        client_socket, data = message
        if client_socket in wlist:
            client_socket.send(format_message(data).encode())
            messages_to_send.remove(message)


def analize_message(msg, game_instance: Jeu):
    # TODO: try/except the method
    call_method = msg[0] == '1'
    if call_method:
        method_name = msg[1:65].rstrip(' ')
        nb_attribute = int(msg[65:66])
        args = msg[66:].split(SEPARATOR, nb_attribute) if nb_attribute > 0 else []
        func = getattr(Controller, method_name)
        if DEBUG:
            print(f"{method_name}, {args}")
        to_send = func(game_instance, *args)
        return to_send

    return "null"


def format_message(msg):
    if type(msg) in [list, tuple]:
        return_string = SEPARATOR.join(msg)
    else:
        return_string = msg
    if DEBUG:
        print(f"Sending: {return_string}")
    return str(len(msg)).rjust(4, "0") + return_string


def incoming_messages():
    while True:
        for message in message_recieved:
            game_instance, data = message
            to_send = call(game_instance, data)
            messages_to_send.append((game_instance, to_send))
            message_recieved.remove(message)


def call(game_instance, data):
    running = running_threads.get(game_instance)
    if running is None:
        game = Jeu()
        running_threads[game_instance] = game
        running = game
    return analize_message(data, running)


def main():
    server_socket = socket.socket()
    server_socket.bind((IP, PORT))
    server_socket.listen(5)
    open_client_sockets = []
    process_incoming_messages = threading.Thread(target=incoming_messages, daemon=True)
    process_incoming_messages.start()
    while True:
        rlist, wlist, xlist = select.select([server_socket] + open_client_sockets, open_client_sockets, [])
        for current_socket in rlist:
            if current_socket is server_socket:
                (new_socket, address) = server_socket.accept()
                open_client_sockets.append(new_socket)
                print("New Client!")
            else:
                try:
                    length = current_socket.recv(4).decode()
                    data = current_socket.recv(int(length)).decode()
                except ValueError:
                    data = ""
                print("New data from client:", data)
                if data == "":
                    open_client_sockets.remove(current_socket)
                    print("Connection with client closed.")
                    del running_threads[current_socket]
                else:
                    message_recieved.append((current_socket, data))

        send_waiting_messages(wlist)


if __name__ == '__main__':
    main()
