import time
import jsonpickle

class User:
    def __init__(self, id, nom):
        self.id = id
        self.nom = nom
        self.affiche = 0
        self.date_inscription = time.time()
        self.date_validation_affiche = []
        self.indices_utilises = [0]

    def nextAffiche(self):
        self.date_validation_affiche.append(time.time())

        temps_affiche = self.date_validation_affiche[-1]
        temps_affiche -= self.date_inscription if self.affiche == 0 else self.date_validation_affiche[-2]

        self.affiche += 1
        self.indices_utilises.append(0)

        return (round(temps_affiche/60.0, 2), self.indices_utilises[-2])
    
    def win(self):
        temps_total = self.date_validation_affiche[-1] - self.date_inscription
        return (round(temps_total/60.0, 2), sum(self.indices_utilises))
                
    def getNbIndiceCourant(self):
        return self.indices_utilises[-1]

    def __str__(self):
        return jsonpickle.encode(self)