from tkinter import *
from tkinter import PhotoImage
from random import *
from winsound import *
from Extras import Marquee
###################

def createdeck(bg1,bg2,bg3,bg4,bg5):
    cdeck = []
    colours = [["brown",bg1],["orange",bg2],["pink",bg3],["purple",bg4],["wild",bg5]]
    elements = ["0","1","2","3","4","5","6","7","8","9","+2","W"]#ADD +4/blank?
    #the deck consists of 5 colours, and 12* possible elements
    ''' the elements are no's 0 to 9, pick up 2, and wild card
    however the wildcard only appears on the 5th colour
    '''
    for colourno in range(len(colours)):
        colour = colours[colourno]
        #colour_cdeck = cdeck[colourno] #current colour
        #will assign separate coloured cards into separate arrays in cdeck
        

        if colour[0] != "wild":     #separates wildcard
            for element in elements:
                cardinfo = []#this clears the array so each element is separate
                for _ in range(2):#repeat 2x for two of each card
                    if element != "W":#do not add wild

                        #colour = colours[colourno]
                        cardinfo = []
                        cardinfo.extend(colour)
                        cardinfo.append(element)#will add the element to the info on the card
                    
                        cdeck.append(cardinfo)#will add all the info to cdeck within its array as a card
                        #cdeck is a 2 dimensional array - each card is an array
                        #cdeck[0] is a card that is brown and zero, cdeck[9] is a brown nine card
                    
        elif colour[0] == "wild":
            for element in range(4):
                cardinfo = []
                cardinfo.extend(colour)
                cardinfo.append(element)
                cdeck.append(cardinfo)
                
        #the deck is now full but NOT separated by colour
    return(cdeck)
        
######################################################################################

'''Tkinter code section'''

root = Tk()
root.title('Crazy Eights')
root.geometry('{}x{}'.format(1000, 790))
root.minsize(1085, 500)
root.state('zoomed') #fullscreen mode, may add later
root.attributes("-fullscreen", False)
root.iconbitmap('C8.ico')

header = StringVar()
ticker = StringVar()
ticker.set("hello world")
marquee = None

def upHUD (header, hand, discards):    #this displays and updates the HUD
    global score
    if hand is not None and discards is not None: htext = ("Name:",name,"\t\tHand size:",len(hand),"\tscore:",score, "\t\tDiscard pile size:",len(discards))
    else: htext = ("Name:",name,"\t\tHand size:",7,"\tscore:",0, "\t\tDiscard pile size:",1)
    header.set(''.join(str(i)+' ' for i in htext)[:-1]) #removes curly brackets

def notify(text):
    print(text)
    ticker.set(text)
    marquee.itemconfigure(marquee.text, text=ticker.get())


def genGUI(header):
    
# create all of the main containers
    top_frame = Frame(root, bg='red3',relief="raised", width=450, height=50, pady=3)
    center = Frame(root, bg='wheat',relief="raised", padx=85, pady=30)
    root.configure(background='sienna')
    
# layout all of the main containers
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    top_frame.grid(row=0, sticky="ew")
    center.grid(row=1, sticky="ns")

# create the widgets for the top frame
    title = Label(top_frame, text=" CRAZY EIGHTS ", bg='red3', fg ="ivory", height=1, relief="raised", borderwidth=2, font=("system", 24))
    head = Label(top_frame, textvariable=header, bg='red3', fg ="ivory", width=90, height=2, relief="raised", borderwidth=2, font=("system", 16))
    bQuit = Button(top_frame, text="Quit", font=("system", 12), height=1, pady=6, padx=16, command=lambda : lose())

# layout the widgets in the top frame
    title.grid(row=0)
    head.grid(row=0, column=1)
    bQuit.grid(row=0,column=2)

# create the center widgets
    center.grid_rowconfigure(0, weight=1)
    center.grid_columnconfigure(1, weight=1)

    scrollbar = Scrollbar(center)                                   # try fix this so scrollreg varies
    ctr_mid = Canvas(center, bg='snow2', width=588, height=40, scrollregion=(0, 0, 100, 1650), yscrollcommand=scrollbar.set)
    scrollbar.configure(command=ctr_mid.yview)
    scrollbar.grid(sticky=NS)

    cmid_frame = Frame(ctr_mid, bg='antiquewhite4',relief= "sunken")
    ctr_right = Frame(center, bg='snow3', width=340, height=40, padx=3, pady=3)

    ctr_mid.grid(row=0, column=1, sticky="nsew")
    ctr_mid.create_window(0,0,window=cmid_frame, anchor='nw')
    ctr_right.grid(row=0, column=2, sticky="ns")

    return(cmid_frame,ctr_mid,ctr_right)


#finalise program (create essential variables)

cmid_frame,ctr_mid,ctr_right = genGUI(header) # this function can't be called before pick() is defined

brn = PhotoImage(file="b.gif")
oge = PhotoImage(file="o.gif")
pnk = PhotoImage(file="p.gif")
prp = PhotoImage(file="pu.gif")
wld = PhotoImage(file="w.gif")
deck = createdeck(brn,oge,pnk,prp,wld)     

global phand_global 
global deck_global 
global discards_global
phand_global = []
deck_global = deck
discards_global = []

# to create some familiarity and context, sounds 1-4 will be for the user & 5-7 for the com
play_sfx = ["wav/D01.wav","wav/D02.wav","wav/D03.wav","wav/D04.wav","wav/D05.wav","wav/D06.wav","wav/D07.wav"]
take_sfx = ["wav/T01.wav","wav/T02.wav","wav/T03.wav","wav/T04.wav","wav/T05.wav","wav/T06.wav","wav/Tk2.wav"]

# create widgets (card buttons) for ctr_mid

def orderbuttons(button,bpos):#  

    for count in range(15):
        condit =6 + (7*count)
        alignment = 0 + (7*count)
        if bpos <= condit:    #will order cards into rows so that they dont go offscreen
            button.grid(row=count, column = bpos-alignment, sticky=W, padx=4, pady=4)  
            bpos = bpos + 1 #increase so each button has unique position
            break
        else:
            continue
        
    
    return(bpos)

#GAMEPLAY functions & procedures

def swap(card, fromm, to):
    for fcard in fromm:
        if card == fcard:
            fromm.remove(card)
            to.append(card)
    return(fromm, to)

#Randomly generate CPU & Player's Hand
def generateHand(deck):
    hand = []
    
    for cards in range(7):                            
        rCID = randint(0, len(deck)-1)#random card ID
        card = deck[rCID]
        deck, hand = swap(card, deck, hand)# assigns 7 random cards to a hand
        
    return(hand, deck)


phand, deck = generateHand(deck)#   player's hand
chand, deck = generateHand(deck)#   computer's hand (not displayed)
#using this function, several computer players can be made

discards = []    #these are the cards that are face up in the middle of the "table" ie the card that's just been placed

def showHand(hand):#will show the given hand (player's) onscreen
    buttons = cmid_frame.grid_slaves()
    if len(buttons) > 0:#if there are already buttons on screen
        for slave in buttons:
            slave.destroy()#clear all buttons before regenerating them
    bposition = 0
    
    for card in hand:
        ID = []
        if card[0] != "wild": cardtext = card[2]
        else: cardtext = " "#blank to show symbol on wild
        cphoto = card[1]
        ID = [card[0],card[2]]#will pass info of card (colour, element) into button input
        button = Button(cmid_frame, image=cphoto, text=cardtext, font=("system", 24), compound = CENTER, command=lambda ID=ID: playUSR(ID, hand, deck, discards,  ))
        button.image = cphoto
        bposition = orderbuttons(button,bposition)
    buttons = cmid_frame.grid_slaves()
    if len(buttons) >0:    
        bStart.config(state = DISABLED)#start button only works once
  
    '''Pick a random card from pick up pile (the deck[] array) and use
    as first card, also to display the currently
    placed card, (top card) in the right hand section:'''
def currentCard(deck, discardpile):
    if discardpile == []:#if no current card, ie game has just begun
        rCID =  randint(0, len(deck)-1)#random card ID
        card = deck[rCID]
        deck, hand = swap(card, deck, discards)     #place random card from deck
        
    topCard = discards[-1]#the last used (discarded) card is the top card, AKA the current card
    
    TCphoto = topCard[1]#assigns image
    TCphoto = TCphoto.zoom(2)
    if topCard[0] != "wild": cardtext = topCard[2]
    else: cardtext = " "#blank to show symbol on wild
    TCpic = Label(ctr_right, image=TCphoto, text=cardtext, font=("system", 46), compound = CENTER, relief="raised",borderwidth=5)
    TCpic.image = TCphoto    #Top Card picture
    TCpic.grid(row =0, column =0,columnspan=5, sticky=N+S+E+W, padx=76, pady=20)

    currentLabel = Label(ctr_right, text=" Current face-up card ", font=("system", 18), relief="groove",borderwidth=2)
    currentLabel.grid(row=1,columnspan=5, pady =4)

    return(deck, discards)

def playCom(hand, deck, currentcards):#when the COM chooses/places a card
    bEND.config(state = DISABLED)
    notify("the COM is thinking...")
    root.after(1500)#some additional time is spent to make it more realistic and obvious that the computer is taking a turn

    currentcard = currentcards[-1]
    comP2 = False
    played = False
    while played == False:
        if currentcard[2] == "+2": #COM must pick up 2 cards and then may play or end turn
            randomNO = randint(0, len(deck)-1)#random card is chosen as deck[] is unshuffled
            card = deck[randomNO]#random card in the 'pick up' pile (deck[])
            deck, hand = swap(card, deck, hand)
            #print("COM has picked up a",card)
            randomNO = randint(0, len(deck)-1)#random card is chosen as deck[] is unshuffled
            card = deck[randomNO]#random card in the 'pick up' pile (deck[])
            deck, hand = swap(card, deck, hand)
            #print("and a",card)
            
        for card in hand:
            if card[2] == currentcard[2] or card[0] == currentcard[0] or card[0]=="wild" or currentcard[0] =="wild":#if the elements/colours match or is wildcard
                swap(card, hand, currentcards)#play this card
                PlaySound(play_sfx[randint(4,6)], SND_NOSTOP | SND_FILENAME | SND_ASYNC)
                notify("COM has played a {} {}.".format(card[0],card[2]))
                if card[2] == "+2": comP2 = True
                
                played = True
                break
            else:
                #if no cards match, must pick up card
                root.after(500)
                swap(deck[-1], deck, hand)
                PlaySound(take_sfx[randint(4,6)], SND_NOSTOP | SND_FILENAME | SND_ASYNC)
                #print("COM has picked up ",deck[-1])
                played = True

    # reactivate player's hud <change this for multiplayer>
    deck, currentcards = currentCard(deck, currentcards)
    bPUC.config(state = NORMAL)
    player_cards = cmid_frame.grid_slaves()
    currentcard = currentcards[-1]
    if comP2 == False:#if COM DID NOT just play a +2
        for button in player_cards:
            button.config(state = NORMAL) #player cannot play a card over +2

    update(phand,deck,discards, hand)
    
    return(hand, deck, currentcard)

def gen_UIbuttons(phand, deck, ctr_right, discards):#this was created to resolve parameter passing errors
    bPUC = Button(ctr_right, text="Pick up card", font=("system", 12), command=lambda : pick(phand, deck, discards), state = DISABLED)#bPUC: button to Pick Up Card
    bPUC.grid(row= 2, column = 0,pady = 20,ipadx = 20,ipady = 10)
    bStart = Button(ctr_right, text="Start", font=("system", 12), command=lambda: showHand(phand))
    bStart.grid(row=2, column=1, pady=20, ipadx=20, ipady=10)
    bEND = Button(ctr_right, text="End turn", font=("system", 12), command=lambda : playCom(chand, deck, discards,  ), state = DISABLED)
    bEND.grid(row= 2, column = 2,pady = 20,ipadx = 20,ipady = 10)

    marquee = Marquee(ctr_right, text=ticker.get(), font=("system", 12), borderwidth=2, relief="sunken")
    marquee.grid(row=3, columnspan=3, sticky=EW, pady=20)

    return(bStart,bEND, bPUC, marquee)
    
def pick(hand, pile, currentcards):
    top_card = currentcards[-1]
    if top_card[2] == "+2": #if the card played is a +2 card you must pick up twice
        repetitions = 2 # # # maybe switch to making user press pick up twice?
    else: repetitions = 1
    for _ in range(repetitions):
        randomNO = randint(0, len(pile)-1)#random card is chosen as deck[] is unshuffled
        card = pile[randomNO]#random card in the 'pick up' pile (deck[])
        pile, hand = swap(card, pile, hand)
        PlaySound(take_sfx[randint(0,3)], SND_NOSTOP | SND_FILENAME | SND_ASYNC)
        notify("you picked up {} {}. pile size: {}.".format(card[0],card[2],len(pile)) )
        root.after(500)

    hand = showHand(hand)
    bEND.config(state = NORMAL) #the end turn button will be valid
        
bStart, bEND, bPUC, marquee = gen_UIbuttons(phand, deck, ctr_right,discards)#generate buttons
   
def playUSR(cardinfo, hand, deck, discards):#called when card is clicked
    cardnum = 0
    currentcard = discards[-1]
    for item in hand:
        if item[0] == cardinfo[0] and item[2] == cardinfo[1]:#if the card matches button pressed
            card = item
            break
        cardnum += 1
    
    if card[2] == currentcard[2] or card[0] == currentcard[0] or card[0] == "wild" or currentcard[0] == "wild":#if the elements/colours match
        valid= True
        
    else:
        valid = False #input validation
        notify("that card cannot be played!!")
        box = Toplevel()
        box.minsize(250,30)
        box.title("Crazy Eights")
        box.iconbitmap('C8.ico')
        msg = Label(box, text="You cannot play that card!")
        msg.pack(pady=12, ipadx= 50)
        button = Button(box, text="Dismiss", command=box.destroy)
        button.pack(pady=10)
    
    if valid == True:
        if len(hand) <= 1:# you win once you play your last card
            playerwin()
        swap(card, hand, discards)
        PlaySound(play_sfx[randint(0,3)],  SND_FILENAME | SND_ASYNC)
        notify("you played a {} {}.".format(card[0],card[2]) )
        bEND.config(state = NORMAL) #the end turn button will be valid
        bPUC.config(state = DISABLED)#cannot pick up a card after playing
        
    #in order for the button to return any values, the parameters must be global
    global phand_global 
    global deck_global 
    global discards_global
    phand_global = hand
    deck_global = deck
    discards_global = discards
    
    update(phand,deck,discards)
    if valid == True:# if just played
        buttons = cmid_frame.grid_slaves()
        for slave in buttons:#disable all cards
            slave.config(state = DISABLED)#will ensure player can only use 1 card per turn
    return()

def update(phand,deck,discards, *args):#called whenever a button is pressed
    
    phand, deck, discards = phand_global, deck_global, discards_global
    
    deck, discards = currentCard(deck, discards)#call this when card is played
    global score
    
    upHUD(header, phand, discards)
    
    phand = showHand(phand)
    
    comcardLabel = Label(ctr_right, text="Opponent's hand size:", font=("system", 16), relief="groove",borderwidth=2)
    comcardLabel.grid(row=4,columnspan=5, pady =7, sticky= "s")
    
    if len(args) > 0:#only when COMs turn is up
        comHand = args[0]
        comHandSize = Label(ctr_right, bg= "darkgreen", fg = "yellow2", text= len(comHand), font=("MS serif", 72), relief="sunken",width=2,borderwidth=4)
        comHandSize.grid(row=4, columnspan=5, pady= 5, ipady= 20, sticky= "s")

        if len(comHand) < 1:
            lose()
            
    else:comHandSize = Label(ctr_right, bg= "darkgreen", fg = "yellow2", text= len(chand), font=("MS serif", 72), relief="sunken",width=2,borderwidth=4).grid(row=4, columnspan=5, pady= 5,  sticky= S,ipady= 20)

    score=int(len(chand) * 100000 / len(discards))
    #print("score",score)
    return(phand, deck, discards, score)

def playerwin():#called when user plays last card

    def finish():
        box.destroy()
        root.destroy()
        import Crazy_Eights #quit game and reopen splash
        
    box = Toplevel(width= 250) #------------------------
    box.title("Congratulations!")
    box.iconbitmap('C8.ico')
    msg = Message(box, text="You have won this game!")#create dialog box
    msg.pack(ipadx=150)
    button = Button(box, text="Return to main menu", command=finish)#quit GUI & open splash
    button.pack(padx=12, pady=36)

    import csv
    with open('Scores.csv', 'a') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=' ', quotechar=',')
        filewriter.writerow([name , score])#add name & score to save file


def lose():#called when computer plays last card [OR user forfeits/quits]

    def finish():
        box.destroy()
        root.destroy()
        import Crazy_Eights #quit game and reopen splash
        
    box = Toplevel(width= 250)
    box.title("Game Over!")

    msg = Message(box, bg= "darkgreen", text="You have lost this game!")#create dialog box
    msg.pack(ipadx=150)
    button = Button(box, text="Return to main menu", command=finish)#quit GUI & open splash
    button.pack(padx=12, pady=36)


name = "jeff"#arbitrary value used before proper assignment
score = 0
phand, deck, discards, score = update(phand,deck,discards)
   
def rungame(fetch):#will be called externally - from splash
    global name
    name = fetch#set player name to parameter given
    
    upHUD(header, phand, discards)

    root.update()
    root.mainloop()
    
    ctr_mid.config(scrollregion=ctr_mid.bbox("all"))
    ctr_mid.mainloop()
    
#root.mainloop()

