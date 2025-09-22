from flask import Flask
from threading import Thread

app = Flask("")

@app.route('/')
def home():
    return "Le Bot est en ligne !"

@app.route("/Test.txt")
def render():
    return open("Test_txt.txt", "r")

@app.route("/bot.py")
def affiche():
    return open("Bot.py", "r")

def run():
    app.run(host= "0.0.0.0", port= 8080)

def keep_alive():
    t = Thread(target= run)
    t.start()




