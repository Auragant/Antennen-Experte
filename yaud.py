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

class yagi_uda_4():
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
                +"erreicht bei Laenge "+'{:6.4f}'.format(optr.x)+"m\n="\
                +'{:6.4f}'.format(optr.x/lam)+" Wellenlaengen\n\n"
        print(res_text)
        self.l=optr.x
        return optr.x,res_text

    def set_radius(self,rad):
        self.radius=rad
    def set_length(self,l):
        self.l=l
    def get_antenna_name(self):
        return "Half Wave Dipole"
