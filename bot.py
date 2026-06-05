# Telegram bot for selling Instagram accounts (zeros)
# Price: $1 per zero, quantity selection 1-10, receipt forwarding only
# Total stock: 50 zeros total
# Multi-language: English / Arabic (toggle with button)

import json
import requests

BOT_TOKEN = "8832129600:AAESASdMAnK_UiBgQAkG8our0LQw_TPaQgg"
ADMIN_ID = "8530670801"
ADMIN_USERNAME = "@AbdallahDied"

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
GIF_URL = "https://media3.giphy.com/media/v1.Y2lkPTZjMDliOTUyb3dsdGJpdXdtYnk5MGMxcDkzdDhoYmxyeXFmNGw0OXNlczM5Nnk5OSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/utx4rJxu0MiGc/giphy.gif"

PRICE_PER_ZERO = 1
remaining_stock = 50

# Language translations
TEXTS = {
    "en": {
        "welcome": "冬 Welcome to Ab Market !\n\nWe sell Instagram accounts (zeros). Use the buttons below to check stock, buy, or see payment methods.",
        "stock": "冬 Total zeros available: {} zeros\n\n冬 Each zero costs $1 USD.\n冬 Minimum order: 1 zero, Maximum: 10 zeros.",
        "select_qty": "Select how many zeros you want to buy:",
        "payment_methods": "冬 Accepted payment methods:\n\nBinance ID: 1158146717\nUSDT BEP20: 0xa674b7d30bbf53dfd83bb6f7d23d5ec2c2f146f1\nCliQ (Bank al Etihad): BDEE\n\nAfter payment, send the receipt here. Admin will contact you.",
        "confirm_purchase": "冬 You selected {} zero(s).\n冬 Total price: ${} USD\n\nPlease type the quantity number again to confirm your purchase.\nType: {}",
        "out_of_stock": "Sorry, only {} zeros left in stock!",
        "send_number": "Please send a number between 1 and 10.",
        "invalid_number": "Please send a valid number (1-10).",
        "payment_request": "冬 You selected {} zero(s).\n冬 Total price: ${} USD (${} per zero)\n\n冬 Payment methods:\nBinance ID: 1158146717\nUSDT BEP20: 0xa674b7d30bbf53dfd83bb6f7d23d5ec2c2f146f1\nCliQ (Bank al Etihad): BDEE\n\nAfter you complete the payment, send the payment receipt (screenshot or transaction ID) to this bot.\n\n冬 Your accounts will be delivered by admin after receipt confirmation.",
        "order_received": "Your order for {} zero(s) has been received!\nPlease contact the admin {} to receive your accounts.\nThank you for your purchase.",
        "use_buttons": "Please use the buttons below.",
        "back": "冬 Back",
        "stock_btn": "冬 Number of zeros (stock)",
        "buy_btn": "冬 Buy zeros",
        "payment_btn": "冬 Payment methods",
        "lang_btn": "🌐 العربية"
    },
    "ar": {
        "welcome": "冬 مرحبا بك في Ab Market !\n\nنبيع حسابات انستغرام (أصفار). استخدم الأزرار أدناه لمعرفة المخزون أو الشراء أو طرق الدفع.",
        "stock": "冬 إجمالي الأصفار المتوفرة: {} صفر\n\n冬 سعر الصفر الواحد: 1 دولار أمريكي\n冬 أقل طلب: 1 صفر، أعلى طلب: 10 أصفار.",
        "select_qty": "اختر عدد الأصفار التي تريد شراءها:",
        "payment_methods": "冬 طرق الدفع المتوفرة:\n\nBinance ID: 1158146717\nUSDT BEP20: 0xa674b7d30bbf53dfd83bb6f7d23d5ec2c2f146f1\nCliQ (Bank al Etihad): BDEE\n\nبعد الدفع، أرسل الإيصال هنا. سيتواصل معك الأدمن.",
        "confirm_purchase": "冬 لقد اخترت {} صفر(اً).\n冬 السعر الإجمالي: ${} دولار\n\nالرجاء كتابة الرقم {} مرة أخرى لتأكيد شرائك.\nاكتب: {}",
        "out_of_stock": "عذراً، لم يتبق سوى {} صفر(اً) فقط!",
        "send_number": "الرجاء إرسال رقم بين 1 و 10.",
        "invalid_number": "الرجاء إرسال رقم صحيح (1-10).",
        "payment_request": "冬 لقد اخترت {} صفر(اً).\n冬 السعر الإجمالي: ${} دولار (${} للصفر الواحد)\n\n冬 طرق الدفع:\nBinance ID: 1158146717\nUSDT BEP20: 0xa674b7d30bbf53dfd83bb6f7d23d5ec2c2f146f1\nCliQ (Bank al Etihad): BDEE\n\nبعد إتمام الدفع، أرسل إيصال الدفع (لقطة شاشة أو معرف العملية) إلى هذا البوت.\n\n冬 سيتم تسليم حساباتك بواسطة الأدمن بعد تأكيد الإيصال.",
        "order_received": "تم استلام طلبك لـ {} صفر(اً)!\nيرجى التواصل مع الأدمن {} لتسلم حساباتك.\nشكراً لك على الشراء.",
        "use_buttons": "الرجاء استخدام الأزرار أدناه.",
        "back": "冬 رجوع",
        "stock_btn": "冬 عدد الأصفار (المخزون)",
        "buy_btn": "冬 شراء أصفار",
        "payment_btn": "冬 طرق الدفع",
        "lang_btn": "🌐 English"
    }
}

user_language = {}

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

def get_lang(chat_id):
    return user_language.get(chat_id, "en")

def main_menu(chat_id):
    lang = get_lang(chat_id)
    t = TEXTS[lang]
    return {
        "inline_keyboard": [
            [{"text": t["stock_btn"], "callback_data": "stock"}],
            [{"text": t["buy_btn"], "callback_data": "buy"}],
            [{"text": t["payment_btn"], "callback_data": "payment"}],
            [{"text": t["lang_btn"], "callback_data": "switch_lang"}]
        ]
    }

def quantity_selector(chat_id):
    lang = get_lang(chat_id)
    t = TEXTS[lang]
    buttons = []
    row = []
    for qty in range(1, 11):
        row.append({"text": f"{qty}", "callback_data": f"qty_{qty}"})
        if len(row) == 5:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([{"text": t["back"], "callback_data": "back"}])
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

print("Bot is running with multi-language support...")
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
                lang = get_lang(chat_id)
                t = TEXTS[lang]
                send_message(chat_id, t["welcome"], main_menu(chat_id))
                if chat_id in user_states:
                    del user_states[chat_id]
                if chat_id in pending_purchase:
                    del pending_purchase[chat_id]
            
            elif chat_id in pending_purchase:
                try:
                    qty = int(text.strip())
                    lang = get_lang(chat_id)
                    t = TEXTS[lang]
                    if 1 <= qty <= 10:
                        if remaining_stock >= qty:
                            total_price = qty * PRICE_PER_ZERO
                            user_states[chat_id] = {"awaiting_receipt": True, "qty": qty}
                            del pending_purchase[chat_id]
                            payment_text = t["payment_request"].format(qty, total_price, PRICE_PER_ZERO)
                            send_message(chat_id, payment_text)
                        else:
                            send_message(chat_id, t["out_of_stock"].format(remaining_stock), main_menu(chat_id))
                            del pending_purchase[chat_id]
                    else:
                        send_message(chat_id, t["send_number"], main_menu(chat_id))
                        del pending_purchase[chat_id]
                except ValueError:
                    lang = get_lang(chat_id)
                    t = TEXTS[lang]
                    send_message(chat_id, t["invalid_number"], main_menu(chat_id))
                    del pending_purchase[chat_id]
            
            elif chat_id in user_states and user_states[chat_id].get("awaiting_receipt"):
                qty = user_states[chat_id]["qty"]
                receipt_text = text if text else "Receipt attached"
                
                # Get user info (username and name)
                user = msg["from"]
                username = user.get("username")
                username_str = f"@{username}" if username else "No username"
                first_name = user.get("first_name", "")
                last_name = user.get("last_name", "")
                full_name = f"{first_name} {last_name}".strip()
                if not full_name:
                    full_name = "No name"
                
                receipt_msg = (
                    f"New Purchase Order!\n"
                    f"User ID: {chat_id}\n"
                    f"Username: {username_str}\n"
                    f"Name: {full_name}\n"
                    f"Quantity: {qty} zero(s)\n"
                    f"Total: ${qty * PRICE_PER_ZERO} USD\n"
                    f"Receipt: {receipt_text}"
                )
                
                send_message(ADMIN_ID, receipt_msg)
                
                lang = get_lang(chat_id)
                t = TEXTS[lang]
                send_message(chat_id, t["order_received"].format(qty, ADMIN_USERNAME))
                
                global remaining_stock
                remaining_stock -= qty
                
                del user_states[chat_id]
            
            else:
                lang = get_lang(chat_id)
                t = TEXTS[lang]
                send_message(chat_id, t["use_buttons"], main_menu(chat_id))
        
        elif "callback_query" in update:
            call = update["callback_query"]
            chat_id = str(call["message"]["chat"]["id"])
            message_id = call["message"]["message_id"]
            data = call["data"]
            callback_id = call["id"]
            
            if data == "switch_lang":
                current = get_lang(chat_id)
                user_language[chat_id] = "ar" if current == "en" else "en"
                new_lang = get_lang(chat_id)
                t = TEXTS[new_lang]
                send_message(chat_id, t["welcome"], main_menu(chat_id))
                answer_callback_query(callback_id, "")
                continue
            
            lang = get_lang(chat_id)
            t = TEXTS[lang]
            
            if data == "stock":
                send_message(chat_id, t["stock"].format(remaining_stock), main_menu(chat_id))
            
            elif data == "buy":
                send_message(chat_id, t["select_qty"], quantity_selector(chat_id))
            
            elif data == "payment":
                send_message(chat_id, t["payment_methods"], main_menu(chat_id))
            
            elif data.startswith("qty_"):
                qty = int(data.split("_")[-1])
                if remaining_stock >= qty:
                    total_price = qty * PRICE_PER_ZERO
                    send_message(chat_id, t["confirm_purchase"].format(qty, total_price, qty))
                    pending_purchase[chat_id] = {"qty": qty, "awaiting_confirmation": True}
                else:
                    answer_callback_query(callback_id, t["out_of_stock"].format(remaining_stock), True)
            
            elif data == "back":
                send_message(chat_id, t["welcome"], main_menu(chat_id))
            
            answer_callback_query(callback_id, "")
