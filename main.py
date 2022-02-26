import tkinter as tk
from tkinter import font
import webbrowser
import win32gui, win32con
import pyaudio
import speech_recognition as sr
import re
from PIL import Image, ImageTk
from datetime import datetime
from itertools import count
from functools import partial
from links import youtube_link
from g_links import google_link
import os
import random

now = datetime.now()
time = int(now.strftime("%H"))
# cp = "C:/Users/<!!username!!>/AppData/Local/Programs/Opera GX/launcher.exe %s --incognito"
# If you use Chrome, for defaul install location use : cp= " C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"

def no_disturb():
    win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SW_MINIMIZE)


def go_youtube(txt):
    link = youtube_link(txt)
    webbrowser.open_new_tab(link)
    root.after(690, lambda: no_disturb()) # use 550 for a very fast pc || use 1000 for low end pc

def go_google(txt):
    link = google_link(txt)
    webbrowser.open_new_tab(link)
def search_google(txt):
    link = "https://www.google.com/search?q=" + txt
    webbrowser.open_new_tab(link)


def go_wiki(txt):
    link = "https://en.wikipedia.org/wiki/"+txt
    webbrowser.open_new_tab(link)


root = tk.Tk()
canvas=tk.Canvas(root, width=500, height=600)
canvas.grid(rowspan=100)

frame=tk.Frame(root, bg='#090C07')
frame.place(relwidth=1, relheight=1)
frame.grid_location(0,0)



# ================= Richard - Face =================
class ImageLabel(tk.Label):
    """a label that displays images, and plays them if they are gifs"""
    def load(self, richard):
        if isinstance(richard, str):
            richard = Image.open(richard)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(richard.copy().resize((150, 100))))
                richard.seek(i)
        except EOFError:
            pass

        try:
            self.delay = richard.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)

richard = Image.open('richard.gif')
lbl = ImageLabel(root, bg='#090C07')
lbl.grid(row=0)
lbl.load(richard)




# ======================== Welcome Text ==========================
salut="Hello, Sir!"
if (time > 18 and time <=23) or (time >= 0 and time <=6):
    salut="Good Evening, Sir!"
elif time > 6 and time<=11:
    salut="Good Morning, Sir!"
elif time > 11 and time <= 14:
    salut="Good day, Sir!"
elif time > 14 and time <= 18:
    salut="Good Afternoon, Sir!"
salut = salut+ " How can I help you?"
dialog = tk.Label(root, text=salut, font="Consolas", bg='#090C07', fg='#55D300')
dialog.grid(row=3)

#======================== Dialog ==========================

def bot_dialog(txt):
    global y
    ct = '[' + datetime.now().strftime('%H:%M:%S') + ']'
    y = y + 0.05
    if y >= 0.65:
        y = 0.35
    blank = "                                                                                    "
    dialog2 = tk.Label(root, text=blank, font="Consolas 9", bg='#090C07', fg='#55D300')
    dialog2.place(relx=0.1, rely=y)

    say = "»» " + ct + txt
    dialog2 = tk.Label(root, text=say, font="Consolas 9", bg='#090C07', fg='#55D300')
    dialog2.place(relx=0.1, rely=y)


# ======================== Voice Listener ==========================

def voice_cmd():
    init_rec = sr.Recognizer()
    with sr.Microphone() as source:
        audio_data = init_rec.record(source, duration=5)
        try:
            text = init_rec.recognize_google(audio_data)
        except Exception as e:
            say =" I don't think I heared anything sir"
            bot_dialog(say)
        else:
            say =" I'll play:  " + text
            bot_dialog(say)
            go_youtube(text)



# ======================== Decisions ==========================



y=0.3
id=0
jcheck=0
bdir ='D:/'
def actions(tt,k):
    global bdir
    if tt[k].upper() == "PLAY":
        if len(tt) > (k+1):
            target = ' '.join(tt[(k+1):])
            say =" I'll play: " + target
            bot_dialog(say)
            go_youtube(target)
        else:
            say =" Type Play then the name of the song / video you would like to play, sir!"
            bot_dialog(say)
            pass
    elif tt[k].upper() == "GO":
        if len(tt) > (k+1):
            target = ' '.join(tt[(k+1):])
            say = " I'll go to: " + target
            bot_dialog(say)
            go_google(target)
        else:
            say =" Type Go and the destination site name, sir!"
            bot_dialog(say)
            pass
    elif tt[k].upper() == "WIKI":
        if len(tt) > (k+1):
            target = '_'.join(tt[(k+1):])
            say =" I'll wiki: " + target
            bot_dialog(say)
            go_wiki(target)
        else:
            say =" Type Wiki and the text you would like to search on Wikipedia, sir!"
            bot_dialog(say)
            pass
    elif tt[k].upper() == "SEARCH":
        if len(tt) > (k+1):
            target = ' '.join(tt[(k+1):])
            say =" I'll search: " + target
            bot_dialog(say)
            target = '%20'.join(tt[(k + 1):])
            search_google(target)
        else:
            say = " Type Search and the text you would like to search on google, sir!"
            bot_dialog(say)
            pass
    if tt[k].upper() == "CHANGE":
        if len(tt) > (k+2) and tt[(k+1)].upper() == "TO":
            bdir = tt[(k+2)]+':'+'/'
            say = " I'll change current directory to: " + bdir
            bot_dialog(say)
        else:
            say =" Type the name of the partition you want to look into. "
            bot_dialog(say)
            pass
    elif tt[k].upper() == "FIND":
        if len(tt) > (k+2):
            check=0
            ext = tt[(k+2)]
            fname = tt[(k+1)]+'.'+ext
            say =" I found this file in those folders: "
            bot_dialog(say)
            for roots, dirs, files in os.walk(bdir):
                for file in files:
                    if file.endswith(ext) and str(file).upper() == fname.upper():
                        check+=1
                        print(roots + '\ ' + str(file))
                        os.startfile(str(roots))
            if check ==0:
                ct = '['+ datetime.now().strftime('%H:%M:%S') + ']'
                say = "»» "+ ct+" Looks like this file doesn't exist on this partition"
                dialog2 = tk.Label(root, text=say, font="Consolas 9", bg='#090C07', fg='#55D300')
                dialog2.place(relx=0.1, rely=y)
                say =" Change the partition using: change to 'C:/' "
                bot_dialog(say)

        else:
            say = " Please specify the file name and extension (eg: run.exe)"
            bot_dialog(say)
            pass

def tell_a_joke1():
    global id
    global jcheck
    jcheck = 1
    id = random.randint(0,9)
    ff = open(os.getcwd() + "/Vocabulary/Jokes.txt", 'r+')
    for pos, line in enumerate(ff):
        if pos == id:
            say=' ' + str(line)
            bot_dialog(say)

def tell_a_joke2():
    global id
    global jcheck
    jcheck = 0
    ff = open(os.getcwd() + "/Vocabulary/JokesA.txt", 'r+')
    for pos, line in enumerate(ff):
        if pos == id:
            say=' ' + str(line)
            bot_dialog(say)






def retrive(event):
    global y
    ct = '[' + datetime.now().strftime('%H:%M:%S') + ']'
    txt=e1.get()
    e1.delete(0,len(txt))
    y=y+0.05
    if y>=0.65:
        y=0.35
    blank = "                                                                                    "
    dialog1 = tk.Label(root, text=blank, font="Consolas 9", bg='#090C07', fg='#55D300')
    dialog1.place(relx=0.1, rely=y)
    dialog1 = tk.Label(root, text='👤  '+ct+' '+txt, font="Consolas 9", bg='#090C07', fg='#55D300')
    dialog1.place(relx=0.1, rely=y)
    tt = re.split('\W+', txt)
    t=' '.join(tt) if len(tt)>1 else tt[0]
    #print(t) - to see the parsed input
    if t.upper() in open(os.getcwd()+"/Vocabulary/Hi.txt", 'r+').read():
        say = " Hello, Sir!"
        bot_dialog(say)

    elif t.upper() in open(os.getcwd()+"/Vocabulary/WhatJoke.txt", 'r+').read() and jcheck == 1:
        tell_a_joke2()

    elif t.upper() in open(os.getcwd()+"/Vocabulary/Hru.txt", 'r+').read():
        say = " Everything's good, Sir! How about you?"
        bot_dialog(say)
    elif len(tt)>1:
        if tt[0].upper() in open(os.getcwd()+"/Vocabulary/Action.txt").read():
            if len(tt)>2 and tt[0].upper() == "LET" and tt[1].upper() == "S":
                actions(tt,2)
            else:
                actions(tt,0)
                pass
        elif tt[0].upper() == "HEAR" and tt[1].upper() == "ME":
            voice_cmd()
        elif t.lower() == "tell me a joke":
            tell_a_joke1()
        else:
            say = " Hmm, I don't think I understand those words, sir!"
            bot_dialog(say)

            say = " Don't worry. I'll save them somewhere to learn later."
            bot_dialog(say)

            ff = open(os.getcwd() + "/Vocabulary/LearnLater.txt", 'a')
            for ii in range(len(tt)):
                #print(tt[ii]) - to seethe parsed unknown word
                ff.write(tt[ii])
                ff.write('\n')
            ff.close()
            pass
    else:
        say = " Hmm, I don't think I understand those words, sir!"
        bot_dialog(say)

        say = " Don't worry. I'll save them somewhere to learn later."
        bot_dialog(say)

        ff = open(os.getcwd()+"/Vocabulary/LearnLater.txt", 'a')
        ff.write(t)
        ff.write('\n')
        ff.close()
        pass


    # print(y) - to see the curent y axis value

e1=tk.Entry(root,
            bd=3,
            width=50,
            bg='#090C07',
            fg='#55D300',
            font="Consolas 11",
            insertbackground='#55D300',
            selectbackground='#55D300',
            selectforeground='#090C07',
            justify='left',
            insertwidth=5)
e1.grid(row=94)
e1.bind('<Return>', retrive)
SubmitBtn = tk.Button(root,bd=3, text="▲", width=2, height=1, bg='#090C07', fg='#55D300')
SubmitBtn.bind('<Button-1>', retrive)
SubmitBtn.grid(row=95)






root.mainloop()
