from dataclasses import dataclass


@dataclass
class Player:
    name: str
    team: str
    position: str
    status: str
