from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from tkinter import font as tkFont # to use fifferent fonts
from PIL import Image, ImageTk # to display a picture as a lable 
from functools import partial # to let call the same function for all the letters depending on the index
import random # to choose secret randomly

string_right_guesses = ""
string_wrong_guesses = ""
wrong_attempt = 0
guessed_count=0

def showpicture(picturename): # display picture of a hangman
    pict = ImageTk.PhotoImage(Image.open(picturename))
    labelpicture.config(image=pict)
    labelpicture.image = pict

def get_rand_word(filename): # get a word randomly from words stored in file
    
    with open(filename,"r") as file:
        words = file.readlines()
        randindex = random.randint(0,len(words)-1)
        secretword = words[randindex].removesuffix("\n")
    
    return secretword

def display_word(): # display secretword in a format _ _ _
    global clist
    clist = [] # list of labels _ _ _
    for i in range(0,len(secretword)):
        clist.append(tkinter.Label(frameletters, text = "_", font = fontchar,bg="white"))
        clist[i].grid(row=0, column=i, padx=10, pady=10)

def choose_letter(index): # what happened if the player presses any letter button index - index of a letter  
    global guessed_count            # a number of letter guessed (e.g. T O_ _ T O guessed count = 4)
    global string_right_guesses     # string variable that stores letter guessed correctly to display them as a lable
    global string_wrong_guesses     # string variable that stores letter guessed incorrectly to display them as a lable
    global wrong_attempt            # stores a number of lost tries to find out when game is over and to hange pictures

    picturename = "hangman"

    getchar = chr(65+index) # get character from a number : 65 - letter 'A'
    message = "You have already tried letter " + getchar
    if getchar in string_right_guesses + string_wrong_guesses: # if a letter was chosen already
        tkinter.messagebox.showinfo(message = message)
    else:
        if getchar in secretword: # if letter is in the secret word
                listbut[index].configure(bg = "lightgreen")                   # letter gets green
                string_right_guesses = string_right_guesses + getchar + " "   # letter is stored in a string of guessed letters
                for i in range(0,len(secretword)):                             
                    if secretword[i] == getchar:
                        index_guessed_letter = i
                        clist[index_guessed_letter].config(text = getchar) # replace undescore with guessed letters
                        guessed_count+=1
                correctletterslabel.config(text = string_right_guesses) # change string of correctly guessed letters
        else:   #if letter is not in the secret word
            listbut[index].configure(bg = "tomato")  # letter gets red
            string_wrong_guesses = string_wrong_guesses + getchar + " "
            incorrectletterslabel.config(text = string_wrong_guesses) #string of letters guessed incorrectly is updated
            wrong_attempt += 1
            picturename += str(wrong_attempt)+".png" # picture depending on a number of wrong tries is shown
            showpicture(picturename)

    if wrong_attempt == 11:        # if the game was lost
        for button in listbut:
            button.configure(state  = DISABLED) # block all buttons
        msg = "Your secret word was " + secretword 
        tkinter.messagebox.showinfo(message = msg)    # displays secret word
        restartbutton.config(state = NORMAL, image = imagerestartvis)   # restart button is available
    if guessed_count == len(secretword): # if the game was won
        showpicture("Winner.png")
        for button in listbut:
            button.configure(state  = DISABLED)  # block all buttons
        restartbutton.config(state = NORMAL, image = imagerestartvis) # restart button is available
    if guessed_count > 0: # if there is at list one letter
        guessedlabeltitle.config(fg="Black") #change font color to make it visible
    if wrong_attempt > 0: # if there is at list one letter
        wrongguessedlabel.config(fg="Black") #change font color to make it visible

def restart():

    global guessed_count
    global string_right_guesses
    global string_wrong_guesses
    global wrong_attempt

    string_right_guesses = "" # get back to start values
    string_wrong_guesses = ""
    wrong_attempt = 0
    guessed_count=0
    for character in clist:
        character.destroy() # delete all buttons
    global secretword
    secretword = get_rand_word("Hangmanwords1.txt") # get secret word randomly 
    display_word() # display a secret word
    showpicture("hangman0.png")
    guessedlabeltitle.config(fg="White")
    wrongguessedlabel.config(fg="White")

    correctletterslabel.config(text = "")
    incorrectletterslabel.config(text="")

    for button in listbut:
        button.configure(state = NORMAL, bg = "white")
    restartbutton.config(state = DISABLED, image = imagerestartinvis)

string_right_guesses = ""
string_wrong_guesses = ""
wrong_attempt = 0
guessed_count=0

window = tkinter.Tk() #create a window
window.title("Hangman")

fontchar = tkFont.Font(family="Comic Sans MS", weight="bold",size=36) 
fontArial_12 = tkFont.Font(family="Arial", size=12,slant="italic")
fontbutton = tkFont.Font(family="Comic Sans MS", weight="bold",size=16)
imagerestartvis=ImageTk.PhotoImage(file="restart_button.png")
imagerestartinvis=ImageTk.PhotoImage(file="restart_button_i.png")

frame = tkinter.Frame(window,background="white",borderwidth=0)
frame.pack()

subframe0 = tkinter.LabelFrame(frame,background="white",borderwidth=0) #display letters in a word _ _ _ _ and hidden restartbutton 
subframe0.grid(row = 0, column = 0)

secretword = get_rand_word("Hangmanwords1.txt")

frameletters = tkinter.Frame(subframe0,background="white",borderwidth=0)
frameletters.grid(row = 0, column = 0)

display_word() 

restartpicture = ImageTk.PhotoImage(file="restart_button_i.png")
restartbutton = tkinter.Button(subframe0,image = restartpicture, borderwidth=0, background="white", command = restart, state = DISABLED)
restartbutton.grid(row=0, column=1, padx=10, pady=10)
subframe1 = tkinter.LabelFrame(frame,background="white",borderwidth=0) # frame where picture, list of write and wrong guesses are located
subframe1.grid(row = 1, column = 0)

image = ImageTk.PhotoImage(Image.open('hangman0.png'))
framepicture = tkinter.LabelFrame(subframe1,background="white",borderwidth=0)   #frame where picture of a hangman is located text = "Hangman"
framepicture.grid(row = 0, column = 0, padx=5, pady=5)
labelpicture = Label(framepicture, image = image,borderwidth=0)
labelpicture.grid()

frameguess = tkinter.LabelFrame(subframe1, width =50,borderwidth=0, background="white") # frame where _ _ _ _, list of write and wrong guesses are located # former "process"
frameguess.grid(row = 0, column = 1,padx=5, pady=5)

guessedlabeltitle = tkinter.Label(frameguess,text = "You guessed correctly: ", font=fontArial_12,background="white",fg="white") #frame where right letters are displayed
guessedlabeltitle.grid(row = 0,column=0)

correctletterslabel = tkinter.Label(frameguess,text = string_right_guesses,justify="left", anchor="nw", font =  tkFont.Font(family="Comic Sans MS",size=12),wraplength=165,bg="white")
correctletterslabel.grid(row=1,column=0)
correctletterslabel.config(width=15, height = 5)

wrongguessedlabel = tkinter.Label(frameguess,text = "You guessed incorrectly:",font=fontArial_12,background="white",fg="white")
wrongguessedlabel.grid(row=2,column=0)

incorrectletterslabel = tkinter.Label(frameguess,text = string_wrong_guesses,justify="left", anchor="nw", font =  tkFont.Font(family="Comic Sans MS",size=12),wraplength=165,bg="white")
incorrectletterslabel.grid(row=3,column=0)
incorrectletterslabel.config(width=15,height = 5)

framebuttons = tkinter.LabelFrame(frame,borderwidth=0,bg="white") # frame where buttons are located
framebuttons.grid(row = 2, column = 0)

listbut = []

for index,letter in enumerate(range(65,91)):     # chr(number), where number - integer - symbol. 65-91 are uppercase letters enumerare will print inxex 0A 1B 2C etc.
    letter = chr(letter)
    listbut.append(tkinter.Button(framebuttons, bg="white", text = letter, height = 1, width = 3, font = fontbutton, borderwidth=0, command = partial(choose_letter, index))) #all the buttons will evoke the same function depending on index
    listbut[-1].grid(row=index//13,column=index%13, padx=5, pady=5)

window.mainloop() #"close" a window