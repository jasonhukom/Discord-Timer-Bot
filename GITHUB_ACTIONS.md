# GitHub Actions setup

The Docker bot is intended for a continuously running server. You can also use GitHub Actions to send one reminder on a schedule without keeping a process online.

## Enable the scheduled GitHub workflow

1. Open the repository on GitHub.
2. Go to **Settings → Secrets and variables → Actions**.
3. Under **Secrets**, add:
   - `DISCORD_TOKEN`: your Discord bot token.
   - `CHANNEL_ID`: the target channel's numeric ID.
4. Optionally, under **Variables**, add `TIMER_MESSAGE` to customize the reminder.
5. Open **Actions**, select **Discord Timer**, and enable workflows if GitHub asks.
6. Use **Run workflow** to test it immediately.

The workflow sends one message every three hours using a GitHub-hosted runner. GitHub cron schedules use UTC and may run later than the exact scheduled minute.

## Important limitations

- GitHub Actions is not a permanent server. Each run starts a temporary runner, sends one message, and exits.
- Scheduled workflows can be delayed, and GitHub may disable schedules in inactive public repositories.
- The workflow is not suitable for real-time commands, continuous presence, or a bot that must stay online.
- For a continuously online Discord bot, use Docker Compose on your home server or another always-on host.

The Docker setup in the main README remains available for that use case.
