import threading
from pytube import YouTube
import clipboard
import keyboard
import re
import time
from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import ttk
import os
import requests
size = 1
percent = 0
def onProcess(stream, chunk, remaining):
    global percent
    old = percent
    percent = int(100*(size-remaining)/size)
    if(old != percent):
        # labelbar.config(f"{percent}% downloaded\n")
        bar['value'] = percent

def isYoutubeVideo(url):
    if(re.search('watch\?v=',url)):
        return True
    return False

def download(link="",prefix=""):
    if(not isYoutubeVideo(link)):
        link = url.get()
    if(isYoutubeVideo(link)):
        log.config(state='normal')
        log.insert('1.0',str(time.strftime("%I:%M:%S%p "))+'Retrieving '+link.strip()+'\n')
        log.config(state='disabled')
    else:
        log.config(state='normal')
        log.insert('1.0',str(time.strftime("%I:%M:%S%p "))+"Please check your url\n")
        log.config(state='disabled')
        return 0
    isDownloading = False
    for i in range(10):
        try:
            yt = YouTube(link, on_progress_callback=onProcess)
            isDownloading = True
        except:
            print("retrying...")
            continue
        log.config(state='normal')
        log.insert('1.0',str(time.strftime("%I:%M:%S%p "))+'Downloading '+yt.title+'\n')
        log.config(state='disabled')
        global size
        video = yt.streams.filter(progressive=True).first()
        size = video.filesize
        video.download(path.get(),filename_prefix=prefix)
        log.config(state='normal')
        log.insert('1.0',str(time.strftime("%I:%M:%S%p "))+f'Downloaded {yt.title}\n')
        log.config(state='disabled')
        break
    if(not isDownloading):
        log.config(state='normal')
        log.insert('1.0',"Check URL and try again!\n")
        log.config(state='disabled')

def links_from_playlist(url):
    links = {}
    response = str(requests.get(url).content)
    title = response[re.search('"title":"',response).span()[1]:re.search('","contents"',response).span()[0]]
    path.insert(END,f'\{title}')
    while(1):
        i = response.find('/watch?v=')
        if(i == -1):
            break
        response = response[i+1:]
        i = response.find('"')
        link = response[:i]
        if(re.search('watch\?v=.*index=\d*$',link)):
            n = int(re.search('\d*$',link).group())
            links[n] = ("https://www.youtube.com/" + link)
    return links

def copyToDownload():
    tk.destroy()
    while(1):
        time.sleep(0.2)
        if(keyboard.is_pressed('ctrl + c')):
            link = clipboard.paste()
            if(re.match(r"https://www.youtube.com/watch\?v=.*",link)):
                print("fetching video.....")
                t = threading.Thread(target=download,args=(link))
                t.start()
        if(keyboard.is_pressed('q')):
            keyboard.press_and_release('backspace')
            break

def download_playlist():
    links = links_from_playlist(url.get())
    for i in sorted(links):
        download(links[i],str(i))
        # print(links[i][:43])
        # t[i] = threading.Thread(target =  download, args = (links[i]))
        # t[i].start()

def fileDialog():
    path.delete(0,END)
    path.insert(0,filedialog.askdirectory(initialdir =  os.path.expanduser("~\Downloads"), title = "Select A Folder" ))

def enterHandler(e):
    if(isYoutubeVideo(url.get())):
        if(url.get().find('list') == -1):
            download_btn.invoke()
        else:
            playlist_btn.invoke()

if __name__ == "__main__":
    tk = Tk()
    tk.iconphoto(False,PhotoImage(file = "E:/PyApps/bot/logo-short.png"))
    tk.config(bd=5)
    tk.title("Youtube Downloader By CODEVER")
    tk.resizable(0,0)
    tk.grid_rowconfigure(0, weight=1)
    tk.grid_columnconfigure(0, weight=1)
    tk.grid_columnconfigure(1, weight=1)
    tk.geometry('500x520')
    f= Frame()
    path = Entry(f,bd=3,width=70)
    path.insert(0,os.path.expanduser("~\Downloads\YouTube"))
    path.pack(side=LEFT)
    browse = Button(f,text='Browse',command=fileDialog)
    browse.pack(side=LEFT,ipadx=10)
    url = Entry(bd=3)
    if(isYoutubeVideo(clipboard.paste())):
        url.insert(0,clipboard.paste())
    url.selection_range(0, END)
    url.focus_set()
    url.bind('<Return>',enterHandler)
    copy_to_download_btn = Button(tk,text="Ctrl+C to Download", command=copyToDownload)
    labelbar = LabelFrame(text = 'No video is downloading')
    bar = ttk.Progressbar(labelbar,length=100,maximum=100)
    def downloadinthread():
        t = threading.Thread(target=download)
        t.start()
    download_btn = Button(tk,text="Download", command=downloadinthread)
    playlist_btn = Button(tk,text="Download Playlist", command=download_playlist)
    log = scrolledtext.ScrolledText(bd=5,state='disabled',bg='#000',fg='#fff')
    f.grid(sticky='nsew',row=0,columnspan=3)
    url.grid(sticky="nsew", row=1,columnspan=3,)
    copy_to_download_btn.grid(sticky="ew", row=2)
    download_btn.grid(sticky=W+E, column=1, row=2)
    playlist_btn.grid(sticky="ew", column=2, row=2, ipadx=50)
    log.grid(sticky="nsew", row=3, columnspan=3)
    labelbar.grid(sticky='nsew',row=4,columnspan=3)
    bar.pack(fill='both')
    tk.mainloop()

