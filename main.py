import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 41.693630
MY_LONG = 44.801620
my_email = "sina_eshrati@yahoo.com"
my_password = "euolagjhjfqaiddm"

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now().hour

while True:
    time.sleep(60)
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        if time_now > sunset or time_now < sunrise:
            with smtplib.SMTP_SSL("smtp.mail.yahoo.com") as connection:
                connection.login(my_email, my_password)
                connection.sendmail(from_addr=my_email,
                                    to_addrs=my_email,
                                    msg="Subject:ISS Notifier\n\nLook up!!!")
