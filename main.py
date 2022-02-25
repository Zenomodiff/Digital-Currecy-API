import requests, json
from  flask import Flask, jsonify
from bs4 import BeautifulSoup as bs
from config import PORT

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home_page():
    url = "https://gadgets.ndtv.com/cryptocurrency#pfrom=home-gadgets_header-globalnav"  
    coin_List = []

    def home_price():

        response = requests.get(url)
        soup = bs(response.text,"lxml")
        anchor1= soup.find_all('div',"_flx crynm") 
        anchor2 = soup.find_all('td',"_rft _tdpr") 
        anchor3 = soup.find_all('div',"_sortval")
        anchor4 = soup.find_all('span',"_chper")

        for i,(Coin_Coin,Price,Change_Top,Change_Bottom) in enumerate(zip(anchor1,anchor2,anchor3,anchor4)):
            Coin = Coin_Coin.text.strip()
            price = Price.text.strip()
            Top = Change_Top.text.strip()
            Bottom = Change_Bottom.text.strip()

            coin = {
                'Coin_Name': Coin,
                'Price_Range': price,
                'Top_Value' : Top,
                'Bottom_Value' : Bottom
            }

            coin_List.append(coin)
            New_List = json.dumps(coin_List, indent =2)

        with open("data.json", "w", encoding="utf-8") as file:
            file.write(str(New_List))

    home_price()
    return jsonify(coin_List)

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port= PORT)
    