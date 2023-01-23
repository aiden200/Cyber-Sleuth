import tkinter as tk
import get_traces

#Runs main when the button is pressed, had to delete call to main at end of get_traces so it didn't run twice
def load_frame2():
    get_traces.main()

#build crhome profile, had to get rid of call in main
def load_frame3():
    get_traces.build_chrome_profile()

def load_frame4():
    get_traces.main()

#sets up the window
index = tk.Tk()
index.title("Web Profiler")
index.eval("tk::PlaceWindow . center")
frame1 = tk.Frame(index, width=600, height=500, bg="#95B9C7")
frame1.grid(row=0, column=0)
frame1.pack_propagate(False)

#Welcome
tk.Label(frame1, text="Welcome to the Web Profiler", bg="#95B9C7", fg="white", font=("TkMenuFont", 14)).pack()

#Three different buttons for background noise, chrome profile, and chosen website
tk.Button(frame1, text="Profile Computer Background", font=("TkHeadingFont", 20), bg="#95B9C7", fg="black", cursor="hand", activebackground="#95B9C7", activeforeground = "black", command=lambda:load_frame2()).pack(pady=30)
tk.Button(frame1, text="Profile Browser Background", font=("TkHeadingFont", 20), bg="#95B9C7", fg="black", cursor="hand", activebackground="#95B9C7", activeforeground = "black", command=lambda:load_frame3()).pack(pady=30)
tk.Button(frame1, text="Profile Chosen Websites", font=("TkHeadingFont", 20), bg="#95B9C7", fg="black", cursor="hand", activebackground="#95B9C7", activeforeground = "black", command=lambda:load_frame2()).pack(pady=30)

index.mainloop()