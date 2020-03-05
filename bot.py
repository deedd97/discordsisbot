import discord
import sint
import random
import sis

client = discord.Client()

TOKEN = "Njg0MDQzOTEzOTIwOTA1MjM5.Xl0eCQ._q1iMWGGz1xDG0MVDUrTz5kkFbI"

bot_channel = 684056945677565958

barbabianca23 = ["ciao sono barbabianca e mi plano nell'ano", "ciao sono barbabianca e mi piace la nutella nel culo", "ciao sono barbabianca e ho l'ombellico storto", "ciao sono barbabietola23"]

cmdValidi = ["new", "add", "del", "players", "info", "stats", "addside"]

def info():
	cmd = ["!cw stats CLAN", "!cw -u 3", "!cw addside TICKET1 TICKET2 MAPPA ID", "!cw new CLAN DATA", "!cw add ID GIOCATORE", "!cw rem ID GIOCATORE", "!cw rem ID", "!cw CLAN", "!cw players ID"]
	info = ""
	for str in cmd:
		info += "> " + str + "\n"
	return info
        

@client.event

async def on_ready():
    await client.change_presence(activity=discord.Game(name='CW vs barbabianca23'))
    canale = client.get_channel(bot_channel)
    await canale.send("ciao mi chiamo barbabianca e mi piace la nutella nel culo")
    sint.init(client, bot_channel)
    print("Connesso")

@client.event
async def on_message(message):
	msg = message.content.split()
	risposta = "-2"
	cmd = False
	if(message.author.id != 684043913920905239):
		print(message.author.id)
		if(msg[0] == "!p" and msg[1] == "add"):
			cmd = True
			risposta = sis.aggiungi(message.guild.members, message.mentions[0], msg[3])
		if(msg[0] == "!cw"):
			cmd = True
			if(len(msg) == 1):
				risposta = info()
			elif(msg[1] == "info"):
				if(len(msg) >= 4 and msg[2] == "-p" ):
					risposta = sis.infoPlayer(message.mentions)
				elif(len(msg) == 3 and msg[2].isnumeric()):
					risposta = sint.infoCw(msg)
					if(risposta.split()[1] != "ERRORE:"):
						await message.channel.send(file=discord.File("out.png"))
			elif(msg[1] == "del" and len(msg) == 3):
				if(msg[2].isnumeric()):
					risposta = sint.rimuoviCw(msg, False)
				elif(msg[2] == "all"):
					risposta = sint.rimuoviCw(msg, True)
			elif(len(msg) == 4 and msg[1] == "new"):
				risposta = sint.cmd(msg)
			elif(len(msg) >= 4 and msg[1] == "add"):
				risposta = sint.aggiungiPlayer(msg, message.mentions)
			elif(len(msg) == 6 and msg[1] == "addside"):
				risposta = sint.aggiungiSide(msg)
			elif(msg[1] == "players"):
				risposta = sint.players(msg)
			elif(len(msg) == 3 and msg[1] == "-u"):
				risposta = sint.ultimeCw(msg)
			elif(len(msg) == 2 and msg[1] not in cmdValidi):
				risposta = sint.cont(msg)
		if(risposta != "-1" and cmd):
			if(risposta == "-2"):
				risposta = "> ERRORE"
			await message.channel.send(risposta)
	msg = ""
	

client.run(TOKEN)
