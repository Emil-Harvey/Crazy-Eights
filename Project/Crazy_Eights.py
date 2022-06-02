#EH AH Computing Project


from tkinter import *
from tkinter import PhotoImage
from winsound import *



main = Tk()
main.title('Splash')
main.geometry('{}x{}'.format(1000, 790))
main.minsize(1085, 500)
#main.maxsize(1085, 2000)
main.state('zoomed') #fullscreen mode, may add later
main.attributes("-fullscreen", True)
main.iconbitmap('C8.ico')


    
def genGUIx():
    
# create all of the main containers
    top_frame = Frame(main, bg='red3', width=450, height=50, pady=3)
    center = Frame(main, bg='red3', padx=85, pady=30)
    main.configure(background='red3')
    
# layout all of the main containers
    main.grid_rowconfigure(1, weight=1)
    main.grid_columnconfigure(0, weight=1)

    top_frame.grid(row=0, sticky="ew")
    center.grid(row=1, sticky="ns")

# create the widgets for the top frame
    title = Label(top_frame, text="CRAZY EIGHTS", bg='red3', fg ="ivory", font=("MS serif", 72),padx=72, pady=132)    
    title.grid(row=10)
    
# create the center widgets
    center.grid_rowconfigure(0, weight= 1)
    center.grid_columnconfigure(0)
    ctr_mid = Canvas(center, bg='darkgreen', width=588, height=40)
    #cmid_frame = Frame(ctr_mid, bg='yellow2',pady=1000)
    ctr_right = Frame(center, bg='darkgreen', width=340, height=40, padx=3, pady=3)

    ctr_mid.grid(row=0, column=1, sticky="nsew")
    #ctr_mid.create_window(0,0,window=cmid_frame, anchor='nw')
    ctr_right.grid(row=0, column=2, sticky="ns")

    return('cmid_frame',ctr_mid,ctr_right)

#finalise program (create essential variables)

cmid_frame,ctr_mid,ctr_right = genGUIx()

def dynamics(): #initialise dynamic elements (buttons etc)
    Label(ctr_right, text=" Enter Name ", font=("system", 12),bg="darkgreen",fg="yellow2", relief="sunken").grid(row=0, pady = 10)
    namebox = Entry(ctr_right)
    namebox.grid(row=1, pady = 1)
    name = namebox.get()
    start = Button(ctr_right, text="Start New Game", font=("system", 12), command=startgame)
    start.grid(row= 2,pady = 10,padx = 10)
    quitbutton = Button(ctr_right, text="Quit Game", font=("system", 12), bg="palegoldenrod",fg = "#420", command =lambda: main.destroy())
    quitbutton.grid(row= 3, pady = 15, padx = 10, sticky="s")
    return(namebox)

def highscores():#gather, sort & display highscores
    Label(ctr_mid, text=" HIGH SCORES ", font=("system", 24),bg="darkgreen",fg="yellow2", relief="ridge").grid(row=0,padx=30, pady = 10, sticky="ew")
    scoreTable = []
    import csv
    with open('Scores.csv', 'r') as csvfile:
        filereader = csv.reader(csvfile, delimiter=' ', quotechar=',')
        for row in filereader:
            if len(row) > 1:#excludes invalid rows in csv
                scoreTable.append(row)#reads and converts file into 2D array

    # selection sort (modified for 2D array)
    Hiscores = []
    while len(scoreTable) > 0:
        #find maximum value of scoreTable
        hiscore = scoreTable[0]
        for num in range(1,len(scoreTable)):
            entry = scoreTable[num]
            score = int(entry[1])
            if score > int(hiscore[1]):
                hiscore=entry
        #add maximum score to Hiscores & remove from scoreTable
        scoreTable.remove(hiscore)
        Hiscores.append(hiscore)
    #print(Hiscores)
    # now display top 9 high scores on screen    
    for num in range(len(Hiscores)):
        if num < 10:
            Label(ctr_mid, text=Hiscores[num], font=("system", 12),bg="darkgreen",fg="yellow2").grid(row=num+1,padx=10, pady = 1, sticky="ew")
        else:break
    
def startgame():
    text = namebox.get()
    while len(text) < 20:#input validation to ensure names fit in Hiscore box
        text = text.lower()
        main.destroy()
        from GUI import rungame
        rungame(text)

namebox = dynamics()
highscores()

PlaySound("splash.wav", SND_LOOP | SND_FILENAME | SND_ASYNC)


main.mainloop()
