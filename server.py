from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import json

from Message import Message, MessageType


def send_msg_to_client(client: socket, msg_type: MessageType, msg_info: str) -> None:
    print("sending msg: {}".format(msg_info))
    msg = Message(msg_type, msg_info)
    encoded_to_json_msg = json.dumps(msg.__dict__)
    client.send(bytes(encoded_to_json_msg, "utf8"))


def init_new_client(client: socket, client_address: str, name: str) -> None:
    addresses[client] = client_address
    clients_c_to_n[client] = name
    clients_n_to_c[name] = client
    free_clients_c_to_n[client] = name
    free_clients_n_to_c[name] = client


def ask_name_for_client(client: socket) -> str:
    send_msg_to_client(client, MessageType.info, "Welcome! Now type your name and press enter!")
    name = client.recv(BUFSIZ).decode("utf8")
    return name


def accept_incoming_connections() -> None:
    while True:
        client, client_address = SERVER.accept()
        try:
            name = ask_name_for_client(client)

            print("{}:{} : {} has connected.".format(*client_address, name))

            init_new_client(client, client_address, name)

            if len(free_clients_c_to_n.keys()) == 1:
                send_msg_to_client(client, MessageType.info, "Please, wait other players")
            broadcast("{} is connected! You can connect to him.".format(name), [client])
        except:
            print('Connection failed')
        else:
            Thread(target=handle_client, args=(client, name)).start()


def broadcast(msg: str, blacklist: list) -> None:
    print("Broadcasting msg: {}".format(msg))
    for client in clients_c_to_n:
        if client not in blacklist:
            send_msg_to_client(client, MessageType.info, msg)


def delete_client(client: socket, name: str) -> None:
    print("{} is disconnect".format(name))
    client.close()
    del clients_c_to_n[client]
    del clients_n_to_c[name]
    if client in free_clients_c_to_n:
        del free_clients_c_to_n[client]
        del free_clients_n_to_c[name]
    del addresses[client]
    if client in exist_games_c_to_c.keys():
        for_del = exist_games_c_to_c[client]
        del exist_games_c_to_c[client]
        del exist_games_c_to_c[for_del]


def wait_request(client: socket) -> Message:
    raw_msg = client.recv(BUFSIZ).decode()
    print('Get new request!')
    json_message = json.loads(raw_msg)
    msg = Message(**json_message)
    return msg


def connecting_request(client: socket, request: Message):
    clientname_to_connect = request.info
    if clientname_to_connect not in free_clients_n_to_c:
        if clientname_to_connect in clients_n_to_c:
            send_msg_to_client(client, MessageType.info, "{} is busy".format(clientname_to_connect))
        else:
            send_msg_to_client(client, MessageType.info, '{} not exist'.format(clientname_to_connect))
    else:
        send_msg_to_client(client, MessageType.info, "Connecting")
        client_to_connect = clients_n_to_c[clientname_to_connect]

        del free_clients_n_to_c[clientname_to_connect]
        del free_clients_c_to_n[client_to_connect]

        current_name = free_clients_c_to_n[client]
        del free_clients_n_to_c[current_name]
        del free_clients_c_to_n[client]

        exist_games_c_to_c[client] = client_to_connect
        exist_games_c_to_c[client_to_connect] = client

        send_msg_to_client(client_to_connect, MessageType.start_game, current_name)
        send_msg_to_client(client, MessageType.start_game, clientname_to_connect)


def attack_request(client: socket, request: Message):
    attacked_client = exist_games_c_to_c[client]
    send_msg_to_client(attacked_client, request.type, request.info)


def handle_client(client: socket, name: str) -> None:
    while True:
        try:
            request = wait_request(client)

            if request.type == MessageType.show_clients:
                send_msg_to_client(client, MessageType.info, str(free_clients_n_to_c.keys()))
            elif request.type == MessageType.connecting:
                connecting_request(client, request)
            elif request.type == MessageType.attack or request.type == MessageType.response_by_attack:
                attack_request(client, request)
            else:
                send_msg_to_client(client, MessageType.info, 'Unknown type')
        except (OSError, json.decoder.JSONDecodeError):
            import sys
            import traceback
            _, _, tb = sys.exc_info()
            print(traceback.format_list(traceback.extract_tb(tb)[-1:])[-1])
            print("deleting client")
            delete_client(client, name)
            break


free_clients_c_to_n = {}
free_clients_n_to_c = {}
clients_c_to_n = {}
clients_n_to_c = {}

exist_games_c_to_c = {}
addresses = {}

HOST = '0.0.0.0'
PORT = 65433
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
