'''
Created by Aiden Chang

WARNING:
    You will need to install tkinter, seprate from your virtual environment
        for mac: $ brew install python-tk
        for windows: $ sudo apt-get install python3-tk
'''


import tkinter as tk                # python 3
from tkinter import font as tkfont  # python 3
from tkinter import filedialog # python 3
from scapy.all import *
import os
import shutil


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=25, weight="bold", slant="italic")
        self.sub_title_font = tkfont.Font(family='Helvetica', size=15)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)



        self.frames = {}
        for F in (StartPage, InstructionsPage, BackgroundPage, ProfilePage, UploadTracePage, AboutPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("StartPage")


        
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        # frame.winfo_toplevel().geometry("")
        frame.tkraise()



class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Trace Analyzer", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        sub_label = tk.Label(self, text="Please read the instructions to get started!", font=controller.sub_title_font)
        sub_label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Instructions",
                            command=lambda: controller.show_frame("InstructionsPage"))
        button2 = tk.Button(self, text="Build Background Profile",
                            command=lambda: controller.show_frame("BackgroundPage"))
        button3 = tk.Button(self, text="Build Profile for a Website",
                            command=lambda: controller.show_frame("ProfilePage"))
        button4 = tk.Button(self, text="Upload Your Own Trace",
                            command=lambda: controller.show_frame("UploadTracePage"))
        button5 = tk.Button(self, text="About", highlightbackground='grey', height= 5, width=10,
                            command=lambda: controller.show_frame("AboutPage"))
        button6 = tk.Button(self, text="Quit", highlightbackground='grey', height= 5, width=10, 
                            command=controller.destroy)
        # button5 = tk.Button(self, text="Exit", command=self.destroy)
        button1.pack()
        button2.pack()
        button3.pack()
        button4.pack()
        button5.pack(anchor="s", side="right")
        button6.pack(anchor="s", side="left")
        


class InstructionsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Instructions", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Back to Start Page",
            highlightbackground='grey', height= 5, width=12,
            command=lambda: controller.show_frame("StartPage"))
        button.pack(anchor="s", side="left")


class BackgroundPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Tracing Computer Background", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Back to Start Page",
            highlightbackground='grey', height= 5, width=12,
            command=lambda: controller.show_frame("StartPage"))
        button.pack(anchor="s", side="left")


class ProfilePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Building a Web Profile", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Back to Start Page",
            highlightbackground='grey', height= 5, width=12,
            command=lambda: controller.show_frame("StartPage"))
        button.pack(anchor="s", side="left")


#User uploads pcap and pcapng files to UploadTraces Page
def UploadPcap(pkt=None):
        filename = filedialog.askopenfilename(title="Choose a File...", filetypes=(('Pcap Files', '.pcap .pcapng' ),))
    #get file pathway
        file = open(str(filename), 'rb')
        print(str(file))
        translate = str(file)
        id1 = translate.index("=")
        id2 = translate.index("'>")
        path = ''
        for i in range(id1 + len("=") + 1, id2):
            path = path + translate[i]
    #open new directory for uploaded traces``
        if filename:
            NEWDIR = (f"Uploaded Traces")
            if not os.path.isdir(NEWDIR):
                os.makedirs(NEWDIR)
#copies file from user's directory into Uploaded Traces folder
        with open(f"Uploaded Traces/{os.path.basename(str(filename))}",'w') as f:
            shutil.copy(path, NEWDIR)
        file_label = tk.Label(text=str(os.path.basename(str(filename))))
        file_label.place(relx = 0.5, rely = 0.5, anchor ='center')




class UploadTracePage(tk.Frame):
            
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Upload Trace Here!", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        upload_button = tk.Button(self, text="Choose a File...", command=lambda:UploadPcap())
        upload_button.pack()
        back_button = tk.Button(self, text="Back to Start Page",
            highlightbackground='grey', height= 5, width=12,
            command=lambda: controller.show_frame("StartPage"))
        back_button.pack(anchor="s", side="left")




class AboutPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="About This Project", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Back to Start Page",
            highlightbackground='grey', height= 5, width=12,
            command=lambda: controller.show_frame("StartPage"))
        button.pack(anchor="s", side="left")



if __name__ == "__main__":
    app = SampleApp()
    app.geometry("800x500")
    app.mainloop()

'''
pass
import tkinter as tk
from tkinter import filedialog

def UploadAction(event=None):
    filename = filedialog.askopenfilename()
    print('Selected:', filename)

root = tk.Tk()

#Root is the window, this has to do with the window 
root.title('Hello Python')
root.geometry("300x200+10+10")

#Buttons and gagets 
button = tk.Button(root, text='Open', command=UploadAction)
button.pack()


btn=Button(window, text="This is Button widget", fg='blue')
btn.place(x=80, y=100)
# lbl=Label(window, text="This is Label widget", fg='red', font=("Helvetica", 16))
# lbl.place(x=60, y=50)

# txtfld=Entry(window, text="This is Entry Widget", bd=5)
# txtfld.place(x=80, y=150)



root.mainloop()
'''