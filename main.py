import btc.btcClasses as btcClasses

AltcoinIndex = btcClasses.AltcoinSeasonIndex()
RainbowChart = btcClasses.RainbowIndexBtc()
CoinMarketCap = btcClasses.CoinMarketCapData()
BirdsEye = btcClasses.BirdseyeData()

''' 
can get recent 5 solana coins
you can input a number and it will find that many recent sol coins
'''
# CoinMarketCap.getRecentCMCCoins(quantity=2)

# CoinMarketCap.getRecentCMCSolanaCoins(quantity=4)
'''
 can input:
        today , yesterday or all  
'''
# CoinMarketCap.getCMCFearAndGreedIndex(period='yesterday')
# AltcoinIndex.getAltcoinSeasonIndex()
RainbowChart.getRanbowIndexBtc()
# BirdsEye.getBirdsEyeCoins()


