{
  "api": {
    "services": ["HandlerService", "StatsService"],
    "tag": "api"
  },
  "policy": {
    "levels": {
      "0": {
        "statsUserUplink": true,
        "statsUserDownlink": true
      }
    }
  },
  "stats": {},
  "routing": {
    "rules": [
      {
        "type": "field",
        "inboundTag": ["api"],
        "outboundTag": "api"
      }
    ]
  },
  "inbounds": [
    {
      "port": 8080,
      "protocol": "http",
      "tag": "api"
    }
  ]
}

با اجرای این تنظیمات، API V2Ray روی پورت 8080 در دسترس خواهد بود.

قدم 2: کد ربات تلگرام

فایل bot.py را ایجاد کنید و کد زیر را در آن قرار دهید:

import telebot
import requests
import json

# 
BOT_TOKEN = 'YOUR_BOT_TOKEN
bot = telebot.TeleBot(BOT_TOKEN)
7878835113:AAGxga0lE1kI1hPK30W-47dqVQ-JJG3PLi8
# آدرس API V2Ray
V2RAY_API_URL = 'http://127.0.0.1:8080'

# دستور اضافه کردن کاربر جدید
def add_user(uuid, email, level=0, alterId=64):
    payload = {
        "method": "add",
        "params": {
            "client": {
                "id": uuid,
                "alterId": alterId,
                "email": email,
                "level": level
            }
        },
        "tag": "api"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f"{V2RAY_API_URL}/xrayapi/command", headers=headers, data=json.dumps(payload))
    return response.json()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "به ربات مدیریت V2Ray خوش آمدید!")

@bot.message_handler(commands=['adduser'])
def handle_adduser(message):
    try:
        args = message.text.split()
        if len(args) < 3:
            bot.reply_to(message, "لطفا دستور را به صورت صحیح وارد کنید:\n/adduser <email> <uuid>")
            return
        
        email = args[1]
        uuid = args[2]

        # اضافه کردن کاربر جدید
        result = add_user(uuid, email)
        if result.get("success"):
            bot.reply_to(message, f"کاربر {email} با موفقیت اضافه شد!")
        else:
            bot.reply_to(message, "خطا در اضافه کردن کاربر.")
    except Exception as e:
        bot.reply_to(message, f"خطا: {e}")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, """
دستورات موجود:
- /start: شروع
- /adduser <email> <uuid>: اضافه کردن کاربر جدید
    """)

if name == "main":
    print("ربات در حال اجراست...")
    bot.polling()
