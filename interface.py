'''
Created by Aiden Chang

WARNING:
    You will need to install tkinter, seprate from your virtual environment
        for mac: $ brew install python-tk
        for windows: $ sudo apt-get install python3-tk
'''


import tkinter as tk                # python 3
from tkinter import font as tkfont  # python 3


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
        for F in (StartPage, PageOne, PageTwo):
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
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="Build Background Profile",
                            command=lambda: controller.show_frame("PageTwo"))
        button3 = tk.Button(self, text="Build Profile for a Website",
                            command=lambda: controller.show_frame("PageTwo"))
        button4 = tk.Button(self, text="Upload Your Own Trace",
                            command=lambda: controller.show_frame("PageTwo"))
        # button5 = tk.Button(self, text="Exit", command=self.destroy)
        button1.pack()
        button2.pack()
        button3.pack()
        button4.pack()
        # button5.pack(side="bottom", pady=10) . 


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.geometry("800x600")
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