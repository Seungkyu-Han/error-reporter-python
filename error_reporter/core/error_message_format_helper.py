import json

from datetime import datetime

from error_reporter.types.message_builder_option import MessageBuilderOption


class ErrorMessageFormatHelper:

    def __init__(self, server_name: str = None):
        self._server_name: str = server_name or "unknown server"

    def error_message(
            self,
            message_builder_option: MessageBuilderOption,
    ) -> str:
        method = message_builder_option.method
        path = message_builder_option.path
        ip = message_builder_option.ip
        error = message_builder_option.error
        stack = message_builder_option.stack

        stack_content = (
            "\n".join(stack.split("\n")) + "\n..."
            if stack else "No stack trace available"
        )

        return f"""
🔥 *[{self._server_name}] Unhandled Exception*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*📍 Request Information*
- *Method:* `{method}`
- *Path:* `{path}`
- *IP:* `{ip}`
- *Timestamp:* `{datetime.now().isoformat()}`

❌ Error Message
{error}

📜 Stack Trace
{stack_content}
        """
