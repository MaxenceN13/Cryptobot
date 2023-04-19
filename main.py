import discord
import time
import os
from affiche import Affiche
from users import Users
from user import User
from cte import events
from unidecode import unidecode
import sys

# TODO : 
# - epreuve scytale (3) et disque alberti (6)
# - filtre anti-spam
# - épreuve 7 faire des sons pour la commande !frequence
# - faire un pool, et le rappeler pour les personnes qui terminent l'aventure
# - radio faire une intervalle entre 91.4 et 91.5 pour la fréquence
# - déplacer la complexité dans un events_manager

users = None

class MyClient(discord.Client):
    userchannel_public_feedback = None
    channel_feedback_miniepreuve = None
    maintenance = False

    def __init__(self, *args, **kwargs,):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        self.userchannel_public_feedback = self.get_channel(1095632033599979551)
        self.channel_feedback_miniepreuve = self.get_channel(1097855112774422549)
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if type(message.channel) is discord.DMChannel:
            if message.author.id == self.user.id:
                return
            
            user = users.get(message.author.id)
            if self.maintenance and (not user or not user.isAdmin()):
                await message.channel.send("Cryptobot est actuellement en maintenance.")
                return
            
            print("{0.author.name} (#{0.author.id}) : {0.content}".format(message))
            message.content = unidecode(message.content)

            if not users.exists(message.author.id):
                new_user = User(message.author.id, message.author.name)
                print("Nouvel utilisateur : {0.nom} (#{0.id})".format(new_user))
                users.add(new_user)
            
            user = users.get(message.author.id)

            if user.is_ban:
                await message.channel.send("Tu es banni !")
                return

            if message.content.startswith("!start ") or message.content == "!start":
                code = message.content[7:].strip()
                if code in events.keys():
                    if not user.startedEvent(code):
                        await message.channel.send("Bonjour {}."\
                                                "\n\nBienvenue dans {} ! Je serais ton guide dans cette aventure."\
                                                "\n\nPour commencer, voici comment communiquer avec moi :"\
                                                "\n\t- `'!help'` pour revoir ces informations"\
                                                "\n\t- `'!resume'` pour revoir l'affiche et les indices de l'épreuve courante"\
                                                "\n\t- `'!indice'` pour obtenir un nouvel indice sur l'épreuve courante"\
                                                "\n\t- `'!solution [solution]'` pour me proposer une solution (je suis insensible à la casse et aux accents), par exemple `\"!solution Master Cryptis\"`"\
                                                "\nJe te conseille d'ouvir les images dans ton navigateur pour mieux les voir."\
                                                "\n\n*Si vous avez un problème avec le bot, n'hésitez à contacter un administrateur.*".format(user.nom, events[code]["name"]))
                        user.startEvent(code)
                        await self.sendRun(user, message.channel)
                        users.save()

                    elif user.finishedEvent(code):
                        await message.channel.send("Tu as déjà terminé l'aventure {}, tu ne peux pas recommencer.".format(events[code]["name"]))

                    elif user.inProgressEvent(code):
                        if user.current_event_code == code:
                            await message.channel.send("Tu es déjà dans l'aventure {} !\nFait `!resume` pour revoir l'affiche et les indices de l'épreuve courante.".format(events[code]["name"]))
                        else:
                            user.current_event_code = code
                            await message.channel.send("Te voilà de retour dans l'aventure {} !".format(events[code]["name"]))
                            await self.sendRun(user, message.channel)
                
            elif message.content == "!help":
                await message.channel.send(self.getHelp(user))
                    
            elif message.content == "!resume" and user.current_event_code != None:
                await self.sendRun(user, message.channel)

            elif message.content == "!indice" and user.current_event_code != None:
                current_run = events[user.getCurrentEvent()]["run"][user.getCurrentRun()]
                if len(current_run.hints) == 0:
                    await message.channel.send("Il n'y a aucun indice pour cette épreuve.")
                hint = self.getNextHint(user)
                if hint:
                    await message.channel.send("Voici l'indice : {}".format(hint))
                    users.save()
                else:
                    await message.channel.send("Tu as déjà utilisé tous les indices.")
            
            elif (message.content.startswith("!solution ") or message.content == "!solution") and user.current_event_code != None:
                solution = message.content[10:].lower().strip()

                if solution == "":
                    await message.channel.send("Tu n'as pas proposé de solution.")
                
                else:
                    current_run = events[user.getCurrentEvent()]["run"][user.getCurrentRun()]

                    if solution == current_run.solution:
                        (temps_affiche, nb_indice) = user.nextRun()
                        current_run = events[user.getCurrentEvent()]["run"][user.getCurrentRun()]
                        
                        if solution != "suivant":
                            await message.channel.send("Bravo ! Tu as trouvé la bonne solution avec {} indice(s) et en moins de {} minute(s).".format(nb_indice, temps_affiche))

                        if current_run.id == "fin":
                            event_name = events[user.getCurrentEvent()]["name"]
                            (temps_total, nb_indice_total) = user.finishEvent()
                            await message.channel.send("Félicitation, tu as terminé l'aventure !", file=discord.File(current_run.paths[0]))
                            await self.userchannel_public_feedback.send("Un grand tonnerre d'applaudissement pour <@{}> qui a terminé l'aventure {} en moins de {} minutes et avec {} indice(s).".format(message.author.id, event_name, temps_total, nb_indice_total))
                        else:
                            await self.sendRun(user, message.channel)
                        
                        users.save()
                    else:
                        await message.channel.send("Désolé, mais \"{}\" n'est pas la bonne solution.".format(solution))
                
            elif message.content.startswith("!frequence ") and user.inProgressEvent("1324") and events["1324"]["run"][user.getCurrentRun()].id == "adfgvx":
                frequence = message.content[11:]
                if frequence == "91.4":
                    await message.channel.send("DA GF GF VA FD GX XX VX VX GV AX VD FF GF XX GV XF VA")
                else:
                    await message.channel.send("Désolé, mais \"{}\" n'est pas la bonne fréquence.".format(frequence))
            
            elif message.content.startswith("!epreuve1 ") or message.content == "!epreuve1":
                solution = message.content[10:].lower().strip()
                
                if solution == "":
                    await message.channel.send("Tu n'as pas proposé de solution.")
                
                elif user.mini_epreuve[0] == 1:
                    await message.channel.send("Tu as déjà trouvé la bonne solution pour la mini-épreuve n°1.")

                elif solution == "youtu.be/":
                    await message.channel.send("Bravo ! Tu as trouvé la bonne solution pour la mini-épreuve n°1.\nGarde bien cette solution pour la prochaine épreuve.")
                    await self.channel_feedback_miniepreuve.send("Bravo à {0.author.mention} qui a trouvé la bonne solution pour la mini-épreuve n°1.".format(message))
                    user.mini_epreuve[0] = 1
                    users.save()
                else:
                    await message.channel.send("\"{}\" n'est pas la bonne solution.".format(solution))
            
            elif message.content.startswith("!epreuve2 ") or message.content == "!epreuve2":
                await message.channel.send("La mini-épreuve n°2 sera disponible le mercredi 19")
            
            elif message.content.startswith("!epreuve3 ") or message.content == "!epreuve3":
                await message.channel.send("La mini-épreuve n°3 sera disponible le mercredi 26")
            
            elif message.content.startswith("!epreuvef ") or message.content == "!epreuvef":
                await message.channel.send("La mini-épreuve finale sera disponible le mercredi 26")

            elif message.content.startswith("!maintenance ") and user.isAdmin():
                if message.content[13:] == "start":
                    await message.channel.send("Lancement de la maintenance en cours...")
                    users.save()
                    self.maintenance = True
                    await message.channel.send("Maintenance lancé.")
                
                elif message.content[13:] == "stop":
                    await message.channel.send("Arrêt de la maintenance en cours...")
                    users.load()
                    self.maintenance = False
                    await message.channel.send("Maintenance arrêté.")
            
            elif message.content == "!save" and user.isAdmin():
                users.save()
                await message.channel.send("Sauvegarde effectuée.")
            
            elif message.content == "!stop" and user.isAdmin():
                await message.channel.send("Arrêt du bot en cours...")
                users.save()
                sys.exit(0)
            
            elif message.content.startswith("!ban ") and user.isAdmin():
                user_id = message.content[5:]
                if not user_id.isdigit():
                    await message.channel.send("L'ID doit être un nombre.")
                else:
                    user_to_ban = users.get(int(user_id))
                    if user_to_ban:
                        if user_to_ban.isAdmin():
                            await message.channel.send("L'utilisateur <@{}> est un administrateur.".format(user_id))
                        else:
                            user_to_ban.is_ban = True
                            await message.channel.send("L'utilisateur <@{}> a été banni.".format(user_id))
                            users.save()
                    else:
                        await message.channel.send("L'utilisateur <@{}> n'a pas démarré de communication avec moi.".format(user_id))
            
            elif message.content.startswith("!unban ") and user.isAdmin():
                user_id = message.content[7:]
                if not user_id.isdigit():
                    await message.channel.send("L'ID doit être un nombre.")
                else:
                    user_to_uban = users.get(int(user_id))
                    if user_to_uban:
                        user_to_uban.is_ban = False
                        await message.channel.send("L'utilisateur \"{}\" a été débanni.".format(user_id))
                        users.save()
                    else:
                        await message.channel.send("L'utilisateur <@{}> n'a pas démarré de communication avec moi.".format(user_id))
            
            elif message.content.startswith("!show ") and user.isAdmin():
                user_id = message.content[6:]
                if not user_id.isdigit():
                    await message.channel.send("L'ID doit être un nombre.")
                else:
                    user_to_show = users.get(int(user_id))
                    if user_to_show:
                        await message.channel.send("```{}```".format(user_to_show))
                    else:
                        await message.channel.send("L'utilisateur \"{}\" n'existe pas.".format(user_id))

            elif message.content.startswith("!reset ") and user.isAdmin():
                user_id, code, *_ = message.content[7:].split(" ") + [None]
                if not user_id.isdigit():
                    await message.channel.send("L'ID doit être un nombre.")
                else:
                    user_to_reset = users.get(int(user_id))
                    if user_to_reset:
                        if code:
                            user_to_reset.resetEvent(code)
                            await message.channel.send("L'utilisateur <@{}> a été réinitialisé sur l'événement {}.".format(user_id, events[code]["name"], code))
                        else:
                            users.remove(int(user_id))
                            await message.channel.send("L'utilisateur <@{}> a été réinitialisé.".format(user_id))
                        users.save()
                    else:
                        await message.channel.send("L'utilisateur <@{}> ne m'est pas connu.".format(user_id))
            
            elif message.content.startswith("!resetEvent ") and user.isAdmin():
                code = message.content[12:]
                if code in events:
                    for user in users.users.values():
                        user.resetEvent(code)
                    await message.channel.send("L'événement {} a été réinitialisé.".format(events[code]["name"]))
                    users.save()
            
            else:
                await message.channel.send(self.getHelp(user))



    async def sendRun(self, user, channel):
        current_run = events[user.getCurrentEvent()]["run"][user.getCurrentRun()]

        await channel.send(file=discord.File(current_run.paths[0]))
        for i in range(1, len(current_run.paths)):
            await channel.send(file=discord.File(current_run.paths[i]))
        if current_run.text:
            await channel.send(current_run.text)
        
        if len(current_run.hints) > 0:
            if user.getNbHintUsed() == 0:
                await channel.send("Tu n'as pas encore utilisé d'indice.\n")
            else:
                response = "Voici les indices que tu as déjà obtenus : "
                for i in range(user.getNbHintUsed()):
                    response += "{}, ".format(current_run.hints[i])
                response += "\n"
                await channel.send(response)

    def getNextHint(self, user):
        current_run = events[user.getCurrentEvent()]["run"][user.getCurrentRun()]
        if user.getNbHintUsed() == len(current_run.hints):
            return None
                
        hint = current_run.hints[user.getNbHintUsed()]
        user.useHint()
        return hint
    
    def getHelp(self, user):
        if user and user.current_event_code != None:
            return "Voici comment communiquer avec moi :"\
                "\n\t- `'!help'` pour revoir ces informations"\
                "\n\t- `'!resume'` pour revoir l'affiche et les indices de l'épreuve courante"\
                "\n\t- `'!indice'` pour obtenir un nouvel indice sur l'épreuve courante"\
                "\n\t- `'!solution [solution]'` pour me proposer une solution (je suis insensible à la casse et aux accents), par exemple `\"!solution Master Cryptis\"`"
        elif user and user.isAdmin():
            return "Voici comment communiquer avec moi :"\
                "\n\t- `'!help'` pour revoir ces informations"\
                "\n\t- `'!ban [id]'` pour bannir un utilisateur (l'ID est le nombre qui suit le @ dans son pseudo)"\
                "\n\t- `'!unban [id]'` pour débannir un utilisateur (l'ID est le nombre qui suit le @ dans son pseudo)"\
                "\n\t- `'!show [id]'` pour afficher les informations d'un utilisateur (l'ID est le nombre qui suit le @ dans son pseudo)"\
                "\n\t- `'!reset [id]'` pour réinitialiser un utilisateur (l'ID est le nombre qui suit le @ dans son pseudo)"\
                "\n\t- `'!resetEvent [code]'` pour réinitialiser un événement (le code est le code de l'événement, par exemple `\"!resetEvent 1\"` pour réinitialiser l'événement 1)"

        else:
            return "\n\nVoici comment communiquer avec moi :"\
                "\n\t- `'!start [code]'` pour commencer l'aventure (le code d'accès sera délivré le 29 avril)"\
                "\n\t- `'!epreuve1 [solution]` pour me proposer une solution à la mini-épreuve 1"\
                "\n\t- `'!epreuve2 [solution]` pour me proposer une solution à la mini-épreuve 2"\
                "\n\t- `'!epreuve3 [solution]` pour me proposer une solution à la mini-épreuve 3"\
                "\n\t- `'!epreuvef [solution]` pour me proposer une solution à la mini-épreuve finale"\
                "\n\t- `'!help'` pour revoir ces informations"

if __name__ == "__main__":
    db_path = "users.json"

    users = Users()
    users.setSavePath(db_path)
    if os.path.exists(db_path):
        users.load()
    
    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)
    client.run('MTA5NTU5Mzc0MjI5NzIyMzE4OQ.GBTzzc.qUvicVFy2YDxVhyFo6tqXJ8UVtX3-P7fnzqq1s')