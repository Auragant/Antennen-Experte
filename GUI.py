from doctest import master
from ssl import Options
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext

import Vars_ant
import sici
import yaud

class Gui():
    def __init__(self):
        self.initFrames()
        self.initInstr(self.InstrFrame)
        self.InitPara(self.ParaFrameS)
        self.antenna_type = sici.dipole_lam2()
        

    def initFrames(self): #Oberflaechendefinition
        self.root = Tk()
        self.root.title("Antenna Designer")
        self.root.geometry("1000x800")

        self.ParaFrame=ttk.Frame(self.root,borderwidth=2)
        self.ParaFrame.grid(row=0,column=0,sticky="NEWS")
        self.ParaFrameCanvas=Canvas(self.ParaFrame)
        self.ParaFrameS=ttk.Frame(self.ParaFrameCanvas,borderwidth=3,relief='groove')
        self.scrollbar=ttk.Scrollbar(self.ParaFrame,orient="vertical",
                                    command=self.ParaFrameCanvas.yview)
        self.ParaFrameCanvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0,column=0,sticky="NS")
        self.ParaFrameCanvas.grid(row=0,column=1,sticky="nsew")

        self.ParaFrameCanvas.create_window((0, 0), window=self.ParaFrameS, anchor="nw")

        self.ParaFrameS.bind(
            "<Configure>",
            lambda e: self.ParaFrameCanvas.configure(
                scrollregion=self.ParaFrameCanvas.bbox("all")
                )
            )

        self.InstrFrame=ttk.Frame(self.root)
        self.InstrFrame.grid(row=1,column=0)

        self.GraphFrame=ttk.Frame(self.root)
        self.GraphFrame.grid(row=0,column=1)


        self.Graph = plt.figure(figsize=(10,10), dpi=72)
        self.canvas = FigureCanvasTkAgg(self.Graph, master=self.GraphFrame)
        self.canvas.get_tk_widget().grid(row=0,column=0,sticky="nsew")

        # Filemenu 
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.main_menu = Menu(self.menu)
        self.menu.add_cascade(label="Berechnung", menu=self.main_menu)
        self.main_menu.add_command(label="Dipole", command=self.set_antenna(1))
        self.main_menu.add_command(label="Yagi-Uda", command=self.set_antenna(2))
        self.main_menu.add_separator()
        self.main_menu.add_command(label="Exit", command=self._quit)

        self.helpmenu = Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
        self.helpmenu.add_command(label="About...", command=self.About())

        self.root.bind('<<visu_flag_next>>',lambda e: Visu()) # virtuelles tkinter-Event mit dem Hauptfenster verknuepfen
        self.root.protocol("WM_DELETE_WINDOW", self._quit) # Routine fuer das Schliessen des Hauptfensters

    def initInstr(self,InstrFrame):
        self.button = ttk.Button(master=InstrFrame, text='Quit', command=self._quit)
        self.button.grid(row=2,column=1)
        button1 = ttk.Button(master=InstrFrame, text='Let\'s Go', command=self.opt_impedance) #IMPORTANT Aktion - Berechne
        button1.grid(row=2,column=0)

    def About(self):
        pass

    def InitPara(self,ParaFrame): 

        self.label1=ttk.Label(master=ParaFrame, text="Frequenz/MHz  ")
        self.label1.grid(row=0,column=1)
        self.input1 = ttk.Entry(master=ParaFrame, width=8)
        self.input1.insert(END,"100")
        self.input1.grid(row=0,column=2)
        self.label2=ttk.Label(master=ParaFrame, text="Drahtdurchmesser/ mm  ")
        self.label2.grid(row=1,column=1)
        self.input2 = ttk.Entry(master=ParaFrame, width=8)
        self.input2.insert(END,"3")
        self.input2.grid(row=1,column=2)
        # #ab hier eigenes System
        # self.label3=ttk.Label(master=ParaFrame, text="Antennentyp") 
        # self.label3.grid(row=2,column=1)
        
        
        # #Drop-Down Menue 

        # Drop_Down_Var = StringVar(ParaFrame)
        # Drop_Down_Var.set(Vars_ant.antenna_list[0])
        # self.input3 = OptionMenu(ParaFrame, Drop_Down_Var, *Vars_ant.antenna_list)
        # #self.input3.pack()
        # self.input3.grid(row=2,column=2)
        
        # #Radio Button Menue

        # self.rad_var = IntVar()
        # self.rad_var.set(1)
        
        # for txt, val in Vars_ant.antenna_list:
        #     Radiobutton(ParaFrame, text=txt, padx = 20,variable=self.rad_var, 
        #         command=self.set_antenna(),
        #         value=val).pack(anchor=W)


        self.result_text=scrolledtext.ScrolledText(master=ParaFrame,width=30,height=5)
        self.result_text.grid(row=40,column=1,columnspan=3,pady=20,sticky="news")

    def set_antenna(self, ant_numb):
        if ant_numb == 1:
            self.antenna_type = sici.dipole_lam2()
        elif ant_numb == 2:
            pass
            self.antenna_type = yaud.yagi_uda_4()
        else:
            self._quit()
        
        

    def _quit(self):
        self.root.quit()     # stops mainloop
        self.root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

    def opt_impedance(self): 
        freq=self.get_freq()
        rad=self.get_radius()
        # self.set_antenna_class()
        self.set_antenna_class(self.get_antenna())
        self.antenna_class.set_radius(rad)
        
        #Unterscheidung nach Antennen mit vollem Strahlungswiederstand und hergebrachten Formeln
        if(self.antenna_class != yaud.yagi_uda_4):
            self.l,res_text=self.antenna_class.opt_refl(float(self.input1.get()))

            self.result_text.insert(index="0.0",chars=res_text)

            freq=self.get_freq()
            freqs=np.linspace(0.5*freq,2*freq,101)

            Rin,Xin,Rm,Xm=self.antenna_class.impedance_f(freqs)
            Gam=self.antenna_class.reflection2_f(freqs)
            self.Graph.clf()
            a=self.Graph.add_subplot(221)
            plt.plot(freqs,Rm)
            plt.plot(freqs,Xm)
            plt.plot(freqs,Rin)
            plt.plot(freqs,Xin)

            plt.ylim([-300,300])
            plt.legend(["Rm","Xm","Rin","Xin"])
            plt.xlabel('Freq')
            plt.ylabel('Rm und Xm')
            plt.grid()

            b=self.Graph.add_subplot(222)
            plt.plot(freqs,Gam,"k")
            plt.legend("Gam")
            plt.ylabel("Reflexion in dB")
            plt.grid()
            self.canvas.draw()
        elif(self.antenna_class == yaud.yagi_uda_4):
            
            
#Definitionen der Uebergaben aus dem self-Bildschirmobjekt
    def get_freq(self):
        return float(self.input1.get())*1e6
    
    def get_radius(self):
        return float(self.input2.get())*1e-3/2

    def get_antenna(self):
        # self.antenna_type = sici.dipole_lam2()
        return self.antenna_type
        
    def set_antenna_class(self,antenna_class):
        self.antenna_class=antenna_class
        self.antenna_name=self.antenna_class.get_antenna_name()
