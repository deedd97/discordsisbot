import discord
import json
import imgkit
import codecs
import sis
import platform

client = 0
canale = 0

def apriFile():
	with open('dati/cw.json') as file:
		clanwar = json.load(file)
	return clanwar

def apriTemplateHTML():
	html = codecs.open("template.html").read()
	if(platform.system() == "Windows"):
		path = "C:/Users/Marco/Documents/bot"
	else:
		path = "/home/ubuntu"
	return html.replace("$indirizzo", path)


def salvaFile(file, obj):
	with open(file, 'w') as file:
		json.dump(obj, file)

def init(discordClient, idCanale):
	clanwar = apriFile()
	client = discordClient
	canale = client.get_channel(idCanale)

def controlloId(cw, id):
	for partite in cw['cw']:
		if(int(id) == int(partite['id'])):
			return True
	return False

def cmd(msg):
	if(msg[1] == "new"):
		print(msg[2])
		return aggiungi(msg)

def calcoloTicket(side, partita):
	ticketFinaliSIS = int(side["SIS"])
	ticketFinaliFOE = int(side["FOE"])
	for side2 in partita["side"]:
		if(side["numSide"] != side2["numSide"] and side["mappa"] == side2["mappa"]):
			ticketFinaliSIS += int(side2["SIS"])
			ticketFinaliFOE += int(side2["FOE"])
	return [ticketFinaliSIS, ticketFinaliFOE]
	
def aggiungi(cw):								#cw[2] nome del clan
	#prende l'id da un file						#cw[3] data cw
	clanwar = apriFile()
	id = int(clanwar['idUltima'])
	clanwar['cw'].append({
		'id': id + 1,
		'clan': cw[2],
		'data': cw[3],
		'giocatori': [],
		'side': []
	})
	clanwar['idUltima'] += 1
	with open('dati/cw.json', 'w') as file:
		json.dump(clanwar, file)
	return "L'id della clanwar contro il clan " + cw[2] + " è " + str(id + 1)

def aggiungiPlayer(cw, giocatori):
	id = cw[2]
	clanwar = apriFile()
	if(not controlloId(clanwar, id)):
		return "> ERRORE: l'id non esiste"
	i = 0
	for cw in clanwar['cw']:
		i += 1
		print(cw['id'])
		if(int(cw['id']) == int(id)):
			for giocatore in giocatori:
				cw['giocatori'].append(giocatore.id)
				msg = sis.aggiornaStats(giocatore.id, cw)
				if(msg != "err"):
					salvaFile("dati/cw.json", clanwar)
			if(msg == "err"):
				return "> ERRORE: vanno aggiunti prima i side"
			else:
				return msg

def aggiungiSide(cw):
	clanwar = apriFile()
	ticketSIS = cw[2]
	ticketFOE = cw[3]
	mappa = cw[4]
	id = int(cw[5])
	for partita in clanwar['cw']:
		if(int(partita["id"]) == id):
			numSide = len(partita["side"])
			partita["side"].append({
				"mappa": mappa,
				"SIS": ticketSIS,
				"FOE": ticketFOE,
				"numSide": numSide,
				"vinto": 1 if ticketSIS > ticketFOE else 0
				})
			salvaFile("dati/cw.json", clanwar)
			return "> side aggiunto";
	return "-2"


def players(cw):
	id = int(cw[2])
	clanwar = apriFile()
	for partita in clanwar['cw']:
		if(int(partita["id"]) == id):
			giocatori = ""
			for giocatore in partita['giocatori']:
				giocatori += giocatore + "\n"
			return giocatori

def esitoFlag(partita):
	partiteGiocate = []
	sideSIS = 0
	sideFOE = 0
	i = 1
	for side in partita["side"]:
		if(i > 3):
			break
		if(side["mappa"] not in partiteGiocate):
			partiteGiocate.append(side["mappa"])
			ticketFinali = calcoloTicket(side, partita)
			if(ticketFinali[0] > ticketFinali[1]):
				sideSIS += 1
			else:
				sideFOE += 1
			i += 1
	return(sideSIS > sideFOE)

def esito(partita, html):
	partiteGiocate = []
	sideSIS = 0
	sideFOE = 0
	i = 1
	for side in partita["side"]:
		if(i > 3):
			break
		if(side["mappa"] not in partiteGiocate):
			partiteGiocate.append(side["mappa"])
			ticketFinali = calcoloTicket(side, partita)
			if(ticketFinali[0] > ticketFinali[1]):
				sideSIS += 1
			else:
				sideFOE += 1
			html = html.replace("mappa" + str(i), side["mappa"].lower() + ".png")
			html = html.replace("strMappa" + str(i), side["mappa"])
			html = html.replace("ticket" + str(i), str(ticketFinali[0]) + " - " + str(ticketFinali[1]))
			i += 1
	print(sideSIS)
	if(sideSIS > sideFOE):
		html = html.replace("coloreEsito", "#0ff90f")
	else:
		html = html.replace("coloreEsito", "#f90f0f")
	html = html.replace("N - N", str(sideSIS) + " - " + str(sideFOE))
	print(html)
	return html			

def generaImg(partita):
	html = apriTemplateHTML()
	html = html.replace("#CLAN", partita['clan'])
	i = 1
	for giocatori in partita["giocatori"]:
		if(i>5):
			break
		print(i)
		nick = "ND"
		membri = sis.getMembri()
		for p in membri:
			print(p["id"])
			if(giocatori == p["id"]):
				nick = p["alias"][0]
		html = html.replace("gioc" + str(i), nick)
		i += 1
	html = esito(partita, html)
	if(platform.system() == "Windows"):
		path_wkthmltoimage = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltoimage.exe'
		config = imgkit.config(wkhtmltoimage=path_wkthmltoimage)
		options = {'width': 352, 'disable-smart-width': ''}
		return [imgkit.from_string(html, "out.png", options=options, config=config), "yes"]
	else:
		options = {'width': 352, 'disable-smart-width': '', 'xvfb': ''}
		return [imgkit.from_string(html, "out.png", options=options), "yes"]

def infoCw(cw):
	id = int(cw[2])
	clanwar = apriFile()
	if(not controlloId(clanwar, id)):
		return "> ERRORE: l'id non esiste"
	ticketSIS = 0
	ticket_FOE = 0
	sideSIS = 0
	sideFOE = 0
	for partita in clanwar['cw']:
		if(int(partita["id"]) == id):
			img = generaImg(partita)
			msg = ""
			mappeGiocate = []
			for side in partita['side']:
				ticketSideSIS = int(side['SIS'])
				ticketSideFOE = int(side['FOE'])
				msg += "> " + side['mappa'] + " " + side['SIS'] + " - " + side['FOE']
				numSide = int(side['numSide'])
				if(side['mappa'] not in mappeGiocate):
					mappeGiocate.append(side['mappa'])
					for side2 in partita['side']:
						if(int(side['numSide']) != int(side2['numSide'])):
							if(side['mappa'] == side2['mappa']):
								ticketSideSIS += int(side2['SIS'])
								ticketSideFOE += int(side2['FOE'])
					if(ticketSideSIS > ticketSideFOE):
						sideSIS += 1
					else:
						sideFOE += 1
				ticketSIS += int(side["SIS"])
				ticket_FOE += int(side["FOE"])
				if(int(side['SIS']) > int(side['FOE'])):
					msg += " SIDE VINTO\n"
				else:
					msg += " SIDE PERSO\n"
			return msg

def ultimeCw(cw):
	clanwar = apriFile()
	giorni = int(cw[2])
	vinte = 0
	perse = 0
	msg = ""
	if(giorni <= 0):
		return str(giorni) + " non è un numero valido"
	print(len(clanwar['cw']))
	if(len(clanwar['cw']) < giorni):
		giorni = len(clanwar['cw'])
		msg += "> Abbiamo disputato solo " + str(giorni) + " partite\n\n"
	else:
		msg += "> Le ultime " + str(giorni) + " partite\n\n"
	for i in range(len(clanwar['cw']) - 1, len(clanwar['cw']) - giorni - 1, -1):
		partita = clanwar['cw'][i]
		esito = ""
		if(esitoFlag(partita)):
			vinte += 1
			esito = "VINTA"
		else:
			perse += 1
			esito = "PERSA"
		msg += "> " + str(partita["id"]) + ") " + "SIS vs " + partita["clan"] + " " + partita["data"] + " " + esito + "\n"
		if(i > len(clanwar['cw']) - 1 or i < 0):
			break;
	return msg + "\n\n> " + str(vinte) + " VINTE\n> " + str(perse) + " PERSE"

def rimuoviCw(cw, tutte):
	clanwar = apriFile()
	id = cw[2]
	if(tutte):
		clanwar["cw"].clear()
		clanwar["idUltima"] = 0
		salvaFile("dati/cw.json", clanwar)
		return "> ho eliminato tutte le partite"
	for partita in clanwar["cw"]:
		if(int(partita["id"]) == int(id)):
			clan = partita["clan"]
			data = partita["data"]
			for i in range(int(clanwar["idUltima"]) - 1, int(id) - 1, -1):
				print(i)
				clanwar["cw"][i]["id"] = int(clanwar["cw"][i]["id"]) - 1
			clanwar["cw"].remove(partita)
			clanwar["idUltima"] -= 1
			salvaFile("dati/cw.json", clanwar)
			return "> ho eliminato la clanwar del " + data + " contro il clan " + clan

def infoPlayer(cw):
	clanwar = apriFile()
	nome = cw[3]
	partiteGiocate = 0
	for partita in clanwar['cw']:
		for giocatore in partita['giocatori']:
			if(giocatore == nome):
				partiteGiocate += 1
	return "> " + nome + " ha giocato " + str(partiteGiocate) + " volte"

def cont(cw):
	clanwar = apriFile()
	cont = 0
	for nome in clanwar['cw']:
		print(nome)
		if(nome['clan'] == cw[1]):
			cont += 1
	return "sono state disputate " + str(cont) + " partite contro il clan " + cw[1]
