import datetime
import time
import requests
from lxml import html
import urllib
import re
import json



# Classes--------------------------------------------------------------------
class Utilities:
    def __init__(self):
        pass
  
    def saveToFile(data):    
    # Save the extracted content to a file
        with open('extracted_content.txt', 'w') as file:
            file.write(data)

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
    
                todayDate = datetime.datetime.today().strftime('%Y-%m-%d')
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
  
AltcoinIndex = AltcoinSeasonIndex()
RainbowChart = RainbowIndexBtc()

AltcoinIndex.getAltcoinSeasonIndex()
RainbowChart.getRanbowIndexBtc()

