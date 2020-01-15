import codecs
import os
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter import ttk, filedialog, scrolledtext
from tkinter.ttk import Combobox
from nltk.tokenize import word_tokenize, sent_tokenize

from numpy import unicode

import backend

def popup_showinfo():
    showinfo("ABOUT US", "This program aims to reduce the number of words in a text! Powered by [TBI][MRA][PR]")


def generate_text(dev, percentage):
    dev.final_text = ""
    final_txt = ""
    text = dev.txt.get("1.0", END)
    percentage = int(percentage[:-1])
    dev.final_text = text

    print(backend.count_of_words(text))

    if backend.summary_status(backend.count_of_words(text),backend.count_of_words(dev.final_text),percentage):
        dev.final_text, len_deleted = backend.removeDialogue(text)
        print("First delete = " + str(len_deleted))
    if backend.summary_status(backend.count_of_words(text), backend.count_of_words(dev.final_text), percentage):
        dev.final_text, len_deleted = backend.remove_brackets(dev.final_text)

        print("Second delete = " + str(len_deleted))
        #print(final_txt)
    if backend.summary_status(backend.count_of_words(text), backend.count_of_words(dev.final_text), percentage):
        dev.final_text, len_deleted = backend.remove_quotes(dev.final_text)

        print("Third delete = " + str(len_deleted))
        #print(final_txt)
    if backend.summary_status(backend.count_of_words(text), backend.count_of_words(dev.final_text), percentage):
        dev.final_text = backend.remove_enum(dev.final_text)

        print("Fourth delete = " + str(backend.count_of_words(text) - backend.count_of_words(dev.final_text)))
        #print(final_txt)
    if backend.summary_status(backend.count_of_words(text), backend.count_of_words(dev.final_text), percentage):

        new_text = dev.final_text
        tokenized_text = sent_tokenize(new_text)
        l_total = backend.count_of_words(new_text)
        dict = backend.words_score(new_text)

        my_list = sorted(dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)

        while backend.summary_status(l_total, backend.words_in_mylist(my_list), percentage):
            if len(my_list) == 1:
                break
            my_list.pop()


        list_of_sentc = []
        for index in my_list:
            list_of_sentc.append(index[0])

        for index in tokenized_text:
            if index in list_of_sentc:
                final_txt = final_txt + index

        print("Algorithm delete: " + str(backend.count_of_words(text) - backend.count_of_words(dev.final_text)))

    print(dev.final_text)
    if final_txt != "":

        dev.final_text = final_txt
    dev.final_text = dev.final_text.rstrip(os.linesep)
    dev.txt_output.delete('1.0', END)
    dev.txt_output.insert(INSERT, dev.final_text)


    label = Label(dev.root, text="Words count: " + str(len(dev.final_text.split(' '))), background="#e0c4d3", fg="#75022d")
    label.place(x=750, y=545)


def function_save_as(dev):
    savelocation = filedialog.asksaveasfilename()
    if savelocation == '':
        return
    with open(savelocation, 'w',encoding='utf-8') as outfile:
        outfile.write(dev.final_text)
        outfile.close()
        showinfo("Successfully!", "You saved your text!")

def function_add_text(dev):
    with codecs.open(filedialog.askopenfilename(filetypes=[("Text files", "*.txt")]), encoding='utf-8') as f:
        dev.final_text = f.read()
        dev.txt.insert(INSERT, dev.final_text)
        f.close()
        showinfo("Successfully!", "You imported your text!")


def main():
    class Final:
        final_text = ""
        root = Tk()
        txt = scrolledtext.ScrolledText(root, undo=True)
        txt_output = scrolledtext.ScrolledText(root, undo=True)

    dev = Final()

    dev.root.geometry("900x650+325+50")
    dev.root.title("Your Summary")
    dev.root.iconbitmap("pics/icon.icon.ico")
    dev.root.resizable(0, 0)
    dev.root.configure(background='#e0c4d3')

    top_line = Frame(dev.root, width=900, heigh=9, bg="#75022d", relief=SUNKEN)
    top_line.pack(side=TOP)

    second_line = Frame(dev.root, width=800, heigh=4, bg="#75022d", relief=SUNKEN)
    second_line.place(x=50, y=240)

    label = Label(dev.root, text="INPUT", background="#e0c4d3", fg="#75022d")
    label.place(x=47, y=357)
    label = Label(dev.root, text="OUTPUT", background="#e0c4d3", fg="#75022d")
    label.place(x=800, y=375)

    middle_line = Frame(dev.root, width=800, heigh=4, bg="#75022d", relief=SUNKEN)
    middle_line.place(x=50, y=375)

    third_line = Frame(dev.root, width=800, heigh=4, bg="#75022d", relief=SUNKEN)
    third_line.place(x=50, y=530)

    bottom_line = Frame(dev.root, width=900, heigh=9, bg="#75022d", relief=SUNKEN)
    bottom_line.pack(side=BOTTOM)

    logo = PhotoImage(file="pics/logo.png")
    logo_label = Label(dev.root, image=logo, borderwidth=0, compound="center", highlightthickness=0)
    logo_label.pack()

    style = ttk.Style()
    style.configure("TButton", background="#75022d")

    dev.txt['font'] = ('consoles', '12')
    dev.txt.pack()
    dev.txt.place(x=50, y=248, height=110, width=800)

    dev.txt_output['font'] = ('consoles', '12')
    dev.txt_output.pack()
    dev.txt_output.place(x=50, y=400, height=120, width=800)

    label = Label(dev.root, text="PERCENTAGE", background="#e0c4d3", fg="#75022d")
    label.place(x=165, y=195)
    v = [str(x) + '%' for x in range(10, 55, 5)]
    combo = Combobox(dev.root, state="readonly", values=v, width=15, height=19)
    combo.set("10%")
    combo.place(x=151, y=213)

    button_add_input = ttk.Button(dev.root, text="IMPORT", style="TButton", command=lambda: function_add_text(dev))
    button_add_input.place(x=53, y=200, height=35)

    button_showinfo = ttk.Button(dev.root, text="About", style="TButton", command=popup_showinfo)
    button_showinfo.place(x=800, y=600)

    button_generate = ttk.Button(dev.root, text="Generate", style="TButton", command=lambda: generate_text(dev, combo.get()))
    button_generate.place(x=340, y=550, height=35)

    button_save_as = ttk.Button(dev.root, text="Save As", style="TButton", command=lambda: function_save_as(dev))
    button_save_as.place(x=450, y=550, height=35)

    dev.root.mainloop()


main()
