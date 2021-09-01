import json
import UnderlyingDataProvider as udp

class StockMarketData:

    def __init__(self):
        self.LoadConfig()

    # Properties

    @property
    def UnderlyingNames(self):
        return self.__UnderlyingNames
    
    @UnderlyingNames.setter
    def UnderlyingNames(self, underlyingNames):
        self.__UnderlyingNames = underlyingNames
    
    @property
    def UnderlyingDataProviderList(self):
        return self.__underlyingDataProviderList
    
    @UnderlyingDataProviderList.setter
    def UnderlyingDataProviderList(self, underlyingDataProviderList):
        self.__underlyingDataProviderList = underlyingDataProviderList

    # End properties

    def LoadConfig(self):
        with open('./config.json') as jsonfile:
            config = json.load(jsonfile)
            self.UnderlyingNames = config['UnderlyginNames']
            self.__period = config['Period']
            self.__interval = config['Interval']
            self.__updateInterval = config['UpdateInterval']

    def BuildStockMarketDataCollection(self):
        underlyingDataProviderList = []
        for underlyingName in self.UnderlyingNames:
            underlyingDataProviderList.append(udp.UnderlyingDataProvider(self.__period, self.__interval, self.__updateInterval, underlyingName, 'on'))
        self.UnderlyingDataProviderList = underlyingDataProviderList
    
    def StartStockMarketDataCollection(self):
        for underlyingDataProvider in self.UnderlyingDataProviderList:
            underlyingDataProvider.StartUnderlyingDataCollection()