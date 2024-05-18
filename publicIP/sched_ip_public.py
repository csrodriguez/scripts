# -------1---------2---------3---------4---------5---------6---------7---------8
#  Project:         Public IP Notifier and DNS Record Modifier
# ------------------------------------------------------------------------------
# Author: CsR
# GitHub: https://github.com/csrodriguez
# Linkedin: https://www.linkedin.com/in/claudio-s-rodriguez/
# ------------------------------------------------------------------------------
#
# Notes:
#
# 1. Use a config file called 'config.json' with the next structure:
#
# {
#     "config": [
#         {
#             "name": "Name",
#             "description": "Description",
#             "location": "Location",
#             "url_token": "Url_token",
#             "file_name_data_saved": "Name_file"
#         }
#     ]
# }
# 
# This file can also be created with the attached make_config_file_json.py 
# module. In that module, edit it with the corresponding values.
# The url_token is for the Web Hook in Slack.
#
# ------------------------------------------------------------------------------
#                                    Imports
# ------------------------------------------------------------------------------

import schedule
import time
from slack_webhook import Slack
import requests
from datetime import datetime
import sys
import json

# ------------------------------------------------------------------------------
#                                    Class
# ------------------------------------------------------------------------------

class UsuarioSlackWebHook:
    def __init__(self, nombre, descripcion, ubicacion, url_token):
        self.nombre = nombre
        self.descripcion = descripcion
        self.ubicacion = ubicacion
        self.url_token = url_token
        self.slack = Slack(url=url_token)

class NotificadorSlackWebHook:
    def __init__(self, usuario):
        self.usuario = usuario
    def send_message(self, message):
        self.usuario.slack.post(text=message)
        
class LastSavedData:
    def __init__(self, name_file):
        self.__name_file = name_file
    def read(self):
        try:
            with open(self.__name_file, encoding="UTF-8") as file:
                data = file.readlines()
            return data
        except:
            # If the file does not exist, then it is created.
            with open(self.__name_file, 'w', encoding="UTF-8") as file:
                return list() #simula que no se leyo ningun dato en el archivo
    def write(self, data, current_time):
        with open(self.__name_file, 'w', encoding="UTF-8") as file:
                file.writelines(data)
                file.writelines("\n" + current_time)
    
# ------------------------------------------------------------------------------
#                                  Functions
# ------------------------------------------------------------------------------

def notifier_slack_webhook(user, message):
    user.slack.post(text=message) #send message to user


def see_public_ip():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #current time and date with format
    ip_publica = requests.get('http://checkip.amazonaws.com').text.strip() #get public ip address
    ip_guardadas = ip_saved.read() #get last ip public address saved
    message = f"{user_slack_wh.nombre} ::: {now} ::: public IP address: {ip_publica}"
    if len(ip_guardadas) == 0: #no records in file
        ip_saved.write(ip_publica,now) #save new ip public address with time-stamp
        notify.send_message(message)
    else:
        if ip_guardadas[0] != (ip_publica+"\n"):
            ip_saved.write(ip_publica,now) #save new ip public address with time-stamp
            notify.send_message(message)

def get_config():
    try:
        with open ("config.json") as file:
            data = json.load(file)
        return UsuarioSlackWebHook(data["config"][0]["name"],data["config"][0]["description"],data["config"][0]["location"],data["config"][0]["url_token"]), data["config"][0]["file_name_data_saved"]
    except:
        # Generate log 
        print("Error: no configuration file")
        sys.exit(1)

# ------------------------------------------------------------------------------
#                         Objects and global variables
# ------------------------------------------------------------------------------

user_slack_wh, file_data_save = get_config()

notify=NotificadorSlackWebHook(user_slack_wh)
ip_saved = LastSavedData(file_data_save)
        
flag_first_init = 1

schedule.every(12).hours.do(see_public_ip) # every 12 hours

# ------------------------------------------------------------------------------
#                                    main
# ------------------------------------------------------------------------------

while True:
    
    if flag_first_init:
        flag_first_init = 0
        see_public_ip()
        
    schedule.run_pending()
    time.sleep(1)
