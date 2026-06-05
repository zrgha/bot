# Telegram bot for selling Instagram accounts (zeros)
# Price: $1 per zero, quantity selection 1-10, receipt forwarding only
# Total stock: 50 zeros total (not per quantity)

import json
import requests

BOT_TOKEN = "8832129600:AAESASdMAnK_UiBgQAkG8our0LQw_TPaQgg"
ADMIN_ID = "8530670801"
ADMIN_USERNAME = "@AbdallahDied"

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
GIF_URL = "https://media3.giphy.com/media/v1.Y2lkPTZjMDliOTUyb3dsdGJpdXdtYnk5MGMxcDkzdDhoYmxyeXFmNGw0OXNlczM5Nnk5OSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/utx4rJxu0MiGc/giphy.gif"

PRICE_PER_ZERO = 1
total_stock = 50  # Total zeros available overall

# Track how many zeros are left in total
remaining_stock = 50

def send_gif(chat_id, caption, reply_markup=None):
    url = API_URL + "/sendAnimation"
    payload = {"chat_id": chat_id, "animation": GIF_URL, "caption": caption, "parse_mode": "HTML"}
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    requests.post(url, json=payload)

def send_message(chat_id, text, reply_markup=None):
    send_gif(chat_id, text, reply_markup)

def answer_callback_query(callback_id, text, show_alert=False):
    url = API_URL + "/answerCallbackQuery"
    payload = {"callback_query_id": callback_id, "text": text, "show_alert": show_alert}
    requests.post(url, json=payload)

def main_menu():
    return {
        "inline_keyboard": [
            [{"text": "冬 Number of zeros (stock)", "callback_data": "stock"}],
            [{"text": "冬 Buy zeros", "callback_data": "buy"}],
            [{"text": "冬 Payment methods", "callback_data": "payment"}]
        ]
    }

def quantity_selector():
    buttons = []
    row = []
    for qty in range(1, 11):
        row.append({"text": f"{qty}", "callback_data": f"qty_{qty}"})
        if len(row) == 5:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([{"text": "冬 Back", "callback_data": "back"}])
    return {"inline_keyboard": buttons}

def get_updates(offset=None):
    url = API_URL + "/getUpdates"
    params = {"timeout": 30}
    if offset:
        params["offset"] = offset
    response = requests.get(url, params=params)
    return response.json().get("result", [])

user_states = {}
pending_purchase = {}

print("Bot is running...")
last_update_id = 0

while True:
    updates = get_updates(last_update_id + 1)
    for update in updates:
        last_update_id = update["update_id"]
        
        if "message" in update:
            msg = update["message"]
            chat_id = str(msg["chat"]["id"])
            text = msg.get("text", "")
            
            if text == "/start":
                send_message(chat_id, 
                    "冬 Welcome to Ab Market !\n\nWe sell Instagram accounts (zeros). Use the buttons below to check stock, buy, or see payment methods.",
                    main_menu())
                if chat_id in user_states:
                    del user_states[chat_id]
                if chat_id in pending_purchase:
                    del pending_purchase[chat_id]
            
            elif chat_id in pending_purchase:
                try:
                    qty = int(text.strip())
                    if 1 <= qty <= 10:
                        if remaining_stock >= qty:
                            total_price = qty * PRICE_PER_ZERO
                            user_states[chat_id] = {"awaiting_receipt": True, "qty": qty}
                            del pending_purchase[chat_id]
                            
                            payment_text = (
                                f"冬 You selected {qty} zero(s).\n"
                                f"冬 Total price: ${total_price} USD (${PRICE_PER_ZERO} per zero)\n\n"
                                f"冬 Payment methods:\n"
                                f"Binance ID: 1158146717\n"
                                f"USDT BEP20: 0xa674b7d30bbf53dfd83bb6f7d23d5ec2c2f146f1\n"
                                f"CliQ (Bank al Etihad): BDEE\n\n"
                                f"After you complete the payment, send the payment receipt (screenshot or transaction ID) to this bot.\n\n"
                                f"冬 Your accounts will be delivered by admin after receipt confirmation."
                            )
                            send_message(chat_id, payment_text)
                        else:
                            send_message(chat_id, f"Sorry, only {remaining_stock} zeros left in stock. Please choose a smaller quantity.", main_menu())
                            del pending_purchase[chat_id]
                    else:
                        send_message(chat_id, "Please send a number between 1 and 10.", main_menu())
                        del pending_purchase[chat_id]
                except ValueError:
                    send_message(chat_id, "Please send a valid number (1-10).", main_menu())
                    del pending_purchase[chat_id]
            
            elif chat_id in user_states and user_states[chat_id].get("awaiting_receipt"):
                qty = user_states[chat_id]["qty"]
                receipt_text = text if text else "Receipt attached"
                receipt_msg = (
                    f"New Purchase Order!\n"
                    f"User ID: {chat_id}\n"
                    f"Quantity: {qty} zero(s)\n"
                    f"Total: ${qty * PRICE_PER_ZERO} USD\n"
                    f"Receipt: {receipt_text}"
                )
                
                send_message(ADMIN_ID, receipt_msg)
                
                send_message(chat_id,
                    f"Your order for {qty} zero(s) has been received!\n"
                    f"Please contact the admin {ADMIN_USERNAME} to receive your accounts.\n"
                    f"Thank you for your purchase.")
                
                # Reduce total stock
                global remaining_stock
                remaining_stock -= qty
                
                del user_states[chat_id]
            
            else:
                send_message(chat_id, "Please use the buttons below.", main_menu())
        
        elif "callback_query" in update:
            call = update["callback_query"]
            chat_id = str(call["message"]["chat"]["id"])
            message_id = call["message"]["message_id"]
            data = call["data"]
            callback_id = call["id"]
            
            if data == "stock":
                stock_text = f"冬 Total zeros available: {remaining_stock} zeros\n\n冬 Each zero costs $1 USD.\n冬 Minimum order: 1 zero, Maximum: 10 zeros."
                send_message(chat_id, stock_text, main_menu())
            
            elif data == "buy":
                send_message(chat_id, "Select how many zeros you want to buy:", quantity_selector())
            
            elif data == "payment":
                payment_text = (
                    "冬 Accepted payment methods:\n\n"
                    "Binance ID: 1158146717\n"
                    "USDT BEP20: 0xa674b7d30bbf53dfd83bb6f7d23d5ec2c2f146f1\n"
                    "CliQ (Bank al Etihad): BDEE\n\n"
                    "After payment, send the receipt here. Admin will contact you."
                )
                send_message(chat_id, payment_text, main_menu())
            
            elif data.startswith("qty_"):
                qty = int(data.split("_")[-1])
                if remaining_stock >= qty:
                    total_price = qty * PRICE_PER_ZERO
                    send_message(
                        chat_id,
                        f"冬 You selected {qty} zero(s).\n冬 Total price: ${total_price} USD\n\nPlease type the quantity number again to confirm your purchase.\nType: {qty}"
                    )
                    pending_purchase[chat_id] = {"qty": qty, "awaiting_confirmation": True}
                else:
                    answer_callback_query(callback_id, f"Sorry, only {remaining_stock} zeros left in stock!", True)
            
            elif data == "back":
                send_message(chat_id, "Main menu:", main_menu())
            
            answer_callback_query(callback_id, "")
