from tkinter import *
from functools import partial
import random
import numpy as np

#Valori default
epoch = 1000
err_max = 0.001
hidden_layer = 10
learning_rate = 0.5
number_inputs = 7
output_led = 10
output_numar = 10
numar_led = np.array([
[1, 1, 1, 0, 1, 1, 1],
[0, 0, 1, 0, 0, 1, 0],
[1, 0, 1, 1, 1, 0, 1],
[1, 0, 1, 1, 0, 1, 1],
[0, 1, 1, 1, 0, 1, 0],
[1, 1, 0, 1, 0, 1, 1],
[1, 1, 0, 1, 1, 1, 1],
[1, 0, 1, 0, 0, 1, 0],
[1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 0, 1, 1]])
numar_binar = np.array([
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 1]])

linii_aprinse = [0, 0, 0, 0, 0, 0, 0]

def sigmoid(act):
    return 1/(1+np.exp(-act))

def forward():
    result = np.dot(numar_led,weight_input_to_hidden)
    result2 = sigmoid(result)
    result3 = np.dot(result2,weight_hidden_to_output)
    end_result = sigmoid(result3)
    return end_result,result2

def sigmoidPrime(var):
    return var*(1-var)

def backward(weight_input_to_hidden, weight_hidden_to_output,result_forward,result2_forward):
    error = numar_binar - result_forward
    delta = error*sigmoidPrime(error)

    error2 = delta.dot(weight_hidden_to_output.T)
    delta2 = error2*sigmoidPrime(result2_forward)
    weight_input_to_hidden += numar_led.T.dot(delta2)
    weight_hidden_to_output += result2_forward.T.dot(delta)

def train(weight_input_to_hidden, weight_hidden_to_output):
    result_forward,result2_forward = forward()
    backward(weight_input_to_hidden, weight_hidden_to_output,result_forward,result2_forward)

matrix = []
for index in range(0,11):
    l = []
    for index2 in range(0,11):
        l.append(round(random.random(),2))
    matrix.append(l)
weight = np.array(matrix)

weight_input_to_hidden = np.random.randn(number_inputs,output_led)
weight_hidden_to_output = np.random.randn(output_led,output_numar)
max_line = np

train(weight_input_to_hidden,weight_hidden_to_output)

def setLine(string,value):
    if string == "TOP":
        linii_aprinse[0] = value
    if string == "MID":
        linii_aprinse[3] = value
    if string == "TOPMIDLEFT":
        linii_aprinse[1] = value
    if string == "TOPMIDRIGHT":
        linii_aprinse[2] = value
    if string == "BOT":
        linii_aprinse[6] = value
    if string == "BOTMIDLEFT":
        linii_aprinse[4] = value
    if string == "BOTMIDRIGHT":
        linii_aprinse[5] = value

##############GUI####
#COLORS:
#PINK = #ce9e8a
#GREEN = #a5d206

def solve(event):
    count = 0
    for index in numar_led:
        l = []
        for i in index:
            l.append(i)
        if l == linii_aprinse:
            print(str(numar_binar[count]))
            setAnswer.set("Answer: "+ str(count))
            return
        count += 1
        setAnswer.set("Answer: -1")

def toggle(button):
    # daca butonul e verde
    if button['bg'] == '#a5d206':
        button['bg'] = '#ce9e8a'
        button['fg'] = '#ce9e8a'
        setLine(button['text'],0)
    else:
        button['bg'] = '#a5d206'
        button['fg'] = '#a5d206'
        setLine(button['text'], 1)
    print(linii_aprinse)
root = Tk()

root.geometry("600x500+0+0")
root.title("Number backpropagation")
root.resizable(0,0)

Top_line = Frame(root, width = 600, heigh = 2, bg = "#ce9e8a", relief = SUNKEN)
Top_line.pack(side = TOP)

Bottom_line = Frame(root, width = 600, heigh = 2, bg = "#ce9e8a", relief = SUNKEN)
Bottom_line.pack(side = BOTTOM)


epoch_label = Label(root,text = "NR Epoci",fg = "black")
epoch_label.place(x=50,y=50)
epoch_entry = Entry(root)
epoch_entry.insert(END, '1000')
epoch_entry.place(x = 50, y = 70)

neurons_label = Label(root,text = "Neuroni",fg = "black")
neurons_label.place(x=50,y=105)
neurons_entry = Entry(root)
neurons_entry.insert(END, '10')
neurons_entry.place(x = 50, y = 125)

rate_label = Label(root,text = "Rata de inv.",fg = "black")
rate_label.place(x=50,y=145)
rate_entry = Entry(root)
rate_entry.insert(END, '0.5')
rate_entry.place(x = 50, y = 165)

err_label = Label(root,text = "Neuroni",fg = "black")
err_label.place(x=50,y=185)
err_entry = Entry(root)
err_entry.insert(END, '0.001')
err_entry.place(x = 50, y = 205)


def setData():
    epoch = int(epoch_entry.get())
    hidden_layer = int(neurons_entry.get())
    learning_rate = float(rate_entry.get())
    err_max = float(err_entry.get())
    print("Datele au fost actualizate: Epoch = " + str(epoch) + " Neuroni = " + str(hidden_layer) + "Rata de intarziere = " + str(learning_rate) + " Eroarea maxima = " + str(err_max))

btn = Button(root, text='SET DATA',width=10,heigh = 2,fg = "yellow", bg='black', activebackground='black', relief=GROOVE, command = setData)
btn.place(x=50,y=235)


#Answer label
setAnswer = StringVar()
answer = Label(root,textvariable=setAnswer,fg = "black")
answer.place(x = 264, y = 400)

#TOP BUTTON
b1 = Button(root, text='TOP',width=22,heigh = 1,fg = "#ce9e8a", bg='#ce9e8a', activebackground='black', relief=GROOVE )
b1['command'] = partial(toggle, b1)
b1.place(x=209,y=100)

#MID BUTTON
b2 = Button(root, text='MID',width=22,heigh = 1,fg = "#ce9e8a", bg='#ce9e8a', activebackground='black', relief=GROOVE )
b2['command'] = partial(toggle, b2)
b2.place(x=209,y=200)

#TOPMID LEFT
b3 = Button(root, text='TOPMIDLEFT',width=1,heigh = 4,fg = "#ce9e8a", bg='#ce9e8a', activebackground='black', relief=GROOVE )
b3['command'] = partial(toggle, b3)
b3.place(x=210,y=127)

# TOPMID RIGHT
b4 = Button(root, text='TOPMIDRIGHT',width=1,heigh = 4,fg = "#ce9e8a", bg='#ce9e8a', activebackground='black', relief=GROOVE )
b4['command'] = partial(toggle, b4)
b4.place(x=355,y=127)

#BOT
b5 = Button(root, text='BOT',width=22,heigh = 1,fg = "#ce9e8a", bg='#ce9e8a', activebackground='black', relief=GROOVE )
b5['command'] = partial(toggle, b5)
b5.place(x=209,y=300)

#BOTMID LEFT
b6 = Button(root, text='BOTMIDLEFT',width=1,heigh = 4,fg = "#ce9e8a", bg='#ce9e8a', activebackground='black', relief=GROOVE )
b6['command'] = partial(toggle, b6)
b6.place(x=210,y=227)

#BOTMID RIGHT
b7 = Button(root, text='BOTMIDRIGHT',width=1,heigh = 4,fg = "#ce9e8a", bg='#ce9e8a', activebackground='black', relief=GROOVE )
b7['command'] = partial(toggle, b7)
b7.place(x=355,y=227)

b8 = Button(root, text='GENERATE',width=10,heigh = 2,fg = "yellow", bg='black', activebackground='black', relief=GROOVE)
b8.bind("<Button-1>",solve)
b8.place(x=250,y=350)


root.mainloop()

