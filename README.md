# Error Reporter for Fast API

[![PyPI version](https://img.shields.io/pypi/v/error-reporter.svg)](https://pypi.org/project/error-reporter/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/error-reporter)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/error-reporter)
![license](https://img.shields.io/pypi/l/error-reporter)

A python library for Fast API that sends error reports to messaging platforms like Slack.

When an error other than an HttpException occurs on the server. it is reported according to the configured settings.

Installation

```shell
pip install error-reporter
```

## Usage

### configuration
```python
from error_reporter import init_error_reporter, SlackOptions

from fastapi import FastAPI

app = FastAPI()

init_error_reporter(
    app=app,
    options=SlackOptions(
        webhook_url='',
        server_name='',
    )
)
```

##### slack, discord, google-chat

| Option     | Type                              | Required | Default        | Description                          |
|------------|-----------------------------------|----------|----------------|--------------------------------------|
| type       | 'slack', 'discord', 'google-chat' | ✅        | -              | type of messenger                    |
| webhookUrl | string                            | ✅        | -              | Slack webhook URL to send error logs |
| serverName | string                            | ❌        | unknown server | Identifier for the server            |

##### github

| Option      | Type     | Required | Default        | Description                                  |
|-------------|----------|----------|----------------|----------------------------------------------|
| type        | 'github' | ✅        | -              | type of messenger                            |
| githubToken | string   | ✅        | -              | GitHub personal access token                 |
| owner       | string   | ✅        | -              | Repository owner (user or organization)      |
| repository  | string   | ✅        | -              | Repository name where issues will be created |
| serverName  | string   | ❌        | unknown server | Identifier for the server                    |


❗Warning

If an invalid or unauthorized token is provided, the application will fail to start.

The server will also fail to start if any of the required GitHub configuration values are missing or incorrect,
including:

## Example

### slack

![slack-example.png](https://raw.githubusercontent.com/Seungkyu-Han/Seungkyu-Han/refs/heads/main/slack_example.png)

### discord

![discord-example.png](https://raw.githubusercontent.com/Seungkyu-Han/Seungkyu-Han/refs/heads/main/discord_example.png)

### google-chat

![google-chat-example.png](https://raw.githubusercontent.com/Seungkyu-Han/Seungkyu-Han/refs/heads/main/google_example.png)

### github

![github-example.png](https://raw.githubusercontent.com/Seungkyu-Han/Seungkyu-Han/refs/heads/main/github_issue_example.png)

## Contact

- Email: [trust1204@gmail.com](mailto:trust1204@gmail.com)