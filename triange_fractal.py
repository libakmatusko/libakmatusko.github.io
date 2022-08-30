from math import sqrt
import tkinter as tk

X = 900
Y = 720
root=tk.Tk()
canvas=tk.Canvas(width=X*1.05, height=Y*1.05, bg='yellow')
canvas.pack()

entry1 = tk.Entry(width=10,bg='yellow')
entry1.pack()



#
pisanie_cisel = False
pekne = 8 #pocet riadkov: 2**pekne
pocet_riadkov = 2**pekne
a = (Y) / ((pocet_riadkov-1)*1.5 + 2) #dlzka strany
#
entry1.insert(0,f'{pocet_riadkov}')
#

List = [1]
fillcolor = 'white'

sin60 = 0.86602540378


def rectangles(y, a,):
    len(List)
    i = 0
    for o in range(len(List)-1, -1*len(List), -2):
        rectangle(X/2 - o*a*sin60, y, a, List[i])
        i +=1



def rectangle(x, y, a, i):
    pencolor = 'black'

    if i==1 or i % 2==1:
        fillcolor = 'white'
        pencolor = 'black'
    elif i==0 or i % 2==0:
        fillcolor = 'black'
        pencolor = 'white'
        
    canvas.create_polygon(x, y, x+sin60*a, y-a/2, x+sin60*a, y-3*a/2, x, y-2*a, x-sin60*a, y-3*a/2, x-sin60*a, y-a/2, fill=fillcolor, outline='black')
    if pisanie_cisel==True:
        canvas.create_text(x, y-a, text=str(i), fill=pencolor)
    #canvas.create_rectangle(x, y, x+a, y+a, fill=fillcolor, outline='black')
    canvas.update()


###
#calculate
###
#fraktalita
def calculate():
    Length = len(List)
    List_temporary = [1]
    if Length > 1:
        for i in range(Length-1):
            if pisanie_cisel==True:
                List_temporary.append(List[i] + List[i + 1])
            else:
                if (List[i] + List[i + 1])%2==0:
                    List_temporary.append(0)
                else:
                    List_temporary.append(1)
    List_temporary .append(1)
    return List_temporary 

#
y = 2*a

def fraktal(a, pocet_riadkov):
    for _ in range(int(pocet_riadkov)): #riadky
        #print(List)
        riadok(a)

def riadok(a):
    global List
    global y

    rectangles(y, a)
    y +=1.5*a
    List = calculate()

def znova(event):
    global List

    canvas.delete('all')
    pocet_riadkov = int(float(entry1.get()))
    global y

    List = [1]
    a = (Y) / ((pocet_riadkov-1)*1.5 + 2)
    y = 2*a

    fraktal(a, pocet_riadkov)



root.bind('<Return>', znova)

fraktal(a, int(float(entry1.get())))

canvas.mainloop()
#