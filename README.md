# Discord Timer Bot

A small Python Discord bot that posts a configurable message to one text channel at a regular interval. It uses [discord.py](https://discordpy.readthedocs.io/) and can run locally or in Docker.

## Features

- Sends a scheduled message every few hours (3 hours by default).
- Configurable channel, interval, and message through environment variables.
- Waits until Discord is connected before starting the timer.
- Logs successful sends and common permission/API errors.
- Docker Compose restarts the bot after a crash or host restart.

The first reminder is sent shortly after the bot becomes ready. Later reminders follow the configured interval.

## 1. Create a Discord application and bot

1. Open the Discord Developer Portal and create an application.
2. Open its **Bot** section and create a bot user.
3. Copy the bot token and keep it private. If it is exposed, reset it in the Developer Portal.
4. Under **OAuth2 → URL Generator**, select the `bot` scope.
5. Give it only the permissions it needs: **View Channel** and **Send Messages**.
6. Use the generated invite URL to add it to your server.
7. Copy the target text channel's ID. Enable Developer Mode in Discord, then use the channel context menu's **Copy Channel ID** action.

This bot does not read message content, so the Message Content privileged intent is not required.

## 2. Configure

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env`:

| Variable | Description | Default |
|---|---|---|
| `DISCORD_TOKEN` | Bot token from the Developer Portal | Required |
| `CHANNEL_ID` | ID of the text channel to post in | Required |
| `INTERVAL_HOURS` | Hours between messages | `3` |
| `TIMER_MESSAGE` | Message to send | Built-in reminder |

Never commit `.env`. It is excluded by `.gitignore` and `.dockerignore`.

## 3. Run with Docker (recommended for a server)

Install Docker Engine and the Docker Compose plugin on your Linux server. From this repository's directory, run:

```bash
docker compose up -d --build
```

Useful commands:

```bash
docker compose logs -f       # Follow logs
docker compose ps            # Check container status
docker compose restart       # Restart the bot
docker compose down          # Stop and remove the container
docker compose up -d --build # Rebuild after code changes
```

The `restart: unless-stopped` policy brings the bot back after a container or host restart, provided Docker itself starts on boot.

## 4. Run locally without Docker

Python 3.12 is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python bot.py
```

On Windows, activate the environment with `.venv\\Scripts\\activate` instead.

## How the pieces fit together

- **Python** runs the bot's logic and timer.
- **discord.py** connects the program to Discord and sends messages.
- **Dockerfile** describes how to build an image containing Python, the dependency, and the bot code.
- **Docker Compose** starts and manages the container using the settings in `.env`.
- **Your server** keeps the container running. Docker does not create the schedule; the Python bot does.

## Troubleshooting

- **Bot is offline:** check `docker compose logs -f`, the token, and your server's internet connection.
- **Missing access / Forbidden:** make sure the bot can view the selected channel and send messages there.
- **Channel not found:** check that `CHANNEL_ID` belongs to a channel in a server where the bot is installed.
- **No messages:** the first message is sent after the bot connects; subsequent messages wait for the configured interval.

## License

Choose a license before distributing this project.
