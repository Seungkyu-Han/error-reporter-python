from dataclasses import dataclass


@dataclass
class MessageBuilderOption:

    method: str = ''
    path: str = ''
    ip: str = ''
    error: str = ''
    stack: str = ''