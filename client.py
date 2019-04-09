from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread, Lock
import json

from Message import Message, MessageType
from GameObjects.Matrix import Matrix
from GameObjects.Coordinate import Coordinate
from GameObjects.Ship import Ship

matrix = None
enemy_matrix = None
lock = Lock()

HOST, PORT = '127.0.0.1', 65433
BUFSIZ = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)


def wait_response() -> Message:
    raw_msg = client_socket.recv(BUFSIZ).decode()
    json_message = json.loads(raw_msg)
    msg = Message(**json_message)
    return msg


def get_coordinate(ship_length: int, type_coordinate: str) -> Coordinate:
    coord = input("Input {} coord (a:2) with length {}\n".format(type_coordinate, ship_length))
    while coord[0] not in 'abcdefgh' or coord[1] != ':' or coord[2] not in '1234567890' or len(coord) != 3:
        print("Enter correct coordinate")
        coord = input("Input {} coord (a:2) with length {}\n".format(type_coordinate, ship_length))
    return Coordinate(*coord.split(':'))


def get_coordinates(ship_length: int) -> (Coordinate, Coordinate):
    start = get_coordinate(ship_length, 'start')
    if ship_length == 1:
        end = start
    else:
        end = get_coordinate(ship_length, 'end')
    return start, end


def add_ships(matrix: Matrix) -> Matrix:
    for ship_length in range(1, 5):
        for _ in range(4 - (ship_length - 1)):
            start, end = get_coordinates(ship_length)

            ship = Ship(start, end)

            while len(ship) != ship_length:
                print('Uncorrect length')
                start, end = get_coordinates(ship_length)
                ship = Ship(start, end)

            matrix.add_ship(ship)
            matrix.print_matrix()
    return matrix


def enemy_attack(attack_coord: Coordinate) -> None:
    global matrix
    if matrix.matrix[attack_coord.number][attack_coord.letter_like_number] == 'X':
        matrix.matrix[attack_coord.number][attack_coord.letter_like_number] = '+'
        response = 'wounded_{}:{}'.format(attack_coord.letter, attack_coord.number)
        print('Enemy wound you')
        if matrix.all_ships_are_dead():
            print("You lose")
            response = "you win"
    else:
        print('Enemy missed')
        matrix.matrix[attack_coord.number][attack_coord.letter_like_number] = '-'
        response = 'missed_{}:{}'.format(attack_coord.letter, attack_coord.number)

    matrix.print_matrix()
    send_request(MessageType.response_by_attack, response)


def your_attack_response(msg: Message) -> None:
    global enemy_matrix
    if msg.info.startswith('wounded'):
        print("You wound enemy")
        msg = msg.info.split('_')[1]
        wounded_coord = Coordinate(msg.split(':')[0], msg.split(':')[1])
        enemy_matrix.matrix[wounded_coord.number][wounded_coord.letter_like_number] = '-'
        enemy_matrix.print_matrix()
    elif msg.info.startswith('missed'):
        print("You missed")
        msg = msg.info.split('_')[1]
        wounded_coord = Coordinate(msg.split(':')[0], msg.split(':')[1])
        enemy_matrix.matrix[wounded_coord.number][wounded_coord.letter_like_number] = '+'
        enemy_matrix.print_matrix()
    elif msg.info == 'you win':
        print("You win")


def game_loop():
    global matrix
    global enemy_matrix
    global lock
    print('Start listening server')
    while True:
        try:
            msg = wait_response()

            if msg.type == MessageType.info:
                print(msg.info)
            elif msg.type == MessageType.start_game:
                matrix = Matrix()
                enemy_matrix = Matrix()
                with lock:
                    print("start game with {}".format(msg.info))
                    # matrix = add_ships(matrix)
            elif msg.type == MessageType.attack:
                enemy_attack(msg.info)

            elif msg.type == MessageType.response_by_attack:
                your_attack_response(msg)
        except OSError:
            break


def send_request(request_type: MessageType, info: str):
    print("start sending request")
    msg = Message(request_type, info)
    encoded_to_json_msg = json.dumps(msg.__dict__)
    client_socket.send(bytes(encoded_to_json_msg, "utf8"))


def send():
    global lock
    while True:
        if not lock.locked():
            client_input = input()
            if client_input == 'show p':
                send_request(MessageType.show_clients, '')
            elif client_input.startswith('connect'):
                clientname_to_connect = client_input.split(' ')[1]
                send_request(MessageType.connecting, clientname_to_connect)
            elif client_input.startswith('attack'):
                coordinates = client_input.split(' ')[1]
                send_request(MessageType.attack, coordinates)
            else:
                print("Unknown command")


def choose_name() -> None:
    json_message = json.loads(client_socket.recv(BUFSIZ).decode())
    msg = Message(**json_message)
    name = input(msg.info + '\n')
    client_socket.send(bytes(name, "utf8"))
    print('Initialization done')


def main():
    client_socket.connect(ADDR)

    choose_name()

    receive_thread = Thread(target=game_loop)
    send_thread = Thread(target=send)
    receive_thread.start()
    send_thread.start()


if __name__ == '__main__':
    main()
