import requests
import json
import time

from boltiot import Bolt
import conf

mybolt = Bolt(conf.api_key, conf.device_id)

def get_sensor_value(pin):
    try:
        response = mybolt.analogRead(pin)
        data = json.loads(response)
        
        if data["success"] != 1:
            print("Request not successfull")
            print("Response ->", data)
            return -999

        sensor_value = int(data["value"])
        return sensor_value

    except Exception as e:
        print("Something went wrong")
        print(e)
        return -999

def send_telegram_msg(message):
    url = "https://api.telegram.org/" + conf.telegram_bot_id + "/sendMessage"
    data = {
        "chat_id": conf.telegram_chat_id,
        "text": message
    }
    try:
        response = requests.request(
            "POST",
            url,
            params=data
        )
        telegram_data = json.loads(response.text)
        return telegram_data["ok"]
    except Exception as e:
        print("An error occurred in sending the alert message via Telegram")
        print(e)
        return False

while True:
    sensor_value = get_sensor_value("A0")
    print("Current sensor value is:", sensor_value)

    if sensor_value == -999:
        print("Request was unsuccessfull. Skipping.")
        time.sleep(10)
        continue

    if sensor_value >= conf.threshold:
        print("Sensor value has exceeded threshold")
        message = "Alert! Sensor value has exceeded " + str(conf.threshold) + ". The current value is " + str(sensor_value)
        telegram_status = send_telegram_msg(message)
        # print("This is the Telegram status:", telegram_status)

    time.sleep(10)