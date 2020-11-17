from tkinter import *
import requests 
import json

pycrypto=Tk()
pycrypto.title('My Crypto Portfolio')

def my_portfolio():
    api_request=requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=430d6f4e-cfe6-416f-8eef-802fc049bf2d')
    #to convert it into a parseable format
    api_json=json.loads(api_request.content)
    # print(api_json)
    print("----------------")
    #coins I already have
    coins = [
    {
        "symbol":"BTC",
        "amount_owned": 15,
        "price_per_coin": 180
    }, 
    {
        "symbol":"ETH",
        "amount_owned":25,
        "price_per_coin": 300
    },
    {
        "symbol":"ALGO",
        "amount_owned":5,
        "price_per_coin": 3000
    },
    {
        "symbol":"SOL",
        "amount_owned":95,
        "price_per_coin": 10
    }
    ]
    
    total_pl = 0 #total profit/loss
    coin_row=1 #row 0 is for headings
    
    for i in range(0, 300):
        for coin in coins:
            if api_json["data"][i]["symbol"] == coin["symbol"]:
                total_paid = coin["amount_owned"] * coin["price_per_coin"]
                current_value = coin["amount_owned"] * api_json["data"][i]["quote"]["USD"]["price"]
                pl_percoin = api_json["data"][i]["quote"]["USD"]["price"] - coin["price_per_coin"]
                total_pl_coin = pl_percoin * coin["amount_owned"]
            
                total_pl = total_pl + total_pl_coin

                # print(api_json["data"][i]["name"] + " - " + api_json["data"][i]["symbol"])
                # print("Price - ${0:.2f}".format(api_json["data"][i]["quote"]["USD"]["price"]))
                # print("Number Of Coin:", coin["amount_owned"])
                # print("Total Amount Paid:", "${0:.2f}".format(total_paid))
                # print("Current Value:", "${0:.2f}".format(current_value))
                # print("P/L Per Coin:", "${0:.2f}".format(pl_percoin))
                # print("Total P/L With Coin:", "${0:.2f}".format(total_pl_coin))
                # print("----------------")
                
                #label data
                name=Label(pycrypto,text=api_json["data"][i]["symbol"],bg='grey',fg='black')
                name.grid(row=coin_row,column=0,sticky=N)

                price=Label(pycrypto,text=api_json["data"][i]["quote"]["USD"]["price"],bg='white',fg='black')
                price.grid(row=coin_row,column=1,sticky=N)

                coin_no=Label(pycrypto,text=coin["amount_owned"],bg='grey',fg='black')
                coin_no.grid(row=coin_row,column=2,sticky=N)

                amount_paid=Label(pycrypto,text="${0:.2f}".format(total_paid),bg='white',fg='black')
                amount_paid.grid(row=coin_row,column=3,sticky=N)

                current_val=Label(pycrypto,text="${0:.2f}".format(current_value),bg='grey',fg='black')
                current_val.grid(row=coin_row,column=4,sticky=N)

                pl_coin=Label(pycrypto,text="${0:.2f}".format(pl_percoin),bg='white',fg='black')
                pl_coin.grid(row=coin_row,column=5,sticky=N)

                #ltotal_pl 'l' prefix is added as there is another float variable ltotal that is required for calculations
                ltotal_pl=Label(pycrypto,text="${0:.2f}".format(total_pl_coin),bg='grey',fg='black')
                ltotal_pl.grid(row=coin_row,column=6,sticky=N)
                
                coin_row += 1
                
    # print("Total P/L For Portfolio:", "${0:.2f}".format(total_pl))


#Label headings
name=Label(pycrypto,text='Coin Name',bg='grey',fg='black')
name.grid(row=0,column=0,sticky=N)

price=Label(pycrypto,text='Price',bg='white',fg='black')
price.grid(row=0,column=1,sticky=N)

coin_no=Label(pycrypto,text='Coins Owned',bg='grey',fg='black')
coin_no.grid(row=0,column=2,sticky=N)

amount_paid=Label(pycrypto,text='Total Amount Paid',bg='white',fg='black')
amount_paid.grid(row=0,column=3,sticky=N)

current_vals=Label(pycrypto,text='Current Value',bg='grey',fg='black')
current_vals.grid(row=0,column=4,sticky=N)

pl_coin=Label(pycrypto,text='Profit/Loss per coin',bg='white',fg='black')
pl_coin.grid(row=0,column=5,sticky=N)

total_pl=Label(pycrypto,text='Total Profit/Loss with Coin',bg='grey',fg='black')
total_pl.grid(row=0,column=6,sticky=N)

my_portfolio()
pycrypto.mainloop()
