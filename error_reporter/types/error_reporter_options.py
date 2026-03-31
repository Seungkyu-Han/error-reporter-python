from dataclasses import dataclass
from typing import Union, Literal, Optional


@dataclass
class SlackOptions:
    type: Literal["slack"]
    webhook_url: str
    server_name: Optional[str] = "unknown server"


ErrorReporterOptions = Union[
    SlackOptions,
]