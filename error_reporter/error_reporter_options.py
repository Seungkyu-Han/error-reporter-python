from pydantic import BaseModel

class SlackOptions(BaseModel):
    webhook_url: str
    server_name: str = "unknown server"

class DiscordOptions(BaseModel):
    webhook_url: str
    server_name: str = "unknown server"

class GoogleChatOptions(BaseModel):
    webhook_url: str
    server_name: str = "unknown server"