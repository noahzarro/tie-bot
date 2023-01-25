import json
from telegram import Update
from telegram.ext import ApplicationBuilder, filters, ContextTypes, MessageHandler, CommandHandler

from datetime import date
import random


# create Bot
with open("token.json","r") as read_file:
    TOKEN = json.load(read_file)["token"]
app = ApplicationBuilder().token(TOKEN).build()


async def results(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    today: str = date.today()
    today_str = today.strftime("%Y-%m-%d")
    random.seed(today_str)

    message = update.message.text

    lines = message.split("\n")

    scores = []
    votes = []

    for i in range(0,len(lines)):
        if "results" in lines[i]:
            continue
        if ":" in lines[i]:
            mensa = lines[i].split(":")[0]
            score = int(lines[i].split("+")[1])
            vote = {"mensa":mensa, "score":score}
            votes.append(vote)
            scores.append(score)

    max_score = max(scores)

    mensas=[]
    for vote in votes:
        if vote["score"] == max_score:
            mensas.append(vote["mensa"])


    mensas.sort()
    reply = "Mensas under consideration:\n"
    for mensa in mensas:
        reply += "- " + mensa + "\n"
    reply+="The winner is: " + random.choice(mensas)
    reply+="\nThe seed was: "+ today_str

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Forward me a Decidobot3000 tied results message"
    )

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL, results))

app.run_polling()
