import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import math
import scipy.special as spec
import scipy.constants as const
from scipy.optimize import minimize_scalar
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext



class dipole_lam2():
    # Strahlungswiderstand eines Dipols nach Balanis S. 465 (8.60)
    def impedance_l(self,l):
        a=self.radius
        eta=math.sqrt(const.mu_0/const.epsilon_0)
        C=0.577215665
        f=self.f
        lam=const.speed_of_light/f
        k=2*math.pi/lam
        Z0=50
        kl=k*l

        [sikl,cikl]=spec.sici(kl)
        [si2kl,ci2kl]=spec.sici(2*kl)
        [sika,cika]=spec.sici(2*k*a*a/l)
        lnkl=np.log(kl)
        lnkl2=np.log(kl/2)
        sinkl=np.sin(kl)
        coskl=np.cos(kl)
        sinkl2=np.sin(kl/2)

        Rm=eta/2/math.pi*(C+lnkl-cikl+0.5*sinkl*(si2kl-2*sikl)+0.5*coskl*(C+lnkl2+ci2kl-2*cikl))

        Xm=eta/4/math.pi*(2*sikl+coskl*(2*sikl-si2kl)-sinkl*(2*cikl-ci2kl-cika))

        Rin=Rm/sinkl2/sinkl2
        Xin=Xm/sinkl2/sinkl2

        return (Rin,Xin,Rm,Xm)

    def impedance_f(self,f,a=1.5e-3):
        a=self.radius
        eta=math.sqrt(const.mu_0/const.epsilon_0)
        C=0.577215665
        k=2*math.pi/const.speed_of_light*f
        Z0=50
        l=self.l
        kl=k*l

        [sikl,cikl]=spec.sici(kl)
        [si2kl,ci2kl]=spec.sici(2*kl)
        [sika,cika]=spec.sici(2*k*a*a/l)
        lnkl=np.log(kl)
        lnkl2=np.log(kl/2)
        sinkl=np.sin(kl)
        coskl=np.cos(kl)
        sinkl2=np.sin(kl/2)

        Rm=eta/2/math.pi*(C+lnkl-cikl+0.5*sinkl*(si2kl-2*sikl)+0.5*coskl*(C+lnkl2+ci2kl-2*cikl))

        Xm=eta/4/math.pi*(2*sikl+coskl*(2*sikl-si2kl)-sinkl*(2*cikl-ci2kl-cika))

        Rin=Rm/sinkl2/sinkl2
        Xin=Xm/sinkl2/sinkl2

        return (Rin,Xin,Rm,Xm)

    def reflection(self,l,Z0):
        Rin,Xin,Rm,Xm=self.impedance_l(l)
        Gam=10*np.log10(np.sqrt(((Rin-Z0)*(Rin-Z0)+Xin*Xin)/((Rin+Z0)*(Rin+Z0)+Xin*Xin)))
        return Gam

    def reflection_f(self,f,Z0):
        Rin,Xin,Rm,Xm=self.impedance_f(f)
        Gam=10*np.log10(np.sqrt(((Rin-Z0)*(Rin-Z0)+Xin*Xin)/((Rin+Z0)*(Rin+Z0)+Xin*Xin)))
        return Gam

    def reflection2(self,l):
        return self.reflection(l, 50)

    def reflection2_f(self,f):
        return self.reflection_f(f, 50)

    def opt_refl(self,freq):
        self.f=freq*1e6
        lam=const.speed_of_light/self.f
        optr=minimize_scalar(self.reflection2,
                     bracket=(lam*0.2,lam*0.8),
                     bounds=(lam*0.1,1.0*lam),
                     method='Bounded')
        print(optr)
        res_text="Reflexion von "+'{:6.1f}'.format(optr.fun)+"dB \n"\
                +"erreicht bei Länge "+'{:6.4f}'.format(optr.x)+"m\n="\
                +'{:6.4f}'.format(optr.x/lam)+" Wellenlängen\n\n"
        print(res_text)
        self.l=optr.x
        return optr.x,res_text

    def set_radius(self,rad):
        self.radius=rad
    def set_length(self,l):
        self.l=l
    def get_antenna_name(self):
        return "Half Wave Dipole"


# class Gui():
#     def __init__(self):
#         self.initFrames()
#         self.initInstr(self.InstrFrame)
#         self.InitPara(self.ParaFrameS)

#     def initFrames(self):
#         self.root = Tk()
#         self.root.title("Antenna Designer")
#         self.root.geometry("1000x800")

#         self.ParaFrame=ttk.Frame(self.root,borderwidth=2)
#         self.ParaFrame.grid(row=0,column=0,sticky="NEWS")
#         self.ParaFrameCanvas=Canvas(self.ParaFrame)
#         self.ParaFrameS=ttk.Frame(self.ParaFrameCanvas,borderwidth=3,relief='groove')
#         self.scrollbar=ttk.Scrollbar(self.ParaFrame,orient="vertical",
#                                     command=self.ParaFrameCanvas.yview)
#         self.ParaFrameCanvas.configure(yscrollcommand=self.scrollbar.set)
#         self.scrollbar.grid(row=0,column=0,sticky="NS")
#         self.ParaFrameCanvas.grid(row=0,column=1,sticky="nsew")

#         self.ParaFrameCanvas.create_window((0, 0), window=self.ParaFrameS, anchor="nw")

#         self.ParaFrameS.bind(
#             "<Configure>",
#             lambda e: self.ParaFrameCanvas.configure(
#                 scrollregion=self.ParaFrameCanvas.bbox("all")
#                 )
#             )

#         self.InstrFrame=ttk.Frame(self.root)
#         self.InstrFrame.grid(row=1,column=0)

#         self.GraphFrame=ttk.Frame(self.root)
#         self.GraphFrame.grid(row=0,column=1)


#         self.Graph = plt.figure(figsize=(10,10), dpi=72)
#         self.canvas = FigureCanvasTkAgg(self.Graph, master=self.GraphFrame)
#         self.canvas.get_tk_widget().grid(row=0,column=0,sticky="nsew")

#         self.root.bind('<<visu_flag_next>>',lambda e: Visu()) # virtuelles tkinter-Event mit dem Hauptfenster verknuepfen
#         self.root.protocol("WM_DELETE_WINDOW", self._quit) # Routine fuer das Schliessen des Hauptfensters

#     def initInstr(self,InstrFrame):
#         self.button = ttk.Button(master=InstrFrame, text='Quit', command=self._quit)
#         self.button.grid(row=2,column=1)
#         button1 = ttk.Button(master=InstrFrame, text='Let\'s Go', command=self.opt_impedance)
#         button1.grid(row=2,column=0)

#     def InitPara(self,ParaFrame):

#         self.label1=ttk.Label(master=ParaFrame, text="Frequenz/MHz  ")
#         self.label1.grid(row=0,column=1)
#         self.input1 = ttk.Entry(master=ParaFrame, width=8)
#         self.input1.insert(END,"100")
#         self.input1.grid(row=0,column=2)
#         self.label2=ttk.Label(master=ParaFrame, text="Drahtdurchmesser/ mm  ")
#         self.label2.grid(row=1,column=1)
#         self.input2 = ttk.Entry(master=ParaFrame, width=8)
#         self.input2.insert(END,"3")
#         self.input2.grid(row=1,column=2)



#         self.result_text=scrolledtext.ScrolledText(master=ParaFrame,width=30,height=5)
#         self.result_text.grid(row=40,column=1,columnspan=3,pady=20,sticky="news")

#     def _quit(self):
#         self.root.quit()     # stops mainloop
#         self.root.destroy()  # this is necessary on Windows to prevent
#                     # Fatal Python Error: PyEval_RestoreThread: NULL tstate

#     def opt_impedance(self):
#         freq=self.get_freq()
#         rad=self.get_radius()
#         self.antenna_class.set_radius(rad)
#         self.l,res_text=self.antenna_class.opt_refl(float(self.input1.get()))

#         self.result_text.insert(index="0.0",chars=res_text)

#         freq=self.get_freq()
#         freqs=np.linspace(0.5*freq,2*freq,101)

#         Rin,Xin,Rm,Xm=self.antenna_class.impedance_f(freqs)
#         Gam=self.antenna_class.reflection2_f(freqs)
#         self.Graph.clf()
#         a=self.Graph.add_subplot(221)
#         plt.plot(freqs,Rm)
#         plt.plot(freqs,Xm)
#         plt.plot(freqs,Rin)
#         plt.plot(freqs,Xin)

#         plt.ylim([-300,300])
#         plt.legend(["Rm","Xm","Rin","Xin"])
#         plt.xlabel('Freq')
#         plt.ylabel('Rm und Xm')
#         plt.grid()

#         b=self.Graph.add_subplot(222)
#         plt.plot(freqs,Gam,"k")
#         plt.legend("Gam")
#         plt.ylabel("Reflexion in dB")
#         plt.grid()
#         self.canvas.draw()

#     def get_freq(self):
#         return float(self.input1.get())*1e6
#     def get_radius(self):
#         return float(self.input2.get())*1e-3/2

#     def set_antenna_class(self,antenna_class):
#         self.antenna_class=antenna_class
#         self.antenna_name=antenna_class.get_antenna_name()



# gui=Gui()

# ant=dipole_lam2()
# gui.set_antenna_class(ant)


# mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.
