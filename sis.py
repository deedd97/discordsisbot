import discord
import json
import sint

def apriFile():
	with open("dati/sis.json") as file:
		sis = json.load(file)
	return sis

def salvaFile(file, obj):
	with open(file, 'w') as file:
		json.dump(obj, file)

def getMembri():
	return apriFile()["membri"]

def infoPlayer(giocatori):
	sis = apriFile()
	msg = ""
	for giocatore in giocatori:
		for playersis in sis["membri"]:
			if(playersis["id"] == giocatore.id):
				msg += "> " + "ID PSN: " + playersis["alias"][0] + "\n\n> " + str(int(playersis["vinte"]) + int(playersis["perse"])) + " partite giocate\n> " + str(playersis["vinte"]) + " partite vinte\n> " + str(playersis["perse"]) + " partite perse\n"
		msg += "\n"
	return msg

def aggiornaStats(idPlayer, cw):
	sis = apriFile()
	if(len(cw["side"]) == 0):
		return "err"
	mappeGiocate = []
	sideSIS = 0
	sideFOE = 0
	for player in sis["membri"]:
		if(idPlayer == player["id"]):
			print("ciao")
			if(sint.esitoFlag(cw)):
				player["vinte"] = int(player["vinte"]) + 1
			else:
				player["perse"] = int(player["perse"]) + 1
			#player["ticketPresi"] = int(player["ticketPresi"]) + ticket[0]
			#player["ticketPersi"] = int(player["ticketPersi"]) + ticket[1]
	salvaFile("dati/sis.json", sis)
	return "aggiunto"

def aggiungi(membri, sisDiscord, nickGioco):
	sis = apriFile()
	trov = True
	if(trov):
		mappaPref = "ND"
		mappaSchif = "ND"
		obj = {
			'id': sisDiscord.id,
			'vinte': '0',
			'perse': '0',
			'ticketPresi': '0',
			'ticketPersi': '0',
			'mappaPref': "ND",
			'mappaSchif': "ND",
			'alias': [nickGioco],
			'squadra': 'ND'
		}
		sis["membri"].append(obj)
		salvaFile("dati/sis.json", sis)
		return "ho salvato " + sisDiscord.name
	else:
		return "il nome su discord non esiste"