# Telegram bot for selling Instagram accounts (zeros)
# No PIL dependency - works on Pythonista iOS

import json
import sys
import requests

# Simple pure Python implementation without telebot library
# Using direct API calls to avoid PIL dependency

BOT_TOKEN = "8832129600:AAESASdMAnK_UiBgQAkG8our0LQw_TPaQgg"
ADMIN_ID = "8530670801"
ADMIN_USERNAME = "@AbdallahDied"

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

stock = {i: 5 for i in range(1, 11)}

def send_message(chat_id, text, reply_markup=None):
    url = API_URL + "/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    requests.post(url, json=payload)

def edit_message_text(chat_id, message_id, text, reply_markup=None):
    url = API_URL + "/editMessageText"
    payload = {"chat_id": chat_id, "message_id": message_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    requests.post(url, json=payload)

def answer_callback_query(callback_id, text, show_alert=False):
    url = API_URL + "/answerCallbackQuery"
    payload = {"callback_query_id": callback_id, "text": text, "show_alert": show_alert}
    requests.post(url, json=payload)

def main_menu():
    return {
        "inline_keyboard": [
            [{"text": "📦 Number of zeros (stock)", "callback_data": "stock"}],
            [{"text": "💰 Buy zeros", "callback_data": "buy"}],
            [{"text": "💳 Payment methods", "callback_data": "payment"}]
        ]
    }

def quantity_selector():
    buttons = []
    row = []
    for qty in range(1, 11):
        available = stock.get(qty, 0)
        label = f"{qty} (👌{available})" if available > 0 else f"{qty} (❌)"
        row.append({"text": label, "callback_data": f"sel_qty_{qty}"})
        if len(row) == 5:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return {"inline_keyboard": buttons}

def get_updates(offset=None):
    url = API_URL + "/getUpdates"
    params = {"timeout": 30}
    if offset:
        params["offset"] = offset
    response = requests.get(url, params=params)
    return response.json().get("result", [])

user_states = {}

print("Bot is running on Pythonista...")
last_update_id = 0

while True:
    updates = get_updates(last_update_id + 1)
    for update in updates:
        last_update_id = update["update_id"]
        
        # Handle message
        if "message" in update:
            msg = update["message"]
            chat_id = msg["chat"]["id"]
            text = msg.get("text", "")
            
            if text == "/start":
                send_message(chat_id, 
                    "✨ Welcome to Zeros Shop!\n\nWe sell Instagram accounts (zeros). Use the buttons below to check stock, buy, or see payment methods.\nAfter payment, send the receipt here. Admin will contact you.",
                    main_menu())
                if chat_id in user_states:
                    del user_states[chat_id]
            else:
                # Handle receipt from user
                if chat_id in user_states and user_states[chat_id].get("awaiting_receipt"):
                    qty = user_states[chat_id]["qty"]
                    receipt_text = text if text else "Receipt attached"
                    receipt_msg = f"User: {chat_id}\nQuantity: {qty} zero(s)\nReceipt: {receipt_text}"
                    
                    # Forward to admin
                    send_message(ADMIN_ID, receipt_msg)
                    
                    send_message(chat_id,
                        f"✅ Your request for {qty} zero(s) has been completed!\nPlease contact the admin {ADMIN_USERNAME} in private to receive your accounts.\nThank you for your purchase.")
                    
                    if stock.get(qty, 0) > 0:
                        stock[qty] -= 1
                    
                    del user_states[chat_id]
                else:
                    send_message(chat_id, "Please use the buttons below.", main_menu())
        
        # Handle callback query (button press)
        elif "callback_query" in update:
            call = update["callback_query"]
            chat_id = call["message"]["chat"]["id"]
            message_id = call["message"]["message_id"]
            data = call["data"]
            callback_id = call["id"]
            
            if data == "stock":
                stock_text = "📊 Available zeros (accounts):\n"
                for qty in range(1, 11):
                    stock_text += f"• {qty} zeros: {stock.get(qty, 0)} available\n"
                edit_message_text(chat_id, message_id, stock_text, main_menu())
            
            elif data == "buy":
                edit_message_text(chat_id, message_id, "Select how many zeros you want to buy (1-10):", quantity_selector())
            
            elif data == "payment":
                payment_text = "💳 Accepted payment methods:\n\n🏦 Binance ID: 1158146717\n💎 USDT BEP20: 0xa674b7d30bbf53dfd83bb6f7d23d5ec2c2f146f1\n🏧 CliQ (Bank al Etihad): BDEE\n\nAfter payment, send the payment receipt (screenshot or transaction ID) here. The bot will forward it to admin."
                edit_message_text(chat_id, message_id, payment_text, main_menu())
            
            elif data.startswith("sel_qty_"):
                qty = int(data.split("_")[-1])
                if stock.get(qty, 0) > 0:
                    payment_text = "💳 Payment methods:\n\n🏦 Binance ID: 1158146717\n💎 USDT BEP20: 0xa674b7d30bbf53dfd83bb6f7d23d5ec2c2f146f1\n🏧 CliQ (Bank al Etihad): BDEE\n\n"
                    edit_message_text(chat_id, message_id,
                        f"You selected {qty} zero(s).\n\n{payment_text}Please send the payment receipt (screenshot or transaction ID) as text.\nAfter sending, your request will be completed.\n\n⚠️ Once you send the receipt, you will be asked to contact {ADMIN_USERNAME} in private.",
                        main_menu())
                    user_states[chat_id] = {"awaiting_receipt": True, "qty": qty}
                else:
                    answer_callback_query(callback_id, f"Sorry, {qty} zero(s) are out of stock!", True)
            
            answer_callback_query(callback_id, "")
