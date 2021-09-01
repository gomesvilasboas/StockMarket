import yfinance as yf
import threading
from threading import Lock
import time
import logging
from UnderlyingData import UnderlyingData

class UnderlyingDataProvider:

    logging.basicConfig(filename='./log/UnderlyingDataProvider.log', level=logging.INFO)
    logger = logging.getLogger(__name__)

    def __init__(self, period, interval, updateInterval, underlyingName, sign):
        self.__period = period
        self.__interval = interval
        self.__updateInterval = updateInterval
        self.__underlyingName = underlyingName
        self.Sign = sign
    
    # Properties

    @property
    def Sign(self):
        return self.__sign
    
    @Sign.setter
    def Sign(self, sign):
        self.__sign = sign

    # End Properties

    def DownloadUnderlyingHistory(self, underlyingName, lock):
        while(True):
            if self.Sign != 'off':
                msg = '[{underlyingName}][{timestamp}] Downloading underlying history'.format(underlyingName=self.__underlyingName, timestamp=time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))
                with lock:
                    logging.info(msg)

                try:
                    startTime = time.time()
                    history = yf.download(underlyingName, period=self.__period, interval=self.__interval, progress=False)
                    endTime = time.time()
                    underlyingData = UnderlyingData(underlyingName, time.gmtime(), history)
                    #Save to MongoDB
                    msg = '[{underlyingName}][{timestamp}] Underlying history downloaded in {sec}s'.format(underlyingName=self.__underlyingName, timestamp=time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()), sec=(endTime-startTime))
                    with lock:
                        logging.info(msg)
                except Exception as ex:
                    msg = '[{underlyingName}][{timestamp}] Error downloading history: {error}'.format(underlyingName=self.__underlyingName, timestamp=time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()), error=str(ex))
                    with lock:
                        logging.info(msg)

                time.sleep(self.__updateInterval)
            else:
                time.sleep(1)
    
    def StartUnderlyingDataCollection(self):
        logger_lock = Lock()
        thread = threading.Thread(target=self.DownloadUnderlyingHistory, args=(self.__underlyingName, logger_lock,))
        thread.start()
        msg = '[{timestamp}] UpdateUnderlyingHistory thread initiated for underlying {underlyingName}'.format(timestamp=time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()), underlyingName=self.__underlyingName)
        logging.info(msg)