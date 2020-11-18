from tkinter import *
import requests 
import json

pycrypto=Tk()
pycrypto.title('My Crypto Portfolio')
pycrypto.iconbitmap('bitcoin.ico')


def font_color(amount):
    if amount>0:
        return "green"
    else:
        return "red"
    
def my_portfolio():
    api_request=requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=430d6f4e-cfe6-416f-8eef-802fc049bf2d')
    #to convert it into a parseable format
    api_json=json.loads(api_request.content)
    # print(api_json)
   
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
    total_current_value=0
    
    for i in range(0, 300):
        for coin in coins:
            if api_json["data"][i]["symbol"] == coin["symbol"]:
                total_paid = coin["amount_owned"] * coin["price_per_coin"]
                current_value = coin["amount_owned"] * api_json["data"][i]["quote"]["USD"]["price"]
                pl_percoin = api_json["data"][i]["quote"]["USD"]["price"] - coin["price_per_coin"]
                total_pl_coin = pl_percoin * coin["amount_owned"]
            
                total_pl += total_pl_coin
                total_current_value += current_value

                # print(api_json["data"][i]["name"] + " - " + api_json["data"][i]["symbol"])
                # print("Price - ${0:.2f}".format(api_json["data"][i]["quote"]["USD"]["price"]))
                # print("Number Of Coin:", coin["amount_owned"])
                # print("Total Amount Paid:", "${0:.2f}".format(total_paid))
                # print("Current Value:", "${0:.2f}".format(current_value))
                # print("P/L Per Coin:", "${0:.2f}".format(pl_percoin))
                # print("Total P/L With Coin:", "${0:.2f}".format(total_pl_coin))

                
                #label data
                name=Label(pycrypto,text=api_json["data"][i]["symbol"],bg='#F3F4F6',fg='black',font='Lato 12',padx='2',pady='2',borderwidth='1',relief='groove')
                name.grid(row=coin_row,column=0,sticky=N+S+E+W)

                price=Label(pycrypto,text=api_json["data"][i]["quote"]["USD"]["price"],bg='white',fg='black',font='Lato 12',padx='2',pady='2',borderwidth='1',relief='groove')
                price.grid(row=coin_row,column=1,sticky=N+S+E+W)

                coin_no=Label(pycrypto,text=coin["amount_owned"],bg='#F3F4F6',fg='black',font='Lato 12',padx='2',pady='2',borderwidth='1',relief='groove')
                coin_no.grid(row=coin_row,column=2,sticky=N+S+E+W)

                amount_paid=Label(pycrypto,text="${0:.2f}".format(total_paid),bg='white',fg='black',font='Lato 12',padx='2',pady='2',borderwidth='1',relief='groove')
                amount_paid.grid(row=coin_row,column=3,sticky=N+S+E+W)

                current_val=Label(pycrypto,text="${0:.2f}".format(current_value),bg='#F3F4F6',fg=font_color(float(current_value)),font='Lato 12',padx='2',pady='2',borderwidth='1',relief='groove')
                current_val.grid(row=coin_row,column=4,sticky=N+S+E+W)

                pl_coin=Label(pycrypto,text="${0:.2f}".format(pl_percoin),bg='white',fg=font_color(float(pl_percoin)),font='Lato 12',padx='2',pady='2',borderwidth='1',relief='groove')
                pl_coin.grid(row=coin_row,column=5,sticky=N+S+E+W)

                #ltotal_pl 'l' prefix is added as there is another float variable ltotal that is required for calculations
                ltotal_pl=Label(pycrypto,text="${0:.2f}".format(total_pl_coin),bg='#F3F4F6',fg=font_color(float(total_pl_coin)),font='Lato 12',padx='2',pady='2',borderwidth='1',relief='groove')
                ltotal_pl.grid(row=coin_row,column=6,sticky=N+S+E+W)
                
                coin_row += 1
                
    # print("Total P/L For Portfolio:", "${0:.2f}".format(total_pl))
    #coin row already incremented so total profit loss will be printed in 5th row only,cheers!
    total_pl=Label(pycrypto,text="${0:.2f}".format(total_pl),bg='white',fg=font_color(float(total_pl)),font='Lato 12',padx='2',pady='2',borderwidth='1',relief='groove')
    total_pl.grid(row=coin_row,column=6,sticky=N+S+E+W)
    
    total_curr_val=Label(pycrypto,text="${0:.2f}".format(total_current_value),bg='white',fg=font_color(float(total_current_value)),font='Lato 12',padx='2',pady='2',borderwidth='1',relief='groove')
    total_curr_val.grid(row=coin_row,column=4,sticky=N+S+E+W)
    
    api_json='' #clearing the data before refreshing
    update=Button(pycrypto,text='Update',bg='#142E54',fg='white',command=my_portfolio,font='Lato 12',padx='2',pady='2',borderwidth='2',relief='groove')
    update.grid(row=coin_row+1,column=6,sticky=N+S+E+W)


#Label headings
name=Label(pycrypto,text='Coin Name',bg='#142E54',fg='white',font='Lato 15 bold',padx='5',pady='5',borderwidth='2',relief='groove')
name.grid(row=0,column=0,sticky=N+S+E+W)

price=Label(pycrypto,text='Price',bg='#142E54',fg='white',font='Lato 15 bold',padx='5',pady='5',borderwidth='2',relief='groove')
price.grid(row=0,column=1,sticky=N+S+E+W)

coin_no=Label(pycrypto,text='Coins Owned',bg='#142E54',fg='white',font='Lato 15 bold',padx='5',pady='5',borderwidth='2',relief='groove')
coin_no.grid(row=0,column=2,sticky=N+S+E+W)

amount_paid=Label(pycrypto,text='Total Amount Paid',bg='#142E54',fg='white',font='Lato 15 bold',padx='5',pady='5',borderwidth='2',relief='groove')
amount_paid.grid(row=0,column=3,sticky=N+S+E+W)

current_vals=Label(pycrypto,text='Current Value',bg='#142E54',fg='white',font='Lato 15 bold',padx='5',pady='5',borderwidth='2',relief='groove')
current_vals.grid(row=0,column=4,sticky=N+S+E+W)

pl_coin=Label(pycrypto,text='Profit/Loss per coin',bg='#142E54',fg='white',font='Lato 15 bold',padx='5',pady='5',borderwidth='2',relief='groove')
pl_coin.grid(row=0,column=5,sticky=N+S+E+W)

total_pl=Label(pycrypto,text='Total Profit/Loss with Coin',bg='#142E54',fg='white',font='Lato 15 bold',padx='5',pady='5',borderwidth='2',relief='groove')
total_pl.grid(row=0,column=6,sticky=N+S+E+W)

my_portfolio()
pycrypto.mainloop()