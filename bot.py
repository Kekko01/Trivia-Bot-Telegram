#!/usr/bin/env python

from datetime import datetime
import logging

from credentials import telegram_token, db_host, db_name, db_user, db_password
from trivia import trivia
import random
import mysql.connector

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This bot is not compatible with your current PTB version {TG_VER}."
    )
from telegram.constants import ParseMode
from telegram import (
    Poll,
    Update,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    PollAnswerHandler,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Inform user about what this bot can do"""
    if update.effective_chat.type == "private":
        await update.effective_message.reply_text(
            f"Hi {update.effective_user.name} 👋! I'm a trivia bot. I can give you a quiz. Use /quiz to get a quiz. For add me to your group, use click here: https://t.me/free_trivia_bot?startgroup=true"
        )
    else:
        await update.effective_message.reply_text(
            f"Hi {update.effective_chat.title} 👋! I'm a trivia bot. I can give you a quiz and send a group ranking. Use /quiz to get a quiz."
        )

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    question = (await trivia.question(amount=1, category=0, difficulty=None, quizType=None))[0]
    
    options = (question["incorrect_answers"])
    options.append(question["correct_answer"])
    random.shuffle(options)
    correct_option = options.index(question["correct_answer"])
    
    message = await update.effective_message.reply_poll(
        f"❔ Category: {questions['category']}\n⚠️ Difficulty: {question['difficulty']}\n{question['question']}",
        options,
        type=Poll.QUIZ,
        correct_option_id=correct_option,
        is_anonymous=False
    )

    payload = {
        message.poll.id: {
            "chat_id": update.effective_chat.id,
            "message_id": message.message_id,
            "questions": options,
            "correct_option_id": correct_option
        }
    }
    
    context.bot_data.update(payload)


async def receive_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Receive the answer to a quiz"""
    # Get the poll id from the message
    poll_id = update.poll_answer.poll_id
    # Get the payload from the bot_data
    payload = context.bot_data[poll_id]
    # Get the correct_option_id from the payload
    correct_option_id = payload["correct_option_id"]
    # Get the answer from the user
    answer = update.poll_answer.option_ids[0]
    # Check if the answer is correct
    if answer == correct_option_id:
        # Get the chat_id and message_id from the payload
        chat_id = payload["chat_id"]
        # Add a point for correct answer
        await add_point(update.poll_answer.user.id, chat_id, update.poll_answer.user.username)

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display a help message"""
    await update.message.reply_text("Use /quiz to get a quiz.\nUse /ranking to get the ranking.\nUse /help to get this message.\nUse /start to get this message.\nUse /points to get the sum of your points.\nUse /vote for voting bot, /code for get the code Github page.")

async def vote_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display a call-to-action vote message"""
    await update.message.reply_text("If you like the bot, please vote me here: https://t.me/BotsArchive/2474 ")

async def github_page(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display Github Page message"""
    await update.message.reply_text("If you want see or make a pull request, here the Github Page of the Bot: https://github.com/Kekko01/Trivia-Bot-Telegram ")


async def add_point(user_id, chat_id, username) -> None:
    """Add a point to the user"""
    mydb = mysql.connector.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password,
    )
    mycursor = mydb.cursor()
    sql = "INSERT INTO ranking (user_id, chat_id, username, date) VALUES (%s, %s, %s, %s)"
    val = (user_id, chat_id, username, datetime.now())
    mycursor.execute(sql, val)
    mydb.commit()
    sql = "UPDATE ranking SET username = %s WHERE user_id = %s"
    val = (username, user_id)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()
    mydb.close()

async def get_ranking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat.type == "private":
        await update.message.reply_text("⚠️ This command is only for groups.")
    else:
        """Display the ranking"""
        mydb = mysql.connector.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
        )
        mycursor = mydb.cursor()
        sql = f"SELECT username, count(date) AS points FROM ranking WHERE chat_id = {str(update.effective_chat.id)} GROUP BY username ORDER BY points DESC"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        ranking = (
            f"🏅 This is the top 10 ranking for the chat {update.effective_chat.title}"
            + ":\n"
        )
        position = 1
        actual_points = myresult[0][1]
        for row in myresult:
            if row[1] < actual_points:
                position += 1
                actual_points = row[1]
            if position <= 10:
                ranking += (
                    f"{str(position)}) [{row[0]}](https://t.me/{row[0]}): {str(row[1])}"
                    + " points\n"
                )
        await update.message.reply_text(ranking, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        mycursor.close()
        mydb.close()

async def get_my_points(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display the ranking"""
    mydb = mysql.connector.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password,
    )
    mycursor = mydb.cursor()
    sql = f"SELECT count(date) AS points FROM ranking WHERE user_id = {str(update.effective_user.id)} GROUP BY username"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    try:
        ranking = f"You have {str(myresult[0][0])}" + " points! 🧮\n"
    except IndexError:
        ranking = "You have no points! ❎\n"
    await update.message.reply_text(ranking)
    mycursor.close()
    mydb.close()


def main() -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(telegram_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("quiz", quiz))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(PollAnswerHandler(receive_quiz_answer))
    application.add_handler(CommandHandler("ranking", get_ranking))
    application.add_handler(CommandHandler("points", get_my_points))
    application.add_handler(CommandHandler("vote", vote_bot))
    application.add_handler(CommandHandler("code", github_page))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
