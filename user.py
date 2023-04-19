import time
import jsonpickle

administrateurs = [696713015159947324, 766566168809963521, 819960130287828993, 477591295926337537]

class User:
    def __init__(self, id, nom):
        self.id = id
        self.nom = nom
        self.date_inscription = time.time()
        self.is_ban = False
        self.events = {}
        self.current_event_code = None
        self.mini_epreuve = [0,0,0,0]

    def startEvent(self, event_code):
        self.events[event_code] = {
            "finished" : False,
            "start_date" : time.time(),
            "validation_dates" : [],
            "current_run" : 0,
            "hint_used" : [0]
        }
        self.current_event_code = event_code
    
    def startedEvent(self, event_code):
        return event_code in self.events.keys()

    def finishEvent(self):
        event = self.events[self.current_event_code]
        temps_total = event["validation_dates"][-1] - event["start_date"]
        
        event["finished"] = True
        self.current_event_code = None

        return (round(temps_total/60.0), sum(event["hint_used"]))
    
    def finishedEvent(self, event_code):
        return event_code in self.events.keys() and self.events[event_code]["finished"]
    
    def inProgressEvent(self, event_code):
        return event_code in self.events.keys() and not self.events[event_code]["finished"]
    
    def resetEvent(self, event_code):
        if event_code in self.events.keys():
            self.events.pop(event_code)
            if self.current_event_code == event_code:
                self.current_event_code = None

    def getCurrentEvent(self):
        return self.current_event_code
    
    def getCurrentRun(self):
        return self.events[self.current_event_code]["current_run"]
    
    def nextRun(self):
        event = self.events[self.current_event_code]
        event["validation_dates"].append(time.time())

        temps_affiche = event["validation_dates"][-1]
        temps_affiche -= event["start_date"] if event["current_run"] == 0 else event["validation_dates"][-2]

        event["current_run"] += 1
        event["hint_used"].append(0)

        return (round(temps_affiche/60.0), event["hint_used"][-2])
    
    def getNbHintUsed(self):
        return self.events[self.current_event_code]["hint_used"][self.getCurrentRun()]

    def useHint(self):
        self.events[self.current_event_code]["hint_used"][self.getCurrentRun()] += 1
    
    def isAdmin(self):
        return self.id in administrateurs

    def __str__(self):
        return jsonpickle.encode(self)