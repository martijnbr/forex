from candle import Candle, CandleSelector
from event import Event
from strategy import strat
from variables import *

from misc import Iterator, Selector, time_to_datetime


import datetime as dt
import json, os

seconds_in_gran = {
    M5: 300,
    M30: 1800
}

class Chart(Event):
    def __init__(self, instrument, gran):
        self.instrument = instrument
        self.parent = instrument
        
        self.indicators = []
        
        self.gran = gran
        self.gran_seconds = seconds_in_gran[self.gran]
        self._candles = []
        
        self.load_chart(strat['load_start'])
        self.trigger_event('Chart-Created')
        
        print("{0}-{1} initiated".format(self.instrument.pair, self.gran))
        
    def tick(self, tick): 
        # find candle to tick to
        for candle in reversed(self._candles):
            if candle.time <= tick['time'] and candle.close > tick['time']:
                candle.tick(tick)
                return
            if candle.time > tick['time']:
                break
        
        candle = Candle(self, tick=tick)
        self.candle_builder(candle)
        
    def candles(self):
        return CandleSelector(self._candles)
    
    def load_chart(self, start):
        con = self.instrument.account.con
        pair = self.instrument.pair
        candles = con.get_instrument_history(pair, granularity=self.gran, count=5000, start=start)
        for candle in candles['candles']:
            candle['time'] = time_to_datetime(candle['time'])
            c = Candle(self, candle=candle)
            self.candle_builder(c)
        if(len(candles['candles']) == 5000):
            self.load_chart(candle['time'].isoformat('T')+'Z')
        
    def candle_builder(self, newCandle):
        n_candles = len(self._candles)
        for i, candle in enumerate(reversed(self._candles)):
            if candle.time == newCandle.time:
                self._candles[n_candles - i - 1] = newCandle
                return
            if newCandle.time > candle.time:
                self._candles.insert(n_candles-i, newCandle)
                return
        self._candles.insert(0, newCandle)
        
class ChartSelector(Selector):
    def get(self):
        return ChartIterator(self.list)

    def withInstrument(self, pair):
        charts = []
        for c in self.list:
            if c.instrument.pair == pair:
                charts.append(c)
        self.list = charts
        return self
    
    def withGranularity(self, gran):
        charts = []
        for c in self.list:
            if c.pair == gran:
                charts.append(c)
        self.list = charts
        return self    
        
class ChartIterator(Iterator):
    pass