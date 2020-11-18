from tkinter import *
from tkinter import messagebox
import requests 
import json
import sqlite3

con=sqlite3.connect('coins.db')
curr=con.cursor()
curr.execute("CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY,symbol TEXT, amount INTEGER,price REAL)")
con.commit()

#Once executed, should be commented to prevent insertions again(of course there will be integrity error refering to the primary key)
# curr.execute("INSERT INTO coin VALUES(1,'BTC',15,180)")
# con.commit()
# curr.execute("INSERT INTO coin VALUES(2,'ETH',5,18)")
# con.commit()
# curr.execute("INSERT INTO coin VALUES(3,'NEO',150,1300)")
# con.commit()
# curr.execute("INSERT INTO coin VALUES(4,'XMR',3,30)")
# con.commit()


pycrypto=Tk()
pycrypto.title('My Crypto Portfolio')
pycrypto.iconbitmap('bitcoin.ico')

    
def refresh():
    for cell in pycrypto.winfo_children():
        cell.destroy()
        
    my_portfolio()
    app_headers()
    app_nav()
    
def app_nav():
    def clear_all():
        curr.execute('DELETE FROM coin')
        con.commit()
        messagebox.showinfo('My Portfolio','All values have been deleted successfully')
        refresh()
    def close():
        pycrypto.destroy()
        
    menu=Menu(pycrypto)
    file=Menu(menu)
    file.add_command(label='Clear All',command=clear_all)
    file.add_command(label='Close',command=close)
    menu.add_cascade(label='File',menu=file)
    pycrypto.config(menu=menu)
    
def my_portfolio():
    api_request=requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=430d6f4e-cfe6-416f-8eef-802fc049bf2d')
    #to convert it into a parseable format
    api_json=json.loads(api_request.content)
    # print(api_json)
    
    curr.execute('SELECT * FROM coin')
    coins=curr.fetchall()
    # print(coins)
    
    def font_color(amount):
        if amount>0:
            return "green"
        else:
            return "red"
    
    def insert_coin():
        curr.execute('INSERT INTO coin(symbol,amount,price) VALUES (?,?,?)',(symbol_txt.get(),amount_txt.get(),price_txt.get()))
        con.commit()
        messagebox.showinfo('My Portfolio','Coin added succesfully')
        refresh()
        
    def update_coin():
        curr.execute('UPDATE coin SET symbol=?, price=?, amount=? WHERE id=?',(symbol_update.get(),price_update.get(),amount_update.get(),id_update.get()))
        con.commit()
        messagebox.showinfo('My Portfolio','Coin updated succesfully')
        refresh()
    
    def delete_coin():
        curr.execute('DELETE FROM coin where id=?',(id_delete.get(),))
        con.commit()  
        messagebox.showinfo('My Portfolio','Coin deleted succesfully')
        refresh()
        
    #coins I already have
    # coins = [
    # {
    #     "symbol":"BTC",
    #     "amount_owned": 15,
    #     "price_per_coin": 180
    # }, 
    # {
    #     "symbol":"ETH",
    #     "amount_owned":25,
    #     "price_per_coin": 300
    # },
    # {
    #     "symbol":"ALGO",
    #     "amount_owned":5,
    #     "price_per_coin": 3000
    # },
    # {
    #     "symbol":"SOL",
    #     "amount_owned":95,
    #     "price_per_coin": 10
    # }
    # ]
    
    total_pl = 0 #total profit/loss
    coin_row=1 #row 0 is for headings
    total_current_value=0
    total_paid_amount=0
    
    for i in range(0, 300):
        for coin in coins:
            if api_json["data"][i]["symbol"] == coin[1]:
                total_paid = coin[2] * coin[3]
                current_value = coin[2] * api_json["data"][i]["quote"]["USD"]["price"]
                pl_percoin = api_json["data"][i]["quote"]["USD"]["price"] - coin[3]
                total_pl_coin = pl_percoin * coin[2]
            
                total_pl += total_pl_coin
                total_current_value += current_value
                total_paid_amount += total_paid

                # print(api_json["data"][i]["name"] + " - " + api_json["data"][i]["symbol"])
                # print("Price - ${0:.2f}".format(api_json["data"][i]["quote"]["USD"]["price"]))
                # print("Number Of Coin:", coin["amount_owned"])
                # print("Total Amount Paid:", "${0:.2f}".format(total_paid))
                # print("Current Value:", "${0:.2f}".format(current_value))
                # print("P/L Per Coin:", "${0:.2f}".format(pl_percoin))
                # print("Total P/L With Coin:", "${0:.2f}".format(total_pl_coin))

                
                #label data
                id=Label(pycrypto,text=coin[0],bg='#F3F4F6',fg='black',font='Lato 12',padx='2',pady='2',borderwidth='1',relief='groove')
                id.grid(row=coin_row,column=0,sticky=N+S+E+W)
                
                name=Label(pycrypto,text=api_json["data"][i]["symbol"],bg='#F3F4F6',fg='black',font='Lato 12',padx='2',pady='2',borderwidth='1',relief='groove')
                name.grid(row=coin_row,column=1,sticky=N+S+E+W)

                price=Label(pycrypto,text=api_json["data"][i]["quote"]["USD"]["price"],bg='white',fg='black',font='Lato 12',padx='2',pady='2',borderwidth='1',relief='groove')
                price.grid(row=coin_row,column=2,sticky=N+S+E+W)

                coin_no=Label(pycrypto,text=coin[2],bg='#F3F4F6',fg='black',font='Lato 12',padx='2',pady='2',borderwidth='1',relief='groove')
                coin_no.grid(row=coin_row,column=3,sticky=N+S+E+W)

                amount_paid=Label(pycrypto,text="${0:.2f}".format(total_paid),bg='white',fg='black',font='Lato 12',padx='2',pady='2',borderwidth='1',relief='groove')
                amount_paid.grid(row=coin_row,column=4,sticky=N+S+E+W)

                current_val=Label(pycrypto,text="${0:.2f}".format(current_value),bg='#F3F4F6',fg=font_color(float(current_value)),font='Lato 12',padx='2',pady='2',borderwidth='1',relief='groove')
                current_val.grid(row=coin_row,column=5,sticky=N+S+E+W)

                pl_coin=Label(pycrypto,text="${0:.2f}".format(pl_percoin),bg='white',fg=font_color(float(pl_percoin)),font='Lato 12',padx='2',pady='2',borderwidth='1',relief='groove')
                pl_coin.grid(row=coin_row,column=6,sticky=N+S+E+W)

                #ltotal_pl 'l' prefix is added as there is another float variable ltotal that is required for calculations
                ltotal_pl=Label(pycrypto,text="${0:.2f}".format(total_pl_coin),bg='#F3F4F6',fg=font_color(float(total_pl_coin)),font='Lato 12',padx='2',pady='2',borderwidth='1',relief='groove')
                ltotal_pl.grid(row=coin_row,column=7,sticky=N+S+E+W)
                
                coin_row += 1
                
    #inserting values
    symbol_txt=Entry(pycrypto,borderwidth=4,relief='groove')
    symbol_txt.grid(row=coin_row+1,column=1)
    
    amount_txt=Entry(pycrypto,borderwidth=4,relief='groove')
    amount_txt.grid(row=coin_row+1,column=2)
    
    price_txt=Entry(pycrypto,borderwidth=4,relief='groove')
    price_txt.grid(row=coin_row+1,column=3)
    
    add_coin=Button(pycrypto,text='Add + ',bg='#142E54',fg='white',command=insert_coin,font='Lato 12',padx='2',pady='2',borderwidth='2',relief='groove')
    add_coin.grid(row=coin_row+1,column=4,sticky=N+S+E+W)
    
    #update values
    id_update=Entry(pycrypto,borderwidth=4,relief='groove')
    id_update.grid(row=coin_row+2,column=0)
    
    symbol_update=Entry(pycrypto,borderwidth=4,relief='groove')
    symbol_update.grid(row=coin_row+2,column=1)
    
    amount_update=Entry(pycrypto,borderwidth=4,relief='groove')
    amount_update.grid(row=coin_row+2,column=2)
    
    price_update=Entry(pycrypto,borderwidth=4,relief='groove')
    price_update.grid(row=coin_row+2,column=3)
    
    update_coin_txt=Button(pycrypto,text='Update',bg='#142E54',fg='white',command=update_coin,font='Lato 12',padx='2',pady='2',borderwidth='2',relief='groove')
    update_coin_txt.grid(row=coin_row+2,column=4,sticky=N+S+E+W)
    
    #delete
    id_delete=Entry(pycrypto,borderwidth=4,relief='groove')
    id_delete.grid(row=coin_row+3,column=0)
    
    delete_coin_txt=Button(pycrypto,text='Delete',bg='#142E54',fg='white',command=delete_coin,font='Lato 12',padx='2',pady='2',borderwidth='2',relief='groove')
    delete_coin_txt.grid(row=coin_row+3,column=4,sticky=N+S+E+W)
    
                
    # print("Total P/L For Portfolio:", "${0:.2f}".format(total_pl))
    #coin row already incremented so total profit loss will be printed in 5th row only,cheers!
    
    total_pa=Label(pycrypto,text="${0:.2f}".format(total_paid_amount),bg='white',fg='black',font='Lato 12',padx='2',pady='2',borderwidth='1',relief='groove')
    total_pa.grid(row=coin_row,column=4,sticky=N+S+E+W)
    
    total_pl=Label(pycrypto,text="${0:.2f}".format(total_pl),bg='white',fg=font_color(float(total_pl)),font='Lato 12',padx='2',pady='2',borderwidth='1',relief='groove')
    total_pl.grid(row=coin_row,column=7,sticky=N+S+E+W)
    
    total_curr_val=Label(pycrypto,text="${0:.2f}".format(total_current_value),bg='white',fg=font_color(float(total_current_value)),font='Lato 12',padx='2',pady='2',borderwidth='1',relief='groove')
    total_curr_val.grid(row=coin_row,column=5,sticky=N+S+E+W)
    
    api_json='' #clearing the data before refreshing
    
    refresh_btn=Button(pycrypto,text='Refresh',bg='#142E54',fg='white',command=refresh,font='Lato 12',padx='2',pady='2',borderwidth='2',relief='groove')
    refresh_btn.grid(row=coin_row+1,column=7,sticky=N+S+E+W)

def app_headers():
    #Label headings
    id=Label(pycrypto,text='Portfolio ID',bg='#142E54',fg='white',font='Lato 12 bold',padx='5',pady='5',borderwidth='2',relief='groove')
    id.grid(row=0,column=0,sticky=N+S+E+W)
    
    name=Label(pycrypto,text='Coin Name',bg='#142E54',fg='white',font='Lato 12 bold',padx='5',pady='5',borderwidth='2',relief='groove')
    name.grid(row=0,column=1,sticky=N+S+E+W)

    price=Label(pycrypto,text='Price',bg='#142E54',fg='white',font='Lato 12 bold',padx='5',pady='5',borderwidth='2',relief='groove')
    price.grid(row=0,column=2,sticky=N+S+E+W)

    coin_no=Label(pycrypto,text='Coins Owned',bg='#142E54',fg='white',font='Lato 12 bold',padx='5',pady='5',borderwidth='2',relief='groove')
    coin_no.grid(row=0,column=3,sticky=N+S+E+W)

    amount_paid=Label(pycrypto,text='Total Amount Paid',bg='#142E54',fg='white',font='Lato 12 bold',padx='5',pady='5',borderwidth='2',relief='groove')
    amount_paid.grid(row=0,column=4,sticky=N+S+E+W)

    current_vals=Label(pycrypto,text='Current Value',bg='#142E54',fg='white',font='Lato 12 bold',padx='5',pady='5',borderwidth='2',relief='groove')
    current_vals.grid(row=0,column=5,sticky=N+S+E+W)

    pl_coin=Label(pycrypto,text='Profit/Loss per coin',bg='#142E54',fg='white',font='Lato 12 bold',padx='5',pady='5',borderwidth='2',relief='groove')
    pl_coin.grid(row=0,column=6,sticky=N+S+E+W)

    total_pl=Label(pycrypto,text='Total Profit/Loss with Coin',bg='#142E54',fg='white',font='Lato 12 bold',padx='5',pady='5',borderwidth='2',relief='groove')
    total_pl.grid(row=0,column=7,sticky=N+S+E+W)

app_nav()
app_headers()
my_portfolio()
pycrypto.mainloop()

curr.close()
con.close()
