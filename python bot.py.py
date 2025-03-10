
from flask import Flask, request
import requests

# Replace with your actual bot token
TOKEN = "8024023472:AAGSjl34x-6d2D23rnxznQIV3Tg6heQzYes"

# Replace with your Telegram Group Chat ID (Negative ID for groups)
GROUP_CHAT_ID = "1369651934"

from flask import Flask

app = Flask(__name__)  # Correct way to initialize Flask

print("Hello, Telegram Bot!")  # This will print, but it's not inside Flask


# Function to add a user to the Telegram group
def add_user_to_group(user_id):
    url = f"https://api.telegram.org/bot{TOKEN}/inviteToGroup"
    payload = {"chat_id": GROUP_CHAT_ID, "user_id": user_id}
    requests.post(url, json=payload)

# Function to remove a user from the Telegram group
def remove_user_from_group(user_id):
    url = f"https://api.telegram.org/bot{TOKEN}/kickChatMember"
    payload = {"chat_id": GROUP_CHAT_ID, "user_id": user_id}
    requests.post(url, json=payload)

# Webhook for successful payments
@app.route("/payment-success", methods=["POST"])
def payment_success():
    data = request.json
    if "user_telegram_id" in data:
        user_id = data["user_telegram_id"]
        add_user_to_group(user_id)
        return {"status": "User Added"}, 200
    return {"error": "Invalid Data"}, 400

# Webhook for failed or expired payments
@app.route("/payment-failed", methods=["POST"])
def payment_failed():
    data = request.json
    if "user_telegram_id" in data:
        user_id = data["user_telegram_id"]
        remove_user_from_group(user_id)
        return {"status": "User Removed"}, 200
    return {"error": "Invalid Data"}, 400

if __name__ == "__main__":
    app.run(port=5000, debug=True)
