from pydantic import BaseModel

class SlackOptions(BaseModel):
    webhook_url: str
    server_name: str = "unknown"

class DiscordOptions(BaseModel):
    webhook_url: str
    server_name: str = "unknown"