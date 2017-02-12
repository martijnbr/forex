from misc import Iterator, Selector
from event import Event

import datetime as dt
import threading

class Candle(Event):
    def __init__(self, chart, candle=None, tick=None):   
        self.chart = chart
        self.parent = chart
        
        self.indicator_points = []
        
        timedelta = dt.timedelta(0, self.chart.gran_seconds)
        if candle:
            self.__dict__.update(candle)    
        if tick:
            self.chart = chart        
            self.lowBid      = tick['bid']
            self.highBid     = tick['bid']
            self.closeBid    = tick['bid']
            self.openBid     = tick['bid']
            self.lowAsk      = tick['ask']
            self.highAsk     = tick['ask']
            self.openAsk     = tick['ask']
            self.closeAsk    = tick['ask']
            self.complete    = False
            
            tick_time = tick['time']
            time = self.chart._candles[-1].time
            while True:
                if time < tick_time and time + timedelta > tick_time:
                    self.time = time
                    break
                time += timedelta

        now = dt.datetime.utcnow()
        self.close = self.time + timedelta
        if now > self.close:
            self.complete = True
        else:
            time = (self.close - now).total_seconds()
            threading.Timer(time, self.close).start()
        self.trigger_event('Candle-Open')
            
    def tick(self, tick):
        bid = tick['bid']
        ask = tick['ask']
        
        self.closeBid = bid
        self.closeAsk = ask
        
        self.highBid = max(self.highBid, bid)
        self.highAsk = max(self.highAsk, ask)
        self.lowBid = min(self.lowBid, bid)
        self.lowAsk = min(self.lowAsk, ask)
        
        self.trigger_event('Candle-Tick')
        
    def close(self):
        self.complete = True
        self.trigger_event('Candle-Close')

class CandleSelector(Selector):
    def get(self):
        return CandleIterator(self.list)
        
class CandleIterator(Iterator):
    pass
        
