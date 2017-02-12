import connections as cons
from strategy import strat
from instrument import Instrument, InstrumentSelector
from chart import ChartSelector
from candle import CandleSelector
from misc import time_to_datetime
from event import Event

import json
import threading

class trader(Event):
    def __init__(self):
        self.con = cons.practice()
        self.strat = strat
        self.stream = []
        self._instruments = {}

        for pair in strat['instruments']:
            threading.Thread(target=self.load_instrument, args=(pair,)).start()
        threading.Thread(target=self.start_tick_stream).start()
        
    def instruments(self):
        return InstrumentSelector(self._instruments)
    
    def charts(self):
        s = ChartSelector([])
        for i in self._instruments:
            s += self._instruments[i].charts()
        return s
    
    def candles(self):
        s = CandleSelector([])
        for i in self._instruments:
            s += self._instruments[i].candles()
        return s

    def load_instrument(self, pair):
        self.stream.append(pair)
        self._instruments[pair] = Instrument(self, pair, self.strat)
        
    def start_tick_stream(self):
        self.tick_stream_running = True
        pairs = ','.join(self.stream)
        for t in self.con.get_prices(pairs).iter_lines():
            if not self.tick_stream_running:
                return
            tick = json.loads(t)
            if 'tick' in tick:
                self.process_tick(tick['tick'])

    def process_tick (self, tick):
        pair = tick['instrument']
        tick['time'] = time_to_datetime(tick['time'])

        if pair in self._instruments:
            self._instruments[pair].tick(tick)
            
    def stop_tick_stream(self):
        self.tick_stream_running = False
        
    def stop(self):
        self.stop_tick_stream()
#        charts = self.charts().get()
#        while charts.hasNext():
#            charts.next().save()
                
t = trader()
