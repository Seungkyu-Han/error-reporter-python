from dataclasses import dataclass


@dataclass
class MessageBuilderOption:

    method: str = ''
    path: str = ''
    ip: str = ''
    body: str = ''
    error: str = ''
    stack: str = ''