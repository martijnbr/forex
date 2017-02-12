class Event:
    def on(self, str_event, fn_listener, priority = None):
        if not '_event_listeners' in self.__dict__:
            self._event_listeners = {}
    
        listeners = self._event_listeners
        if not str_event in listeners:
            listeners[str_event] = []
        listeners = listeners[str_event]
        listener_object = {'listener':fn_listener, 'priority':priority}
        if priority is None: 
            listeners.append(listener_object)
        else:
            for i, listener in enumerate(listeners):
                if not listener['priority']:
                    listeners.insert(i, listener_object)
                    return
                if listener['priority'] > priority:
                    listeners.insert(i, listener_object)
                    return
            listeners.append(listener_object)
            
    def trigger_event(self, str_event):
        if not '_event_listeners' in self.__dict__:
            self._event_listeners = {}
        
        if not str_event in self._event_listeners:
            self._event_listeners[str_event] = []
        for listener in self._event_listeners[str_event]:
            listener['listener'](self)