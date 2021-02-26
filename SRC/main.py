from tkinter import *
import os
from datetime import date
gui = Tk()
textvar = StringVar()
global canvas, num, high, Verze
Verze = "0.0.1"
num=0
high = 600

canvas=Canvas(gui,width=1300,height=high+40)
canvas.pack(side = "bottom")


class main:
    def __init__(self):
        #DEFINE
        self.text = Text(gui,height=1 ,wrap="none")
        self.scrollbar = Scrollbar(gui,orient="horizontal",command=self.text.xview)
        #CONFIGURE
        self.text.configure(xscrollcommand=self.scrollbar.set)
        #PACK
        self.scrollbar.pack(side="top", fill="x")
        self.text.pack(fill="both")
        #IMPORT
        imports = self.import_logs()
        #ADD DAT to line
        x=[]
        for num,i in enumerate(imports):
            x.append(day(i,num,self))
        self.text.configure(state="disabled")
    def log_under(self):
        canvas.create_line(40, 30, 40, high+40, dash=(4, 2))
        for n in range(24):
            y=n*high/24+40
            x=20
            canvas.create_line(40, y, 60, y)#horizontal
            canvas.create_text(x,y,fill="black",font="Times 10 bold",text=f"{n}:00")
    def import_logs(self):
        names=[]
        file = "Data\logs"
        for filename in os.listdir(file):
            if filename.endswith(".dat"):
                #os.path.join(file, filename)
                names.append(filename[0:-4])
            else:
                continue
        today = str(date.today())
        if not (today in names):
            names.append(today)
            a=open(f"{os.path.join(file, today)}.dat","w+")
            a.write(Verze)
            a.close()
        return names
    def delete_logs(self,myData):# delete file
        pass
    def add_logs(self,myData):
        pass
    def run(self):
        mainloop()

class day:
    def __init__(self,name,raw,self2):
        self.raw = raw
        self.self2 = self2
        self.name = name
        self.path = os.path.join("Data\logs",self.name+".dat")
        
        self.b = Button(gui, text="%s" % self.name,command = self.openfile)
        self.self2.text.window_create("end", window=self.b)
        self.self2.text.insert("end","")

        
        
        
    def openfile(self):
        canvas.unbind("<Button-3>")
        canvas.bind("<Button-3>", self.draw_new_event)
        self.events = []
        with open(self.path) as file:
            for a,l in enumerate(file):
                print (l,a)
                if a == 0:
                    if l[0:-1] == Verze or l == Verze:
                        continue
                    else:
                        print ("!Old Verze: ",self.name)
                        continue
                event = []
                myW=""
                for w in l:
                    if w =="}":
                        event.append(myW)
                        myW=""
                    else:
                        myW=myW+w
                
                self.events.append(event)
        canvas.delete("all")
        self.self2.log_under()
        self.draw_events()
    def draw_events(self):
        for raw,n in enumerate(self.events):
            time = n[0]
            food = n[1]
            x = n[2]
            other = n[3]
            time = int(time[0:2])+int(time[3:5])/60
            y = time*high/24+40
            text(self.self2,self,x,y,food,other,raw)
    def draw_new_event(self,args):
        time = (args.y-25)*24/(high+40)
        timeh = str(round(time))
        if len(timeh) == 1:
            timeh="0"+timeh
            print(timeh)
        time = timeh + ":00"
        print(time)
        food = "text"
        x = args.x
        times = int(time[0:2])+int(time[3:5])/60
        y = times*high/24+40
        other = ""
        a =[str(time),food,str(x),other]
        self.events.append(a)
        text(self.self2,self,x,y,food,other,len(self.events)-1)
    def savefile(self):
        file = open(self.path, "w+")
        file.write(Verze)
        file.write("\n")
        for n in self.events:
            a = ""
            for i in n:
                a=a+i+"}"
            file.write(a)
            file.write("\n")
            


    
class text:
    def __init__(self,self2,self3,x,y,food,other,raw):#
        global num
        self.raw = raw
        num+=1
        self.num = num
        self.x = int(x)
        self.y = int(y)
        self.food = food
        self.other = other
        self.self3 = self3
        self.self2 = self2
        self.a=canvas.create_text(self.x,self.y,fill="blue",font="Times 15 bold",text=self.food,tag = str(self.num)+"x")
        canvas.tag_bind(str(self.num)+"x","<Button-1>", self.edit_begin)
        canvas.tag_bind(str(self.num)+"x","<Enter>", self.tooltip_show)
        canvas.tag_bind(str(self.num)+"x","<Leave>", self.tooltip_hide)
    def tooltip_hide(self,args=None):
        canvas.delete(str(self.num)+"z")
    def tooltip_show(self,args=None):
        s = canvas.create_text(self.x+25,self.y+20,fill="black",font="Times 10",text=self.other,tag = str(self.num)+"z")
        #canvas.create_window(self.x, self.y+20, window=s, tags=(str(self.num)+"z"), anchor="nw")
            
    def edit_begin(self,args=None):#
        textvar.set(self.food) 
        e = Entry(gui, width=10, textvariable=textvar, bd=0,highlightthickness=1, bg="white") 
        e.selection_range(0, "end")
        w = canvas.create_window(self.x, self.y, window=e, tags=(str(self.num)+"a"), anchor="nw")
        e.focus_set()
        e.bind("<Return>", self.edit_end)
        e.bind("<Escape>", self.edit_cancel)
        e.bind("<Button-3>", self.edit_end)
    def edit_cancel(self,args):#
        canvas.delete(str(self.num)+"a")
        args.widget.destroy()
    def edit_end(self,args):
        self.edit_cancel(args)
        text=self.edit_choose(textvar.get())
        canvas.itemconfigure((str(self.num)+"x"), text=text)# upravit num na pořadí ve dnu - listu + editovat list
        self.food = text
        self.self3.events[self.raw][1]=text
        self.self3.savefile()
        print(text)

    def edit_choose(self,text):#
        if not text in ["}"]:
            return text
        else:
            return self.food

        
        
