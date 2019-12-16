from tkinter import *
from tkinter.messagebox import showinfo
from tkinter import ttk


def popup_showinfo():
    showinfo("ABOUT US", "This program aims to reduce the number of words in a text! Powered by [TBI][MRA][PR]")

def main():
    root = Tk()
    root.geometry("900x450+300+150")
    root.title("Your Summary")
    root.resizable(0, 0)
    root.configure(background='#e0c4d3')

    Top_line = Frame(root, width=900, heigh=9, bg="#75022d", relief=SUNKEN)
    Top_line.pack(side=TOP)

    Bottom_line = Frame(root, width=900, heigh=9, bg="#75022d", relief=SUNKEN)
    Bottom_line.pack(side=BOTTOM)

    logo = PhotoImage(file="pics/logo.png")
    logo_label = Label(root, image=logo, borderwidth=0,compound="center",highlightthickness = 0)
    logo_label.pack()

    style = ttk.Style()
    style.configure("TButton",background="#75022d")


    button_showinfo = ttk.Button(root, text="About",style ="TButton", command=popup_showinfo)
    button_showinfo.place(x=800, y=400)

    root.mainloop()

main()