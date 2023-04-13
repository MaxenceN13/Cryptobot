import discord
import time
import os
from affiche import Affiche
from users import Users
from user import User
from cte import affiches
from unidecode import unidecode

# TODO : 
# - epreuve scytale (3) et disque alberti (6)
# - ajouter des commandes pour administrateur (!save, !reset, !ban, !unban)
# - filtre anti-spam
# - épreuve 7 faire des sons pour la commande !frequence
# - faire un pool, et le rappeler pour les personnes qui terminent l'aventure
# - gérer les épreuves pré-évenements

users = None

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
            
            message.content = unidecode(message.content)

            # Lorsque c'est le premier message d'un utilisateur
            if not users.exist(message.author.id):
                if message.content == "!start 1324":
                    new_user = User(message.author.id, message.author.name)
                    print("Nouvel utilisateur : {0.nom} (#{0.id})".format(new_user))
                    users.add(new_user)
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
                
            elif users.exist(message.author.id) and affiches[users.get(message.author.id).affiche].id != "fin":
                user = users.get(message.author.id)
                affiche = affiches[user.affiche]

                if message.content == "!start":
                    await message.channel.send("Tu as déjà commencé l'aventure, tu ne peux pas recommencer.\nFait `!resume` pour revoir l'affiche et les indices de l'épreuve courante.")
                
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
                
                elif message.content.startswith("!solution ") or message.content == "!solution":
                    solution = message.content[10:].lower().strip()
                    # Remove accent
                    if solution == "":
                        await message.channel.send("Tu n'as pas proposé de solution.")

                    elif solution == affiche.solution:
                        
                        (temps_affiche, nb_indice) = user.nextAffiche()
                        
                        if affiche.solution != "suivant":
                            await message.channel.send("Bravo ! Tu as trouvé la bonne solution avec {} indice(s) et en moins de {} minute(s).".format(nb_indice, temps_affiche))

                        affiche = affiches[user.affiche]

                        if affiche.id == "vigenere":
                            (temps_total, nb_indice_total) = user.win()
                            await message.channel.send("Félicitation, tu as terminé l'aventure !", file=discord.File(affiche.paths[0]))
                            await self.userchannel_public_feedback.send("Un grand tonnerre d'applaudissement pour <@{}> qui a terminé l'aventure en moins de {} minutes(s) et avec {} indice(s).".format(message.author.id, temps_total, nb_indice_total))
                        else:
                            await self.send_affiche(message.channel, affiche)
                        
                        # Sauvegarde des données
                        users.save(db_path)
                    else:
                        await message.channel.send("Désolé, mais \"{}\" n'est pas la bonne solution.".format(solution))
                
                elif message.content.startswith("!frequence ") and affiche.id == "adfgvx":
                    frequence = message.content[11:]
                    if frequence == "91.4":
                        await message.channel.send("DA GF GF VA FD GX XX VX VX GV AX VD FF GF XX GV XF VA")
                    else:
                        await message.channel.send("Désolé, mais \"{}\" n'est pas la bonne fréquence.".format(frequence))
                    

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

if __name__ == "__main__":
    db_path = "users.json"

    users = Users()
    if os.path.exists(db_path):
        users.load(db_path)

    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)
    client.run('MTA5NTU5Mzc0MjI5NzIyMzE4OQ.GBTzzc.qUvicVFy2YDxVhyFo6tqXJ8UVtX3-P7fnzqq1s')