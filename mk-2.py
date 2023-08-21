from tkinter import *
from time import ctime
from random import sample
from functools import partial
import tkinter.messagebox as msg

#==================================== Main Game =======================================#

def game():
    row=[r*3+g for r in sample(range(3),3) for g in sample(range(3),3)]
    col=[r*3+g for r in sample(range(3),3) for g in sample(range(3),3)]
    num=sample(range(1,10),9)
    board=[[num[(3*(r%3)+r//3+c)%9] for c in col] for r in row]
    dup,dup3=[],[]
    for i in range(len(board)):
        for j in board[i]:
            dup.append(j),dup3.append(j)
    for i in sample(range(81),48):
        dup[i]=" "
    return dup,dup3

#==================================== Global Variables =================================#

gs=[]
no,bl,allnum,frame,btn=" ",[],[],[],[]
start_widget=[]
menu,game_frames=[],[]
howto=[]
all_moves,flag=[],0
erase=False
fin_flag,start=0,0

#==================================== Start Page =======================================#

def start_page():
    global start_widget
    b1=Label(root,bg='gray',height=1)
    b1.pack()
    wel=Label(root,bg='gray',text="Welcome!!!",fg="white",font=('arial',28,'bold'))
    wel.pack()
    b2=Label(root,bg='gray',height=2)
    b2.pack()
    start=Button(root,bg="white",text='Start Game',relief=RIDGE,bd=3,width=10,
                 font=('times new roman',19),command=start_game)
    start.pack()
    b3=Label(root,bg='gray')
    b3.pack()
    htp=Button(root,bg="white",text='How To Play',relief=RIDGE,bd=3,width=10,
                 font=('times new roman',19),command=howtoplay)
    htp.pack()
    b4=Label(root,bg='gray')
    b4.pack()
    iext=Button(root,bg="white",text='Exit',relief=RIDGE,bd=3,width=10,
                 font=('times new roman',19),command=iexit)
    iext.pack()
    start_widget=[b1,wel,b2,start,b3,htp,b4,iext]

def iexit():
    con=msg.askyesno("Confirm Exit?","Are you sure you want to leave?")
    if con==1:
        root.destroy()

#================================= How To Play Page ====================================#

def howtoplay():
    global howto
    for i in start_widget:
        i.destroy()
    b1=Label(root,text="The Game Of \nNumbers",bg="gray",fg='white',height=2,
             font=('times',30,'bold'))
    b1.pack()
    b2=Label(root,text='''Sudoku is played on a grid of 9x9
spaces. With in the columns and
rows are 9 squares. Each square
needs to be filled out with the
numbers 1-9, without repeating
any numbers with in the column,
row or square. Select the number
to fill from blue boxes and fill
all the empty boxes by clicking
on them.''',
             height=11,bg="gray",fg='white',font=('times',15,'bold'))
    b2.pack()
    ok=Button(root,text='Go Back',bg='white',font=('times',14),relief=RIDGE,bd=5,
              command=returnback)
    ok.pack()
    howto=[b1,b2,ok]

def returnback():
    global howto
    for i in howto:
        i.destroy()
    start_page()
    howto=[]

#==================================== Game Page ========================================#

def start_game():
    for i in start_widget:
        i.destroy()
    game_layout()

def game_layout():
    global menu,game_frames,gs,start
    start=ctime()[11:19]
    gs=game()
    menubar=Menu(root)
    menubar.add_command(label="New Game",command=partial(change_game,0))
    menubar.add_command(label="Restart",command=partial(change_game,1))
    menubar.add_command(label="Undo",command=undo)
    menubar.add_command(label="Eraser",command=eraser)
    menubar.add_command(label="Check",command=check)
    root.config(menu=menubar)
    menu=menubar
    k=0
    for i in range(9):
        frame.append(Frame(root,height=10,width=15,bg="gray"))
        frame[i].pack()
        btn.append([])
        if i==3 or i==6:
            bl.append(Label(frame[i],height=1,width=1,bg="gray",font=('arial',3)))
            bl[k].pack()
            k+=1
        for j in range(9):
            if j==3 or j==6:
                bl.append(Label(frame[i],height=1,width=1,bg="gray",font=('arial',3)))
                bl[k].pack(side=LEFT)
                k+=1
            btn[i].append(Button(frame[i],relief=RIDGE,height=1,width=2,text=gs[0][i*9+j]
                                 ,bg='black',fg='white',font=('arial',12,'bold')))
            btn[i][j].pack(side=LEFT,padx=1,pady=1)
            btn[i][j]['command']=partial(number_ent,i,j)
            if btn[i][j]["text"]!=' ':
                btn[i][j]["activebackground"]='red'
    b1=Label(root,width=20,bg="gray")
    b1.pack()
    main_f=Frame(root,height=8,width=15,bg="gray")
    main_f.pack()
    for i in range(9):
        allnum.append(Button(main_f,bd=2,text=i+1,bg="steel blue",fg="white",
                             font=('courier',12,'bold'),relief=RIDGE,height=1,width=2))
        allnum[i].pack(side=LEFT,padx=2)
        allnum[i]['command']=partial(number_ch,i+1)
    b2=Label(root,height=1,width=20,bg="gray")
    b2.pack()
    fin=Frame(root,height=10,width=15,bg="gray")
    fin.pack()
    btn_fin=Button(fin,width=8,text="Go Back",font=('times new roman',14),relief=RIDGE,
                   command=goback)
    btn_fin.pack(side=LEFT,padx=13)
    btn_res=Button(fin,width=8,text="Finish",font=('times new roman',14),relief=RIDGE,
                   command=finish_game)
    btn_res.pack(side=LEFT,padx=13)
    game_frames=[b1,main_f,b2,fin]

#==================================== Game Functions ===================================#

def number_ch(i):
    global no,erase
    erase=False
    if no==i:
        no=" "
        for i in range(9):
            allnum[i]['bg']='steel blue'
            for j in range(9):
                btn[i][j]['bg']='black'
    else:
        no=i
        for i in range(9):
            if allnum[i]['text']==no:
                allnum[i]['bg']='black'
            else:
                allnum[i]['bg']='steel blue'
            for j in range(9):
                if btn[i][j]['text']==no:
                    btn[i][j]['bg']='steel blue'
                else:
                    btn[i][j]['bg']='black'

def number_ent(x,y):
    global flag,erase 
    if flag!=0:
        flag-=1
    if erase==True and gs[0][x*9+y]==' ':
        btn[x][y]['text']=' '
        btn[x][y]['bg']='black'
    elif gs[0][x*9+y]==' ' and no!=' ':
        btn[x][y]['text']=no
        btn[x][y]['bg']='steel blue'
        all_moves.append((x,y))

def goback(n=1):
    global frame,menu,game_frames,btn,bl,allnum
    if n==1:
        con=msg.askyesno("Leave?","Are you sure you want to leave")
    else:
        con=1
    if con==1:
        menu.destroy()
        for i in frame:
            i.destroy()
        for j in game_frames:
            j.destroy()
        for i in btn:
            for j in i:
                j.destroy()
        for i in bl:
            i.destroy()
        for i in allnum:
            i.destroy()
        start_page()
        frame,menu,game_frames,btn,bl,allnum=[],[],[],[],[],[]

def finish_game():
    global fin_flag
    for i in range(9):
        for j in range(9):
            if btn[i][j]['text']!=gs[1][i*9+j]:
                fin_flag=1
    if fin_flag==0:
        fin=msg.showinfo("Game Over",f"The game is over. You won\n\n  Started    : \
{start}\n\n  Finished  : {ctime()[11:19]}")
        goback(n=0)
    else:
        fin=msg.showinfo("Error","The game is not over yet")
        fin_flag=0

#================================= MenuBar Functions ===================================#

def change_game(no):
    if no==0:
        global gs
        gs=game()
    for i in range(9):
        allnum[i]['bg']='steel blue'
        for j in range(9):
            btn[i][j]["text"]=gs[0][i*9+j]
            btn[i][j]['bg']='black'
            if btn[i][j]["text"]!=' ':
                btn[i][j]["activebackground"]='red'
            else:
                btn[i][j]["activebackground"]='white'

def undo():
    global flag
    if flag<5 and len(all_moves)!=0:
        pos=all_moves[-1]
        all_moves.pop(-1)
        btn[pos[0]][pos[1]]['text']=' '
        btn[pos[0]][pos[1]]['bg']='black'
        flag+=1
    else:
        msg.showinfo("Undo Move","Cannot Undo Move Now")

def eraser():
    global erase
    erase=True
    for i in range(9):
        allnum[i]['bg']='steel blue'
        for j in range(9):
            if gs[0][i*9+j]!=' ' or btn[i][j]['text']==' ':
                btn[i][j]['bg']='black'
            else:
                btn[i][j]['bg']='steel blue'

def check():
    global no
    no=' '
    sol=gs[1]
    for i in range(9):
        allnum[i]['bg']='steel blue'
        for j in range(9):
            btn[i][j]['bg']='black'
            if btn[i][j]['text']!=' ':
                if btn[i][j]['text']==sol[i*9+j]:
                    btn[i][j]['bg']='steel blue'
                else:
                    btn[i][j]['bg']='red'

#====================================== Main Program ===================================#

root=Tk()
root.title("Sudoku")
root.config(bg="gray")
root.resizable(False,False)
root.geometry("320x520+480+110")

b1=Label(root,bg='gray',height=2)
b1.pack()

#===================================== Main Function ===================================#

if __name__ == "__main__":
    start_page()

root.mainloop()
