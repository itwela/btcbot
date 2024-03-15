import datetime
import os
import time
import requests
from lxml import html
import urllib
import re
import json
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup

# Classes--------------------------------------------------------------------
class Utilities:
    def __init__(self):
        pass
  
    def saveToFile(data):    
    # Save the extracted content to a file
        with open('extracted_content.txt', 'w') as file:
            file.write(data)

# --- Bitcoin Data Classes --- Starts Here ----
class AltcoinSeasonIndex:

    def __init__(self):
        pass


    def getAltcoinSeasonIndex(self):
                # URL of the page you want to fetch
            url = "https://www.blockchaincenter.net/en/altcoin-season-index/"

            # Make an HTTP GET request to fetch the page content
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the HTML content
                tree = html.fromstring(response.content)

                # Find the element using XPath
                element = tree.xpath('//*[@id="season"]/div/div/div[2]/div[1]')

                # If the element is found, extract its text
                if element:
                    value = element[0].text_content().strip()
                    print("Altcoin Season Index Value is:", value)
                else:
                    print("Element not found")
            else:
                print("Failed to fetch page:", response.status_code)

class RainbowIndexBtc:
    def __init__(self):
        pass
    
    def parseRows(self, data, xpaths, var, start, end, name):
        # Find all script tags

        for path in xpaths:
            if path.text is not None:
                if var in path.text:
                    label_index = path.text.find(start)
                    theEnd = path.text.find(end, label_index)

                    if label_index != -1:
                        extracted_content = path.text[label_index:theEnd]
                        data_list = [float(x.strip().replace('"', '')) for x in extracted_content.split(',')]
                        # Now data_list contains the individual numbers as floats
                        print(data_list[6])

                        # Save the extracted content to a file
                        # with open(name, 'w') as file:
                        #     file.write(extracted_content)

    
    def getRanbowIndexBtc(self):
        # URL of the page you want to fetch
        url = "https://www.blockchaincenter.net/en/bitcoin-rainbow-chart/"

        rainbowDict = {}
        # Make an HTTP GET request to fetch the page content
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
                # Parse the HTML content
            theHtml = html.fromstring(response.content)
                     # Find all script tags
            scripts = theHtml.xpath('//script')

             # Define a function to parse rows and add data to the rainbowDict dictionary
            def parse_and_add(start, end, key, label):
                extracted_content = extract_content(theHtml, scripts, start, end)
                if extracted_content:
                    data_list = parse_and_clean(extracted_content)
                    rainbowDict[key] = {'label': label, 'data': data_list}
            
            def extract_content(theHtml, scripts, start, end):
                for script in scripts:
                    text = script.text_content()
                    if start in text:
                        start_index = text.find(start)
                        end_index = text.find(end, start_index)
                        return text[start_index:end_index]

            # Define function to parse and clean the extracted content
            def parse_and_clean(content):
                content = content.strip()
                if content.startswith('[') and content.endswith(']'):
                    content = content[1:-1]
                content = content.replace("'", "")
                cleaned_data = []
                for x in content.split(','):
                    x = x.strip().replace('"', '')
                    try:
                        cleaned_data.append(float(x))
                    except ValueError:
                        cleaned_data.append(x)  # If it's not a float, keep it as is
                return cleaned_data
            # Parse and add each type of data
            parse_and_add('"2010-09-22"', ']', 'bitcoin_days', 'Bitcoin Days')
            parse_and_add('"1.04"', ']', 'bitcoin_prices', 'Bitcoin Prices')
            parse_and_add('4.7365947404693545,', ']', 'max_bubble_territory', 'Max Bubble Territory')
            parse_and_add('2.8985308366049125,', ']', 'sell_seriously', 'Sell. Seriously')
            parse_and_add('1.7835155338503275,', ']', 'fomo', 'FOMO')
            parse_and_add('1.109834714957462,', ']', 'is_this_a_bubble', 'Is This a Bubble?')
            parse_and_add('0.7017275375974457,', ']', 'hodl', 'HODL')
            parse_and_add('0.42493612885605564,', ']', 'still_cheap', 'Still Cheap')
            parse_and_add('0.2629051670964854,', ']', 'accumulate', 'Accumulate')
            parse_and_add('0.16270771772966758,0', ']', 'buy', 'BUY!')
            parse_and_add('0.09598237882282783', ']', 'basically_a_fire_sale', 'Basically a Fire Sale')
            parse_and_add('0.05899063894601712,0 ', ']', 'below_firesale', 'Below Firesale')
        
            def getTodaysData():
    
                todayDate = datetime.today().strftime('%Y-%m-%d')
                positions = []

                for key, value in rainbowDict.items():
                    data = value['data']
                    
                    if todayDate in data:  # Check if the date exists in the data
                        position_in_data = data.index(todayDate)  # Find the position of the date in the data                
                    
                for key, value in rainbowDict.items():
                    data = value['data']  # Access the data associated with the current key
                    # print('Data:', key+ ":", data[position_in_data])
                    
                    # Check if key is 'bitcoin_prices' for Bitcoin price extraction
                    if key == 'bitcoin_prices':
                        price = data[position_in_data]
                        category = None
                        
                        # Determine the category
                        if price > rainbowDict["max_bubble_territory"]['data'][position_in_data]:
                            category = "were past max_bubble_territory - (Past top Red Line)"
                        elif price > rainbowDict["sell_seriously"]['data'][position_in_data]:
                            category = "max_bubble_territory, (Inside top Red Line)"
                        elif price > rainbowDict["fomo"]['data'][position_in_data]:
                            category = "sell_seriously, (Inside top Dark Orange Line)"
                        elif price > rainbowDict["is_this_a_bubble"]['data'][position_in_data]:
                            category = "fomo, (Inside Light Orange Line)"
                        elif price > rainbowDict["hodl"]['data'][position_in_data]:
                            category = "is_this_a_bubble, (Inside Dark Yellow Line)"
                        elif price > rainbowDict["still_cheap"]['data'][position_in_data]:
                            category = "hodl (Inside Light Yellow Line)"
                        elif price > rainbowDict["accumulate"]['data'][position_in_data]:
                            category = "still_cheap, (Inside Light Green Line)"
                        elif price > rainbowDict["buy"]['data'][position_in_data]:
                            category = "accumulate (Inside Dark Green Line)"
                        elif price > rainbowDict["basically_a_fire_sale"]['data'][position_in_data]:
                            category = "buy, (Inside Light Blue Line)"
                        else:
                            category = "basically_a_fire_sale, (Inside Dark Blue Line)"

                        # Print Bitcoin price, date, and category
                        print("Bitcoin Price: $", price)
                        print("Date: ", todayDate)
                        print("Raibow Chart Says: ", category)

            getTodaysData()

        return rainbowDict

# ----  Bitcoin Data Classes --- End ----

# ---- Defi CoinRanking Data Classes --- Starts Here ----
class CoinRankingData:
    def __init__(self):
        pass
    def coinRanking_getRecentCoins(self):
        # get all coins listed on CoinGecko
        Akey = os.environ['CoinRanking']
        headers = {
            'Content-Type': 'application/json',
            'x-access-token':  Akey,
        }
        solcoins = requests.get('https://coinranking.com/api/v2/coins?tags[]=layer-1&limit=50&orderBy=listedAt&orderDirection=desc&timePeriod=24h&referenceCurrencyUuid=yhjMzLPhuIDl', headers=headers).json()
        # Define a dictionary to store the extracted data
        solcoins_dict = {
            'data': {
                'coins': solcoins.get('data', {}).get('coins', [])
            }
        }

            
        # Access the list of coins
        coins = solcoins_dict['data']['coins']
        for i in range(len(coins)):
            if coins[i]['tier'] < 3:
                coin_1 = coins[i]
                print (
                    "Symbol:", coin_1['symbol'], "\n",
                    'Change:', coin_1['change'], "\n",
                    'Listed At:', coin_1['listedAt'], "\n",
                    "Name:", coin_1['name'], "\n",
                    'Price:', coin_1['price'], "\n",
                    'Market Cap:', coin_1['marketCap'], "\n",
                    'Contract Address:', coin_1['contractAddresses'], "\n",
                    'Tier:', coin_1['tier'], "\n",
                    'Url:', coin_1['coinrankingUrl'], "\n",
                    '24h Volume:', coin_1['24hVolume'], "\n",
                )

# ---- Defi CoinRanking Data Classes --- End ----

# ----  CoinMaretCap Data Classes --- Starts Here ----            
class CoinMarketCapData:
        
        def __init__(self):
            pass
    
        def getRecentCMCCoins(self, quantity=1):
            # URL of the page you want to fetch
            url = "https://coinmarketcap.com/new/"

            # Make an HTTP GET request to fetch the page content
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the HTML content
                tree = html.fromstring(response.content)

                # Find the rows using XPath
                rows = tree.xpath('//*[@id="__next"]/div[2]/div[1]/div[2]/div/div[2]/table/tbody/tr')

                count = 0
                print(f"Getting {quantity} of the most recent coins on CoinMarketCap...", '\n'*2)
                for i in range(len(rows)):
                    stop = quantity
                    if count != stop:
                        td1 = rows[i].cssselect('td')[1].text_content()
                        td2 = rows[i].cssselect('td')[2].text_content()
                        td3 = rows[i].cssselect('td')[3].text_content()
                        td4 = rows[i].cssselect('td')[4].text_content()
                        td5 = rows[i].cssselect('td')[5].text_content()
                        td6 = rows[i].cssselect('td')[6].text_content()
                        td7 = rows[i].cssselect('td')[7].text_content()
                        td8 = rows[i].cssselect('td')[8].text_content()
                        td9 = rows[i].cssselect('td')[9].text_content()
                        
                        # Use regex to extract the name
                        name_match = re.match(r'^([^0-9]*)', td2)
                        name = name_match.group(1).strip() if name_match else td2.strip()
                        # Extract the symbol by splitting at the first number
                        symbol_parts = re.split(r'[0-9]', td2, 1)
                        symbol = symbol_parts[1].strip() if len(symbol_parts) > 1 else ""

                        url = f'https://coinmarketcap.com/currencies/{symbol}/'
                                    # Make an HTTP GET request to fetch the page content
                        response = requests.get(url)

                        # Check if the request was successful (status code 200)
                        if response.status_code == 200:
                            # Parse the HTML content
                            page = html.fromstring(response.content)

                            cols = page.cssselect('#__next > div.sc-637f0039-1.hnHyvc.global-layout-v2 > div > div.cmc-body-wrapper > div > div > div.sc-aef7b723-0.sc-a6bd470-0.gavgYW.coin-stats > div.sc-f70bb44c-0.eyKDkF > section:nth-child(2) > div')   
                            
                            try: 
                                totalSupply = cols[0].cssselect('#section-coin-stats > div > dl > div:nth-child(5) > div > dd')[0].text_content()
                            except: 
                                totalSupply = 'N/A'
                            try:
                                maxSupply = cols[0].cssselect('#section-coin-stats > div > dl > div:nth-child(6) > div > dd')[0].text_content()
                            except:
                                maxSupply = 'N/A'
                            # Extract href from anchor tag
                            try:
                                contact_href = cols[0].cssselect('a.chain-name')[0].get('href') if cols[0].cssselect('a.chain-name') else 'N/A'
                            except:
                                contact_href = 'N/A'
                        
                            print(
                                'Number:', td1, '\n',
                                'Name:', name, '\n',
                                'Symbol:', symbol, '\n',
                                'Price:', td3, '\n',
                                '1hr % Change:', td4, '\n',
                                '24hr % Change:', td5, '\n',
                                'Full Dill Market Cap:', td6, '\n',
                                'Volume:', td7, '\n',
                                "Total Supply:", totalSupply, '\n',
                                "Max Supply:", maxSupply, '\n',
                                'BlockChain:', td8, '\n',
                                'Contact Information:', contact_href, '\n',
                                'Added:', td9, '\n',
                                )
                            time.sleep(1)
                            count += 1
                    
        def getRecentCMCSolanaCoins(self, quantity=1):
            # URL of the page you want to fetch
            url = "https://coinmarketcap.com/new/"

            # Make an HTTP GET request to fetch the page content
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the HTML content
                tree = html.fromstring(response.content)

                # Find the rows using XPath
                rows = tree.xpath('//*[@id="__next"]/div[2]/div[1]/div[2]/div/div[2]/table/tbody/tr')

                # Dictionary to store grouped data
                coins_data = {}
                removeDupSet = set()

                count = 0

                print(f"Getting {quantity} of the most recent Solana coins on CoinMarketCap...", '\n'*2)
                for i in range(len(rows)):
                    stop = quantity
                    sol =  rows[i].cssselect('td')[8].text_content()
                    if count < quantity and sol == 'Solana':
                        td1 = rows[i].cssselect('td')[1].text_content()
                        td2 = rows[i].cssselect('td')[2].text_content()
                        td3 = rows[i].cssselect('td')[3].text_content()
                        td4 = rows[i].cssselect('td')[4].text_content()
                        td5 = rows[i].cssselect('td')[5].text_content()
                        td6 = rows[i].cssselect('td')[6].text_content()
                        td7 = rows[i].cssselect('td')[7].text_content()
                        td8 = rows[i].cssselect('td')[8].text_content()
                        td9 = rows[i].cssselect('td')[9].text_content()
                        
                                                # Use regex to extract the name
                        name_match = re.match(r'^([^0-9]*)', td2)
                        name = name_match.group(1).strip() if name_match else td2.strip()
                        # Extract the symbol by splitting at the first number
                        symbol_parts = re.split(r'[0-9]', td2, 1)
                        symbol = symbol_parts[1].strip() if len(symbol_parts) > 1 else ""
                        url = f'https://coinmarketcap.com/currencies/{symbol[1:]}/'
                                    # Make an HTTP GET request to fetch the page content
                        response = requests.get(url)

                        # Check if the request was successful (status code 200)
                        if response.status_code == 200:
                            # Parse the HTML content
                            page = html.fromstring(response.content)

                            cols = page.cssselect('#__next > div.sc-637f0039-1.hnHyvc.global-layout-v2 > div > div.cmc-body-wrapper > div > div > div.sc-aef7b723-0.sc-a6bd470-0.gavgYW.coin-stats > div.sc-f70bb44c-0.eyKDkF > section:nth-child(2) > div')   
                            
                            try:
                                totalSupply = cols[0].cssselect('#section-coin-stats > div > dl > div:nth-child(5) > div > dd')[0].text_content()
                            except:
                                totalSupply = 'N/A'
                            try:
                                maxSupply = cols[0].cssselect('#section-coin-stats > div > dl > div:nth-child(6) > div > dd')[0].text_content()
                            except:
                                maxSupply = 'N/A'
                            # Extract href from anchor tag
                            try:
                                contact_href = cols[0].cssselect('a.chain-name')[0].get('href') if cols[0].cssselect('a.chain-name') else 'N/A'
                            except:
                                contact_href = 'N/A'                        

                            print(
                                'Number:', td1, '\n',
                                'Name:', name, '\n',
                                'Symbol:', symbol, '\n',
                                'Price:', td3, '\n',
                                '1hr % Change:', td4, '\n',
                                '24hr % Change:', td5, '\n',
                                'Full Dill Market Cap:', td6, '\n',
                                "Total Supply:", totalSupply, '\n',
                                "Max Supply:", maxSupply, '\n',
                                'Volume:', td7, '\n',
                                'BlockChain:', td8, '\n',
                                'Contact Information:', contact_href, '\n',
                                'Added:', td9, '\n',
                                )
                            count += 1

        def getCMCFearAndGreedIndex(self, period='default'):
            # URL of the page you want to fetch
            url = "https://alternative.me/crypto/fear-and-greed-index/"

            # Make an HTTP GET request to fetch the page content
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the HTML content
                tree = html.fromstring(response.content)

                                # Find the element using XPath
                element = tree.xpath('//*[@id="main"]/section/div/div[3]/div[2]/div/div')


            if element:
                data = {}
                # Extracting the text content
                content = element[0].text_content().strip()
                # Splitting the content by newlines to separate the key and value
                parts = content.split('\n')
                # The first part is the key
                nowkey = 'Now'
                yesterdaykey = 'Yesterday'
                lastweekkey = 'Last_Week'
                lastmonthkey = 'Last_Month'

                # The rest of the parts are the values
                nowvalues = [v.strip() for v in parts[1:5] if v.strip()]
                yesterdayvalues = [v.strip() for v in parts[10:15] if v.strip()]
                lastweekvalues = [v.strip() for v in parts[19:25] if v.strip()]
                lastmonthvalues = [v.strip() for v in parts[28:35] if v.strip()]

                # Storing the key-value pair in the dictionary
                data[nowkey] = nowvalues
                data[yesterdaykey] = yesterdayvalues
                data[lastweekkey] = lastweekvalues
                data[lastmonthkey] = lastmonthvalues
            
            if period == 'today':
                print('Fear Index is at the:', '\n', '|----', data[nowkey][0] , '-', data[nowkey][1], 'level TODAY.', '\n')
            elif period == 'yesterday':
                print('Fear Index is at the:', '\n', '|----', data[nowkey][0] , '-', data[nowkey][1], 'level TODAY.','\n',)
                print('Fear Index was at the:', '\n', '|----', data[yesterdaykey][0] , '-', data[yesterdaykey][1], 'level YESTERDAY.', '\n',)
            elif period == 'all':
                print('Fear Index is at the:', '\n', '|----', data[nowkey][0] , '-', data[nowkey][1], 'level TODAY.', '\n',)
                print('Fear Index was at the:', '\n', '|----', data[yesterdaykey][0] , '-', data[yesterdaykey][1], 'level YESTERDAY.', '\n',)
                print('Fear Index was at the:', '\n', '|----', data[lastweekkey][0] , '-', data[lastweekkey][1], 'level LAST WEEK.', '\n',)
                print('Fear Index was at the:', '\n', '|----', data[lastmonthkey][0] , '-', data[lastmonthkey][1], 'level LAST MONTH.', '\n',)
            else:
                print('Fear Index is at the:', '\n', '|----', data[nowkey][0] , '-', data[nowkey][1], 'level TODAY.', '\n',)

# ----  CoinMaretCap Data Classes --- End ----
                    


