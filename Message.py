from enum import Enum


class MessageType(str, Enum):
    info = 'info'
    show_clients = 'show_clients'
    connecting = 'connecting'
    attack = 'attack'
    start_game = 'start_game'
    response_by_attack = 'response_by_attack'


class Message:
    def __init__(self, type: MessageType, info: str):
        self.type = type
        self.info = info
