import discord
import time
import json
import os

solutions = [
    "la guerre des gaules",
    "le concile de troyes",
    "spartacus",
    "france",
    "vigenere",
    "de componendis cifris cyphris",
    "offensive du printemps",
    "idk",
    "enseignant chercheur",
    "suivant",
    "suivant",
    "idk",
]

indices = [
    ["test", "coucou"],
    ["test", "coucou"],
    ["test", "coucou"],
    ["test", "coucou"],
    ["test", "coucou"],
    ["test", "coucou"],
    ["test", "coucou"],
    ["test", "coucou"],
    ["test", "coucou"],
    [],
    [],
    ["test", "coucou"],
]

class MyClient(discord.Client):
    users = None
    userchannel_public_feedback = None
    saved_time = time.time()

    def __init__(self, *args, **kwargs,):
        super().__init__(*args, **kwargs)
        if os.path.exists("users.json"):
            with open("users.json", "r") as file:
                self.users = json.loads(file.read())
        else:
            self.users = {}

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
        
            print(message.author.name, ":", message.content)
            
            # Lorsque c'est le premier message d'un utilisateur
            if message.author.id not in self.users:
                if message.content == "!start":
                    self.users[message.author.id] = {
                        "nom": message.author.name,
                        "date_inscription": time.time(),
                        "messages": 1,
                        "affiche": 0,
                        "date_validation_affiche": [],
                        "indices_utilises": [0],
                    }
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
                                            file=discord.File('ressources/epreuves/affiche_0.jpg'))
                    
                    # Sauvegarde des données
                    with open("users.json", "w") as file:
                        file.write(json.dumps(self.users))

            else:
                user = self.users[message.author.id]
                user["messages"] += 1

                if message.content == "!start":
                    await message.channel.send("Tu as déjà commencé l'aventure, tu ne peux pas recommencer.")
                
                elif message.content == "!help":
                    await message.channel.send("Voici comment communiquer avec moi :"\
                                                "\n\t- `'!help'` pour revoir ces informations"\
                                                "\n\t- `'!resume'` pour revoir l'affiche et les indices de l'épreuve courante"\
                                                "\n\t- `'!indice'` pour obtenir un nouvel indice sur l'épreuve courante"\
                                                "\n\t- `'!solution [solution]'` pour me proposer une solution (je suis insensible à la casse et aux accents), par exemple `\"!solution Master Cryptis\"`")
                
                elif message.content == "!resume":
                    await message.channel.send("Voici l'affiche de l'épreuve courante :", file=discord.File('ressources/epreuves/affiche_{}.jpg'.format(user["affiche"])))
                    
                    response = ""
                    if user["indices_utilises"][user["affiche"]] == 0:
                        response += "Tu n'as pas encore utilisé d'indice.\n"
                    else:
                        response += "Voici les indices que tu as déjà obtenus : "
                        for indice in range(user["indices_utilises"][user["affiche"]]):
                            response += "{}, ".format(indices[user["affiche"]][indice])
                        response += "\n"
                    
                    await message.channel.send(response)

                elif message.content == "!indice":
                    if user["indices_utilises"][user["affiche"]] == len(indices[user["affiche"]]):
                        await message.channel.send("Tu as déjà utilisé tous les indices disponibles.")
                    else:
                        await message.channel.send("Voici l'indice {} : {}".format(user["indices_utilises"][user["affiche"]]+1, indices[user["affiche"]][user["indices_utilises"][user["affiche"]]]))
                        user["indices_utilises"][user["affiche"]] += 1
                
                elif message.content.startswith("!solution "):
                    solution = message.content[10:].lower()
                    if solution == "":
                        await message.channel.send("Tu n'as pas proposé de solution.")
                    elif solution == solutions[user["affiche"]]:
                        if user["affiche"] == 0:
                            temps_total = round((time.time()-user["date_inscription"])/60, 2)
                        else:
                            temps_total = round(((time.time()-user["date_validation_affiche"][user["affiche"]-1]))/60, 2)
                        
                        await message.channel.send("Bravo ! Tu as trouvé la bonne solution avec {} indice(s) et en moins de {} minute(s).".format(user["indices_utilises"][user["affiche"]], temps_total))
                        
                        # Sauvegarde des données
                        with open("users.json", "w") as file:
                            file.write(json.dumps(self.users))
                        
                        if user["affiche"] == len(solutions)-1:
                            await message.channel.send("Bravo, tu as terminé l'aventure !", file=discord.File('ressources/epreuves/affiche_12.jpg'))
                            await self.userchannel_public_feedback.send("Un grand tonnerre d'applaudissement pour <@{}> qui a terminé l'aventure en moins de {} minutes(s) et avec {} indice(s).".format(message.author.id, temps_total, user["indices_utilises"][user["affiche"]]))
                        else:
                            user["affiche"] += 1
                            user["indices_utilises"].append(0)
                            user["date_validation_affiche"].append(time.time())
                            
                            if user["affiche"] == 9 or user["affiche"] == 10:
                                await message.channel.send("Voici l'affiche de l'épreuve suivante :", file=discord.File('ressources/epreuves/affiche_{}.jpg'.format(user["affiche"])))
                                await message.channel.send("Envoie `!solution suivant` pour passer à l'épreuve suivante.")
                            else:
                                await message.channel.send("Voici l'affiche de l'épreuve suivante :", file=discord.File('ressources/epreuves/affiche_{}.jpg'.format(user["affiche"])))
                    else:
                        await message.channel.send("Désolé, mais ce n'est pas la bonne solution.")


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run('MTA5NTU5Mzc0MjI5NzIyMzE4OQ.GBTzzc.qUvicVFy2YDxVhyFo6tqXJ8UVtX3-P7fnzqq1s')

