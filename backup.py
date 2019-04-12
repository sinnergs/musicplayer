from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk
from pygame import mixer
from mutagen.mp3 import MP3
import threading
import os
import time

root = tk.ThemedTk()
root.get_themes()
root.set_theme('clearlooks')

# create a menu bar
menubar = Menu(root)
root.config(menu=menubar)

statusbar = ttk.Label(root, text="Welcome to Melody", relief=SUNKEN, anchor=W, font='Times 10 italic')
statusbar.pack(side=BOTTOM, fill=X)


def about_us():
    tkinter.messagebox.showinfo('About melody', 'Music player created using python')


playlist = []  # playlist it contains the full path + file name and playlist box contain jst the filename


# full path is req to play the music inside the play_music load func

def browse_file():
    global filename_path
    filename_path = tkinter.filedialog.askopenfilename()
    add_to_playlist(filename_path)


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1


# create a sub menubar
submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=submenu)
submenu.add_command(label="open", command=browse_file)
submenu.add_command(label="Exit", command=root.destroy)

submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=submenu)
submenu.add_command(label="About us", command=about_us)

mixer.init()  # initializing the mixer for music

# root.geometry('300x300')  # change the size of the window
root.title("melody")  # change title
root.iconbitmap(r'image/melody.ico')  # change icon

leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30)

playlistbox = Listbox(leftframe,width = 40)
playlistbox.pack()

addbtn = ttk.Button(leftframe, text=' + ADD', command=browse_file)
addbtn.pack(side=LEFT)


def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)


delbtn = ttk.Button(leftframe, text=' - DEL', command=del_song)
delbtn.pack(side=LEFT, padx=10)

rightframe = Frame(root)
rightframe.pack()

topframe = Frame(rightframe)
topframe.pack()

lengthlabel = ttk.Label(topframe, text="Total Length -: --:--")
lengthlabel.pack(pady=5)

currenttimelabel = ttk.Label(topframe, text="Current Time -: --:-- ", relief=GROOVE)
currenttimelabel.pack()


def show_details(play_it):
    # filelabel['text'] = "Playing" + ' - ' + os.path.basename(play_it)

    file_data = os.path.splitext(play_it)

    if file_data[1] == '.mp3':
        audio = MP3(play_it)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_it)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # Continue - Ignores all of the statements below it. We check if music is paused or not.
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1


def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'Melody could not find the file. Please check again.')


def stop_music():
    mixer.music.stop()
    statusbar['text'] = 'music stop'


paused = FALSE


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = 'music paused'


def set_vol(val):
    volume = float(val) / 100  # set_volume only take values from 0 to 1
    mixer.music.set_volume(volume)  # set the volume


muted = FALSE


def mute_music():
    global muted
    if muted:  # unmute the music
        mixer.music.set_volume(0.7)
        volumebutton.config(image=volumephoto)
        scale.set(70)
        muted = FALSE
    else:  # mute the music
        mixer.music.set_volume(0)
        volumebutton.config(image=mutephoto)
        scale.set(0)
        muted = TRUE


middleframe = Frame(rightframe)
middleframe.pack(padx=30, pady=30)

playphoto = PhotoImage(file='image/play.png')
playbutton = ttk.Button(middleframe, image=playphoto, command=play_music)
playbutton.grid(row=0, column=0, padx=10)

stopphoto = PhotoImage(file='image/stop.png')
stopbutton = ttk.Button(middleframe, image=stopphoto, command=stop_music)
stopbutton.grid(row=0, column=1, padx=10)

pausephoto = PhotoImage(file='image/pause.png')
pausebutton = ttk.Button(middleframe, image=pausephoto, command=pause_music)
pausebutton.grid(row=0, column=2, padx=10)

bottomframe = Frame(rightframe)
bottomframe.pack(padx=10, pady=10)

rewindphoto = PhotoImage(file='image/rewind.png')
rewindbutton = ttk.Button(bottomframe, image=rewindphoto, command=play_music)
rewindbutton.grid(row=0, column=0)

mutephoto = PhotoImage(file='image/mute.png')
volumephoto = PhotoImage(file='image/volume.png')
volumebutton = ttk.Button(bottomframe, image=volumephoto, command=mute_music)
volumebutton.grid(row=0, column=1)

scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(80)
mixer.music.set_volume(0.8)
scale.grid(row=0, column=2, pady=15, padx=30)


def on_closing():
    stop_music()
    root.destroy()


root.protocol('WM_DELETE_WINDOW', on_closing)

root.mainloop()
