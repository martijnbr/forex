from chart import Chart, ChartSelector
from candle import CandleSelector
from misc import *
from event import Event

class Instrument(Event):
    def __init__(self, account, pair, strat):
        self.account = account
        self.parent = account
        
        self.pair = pair
        self._charts = {}
        
        for gran in strat['charts']:
            self.load_chart(gran)
            
        self.trigger_event('Instrument-Created')
    
    def charts(self):
        return ChartSelector(self._charts)
    
    def candles(self):
        a = CandleSelector([])
        for c in self._charts:
            a += self._charts[c].candles()
        return a
    
    def tick(self, tick):
        for chart in self._charts:
            self._charts[chart].tick(tick)
    
    def load_chart(self, gran):
        self._charts[gran] = Chart(self, gran)
    
    
class InstrumentSelector(Selector):
    def get(self):
        return InstrumentIterator(self.list)

class InstrumentIterator(Iterator):
    pass
     