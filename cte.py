from affiche import Affiche

events = {
        "1324" : {
                "name" : "Cryptaventure",
                "code" : "1324",
                "run" : [
                        Affiche("introduction", 
                                ["ressources/images/affiche_0.jpg"], 
                                "la guerre des gaules", 
                                ["miroir miroir", "manga", "sens de lecture"]),

                        Affiche("cesar", 
                                ["ressources/images/affiche_1.jpg"], 
                                "le concile de troyes", 
                                ["comme César"]),

                        Affiche("templier", 
                                ["ressources/images/affiche_2.jpg"], 
                                "spartiate", 
                                ["le première lettre est un s"]),

                        Affiche("scytale", 
                                ["ressources/images/affiche_3.jpg"], 
                                "france", 
                                [], 
                                "Distanciel oblige, vous devrez utiliser le site dcode : https://www.dcode.fr/chiffre-scytale pour cette épreuve.\nLe message chiffré retrouvé est : xxx (solution est france pour l'instant)"),
                        
                        Affiche("vigenere", 
                                ["ressources/images/affiche_4.jpg", "ressources/images/affiche_4b.jpg"], 
                                "gisement", 
                                ["le clair v avec la sous clé t donne z"]),
                        
                        Affiche("beale", 
                                ["ressources/images/affiche_5.jpg",  "ressources/images/affiche_5b.jpg"], 
                                "de componendis cyfris", 
                                ["un nombre pour un mot", "la première lettre est le clair"]),
                        
                        Affiche("alberti", 
                                ["ressources/images/affiche_6.jpg"], 
                                "offensive du printemps", 
                                ["le décalage de départ est de 0"], 
                                "Distanciel oblige, vous devrez utiliser le site dcode : https://www.dcode.fr/alberti-cipher pour cette épreuve.\nDisque exterieur : ABCDEFGILMNOPQRSTUVZ1234 ; Disque intérieur : acegklnprtvz&xysomqihfdb"),
                        
                        Affiche("adfgvx", 
                                ["ressources/images/affiche_7.jpg", "ressources/images/affiche_7b.jpg"], 
                                "guerre de secession", 
                                ["fréquence radio : e=5 et pi=3.14", "construiser d'abord votre table avec la clé en haut rangée dans l'ordre alphabétique et le chiffré écrit de haut en bas et de gauche à droite"], "Donner moi la valeur de la fréquence radio avec la commande `!frequence` pour retrouver le message chiffré."),
                        
                        Affiche("rail_fence", 
                                ["ressources/images/affiche_8.jpg"], 
                                "enseignant chercheur", ["chaque cycle est composé de 4 lettres (1ère ligne, 2ème ligne, 3ème ligne, 2ème ligne)", "la taille du message est de 19 lettres, 19//4=4 cycles et reste 3", "premier ligne \"einee\""]),
                        
                        Affiche("entre_dimension", 
                                ["ressources/images/affiche_9.jpg"], 
                                "suivant", 
                                [],
                                "Dis moi `!solution suivant` pour passer à la prochaine fiche !"),
                        
                        Affiche("revelation_mechant", 
                                ["ressources/images/affiche_10.jpg"], 
                                "suivant", 
                                [],
                                "Dis moi `!solution suivant` pour passer à la prochaine fiche !"),
                        
                        Affiche("epreuves_finales_1", 
                                ["ressources/images/affiche_11.jpg"], 
                                "vercingetorix", 
                                ["le décalage est un multiple de 2", "le décalage ne dépasse pas 10"], 
                                "Donne moi la réponse à l'épreuve d'en haut à gauche !"),
                        
                        Affiche("epreuves_finales_2", 
                                ["ressources/images/affiche_11.jpg"], 
                                "franc macon", 
                                [], 
                                "Donne moi la réponse à l'épreuve d'en haut à droite !"),
                        
                        Affiche("epreuves_finales_3", 
                                ["ressources/images/affiche_11.jpg"], 
                                "carre de polybe", 
                                [], 
                                "Donne moi la réponse à l'épreuve d'en bas à gauche !"),
                        
                        Affiche("epreuves_finales_4", 
                                ["ressources/images/affiche_11.jpg"], 
                                "transposition", 
                                ["ça me rappelle une histoire de lapin :rabbit2:"], 
                                "Donne moi la réponse à l'épreuve d'en bas à droite !"),
                        
                        Affiche("fin", 
                                ["ressources/images/affiche_12.jpg"],
                                "",
                                []),
                        ],
                },
        "1345" : {
                "name" : "Cryptaventure Bis",
                "code" : "1345",
                "run" : [
                        Affiche("epreuves_finales_4", 
                                ["ressources/images/affiche_11.jpg"], 
                                "transposition", 
                                ["ça me rappelle une histoire de lapin :rabbit2:"], 
                                "Donne moi la réponse à l'épreuve d'en bas à droite !"),
                        
                        Affiche("fin", 
                                ["ressources/images/affiche_12.jpg"],
                                "",
                                []),
                        ],
                },
                        
        }

# def afficher_indices(history_name):
#     print("{")
#     for affiche in events[history_name]["affiches"]:
#         print("\"{0.id}\" : [".format(affiche), end="")
#         for indice in affiche.indices:
#             print("\"{0}\" ,".format(indice), end="")
#         print("],")
#     print("}")