class UnderlyingData:

    def __init__(self, underlyingName, timestamp, history):
        self.__underlyingName = underlyingName
        self.__timestamp = timestamp
        self.__history = history
        
    @property
    def UnderlyingName(self):
        return self.__underlyingName

    @property
    def History(self):
        return self.__history
    
    @property
    def Timestamp(self):
        return self.__timestamp