import requests
import json
import time

BOT_TOKEN = "8832129600:AAESASdMAnK_UiBgQAkG8our0LQw_TPaQgg"
ADMIN_ID = "8530670801"
ADMIN_USERNAME = "@AbdallahDied"

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
GIF_URL = "https://media3.giphy.com/media/v1.Y2lkPTZjMDliOTUyb3dsdGJpdXdtYnk5MGMxcDkzdDhoYmxyeXFmNGw0OXNlczM5Nnk5OSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/utx4rJxu0MiGc/giphy.gif"

remaining_stock = 50
user_states = {}
pending_purchase = {}

def send_gif(chat_id, caption, reply_markup=None):
    url = API_URL + "/sendAnimation"
    payload = {"chat_id": chat_id, "animation": GIF_URL, "caption": caption}
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    requests.post(url, json=payload)

def send_message(chat_id, text, reply_markup=None):
    send_gif(chat_id, text, reply_markup)

def get_updates(offset=None):
    url = API_URL + "/getUpdates"
    params = {"timeout": 30}
    if offset:
        params["offset"] = offset
    try:
        r = requests.get(url, params=params, timeout=35)
        return r.json().get("result", [])
    except:
        return []

print("Bot starting...")
last_id = 0

while True:
    try:
        updates = get_updates(last_id + 1)
        for upd in updates:
            last_id = upd["update_id"]
            
            if "message" in upd:
                msg = upd["message"]
                cid = str(msg["chat"]["id"])
                txt = msg.get("text", "")
                
                if txt == "/start":
                    markup = {"inline_keyboard": [[{"text": "Stock", "callback_data": "st"}],[{"text": "Buy", "callback_data": "by"}],[{"text": "Payment", "callback_data": "pm"}]]}
                    send_message(cid, "冬 Welcome to Ab Market!\nSell Instagram accounts (zeros).", markup)
                
                elif cid in pending_purchase:
                    try:
                        qty = int(txt.strip())
                        if 1 <= qty <= 10 and remaining_stock >= qty:
                            user_states[cid] = {"awaiting_receipt": True, "qty": qty}
                            del pending_purchase[cid]
                            send_message(cid, f"冬 Selected {qty} zeros. Total: ${qty} USD\n\nPayment:\nBinance ID: 1158146717\nUSDT BEP20: 0xa674b7d30bbf53dfd83bb6f7d23d5ec2c2f146f1\nCliQ: BDEE\n\nSend receipt after payment.")
                        else:
                            send_message(cid, "Invalid or out of stock.", {"inline_keyboard": [[{"text": "Back", "callback_data": "back"}]]})
                            del pending_purchase[cid]
                    except:
                        send_message(cid, "Send number 1-10.")
                        del pending_purchase[cid]
                
                elif cid in user_states and user_states[cid].get("awaiting_receipt"):
                    qty = user_states[cid]["qty"]
                    uname = msg["from"].get("username")
                    uname_str = f"@{uname}" if uname else "No username"
                    send_message(ADMIN_ID, f"Order!\nUser: {cid}\nUsername: {uname_str}\nQty: {qty}\nReceipt: {txt}")
                    send_message(cid, f"Order received! Contact {ADMIN_USERNAME} to get accounts.")
                    remaining_stock -= qty
                    del user_states[cid]
                
                else:
                    markup = {"inline_keyboard": [[{"text": "Stock", "callback_data": "st"}],[{"text": "Buy", "callback_data": "by"}],[{"text": "Payment", "callback_data": "pm"}]]}
                    send_message(cid, "Use buttons:", markup)
            
            elif "callback_query" in upd:
                call = upd["callback_query"]
                cid = str(call["message"]["chat"]["id"])
                data = call["data"]
                cb_id = call["id"]
                
                if data == "st":
                    send_message(cid, f"冬 Stock: {remaining_stock} zeros")
                elif data == "by":
                    send_message(cid, "冬 Choose quantity (1-10):\nType the number.")
                    pending_purchase[cid] = {}
                elif data == "pm":
                    send_message(cid, "冬 Payment:\nBinance ID: 1158146717\nUSDT BEP20: 0xa674b7d30bbf53dfd83bb6f7d23d5ec2c2f146f1\nCliQ: BDEE")
                elif data == "back":
                    markup = {"inline_keyboard": [[{"text": "Stock", "callback_data": "st"}],[{"text": "Buy", "callback_data": "by"}],[{"text": "Payment", "callback_data": "pm"}]]}
                    send_message(cid, "Main menu:", markup)
                
                requests.post(API_URL + "/answerCallbackQuery", json={"callback_query_id": cb_id})
        
        time.sleep(0.5)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)
