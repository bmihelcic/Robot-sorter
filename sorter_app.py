#!/usr/bin/python3
from tkinter import *
from tkinter import messagebox

''' global settings '''
DASH_COUNT=25

RB_WIDTH=6
RB_HEIGHT=1
RB_FONT_SIZE=15

TOG_WIDTH=8

TERMINAL_X=40
TERMINAL_Y=20



''' root frame '''
main_frame=Tk()

oblikA=IntVar()
bojaA=IntVar()
masaA_min=IntVar()
masaA_max=IntVar()
oblikB=IntVar()
bojaB=IntVar()
masaB_min=IntVar()
masaB_max=IntVar()
oblikC=IntVar()
bojaC=IntVar()
masaC_min=IntVar()
masaC_max=IntVar()

message_list=['A',0,0,0,0,0,0,0,0,0,'B',0,0,0,0,0,0,0,0,0,'C',0,0,0,0,0,0,0,0,0,'#']

''' unosenje znamenki MIN mase u uart poruku (za sve spremnike)'''
def min_masa_digits():
    temp = [0, 0, 0]
    list_min=[masaA_min.get(),masaB_min.get(),masaC_min.get()]
    for c in range(0,3):
        choice=list_min[c]
        for i in range(0, 3):
            ostatak = choice % 10
            temp[2 - i] = ostatak
            choice = int(choice / 10)
        message_list[3+c*10] = temp[0]
        message_list[4+c*10] = temp[1]
        message_list[5+c*10] = temp[2]

''' unosenje znamenki MAX mase u uart poruku (za sve spremnike)'''
def max_masa_digits():
    temp = [0, 0, 0, 0]
    list_max=[masaA_max.get(),masaB_max.get(),masaC_max.get()]
    for c in range(0,3):
        choice=list_max[c]
        for i in range(0, 4):
            ostatak = choice % 10
            temp[3 - i] = ostatak
            choice = int(choice / 10)
        message_list[6+c*10] = temp[0]
        message_list[7+c*10] = temp[1]
        message_list[8+c*10] = temp[2]
        message_list[9+c*10] = temp[3]

''' pregled spremnika A i upozoravanje po potrebi '''
def check_spremnikA():
    if bojaA.get()==0 and oblikA.get()==0 and toggle_btn_masaA['text']=='OFF':
        for i in range(1,10):
            message_list[i]=0
    else:
        message_list[1] = oblikA.get()
        message_list[2] = bojaA.get()
        if toggle_btn_masaA['text']=='ON':
            if len(entry_masaA_min.get())== 0 or len(entry_masaA_max.get())==0:
                raise ValueError
            masaA_min.set(int(entry_masaA_min.get()))
            masaA_max.set(int(entry_masaA_max.get()))
            if masaA_max.get() < masaA_min.get() or masaA_max.get() > 1000 or masaA_min.get() < 0:
                raise ValueError

''' pregled spremnika B i upozoravanje po potrebi '''
def check_spremnikB():
    if bojaB.get()==0 and oblikB.get()==0 and toggle_btn_masaB['text']=='OFF':
        for i in range(11,20):
            message_list[i]=0
    else:
        message_list[11] = oblikB.get()
        message_list[12] = bojaB.get()
        if toggle_btn_masaB['text']=='ON':
            if len(entry_masaB_min.get())== 0 or len(entry_masaB_max.get())==0:
                raise ValueError
            masaB_min.set(int(entry_masaB_min.get()))
            masaB_max.set(int(entry_masaB_max.get()))
            if masaB_max.get() < masaB_min.get() or masaB_max.get() > 1000 or masaB_min.get() < 0:
                raise ValueError

''' pregled spremnika C i upozoravanje po potrebi '''
def check_spremnikC():
    if bojaC.get()==0 and oblikC.get()==0 and toggle_btn_masaC['text']=='OFF':
        for i in range(21,30):
            message_list[i]=0
    else:
        message_list[21] = oblikC.get()
        message_list[22] = bojaC.get()
        if toggle_btn_masaC['text']=='ON':
            if len(entry_masaC_min.get())== 0 or len(entry_masaC_max.get())==0:
                raise ValueError
            masaC_min.set(int(entry_masaC_min.get()))
            masaC_max.set(int(entry_masaC_max.get()))
            if masaC_max.get() < masaC_min.get() or masaC_max.get() > 1000 or masaC_min.get() < 0:
                raise ValueError


def send():
    try:
        check_spremnikA()
        check_spremnikB()
        check_spremnikC()
        min_masa_digits()
        max_masa_digits()
        message = ''.join(str(e) for e in message_list)
        terminal.insert(END,message+'\n')
        terminal.see('end')
        #print(message)
    except ValueError:
        messagebox.showwarning("Warning!","Molim ispravan unos mase (0-1000 grama)")

''' toggle funkcije za A widgete '''
def toggle_oblikA(state=[False]):
    state[0]=not state[0]
    if state[0]==True:
        toggle_btn_oblikA.config(bg='light green')
        toggle_btn_oblikA.config(text='ON')
        radio_btn_kuglaA.config(state=NORMAL)
        radio_btn_kockaA.config(state=NORMAL)
        radio_btn_piramidaA.config(state=NORMAL)
        radio_btn_kuglaA.select()
    elif state[0]==False:
        toggle_btn_oblikA.config(bg='red')
        toggle_btn_oblikA.config(text='OFF')
        radio_btn_kuglaA.config(state=DISABLED)
        radio_btn_kockaA.config(state=DISABLED)
        radio_btn_piramidaA.config(state=DISABLED)
        oblikA.set(0)
def toggle_bojaA(state=[False]):
    state[0]=not state[0]
    if state[0]==True:
        toggle_btn_bojaA.config(bg='light green')
        toggle_btn_bojaA.config(text='ON')
        radio_btn_crvenaA.config(state=NORMAL)
        radio_btn_plavaA.config(state=NORMAL)
        radio_btn_zelenaA.config(state=NORMAL)
        radio_btn_zutaA.config(state=NORMAL)
        radio_btn_zelenaA.select()
    elif state[0]==False:
        toggle_btn_bojaA.config(bg='red')
        toggle_btn_bojaA.config(text='OFF')
        radio_btn_crvenaA.config(state=DISABLED)
        radio_btn_plavaA.config(state=DISABLED)
        radio_btn_zutaA.config(state=DISABLED)
        radio_btn_zelenaA.config(state=DISABLED)
        bojaA.set(0)
def toggle_masaA(state=[False]):
    state[0]=not state[0]
    if state[0]==True:
        toggle_btn_masaA.config(bg='light green')
        toggle_btn_masaA.config(text='ON')
        entry_masaA_max.config(state=NORMAL)
        entry_masaA_min.config(state=NORMAL)
        label_masaA_min.config(fg='black')
        label_masaA_max.config(fg='black')
        masaA_min.set(0)
        masaA_max.set(1000)
        entry_masaA_min.insert(0,0)
        entry_masaA_max.insert(0,1000)
    elif state[0]==False:
        toggle_btn_masaA.config(bg='red')
        toggle_btn_masaA.config(text='OFF')
        entry_masaA_min.delete(0,END)
        entry_masaA_max.delete(0,END)
        entry_masaA_max.config(state=DISABLED)
        entry_masaA_min.config(state=DISABLED)
        label_masaA_min.config(fg='grey')
        label_masaA_max.config(fg='grey')
        masaA_min.set(0)
        masaA_max.set(0)
        min_masa_digits()
        max_masa_digits()

''' toggle funkcije za B widgete '''
def toggle_oblikB(state=[False]):
    state[0]=not state[0]
    if state[0]==True:
        toggle_btn_oblikB.config(bg='light green')
        toggle_btn_oblikB.config(text='ON')
        radio_btn_kuglaB.config(state=NORMAL)
        radio_btn_kockaB.config(state=NORMAL)
        radio_btn_piramidaB.config(state=NORMAL)
        radio_btn_kuglaB.select()
    elif state[0]==False:
        toggle_btn_oblikB.config(bg='red')
        toggle_btn_oblikB.config(text='OFF')
        radio_btn_kuglaB.config(state=DISABLED)
        radio_btn_kockaB.config(state=DISABLED)
        radio_btn_piramidaB.config(state=DISABLED)
        oblikB.set(0)
def toggle_bojaB(state=[False]):
    state[0]=not state[0]
    if state[0]==True:
        toggle_btn_bojaB.config(bg='light green')
        toggle_btn_bojaB.config(text='ON')
        radio_btn_crvenaB.config(state=NORMAL)
        radio_btn_plavaB.config(state=NORMAL)
        radio_btn_zelenaB.config(state=NORMAL)
        radio_btn_zutaB.config(state=NORMAL)
        radio_btn_zelenaB.select()
    elif state[0]==False:
        toggle_btn_bojaB.config(bg='red')
        toggle_btn_bojaB.config(text='OFF')
        radio_btn_crvenaB.config(state=DISABLED)
        radio_btn_plavaB.config(state=DISABLED)
        radio_btn_zutaB.config(state=DISABLED)
        radio_btn_zelenaB.config(state=DISABLED)
        bojaB.set(0)
def toggle_masaB(state=[False]):
    state[0]=not state[0]
    if state[0]==True:
        toggle_btn_masaB.config(bg='light green')
        toggle_btn_masaB.config(text='ON')
        entry_masaB_max.config(state=NORMAL)
        entry_masaB_min.config(state=NORMAL)
        label_masaB_min.config(fg='black')
        label_masaB_max.config(fg='black')
        masaB_min.set(0)
        masaB_max.set(1000)
        entry_masaB_min.insert(0,0)
        entry_masaB_max.insert(0,1000)
    elif state[0]==False:
        toggle_btn_masaB.config(bg='red')
        toggle_btn_masaB.config(text='OFF')
        entry_masaB_min.delete(0,END)
        entry_masaB_max.delete(0,END)
        entry_masaB_max.config(state=DISABLED)
        entry_masaB_min.config(state=DISABLED)
        label_masaB_min.config(fg='grey')
        label_masaB_max.config(fg='grey')
        masaB_min.set(0)
        masaB_max.set(0)

''' toggle funkcije za C widgete '''
def toggle_oblikC(state=[False]):
    state[0]=not state[0]
    if state[0]==True:
        toggle_btn_oblikC.config(bg='light green')
        toggle_btn_oblikC.config(text='ON')
        radio_btn_kuglaC.config(state=NORMAL)
        radio_btn_kockaC.config(state=NORMAL)
        radio_btn_piramidaC.config(state=NORMAL)
        radio_btn_kuglaC.select()
    elif state[0]==False:
        toggle_btn_oblikC.config(bg='red')
        toggle_btn_oblikC.config(text='OFF')
        radio_btn_kuglaC.config(state=DISABLED)
        radio_btn_kockaC.config(state=DISABLED)
        radio_btn_piramidaC.config(state=DISABLED)
        oblikC.set(0)
def toggle_bojaC(state=[False]):
    state[0]=not state[0]
    if state[0]==True:
        toggle_btn_bojaC.config(bg='light green')
        toggle_btn_bojaC.config(text='ON')
        radio_btn_crvenaC.config(state=NORMAL)
        radio_btn_plavaC.config(state=NORMAL)
        radio_btn_zelenaC.config(state=NORMAL)
        radio_btn_zutaC.config(state=NORMAL)
        radio_btn_zelenaC.select()
    elif state[0]==False:
        toggle_btn_bojaC.config(bg='red')
        toggle_btn_bojaC.config(text='OFF')
        radio_btn_crvenaC.config(state=DISABLED)
        radio_btn_plavaC.config(state=DISABLED)
        radio_btn_zutaC.config(state=DISABLED)
        radio_btn_zelenaC.config(state=DISABLED)
        bojaC.set(0)
def toggle_masaC(state=[False]):
    state[0]=not state[0]
    if state[0]==True:
        toggle_btn_masaC.config(bg='light green')
        toggle_btn_masaC.config(text='ON')
        entry_masaC_max.config(state=NORMAL)
        entry_masaC_min.config(state=NORMAL)
        label_masaC_min.config(fg='black')
        label_masaC_max.config(fg='black')
        masaC_min.set(0)
        masaC_max.set(1000)
        entry_masaC_min.insert(0,0)
        entry_masaC_max.insert(0,1000)
    elif state[0]==False:
        toggle_btn_masaC.config(bg='red')
        toggle_btn_masaC.config(text='OFF')
        entry_masaC_min.delete(0,END)
        entry_masaC_max.delete(0,END)
        entry_masaC_max.config(state=DISABLED)
        entry_masaC_min.config(state=DISABLED)
        label_masaC_min.config(fg='grey')
        label_masaC_max.config(fg='grey')
        masaC_min.set(0)
        masaC_max.set(0)

top_frame=Frame(main_frame)
frame_A=Frame(top_frame)
frame_B=Frame(top_frame)
frame_C=Frame(top_frame)

bottom_frame=Frame(main_frame)
terminal=Text(bottom_frame,height=TERMINAL_Y,width=TERMINAL_X)
terminal_scrollbar=Scrollbar(bottom_frame,command=terminal.yview)
terminal.config(yscrollcommand=terminal_scrollbar.set)

main_frame.title('Sorter izbornik')
main_frame.geometry('1024x600')
#main_frame.config()
main_frame.update()

label_A=Label(top_frame,text=DASH_COUNT*"-"+" Spremnik A "+DASH_COUNT*"-",bd=2,relief="solid",fg='white',bg='grey')
label_B=Label(top_frame,text=DASH_COUNT*'-'+" Spremnik B "+DASH_COUNT*"-",bd=2,relief="solid",fg='white',bg='grey')
label_C=Label(top_frame,text=DASH_COUNT*'-'+" Spremnik C "+DASH_COUNT*"-",bd=2,relief="solid",fg='white',bg='grey')

send_btn=Button(bottom_frame,text="SEND",command=send,width=8)
'''
 PRVI SPREMNIK (A)
'''
Label(frame_A,text="OBLICI").grid(row=0,column=0)
Label(frame_A,text="BOJA").grid(row=0,column=1)
Label(frame_A,text="MASA").grid(row=0,column=2)
toggle_btn_oblikA=Button(frame_A,text="OFF",bg='red',command=toggle_oblikA,width=TOG_WIDTH)
toggle_btn_oblikA.grid(row=1,column=0)
toggle_btn_bojaA=Button(frame_A,text="OFF",bg='red',command=toggle_bojaA,width=TOG_WIDTH)
toggle_btn_bojaA.grid(row=1,column=1)
toggle_btn_masaA=Button(frame_A,text="OFF",bg='red',command=toggle_masaA,width=TOG_WIDTH)
toggle_btn_masaA.grid(row=1,column=2)
radio_btn_kuglaA=Radiobutton(frame_A,variable=oblikA,value=1,text='kugla',state=DISABLED,width=RB_WIDTH,height=RB_HEIGHT,anchor=W,font=(None,RB_FONT_SIZE))
radio_btn_kuglaA.grid(row=2,column=0)
radio_btn_kockaA=Radiobutton(frame_A,variable=oblikA,value=2,text='kocka',state=DISABLED,width=RB_WIDTH,height=RB_HEIGHT,anchor=W,font=(None,RB_FONT_SIZE))
radio_btn_kockaA.grid(row=3,column=0)
radio_btn_piramidaA=Radiobutton(frame_A,variable=oblikA,value=3,text='piramida',state=DISABLED,width=RB_WIDTH,height=RB_HEIGHT,anchor=W,font=(None,RB_FONT_SIZE))
radio_btn_piramidaA.grid(row=4,column=0)
radio_btn_zelenaA=Radiobutton(frame_A,variable=bojaA,value=1,text='zelena',state=DISABLED,width=RB_WIDTH,height=RB_HEIGHT,anchor=W,font=(None,RB_FONT_SIZE))
radio_btn_zelenaA.grid(row=2,column=1)
radio_btn_crvenaA=Radiobutton(frame_A,variable=bojaA,value=2,text='crvena',state=DISABLED,width=RB_WIDTH,height=RB_HEIGHT,anchor=W,font=(None,RB_FONT_SIZE))
radio_btn_crvenaA.grid(row=3,column=1)
radio_btn_plavaA=Radiobutton(frame_A,variable=bojaA,value=3,text='plava',state=DISABLED,width=RB_WIDTH,height=RB_HEIGHT,anchor=W,font=(None,RB_FONT_SIZE))
radio_btn_plavaA.grid(row=4,column=1)
radio_btn_zutaA=Radiobutton(frame_A,variable=bojaA,value=4,text='zuta',state=DISABLED,width=RB_WIDTH,height=RB_HEIGHT,anchor=W,font=(None,RB_FONT_SIZE))
radio_btn_zutaA.grid(row=5,column=1)
label_masaA_min=Label(frame_A,text="  MIN",fg="grey")
label_masaA_min.grid(row=2,column=2,sticky=W)
entry_masaA_min=Entry(frame_A,width=5,state=DISABLED)
entry_masaA_min.grid(row=2,column=2,columnspan=2,sticky=E)
label_masaA_max=Label(frame_A,text="  MAX",fg="grey")
label_masaA_max.grid(row=3,column=2,sticky=W)
entry_masaA_max=Entry(frame_A,width=5,state=DISABLED)
entry_masaA_max.grid(row=3,column=2,sticky=E)

'''
 DRUGI SPREMNIK (B)
'''

Label(frame_B,text="OBLICI").grid(row=0,column=0)
Label(frame_B,text="BOJA").grid(row=0,column=1)
Label(frame_B,text="MASA").grid(row=0,column=2)
toggle_btn_oblikB=Button(frame_B,text="OFF",bg='red',command=toggle_oblikB,width=TOG_WIDTH)
toggle_btn_oblikB.grid(row=1,column=0)
toggle_btn_bojaB=Button(frame_B,text="OFF",bg='red',command=toggle_bojaB,width=TOG_WIDTH)
toggle_btn_bojaB.grid(row=1,column=1)
toggle_btn_masaB=Button(frame_B,text="OFF",bg='red',command=toggle_masaB,width=TOG_WIDTH)
toggle_btn_masaB.grid(row=1,column=2)
radio_btn_kuglaB=Radiobutton(frame_B,variable=oblikB,value=1,text='kugla',state=DISABLED,width=RB_WIDTH,height=RB_HEIGHT,anchor=W,font=(None,RB_FONT_SIZE))
radio_btn_kuglaB.grid(row=2,column=0)
radio_btn_kockaB=Radiobutton(frame_B,variable=oblikB,value=2,text='kocka',state=DISABLED,width=RB_WIDTH,height=RB_HEIGHT,anchor=W,font=(None,RB_FONT_SIZE))
radio_btn_kockaB.grid(row=3,column=0)
radio_btn_piramidaB=Radiobutton(frame_B,variable=oblikB,value=3,text='piramida',state=DISABLED,width=RB_WIDTH,height=RB_HEIGHT,anchor=W,font=(None,RB_FONT_SIZE))
radio_btn_piramidaB.grid(row=4,column=0)
radio_btn_zelenaB=Radiobutton(frame_B,variable=bojaB,value=1,text='zelena',state=DISABLED,width=RB_WIDTH,height=RB_HEIGHT,anchor=W,font=(None,RB_FONT_SIZE))
radio_btn_zelenaB.grid(row=2,column=1)
radio_btn_crvenaB=Radiobutton(frame_B,variable=bojaB,value=2,text='crvena',state=DISABLED,width=RB_WIDTH,height=RB_HEIGHT,anchor=W,font=(None,RB_FONT_SIZE))
radio_btn_crvenaB.grid(row=3,column=1)
radio_btn_plavaB=Radiobutton(frame_B,variable=bojaB,value=3,text='plava',state=DISABLED,width=RB_WIDTH,height=RB_HEIGHT,anchor=W,font=(None,RB_FONT_SIZE))
radio_btn_plavaB.grid(row=4,column=1)
radio_btn_zutaB=Radiobutton(frame_B,variable=bojaB,value=4,text='zuta',state=DISABLED,width=RB_WIDTH,height=RB_HEIGHT,anchor=W,font=(None,RB_FONT_SIZE))
radio_btn_zutaB.grid(row=5,column=1)
label_masaB_min=Label(frame_B,text="  MIN",fg="grey")
label_masaB_min.grid(row=2,column=2,sticky=W)
entry_masaB_min=Entry(frame_B,width=5,state=DISABLED)
entry_masaB_min.grid(row=2,column=2,columnspan=2,sticky=E)
label_masaB_max=Label(frame_B,text="  MAX",fg="grey")
label_masaB_max.grid(row=3,column=2,sticky=W)
entry_masaB_max=Entry(frame_B,width=5,state=DISABLED)
entry_masaB_max.grid(row=3,column=2,sticky=E)

'''
 TRECI SPREMNIK (C)
'''
Label(frame_C,text="OBLICI").grid(row=0,column=0)
Label(frame_C,text="BOJA").grid(row=0,column=1)
Label(frame_C,text="MASA").grid(row=0,column=2)
toggle_btn_oblikC=Button(frame_C,text="OFF",bg='red',command=toggle_oblikC,width=TOG_WIDTH)
toggle_btn_oblikC.grid(row=1,column=0)
toggle_btn_bojaC=Button(frame_C,text="OFF",bg='red',command=toggle_bojaC,width=TOG_WIDTH)
toggle_btn_bojaC.grid(row=1,column=1)
toggle_btn_masaC=Button(frame_C,text="OFF",bg='red',command=toggle_masaC,width=TOG_WIDTH)
toggle_btn_masaC.grid(row=1,column=2)
radio_btn_kuglaC=Radiobutton(frame_C,variable=oblikC,value=1,text='kugla',state=DISABLED,width=RB_WIDTH,height=RB_HEIGHT,anchor=W,font=(None,RB_FONT_SIZE))
radio_btn_kuglaC.grid(row=2,column=0)
radio_btn_kockaC=Radiobutton(frame_C,variable=oblikC,value=2,text='kocka',state=DISABLED,width=RB_WIDTH,height=RB_HEIGHT,anchor=W,font=(None,RB_FONT_SIZE))
radio_btn_kockaC.grid(row=3,column=0)
radio_btn_piramidaC=Radiobutton(frame_C,variable=oblikC,value=3,text='piramida',state=DISABLED,width=RB_WIDTH,height=RB_HEIGHT,anchor=W,font=(None,RB_FONT_SIZE))
radio_btn_piramidaC.grid(row=4,column=0)
radio_btn_zelenaC=Radiobutton(frame_C,variable=bojaC,value=1,text='zelena',state=DISABLED,width=RB_WIDTH,height=RB_HEIGHT,anchor=W,font=(None,RB_FONT_SIZE))
radio_btn_zelenaC.grid(row=2,column=1)
radio_btn_crvenaC=Radiobutton(frame_C,variable=bojaC,value=2,text='crvena',state=DISABLED,width=RB_WIDTH,height=RB_HEIGHT,anchor=W,font=(None,RB_FONT_SIZE))
radio_btn_crvenaC.grid(row=3,column=1)
radio_btn_plavaC=Radiobutton(frame_C,variable=bojaC,value=3,text='plava',state=DISABLED,width=RB_WIDTH,height=RB_HEIGHT,anchor=W,font=(None,RB_FONT_SIZE))
radio_btn_plavaC.grid(row=4,column=1)
radio_btn_zutaC=Radiobutton(frame_C,variable=bojaC,value=4,text='zuta',state=DISABLED,width=RB_WIDTH,height=RB_HEIGHT,anchor=W,font=(None,RB_FONT_SIZE))
radio_btn_zutaC.grid(row=5,column=1)
label_masaC_min=Label(frame_C,text="  MIN",fg="grey")
label_masaC_min.grid(row=2,column=2,sticky=W)
entry_masaC_min=Entry(frame_C,width=5,state=DISABLED)
entry_masaC_min.grid(row=2,column=2,columnspan=2,sticky=E)
label_masaC_max=Label(frame_C,text="  MAX",fg="grey")
label_masaC_max.grid(row=3,column=2,sticky=W)
entry_masaC_max=Entry(frame_C,width=5,state=DISABLED)
entry_masaC_max.grid(row=3,column=2,sticky=E)

label_A.grid(row=0,column=0)
frame_A.grid(row=1,column=0)
label_B.grid(row=0,column=1)
frame_B.grid(row=1,column=1)
label_C.grid(row=0,column=2)
frame_C.grid(row=1,column=2)

terminal.grid(row=0,column=0)
terminal_scrollbar.grid(row=0,column=1,sticky='ns')
send_btn.grid(row=0,column=2,padx=50)

top_frame.pack()
Label(main_frame,text=270*'-').pack()
bottom_frame.pack(side=LEFT)

main_frame.mainloop()
