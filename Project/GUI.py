from tkinter import *
from tkinter import PhotoImage
from random import randint
import simpleaudio
from Extras import Marquee


###################

def createdeck(bg1, bg2, bg3, bg4, bg5):
	cdeck = []
	colours = [["brown", bg1], ["orange", bg2], ["pink", bg3], ["purple", bg4], ["wild", bg5]]
	elements = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+2", "W"]  #ADD +4/blank?
	#the deck consists of 5 colours, and 12* possible elements
	''' the elements are no's 0 to 9, pick up 2, and wild card
	however the wildcard only appears on the 5th colour
	'''
	for colourno in range(len(colours)):
		colour = colours[colourno]
		#colour_cdeck = cdeck[colourno] #current colour
		#will assign separate coloured cards into separate arrays in cdeck

		if colour[0] != "wild":  #separates wildcard
			for element in elements:
				cardinfo = []  #this clears the array so each element is separate
				for _ in range(2):  #repeat 2x for two of each card
					if element != "W":  #do not add wild

						#colour = colours[colourno]
						cardinfo = []
						cardinfo.extend(colour)
						cardinfo.append(element)  #will add the element to the info on the card

						cdeck.append(cardinfo)  #will add all the info to cdeck within its array as a card
					#cdeck is a 2 dimensional array - each card is an array
					#cdeck[0] is a card that is brown and zero, cdeck[9] is a brown nine card

		elif colour[0] == "wild":
			for element in range(4):
				cardinfo = []
				cardinfo.extend(colour)
				cardinfo.append(element)
				cdeck.append(cardinfo)

	#the deck is now full but NOT separated by colour
	return cdeck


# def a custom playsound function to avoid replacing all instances when testing audio player libraries
def playsound(wav_file_name):
	sound = simpleaudio.WaveObject.from_wave_file(wav_file_name).play()

	return sound


######################################################################################

'''Tkinter code section'''

root = Tk()
root.title('Crazy Eights')
root.geometry('{}x{}'.format(1000, 790))
root.minsize(1252, 500)
root.state('zoomed')  #fullscreen mode, may add later
root.attributes("-fullscreen", False)
root.iconbitmap('C8.ico')

header = StringVar()
ticker = StringVar()
ticker.set("Welcome to Crazy Eights!")
marquee = None


def upHUD(header, hand, discards):  #this displays and updates the HUD
	global score
	if hand is not None and discards is not None:
		htext = ("Name:", name, "\t\tHand size:", len(hand), "\tscore:", score, "\t\tDiscard pile size:", len(discards))
	else:
		htext = ("Name:", name, "\t\tHand size:", 7, "\tscore:", 0, "\t\tDiscard pile size:", 1)
	header.set(''.join(str(i) + ' ' for i in htext)[:-1])  #removes curly brackets


def notify(text):
	print(text)
	ticker.set(text)
	marquee.itemconfigure(marquee.text, text=ticker.get())


def genGUI():
	global header, cmid_frame, center, ctr_mid, ctr_right

	# create all of the main containers
	top_frame = Frame(root, bg='red3', relief="raised", width=450, height=50, pady=3)
	center = Frame(root, bg='wheat', relief="raised", padx=85, pady=30)
	root.configure(background='sienna')

	# layout all of the main containers
	root.grid_rowconfigure(1, weight=1)
	root.grid_columnconfigure(0, weight=1)
	top_frame.grid_columnconfigure(1, weight=1)

	top_frame.grid(row=0, sticky="ew")
	center.grid(row=1, sticky="ns")

	# create the widgets for the top frame
	title = Label(top_frame, text=" CRAZY EIGHTS ", bg='red3', fg="ivory", height=1, relief="raised", borderwidth=2,
				  font=("system", 24))
	head = Label(top_frame, textvariable=header, bg='red3', fg="ivory", width=90, height=2, relief="raised",
				 borderwidth=2, font=("system", 16))
	bQuit = Button(top_frame, text="Quit", font=("system", 12), height=1, pady=7, padx=16, command=lambda: lose())

	# layout the widgets in the top frame
	title.grid(row=0, sticky="ew")
	head.grid(row=0, column=1, sticky="ew")
	bQuit.grid(row=0, column=2, sticky="ew")

	# create the center widgets
	center.grid_rowconfigure(0, weight=1)
	center.grid_columnconfigure(1, weight=1)

	scrollbar = Scrollbar(center)  # try fix this so scrollreg varies
	ctr_mid = Canvas(center, bg='snow2', width=588, height=40, scrollregion=(0, 0, 100, 1650),
					 yscrollcommand=scrollbar.set)
	scrollbar.configure(command=ctr_mid.yview)
	scrollbar.grid(sticky=NS)

	cmid_frame = Frame(ctr_mid, bg='antiquewhite4', relief="sunken")
	ctr_right = Frame(center, bg='snow3', width=340, height=40, padx=3, pady=3)

	ctr_mid.grid(row=0, column=1, sticky="nsew")
	ctr_mid.create_window(0, 0, window=cmid_frame, anchor='nw')
	ctr_right.grid(row=0, column=2, sticky="ns")

	return (cmid_frame, ctr_mid, ctr_right)


#finalise program (create essential variables)

cmid_frame, ctr_mid, ctr_right = genGUI()  # this function can't be called before pick() is defined

brn = PhotoImage(file="b.gif")
oge = PhotoImage(file="o.gif")
pnk = PhotoImage(file="p.gif")
prp = PhotoImage(file="pu.gif")
wld = PhotoImage(file="w.gif")
deck = createdeck(brn, oge, pnk, prp, wld)

# to create some familiarity and context, sounds 1-4 will be for the user & 5-7 for the com
play_sfx = ["wav/D01.wav", "wav/D02.wav", "wav/D03.wav", "wav/D04.wav", "wav/D05.wav", "wav/D06.wav", "wav/D07.wav"]
take_sfx = ["wav/T01.wav", "wav/T02.wav", "wav/T03.wav", "wav/T04.wav", "wav/T05.wav", "wav/T06.wav", "wav/Tk2.wav"]
# music
bgm_songs = ["wav/S01.wav", "wav/S02.wav", "wav/S03.wav", "wav/S04.wav", "wav/S05.wav", "wav/S06.wav"]
global current_bgm_global


# create widgets (card buttons) for ctr_mid

def orderbuttons(button, bpos):  #

	for count in range(15):
		condit = 6 + (7 * count)
		alignment = 0 + (7 * count)
		if bpos <= condit:  #will order cards into rows so that they dont go offscreen
			button.grid(row=count, column=bpos - alignment, sticky=W, padx=4, pady=4)
			bpos = bpos + 1  #increase so each button has unique position
			break
		else:
			continue

	return bpos


#GAMEPLAY functions & procedures

def swap(card, fromm, to):
	for fcard in fromm:
		if card == fcard:
			fromm.remove(card)
			to.append(card)
	return (fromm, to)


#Randomly generate CPU & Player's Hand
def generateHandFromDeck():
	global deck
	hand = []

	for cards in range(7):
		rCID = randint(0, len(deck) - 1)  #random card ID
		card = deck[rCID]
		deck, hand = swap(card, deck, hand)  # assigns 7 random cards to a hand

	return hand


phand = generateHandFromDeck()  # player's hand
c1hand = generateHandFromDeck()  # computer's hand (not displayed)
#using this function, several computer players can be made

discards = []  #these are the cards that are face up in the middle of the "table" ie the card that's just been placed


def showHand(hand):  #will show the given hand (player's) onscreen
	buttons = cmid_frame.grid_slaves()
	if len(buttons) > 0:  #if there are already buttons on screen
		for slave in buttons:
			slave.destroy()  #clear all buttons before regenerating them
	bposition = 0

	for card in hand:
		cardID = []
		if card[0] != "wild":
			cardtext = card[2]
		else:
			cardtext = " "  #blank to show symbol on wild
		cphoto = card[1]
		cardID = [card[0], card[2]]  #will pass info of card (colour, element) into button input
		button = Button(cmid_frame, image=cphoto, text=cardtext, font=("system", 24), fg="black", compound=CENTER,
						command=lambda ID=cardID: playUSR(ID, hand))
		button.image = cphoto
		bposition = orderbuttons(button, bposition)
	buttons = cmid_frame.grid_slaves()
	if len(buttons) > 0 and bStart["state"] == NORMAL:
		print("here")
		bPUC.config(state=NORMAL)
		bStart.config(state=DISABLED)  #start button only works once

	'''Pick a random card from pick up pile (the deck[] array) and use
	as first card, also to display the currently
	placed card, (top card) in the right hand section:'''


def updateCurrentTopCard():
	global deck, discards
	#print("updating top card")
	if discards == []:  #if no current card, ie game has just begun
		rCID = randint(0, len(deck) - 1)  #random card ID
		card = deck[rCID]
		deck, hand = swap(card, deck, discards)  #place random card from deck

	topCard = discards[-1]  #the last used (discarded) card is the top card, AKA the current card
	#print("top card is now {} {}".format(topCard[0], topCard[2]))
	TCphoto = topCard[1]  #assigns image
	TCphoto = TCphoto.zoom(2)
	if topCard[0] != "wild":
		cardtext = topCard[2]
	else:
		cardtext = " "  #blank to show symbol on wild
	TCpic = Label(ctr_right, image=TCphoto, fg="black", text=cardtext, font=("system", 46), compound=CENTER,
				  relief="raised",
				  borderwidth=5)
	TCpic.image = TCphoto  #Top Card picture
	TCpic.grid(row=0, column=0, columnspan=5, sticky=N + S + E + W, padx=76, pady=20)

	currentLabel = Label(ctr_right, text=" Current face-up card ", font=("system", 18), relief="groove", borderwidth=2)
	currentLabel.grid(row=1, columnspan=5, pady=4)


#return (deck, discards)


def playCOM(hand, currentcards):  #when the COM chooses/places a card
	bEND.config(state=DISABLED)
	notify("the COM is thinking...")

	root.after(4100, playCOMafterThinking,
			   hand)  #some additional time is spent to make it more realistic and obvious that the computer is taking a turn


def playCOMafterThinking(hand):
	global deck
	currentcard = deck[-1]
	comP2 = False
	played = False
	while played is False:
		if currentcard[2] == "+2":  #COM must pick up 2 cards and then may play or end turn
			randomNO = randint(0, len(deck) - 1)  #random card is chosen as deck[] is unshuffled
			card = deck[randomNO]  #random card in the 'pick up' pile (deck[])
			deck, hand = swap(card, deck, hand)
			#print("COM has picked up a",card)
			randomNO = randint(0, len(deck) - 1)  #random card is chosen as deck[] is unshuffled
			card = deck[randomNO]  #random card in the 'pick up' pile (deck[])
			deck, hand = swap(card, deck, hand)
		#print("and a",card)

		for card in hand:
			if card[2] == currentcard[2] or card[0] == currentcard[0] or card[0] == "wild" or currentcard[
				0] == "wild":  #if the elements/colours match or is wildcard
				swap(card, hand, discards)  #play this card
				playsound(play_sfx[randint(4, 6)])
				notify("COM has played a {} {}.".format(card[0], card[2]))
				if card[2] == "+2": comP2 = True

				played = True
				break
		if played is False:
			#if no cards match, must pick up card
			root.after(500)
			print("COM had to pick up ", deck[-1])
			swap(deck[-1], deck, hand)
			playsound(play_sfx[randint(4, 6)])
			played = True

	# reactivate player's hud <change this for multiplayer>
	updateCurrentTopCard()
	bPUC.config(state=NORMAL)
	player_cards = cmid_frame.grid_slaves()
	#currentcard = deck[-1]
	if comP2 is False:  #if COM DID NOT just play a +2
		for button in player_cards:
			button.config(state=NORMAL)  #player cannot play a card over +2

	update(hand)


#return (hand, deck, currentcard)


# declare GUI buttons: Pick Up Card, End Turn, Start Game
bPUC, bEND, bStart = Button(), Button(), Button()


def gen_UIbuttons(playerHand):  #this was created to resolve parameter passing errors
	global bPUC, bEND, marquee, discards, bStart
	bPUC = Button(ctr_right, text="Pick up card", font=("system", 12), command=lambda: pick(playerHand, deck, discards),
				  state=DISABLED)  #bPUC: button to Pick Up Card
	bPUC.grid(row=2, column=0, pady=20, ipadx=20, ipady=10)
	bStart = Button(ctr_right, text="Start", font=("system", 12), command=showHand(playerHand))
	bStart.grid(row=2, column=1, pady=20, ipadx=20, ipady=10)
	bEND = Button(ctr_right, text="End turn", font=("system", 12), command=lambda: playCOM(c1hand, deck),
				  state=DISABLED)
	bEND.grid(row=2, column=2, pady=20, ipadx=20, ipady=10)

	marquee = Marquee(ctr_right, text=ticker.get(), font=("system", 12), borderwidth=2, relief="sunken")
	marquee.grid(row=3, columnspan=3, sticky=EW, pady=20)


#return (bStart, bEND, bPUC, marquee)


def pick(hand, pile, currentcards):
	top_card = currentcards[-1]
	if top_card[2] == "+2":  #if the card played is a +2 card you must pick up twice
		repetitions = 2  # # # maybe switch to making user press pick up twice?
	else:
		repetitions = 1
	for _ in range(repetitions):
		randomNO = randint(0, len(pile) - 1)  #random card is chosen as deck[] is unshuffled
		card = pile[randomNO]  #random card in the 'pick up' pile (deck[])
		pile, hand = swap(card, pile, hand)
		playsound(play_sfx[randint(0, 3)])  #PlaySound(take_sfx[randint(0,3)], SND_NOSTOP | SND_FILENAME | SND_ASYNC)
		notify("you picked up {} {}. pile size: {}.".format(card[0], card[2], len(pile)))
		root.after(500)

	showHand(hand)
	bEND.config(state=NORMAL)  #the end turn button will be valid


gen_UIbuttons(phand)  #generate buttons


def playUSR(cardinfo, hand):  #called when card is clicked
	global deck, discards
	cardnum = 0
	currentcard = discards[-1]
	for item in hand:
		if item[0] == cardinfo[0] and item[2] == cardinfo[1]:  #if the card matches button pressed
			card = item
			break
		cardnum += 1

	if (card[2] == currentcard[2]
			or card[0] == currentcard[0]
			or card[0] == "wild"
			or currentcard[0] == "wild"):  #if the elements/colours match
		valid = True

	else:
		valid = False  #input validation
		notify("that card cannot be played!!")
		box = Toplevel()
		box.minsize(250, 30)
		box.title("Crazy Eights")
		box.iconbitmap('C8.ico')
		msg = Label(box, text="You cannot play that card!")
		msg.pack(pady=12, ipadx=50)
		button = Button(box, text="Dismiss", command=box.destroy)
		button.pack(pady=10)

	if valid:
		if len(hand) <= 1:  # you win once you play your last card
			playerwin()
		swap(card, hand, discards)
		playsound(play_sfx[randint(0, 3)])  #PlaySound(play_sfx[randint(0,3)],  SND_FILENAME | SND_ASYNC)
		notify("you played a {} {}.".format(card[0], card[2]))
		bEND.config(state=NORMAL)  #the end turn button will be valid
		bPUC.config(state=DISABLED)  #cannot pick up a card after playing

	#in order for the button to return any values, the parameters must be global
	global phand
	phand = hand

	update()
	if valid:  # if just played
		buttons = cmid_frame.grid_slaves()
		for slave in buttons:  #disable all cards
			slave.config(state=DISABLED)  #will ensure player can only use 1 card per turn



def update(*args):  #called whenever a button is pressed

	global phand, deck, discards, score

	updateCurrentTopCard()  #call this when card is played

	upHUD(header, phand, discards)

	showHand(phand)

	comcardLabel = Label(ctr_right, text="Opponent's hand size:", font=("system", 16), relief="groove", borderwidth=2)
	comcardLabel.grid(row=4, columnspan=5, pady=7, sticky="s")

	if len(args) > 0:  #only when COMs turn is up
		comHand = args[0]
		comHandSize = Label(ctr_right, bg="darkgreen", fg="yellow2", text=len(comHand), font=("MS serif", 72),
							relief="sunken", width=2, borderwidth=4)
		comHandSize.grid(row=5, columnspan=5, pady=5, ipady=20, sticky="s")

		if len(comHand) < 1:
			lose()

	else:
		comHandSize = Label(ctr_right, bg="darkgreen", fg="yellow2", text=len(c1hand), font=("MS serif", 72),
							relief="sunken", width=2, borderwidth=4).grid(row=5, columnspan=5, pady=5, sticky=S,
																		  ipady=20)

	score = int(len(c1hand) * 100000 / len(discards))
	#print("score",score)
	return (phand, deck, discards, score)


def finish(msg_box):
	global current_bgm_global, root

	current_bgm_global.stop()
	msg_box.destroy()
	root.destroy()
	import Crazy_Eights  #quit game and reopen splash


def playerwin():  #called when user plays last card

	box = Toplevel(width=250)  #------------------------
	box.title("Congratulations!")
	box.iconbitmap('C8.ico')
	msg = Message(box, text="You have won this game!")  #create dialog box
	msg.pack(ipadx=150)
	quit_button = Button(box, text="Return to main menu", command=lambda: finish(box))  #quit GUI & open splash
	quit_button.pack(padx=12, pady=36)

	import csv
	with open('Scores.csv', 'a') as csvfile:
		filewriter = csv.writer(csvfile, delimiter=' ', quotechar=',')
		filewriter.writerow([name, score])  #add name & score to save file


def lose():  #called when computer plays last card [OR user forfeits/quits]
	print("You lost!")
	box = Toplevel(width=250)
	box.title("Game Over!")

	msg = Message(box, bg="darkgreen", text="You have lost this game!")  #create dialog box
	msg.pack(ipadx=150)
	quit_button = Button(box, text="Return to main menu", command=lambda: finish(box))  #quit GUI & open splash
	quit_button.pack(padx=12, pady=36)


name = "jeff"  #arbitrary value used before proper assignment
score = 0
update()


def rungame(fetch):  #will be called externally - from splash
	global name
	global current_bgm_global
	name = fetch  #set player name to parameter given

	upHUD(header, phand, discards)
	current_bgm_global = playsound(bgm_songs[randint(0, 5)])  #

	ctr_mid.config(scrollregion=ctr_mid.bbox("all"))
	ctr_mid.mainloop()
	root.update()
	root.mainloop()

	print(root)
	print(center)
	print(ctr_mid)


#root.mainloop() # to run without splash screen
