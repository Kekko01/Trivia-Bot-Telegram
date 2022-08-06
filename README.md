# Triva Bot Telegram

 A trivia bot to get random quizzes in private chat or in groups with a ranking system.

[![GitHub issues](https://img.shields.io/github/issues/Kekko01/Trivia-Bot-Telegram)](https://github.com/Kekko01/Trivia-Bot-Telegram/issues)
[![GitHub forks](https://img.shields.io/github/forks/Kekko01/Trivia-Bot-Telegram)](https://github.com/Kekko01/Trivia-Bot-Telegram/network)
[![GitHub stars](https://img.shields.io/github/stars/Kekko01/Trivia-Bot-Telegram)](https://github.com/Kekko01/Trivia-Bot-Telegram/stargazers)
[![GitHub license](https://img.shields.io/github/license/Kekko01/Trivia-Bot-Telegram)](https://github.com/Kekko01/Trivia-Bot-Telegram/blob/main/LICENSE)
[![Twitter](https://img.shields.io/twitter/url?url=https%3A%2F%2Fgithub.com%2FKekko01%2FTrivia-Bot-Telegram)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2FKekko01%2FTrivia-Bot-Telegram)

## What is it?

Trivia Bot send quiz to chat (groups or personal chats) and if someone answers correctly, add a point. Also, can send a ranking with all members group with the points accumulated.

## How to clone bot and setup

1. Download bot files from: <https://github.com/Kekko01/Trivia-Bot-Telegram/archive/refs/heads/main.zip>

2. Extract it and open folder

3. Create file named **credentials.py** with the DB credentials and Telegram Token:

    ```python
    telegram_token = "" # Telegram Bot Token
    db_host = ""        # Database host name
    db_name = ""        # Database database name
    db_user = ""        # Database user name
    db_password = ""    # Database user password
    ```

4. Create a MySQL DB o similar like MariaDB, and start this query in the database:

    ```SQL
    CREATE TABLE `ranking` (
    `user_id` bigint NOT NULL,
    `chat_id` bigint NOT NULL,
    `username` varchar(50) NOT NULL,
    `date` datetime NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    ```

5. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

6. Start the bot:

    ```bash
    python bot.py
    ```

------------

# FAQ

## How to install Python?

Go here: <https://www.python.org/downloads/> and install the verson for yout PC

## How to install a MySQL DB?

You can install for example [XAMPP](https://www.apachefriends.org/download.html "XAMPP")

## How to create a Telegram Bot?

Telegram Official Guide: <https://core.telegram.org/bots#3-how-do-i-create-a-bot>

## There are commands?

Yes, there are commands:

```
start - Start the bot
quiz - Send a quiz
help - Send help message
ranking - Send the ranking of the chat
points - Send the sum of your points
vote - Vote the bot in BotsArchive
code - Project's GitHub Page
```

## Have you problems?

Don't worry, please you can found or create a issue here: <https://github.com/Kekko01/Trivia-Bot-Telegram/issues>
