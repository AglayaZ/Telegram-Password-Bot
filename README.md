# Telegram Password Bot

A simple Telegram bot that generates random passwords and checks how strong a password is.

## Features

- **/generate** — generates a random password of a length you choose (letters, digits, and symbols)
- **/check** — analyzes a password and tells you how strong it is, using [zxcvbn](https://github.com/dropbox/zxcvbn), with an estimated crack time and suggestions for improvement

## Setup

1. Clone this repo and open it in your editor.

2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your bot token:
   ```
   BOT_TOKEN=your.token.here
   ```
   (Get a token by messaging [@BotFather](https://t.me/BotFather) on Telegram.)

4. Run the bot
