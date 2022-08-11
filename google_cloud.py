
import time
import urllib.request
import base64
import hmac
import os
os.system("clear")
os.system("pip install selenium")
os.system("apt install chromium-browser")
os.system("apt install chromium-driver")

coin = input("coin : ")
coin_d = coin
bey = 15
rate = input("rate : ")
stop_rate = 0
#170961
os.system("clear")

APIURL = "https://api-swap-rest.bingbon.pro"
APIKEY = "6aI6LP3LBoJ72FwdlXPNac1KgX7nOp6qQbPJ2AeTIZokfxOe"
SECRETKEY = "75XcRCFD97rK9whATGWbZDKkIPRAZFNZm7ZGsaNWMSxEe8HVvmPh250gUdgJgbgW"

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--disable-javascript")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')

prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
wd = webdriver.Chrome(options=chrome_options)
wd2 = webdriver.Chrome(options=chrome_options)
wd.get('https://www.binance.com/en/trade/'+coin.upper()+'_USDT?theme=dark&type=spot')
wd2.get('https://swap.bingx.com/en-us/'+coin.upper()+'-USDT')

price = 0

def genSignature(path, method, paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    paramsStr = method + path + paramsStr
    return hmac.new(SECRETKEY.encode("utf-8"), paramsStr.encode("utf-8"), digestmod="sha256").digest()

def post(url, body):
    req = urllib.request.Request(url, data=body.encode("utf-8"), headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req).read()

def getBalance():
    paramsMap = {
        "apiKey": APIKEY,
        "timestamp": int(time.time()*1000),
        "currency": "USDT",
    }
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    paramsStr += "&sign=" + urllib.parse.quote(base64.b64encode(genSignature("/api/v1/user/getBalance", "POST", paramsMap)))
    url = "%s/api/v1/user/getBalance" % APIURL
    return post(url, paramsStr)


def closePositions():
    placeOrder(symbol=coin_d.upper()+"-USDT", side="Ask",volume=amount , tradeType="Market", action="Close", price=0)
    placeOrder(symbol=coin_d.upper()+"-USDT", side="Bid",volume=amount , tradeType="Market", action="Close", price=0)
    return "close"

def placeOrder(symbol, side, price, volume, tradeType, action):
    paramsMap = {
        "symbol": symbol,
        "apiKey": APIKEY,
        "side": side,
        "entrustPrice": price,
        "entrustVolume": volume,
        "tradeType": tradeType,
        "action": action,
        "timestamp": int(time.time()*1000),
    }
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    paramsStr += "&sign=" + urllib.parse.quote(base64.b64encode(genSignature("/api/v1/user/trade", "POST", paramsMap)))
    url = "%s/api/v1/user/trade" % APIURL
    return post(url, paramsStr)


mode = 0
price = 0
time.sleep(5)

okx = float(wd.title.split()[0])
bingx = float(wd2.find_element(by=By.XPATH, value='/html/body/div/section/div[2]/div[1]/div/div[2]/div/div[1]/div[3]/div/div[2]/div/div').text)

print("start !!!",okx , bingx)


amount = 100*bey/bingx

#log = ""

while True:
    try:

        okx = float(wd.title.split()[0])
        bingx = float(wd2.find_element(by=By.XPATH, value='/html/body/div/section/div[2]/div[1]/div/div[2]/div/div[1]/div[3]/div/div[2]/div/div').text)

        if price != 0 and mode == 1 and okx >= bingx*(1-stop_rate/100):
            closePositions()
            mode = 0
            #log += "CLOSE "+str(bingx)+"@"
            amount = 100*bey/bingx

        if price != 0 and mode == 2 and okx <= bingx*(1+stop_rate/100):
            closePositions()
            mode = 0
            #log += "CLOSE "+str(bingx)+"@"
            amount = 100*bey/bingx

        if mode != 1 and okx < bingx*(1-rate/100):
            placeOrder(symbol=coin_d.upper()+"-USDT", side="Ask",volume=amount , tradeType="Market", action="Open", price=0)
            mode = 1
            price = bingx
            #log += "SELL "+str(bingx)+"@"

        if mode != 2 and okx > bingx*(1+rate/100):
            placeOrder(symbol=coin_d.upper()+"-USDT", side="Bid",volume=amount , tradeType="Market", action="Open", price=0)
            mode = 2
            price = bingx




    except:
        pass
