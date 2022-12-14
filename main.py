import requests
from bs4 import BeautifulSoup
import lxml
import smtplib

MY_TARGET_PRICE = 100.01
MY_EMAIL = "xxxxxxx@gmail.com"
MY_PASSWORD = "xxxxxxx"

#------------------------------------------GET PRODUCT DETAILS FROM AMAZON----------------------------------#
URL = "https://www.amazon.com/Samsung-Galaxy-Wireless-Earbuds-Cancelling/dp/B08FSL1W9Z/ref=sr_1_8?crid=286KFDQ0W20RB&keywords=samsung+earpods+android+wireless&qid=1643637608&sprefix=samsung+earpo%2Caps%2C709&sr=8-8"
header = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47"
}
response = requests.get(url=URL, headers=header)
# print(response.text)

#---------------------------------------PARSE PRODUCT TITLE AND PRICE------------------------------------------#
soup = BeautifulSoup(response.text, "lxml")

# Getting Title
title = soup.find(id="productTitle").get_text().strip()
print(title)

# Getting Price
price = soup.find(id="price_inside_buybox").getText()
price_without_dollar = price.split("$")[1]
price_in_float = float(price_without_dollar)
print(f"Price: {price_in_float}")

#-----------------------------------PRICE CONDITION AND EMAIL---------------------------------------------#
if price_in_float < MY_TARGET_PRICE:
    print("Current price is less than the target price")
    current_price = price_in_float
    message = f"{title}\n Current Price: {current_price} \n You can buy via: {URL}"

    connection = smtplib.SMTP("smtp.gmail.com", port=587)
    connection.starttls()
    connection.login(user=MY_EMAIL, password=MY_PASSWORD)
    connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL, msg=f"Subject: Amazon Price Alert!\n\n{message}")
    connection.close()
