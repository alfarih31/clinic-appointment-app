from dataclasses import dataclass


@dataclass
class RegisterCommand:
    full_name: str
    username: str
    password: str
