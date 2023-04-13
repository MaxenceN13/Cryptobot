import discord
import time
import os
from affiche import Affiche
from users import Users
from user import User

affiches = [
    Affiche("0", ["ressources/epreuves/affiche_0.jpg"], "la guerre des gaules", ["miroir miroir", "sens de lecture"]),
    Affiche("1", ["ressources/epreuves/affiche_1.jpg"], "le concile de troyes", ["comme César"]),
    Affiche("2", ["ressources/epreuves/affiche_2.jpg"], "spartacus", ["le première lettre est un s"]),
    Affiche("3", ["ressources/epreuves/affiche_3.jpg"], "france"),
    Affiche("4", ["ressources/epreuves/affiche_4.jpg"], "vigenere", ["le clair v avec la sous clé t donne z"]),
    Affiche("5", ["ressources/epreuves/affiche_5.jpg"], "de componendis cifris cyphris", ["un chiffre pour une lettre"]),
    Affiche("6", ["ressources/epreuves/affiche_6.jpg"], "offensive du printemps", ["le décalage de départ est de 0"]),
    Affiche("7", ["ressources/epreuves/affiche_7.jpg"], ["91.4"], ["e=5 et pi=3.14"], "Donner moi la fréquence radio avec la commande solution pour retrouver le message chiffré."),
    Affiche("7b", ["ressources/epreuves/affiche_7.jpg"]), 
    Affiche("8", ["ressources/epreuves/affiche_8.jpg"], ["enseignant chercheur"], ["chaque cycle est composé de 4 lettres (1ère ligne, 2ème ligne, 3ème ligne, 2ème ligne)", "la taille du message est de 19 lettres, 19//4=4 cycles et reste 3", "premier ligne \"einee\""]),
    Affiche("9", ["ressources/epreuves/affiche_9.jpg"], texte = "**Dis moi `!solution suivant` pour passer à la prochaine fiche !**"),
    Affiche("10", ["ressources/epreuves/affiche_10.jpg"], texte = "**Dis moi `!solution suivant` pour passer à la prochaine fiche !**"),
    Affiche("11", ["ressources/epreuves/affiche_11.jpg"], ["polybe", "vercingetorix", "franc macon", "transposition"]),
    Affiche("12", ["ressources/epreuves/affiche_12.jpg"]),
]

db_path = "users.json"

users = Users()
if os.path.exists(db_path):
    users.load(db_path)


class MyClient(discord.Client):
    userchannel_public_feedback = None
    saved_time = time.time()

    def __init__(self, *args, **kwargs,):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        self.userchannel_public_feedback = self.get_channel(1095632033599979551)
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if type(message.channel) is discord.DMChannel:
            if message.author.id == self.user.id:
                return
        
            print("{0.author.name} (#{0.author.id}) : {0.content}".format(message))
            
            # Lorsque c'est le premier message d'un utilisateur
            if not users.exist(message.author.id):
                if message.content == "!start":
                    new_user = User(message.author.id, message.author.name)
                    print("Nouvel utilisateur : {0.nom} (#{0.id})".format(new_user))
                    users.add(new_user)
                    print(users)
                    await message.channel.send("Bonjour {0.author.mention}."\
                                            "\n\nBienvenue dans Cryptaventure ! Je serais ton guide dans cette aventure."\
                                            "\n\nPour commencer, voici comment communiquer avec moi :"\
                                            "\n\t- `'!help'` pour revoir ces informations"\
                                            "\n\t- `'!resume'` pour revoir l'affiche et les indices de l'épreuve courante"\
                                            "\n\t- `'!indice'` pour obtenir un nouvel indice sur l'épreuve courante"\
                                            "\n\t- `'!solution [solution]'` pour me proposer une solution (je suis insensible à la casse et aux accents), par exemple `\"!solution Master Cryptis\"`"\
                                            "\nJe te conseille d'ouvir les images dans ton navigateur pour mieux les voir."\
                                            "\n\n*Si vous avez un problème avec le bot, n'hésitez à contacter un administrateur.*"\
                                            "\n\n**Et voilà, maintenant nous pouvons y allez.**".format(message),
                                            file=discord.File(affiches[0].paths[0]))
                    
                    # Sauvegarde des données
                    users.save(db_path)

            elif users.get(message.author.id).affiche == len(affiches):
                await message.channel.send("Tu as déjà terminé l'aventure !")
                
            else:
                user = users.get(message.author.id)
                affiche = affiches[user.affiche]

                if message.content == "!start":
                    await message.channel.send("Tu as déjà commencé l'aventure, tu ne peux pas recommencer.")
                
                elif message.content == "!help":
                    await message.channel.send("Voici comment communiquer avec moi :"\
                                                "\n\t- `'!help'` pour revoir ces informations"\
                                                "\n\t- `'!resume'` pour revoir l'affiche et les indices de l'épreuve courante"\
                                                "\n\t- `'!indice'` pour obtenir un nouvel indice sur l'épreuve courante"\
                                                "\n\t- `'!solution [solution]'` pour me proposer une solution (je suis insensible à la casse et aux accents), par exemple `\"!solution Master Cryptis\"`")
                
                elif message.content == "!resume":
                    await self.send_affiche(message.channel, affiche)
                    
                    if user.getNbIndiceCourant() == 0:
                        await message.channel.send("Tu n'as pas encore utilisé d'indice.\n")
                    else:
                        response = "Voici les indices que tu as déjà obtenus : "
                        for i in range(user.getNbIndiceCourant()):
                            response += "{}, ".format(affiche.indices[i])
                        response += "\n"
                        await message.channel.send(response)

                elif message.content == "!indice":
                    indice = self.getNextIndice(user, affiche)
                    if indice:
                        await message.channel.send("Voici l'indice : {}".format(indice))
                    else:
                        await message.channel.send("Tu as déjà utilisé tous les indices.")
                
                elif message.content.startswith("!solution "):
                    solution = message.content[10:].lower()
                    if solution == "":
                        await message.channel.send("Tu n'as pas proposé de solution.")
                    elif solution == affiche.solution:
                        # Sauvegarde des données
                        users.save(db_path)
                        
                        (temps_affiche, nb_indice) = user.nextAffiche()
                        affiche = affiches[user.affiche]
                        
                        await message.channel.send("Bravo ! Tu as trouvé la bonne solution avec {} indice(s) et en moins de {} minute(s).".format(nb_indice, temps_affiche))
                        
                        if user.affiche == len(affiches):
                            (temps_total, nb_indice_total) = user.win()
                            await message.channel.send("Félicitation, tu as terminé l'aventure !", file=discord.File(affiches[-1].paths[0]))
                            await self.userchannel_public_feedback.send("Un grand tonnerre d'applaudissement pour <@{}> qui a terminé l'aventure en moins de {} minutes(s) et avec {} indice(s).".format(message.author.id, temps_total, nb_indice_total))
                        else:
                            await self.send_affiche(message.channel, affiche)
                    else:
                        await message.channel.send("Désolé, mais ce n'est pas la bonne solution.")

    async def send_affiche(self, channel, affiche):
        await channel.send("Voici l'affiche :", file=discord.File(affiche.paths[0]))
        for i in range(1, len(affiche.paths)):
            await channel.send(file=discord.File(affiche.paths[i]))
        if affiche.texte:
            await channel.send(affiche.texte)

    def getNextIndice(self, user, affiche):
        if user.getNbIndiceCourant() == len(affiche.indices):
            return None
                
        indice = affiche.indices[user.getNbIndiceCourant()]
        user.indices_utilises[-1] += 1
        return indice


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run('MTA5NTU5Mzc0MjI5NzIyMzE4OQ.GBTzzc.qUvicVFy2YDxVhyFo6tqXJ8UVtX3-P7fnzqq1s')