import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import math
from scipy.optimize._lsq.dogbox import find_intersection
import scipy.special as spec
import scipy.constants as const
from scipy.optimize import minimize_scalar
from scipy.optimize import fsolve
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext

class yagi_uda_4():
    # Berechnung in 4 Schritten nach NBS Technical Note 688
    # Angestrebt: Maximaler Gain
    
    def __init__(self):
        self.length_S1 = list(range(4))

    def parasicitic_element_length(self, Curve, Ratio):
        #Functions from Fig.9 fitted by Wolfram Alpha
        x = float(Ratio)
        x2 = np.float_power(Ratio,2)
        x3 = np.float_power(Ratio,3)
        if Curve == 'A':
            f_x = -1159.38 * x3 + 98.156 * x2 - 3.722 * x + 0.468
        elif Curve == 'B':
            f_x = -974.036*x3+96.7092*x2-4.10473*x+0.461716
        elif Curve == 'C':
            f_x = -1365.36*x3+122.013*x2-4.56032*x+0.460434
        elif Curve == 'D':
            f_x = -1204.02*x3+112.893*x2-4.45069*x+0.45545
        elif Curve == 'E':
            f_x = -1184.46*x3+110.911*x2-4.45133*x+0.451263
        elif Curve == 'R1':
            f_x = 0.46068-0.00440181*np.log(x)
        elif Curve == 'R2':
            f_x = 0.483-0.5*x
        elif Curve == 'Boom':
            #Function from Fig. 10 fitted by Wolfram Alpha
            x4 = np.float_power(Ratio,4)
            f_x = 65342.6 * x4 - 4160.88 * x3 + 88.2198 * x2 + 0.0472773 * x + 0.000599967
        return f_x
    
    def circle_equation(self, x, y):
        """
        Gleichung eines Kreises.

        Parameters:
            x, y (float): Koordinaten des Punktes.
            center (tuple): (h, k) Koordinaten des Mittelpunkts des Kreises.
            radius (float): Radius des Kreises.

        Returns:
            float: Differenz zwischen linker und rechter Seite der Kreisgleichung.
        """
        h, k = self.center
        return (x - h)**2 + (y - k)**2 - self.radius**2

    def find_intersection_points(self, cubic_func, circle_eq):
        """
        Findet die Schnittpunkte zwischen einer kubischen Funktion und einem Kreis.

        Parameters:
        cubic_func : Kubische Funktion.
        circle_eq : Gleichung des Kreises.
        center : (h, k) Koordinaten des Mittelpunkts des Kreises.
        radius : Radius des Kreises.

        Returns:
        numpy.ndarray: Ein Array der Schnittpunkte als (x, y)-Koordinaten.
        """
        def intersection_equation(variables):
            x, y = variables
            return [cubic_func(x) - y, circle_eq(x, y)]

        # Startwerte fuer das fsolve-Verfahren
        initial_guess = [0, 0]

        # Loesen des Gleichungssystems fuer die Schnittpunkte
        intersection_points = fsolve(intersection_equation, initial_guess)

        return intersection_points

    def radius_Step4(self): #Beaware of magic numbers
        """ 
        Bestimmung des Abstandes der Punkt:
        D1 - D2 aus Tabelle 9
        ---------------
        x           |y
        ------------+-------
        d/Lambda|D1 | self.length_S1[1]     - Beispiel fuer 4 Elemente
        d/Lambda|D2 | self.length_S1[2]     - s.o.
        1. Bestimme d/Lambda|Dx
        2. Bestimme den Abstand
        """
        def funktion_D1(x):
            Curve = self.Curve
            if Curve == 'A':
                return -1159.38 * np.float_power(x,3) \
                       + 98.156 * np.float_power(x,2) \
                       - 3.722 * x \
                       + 0.468 \
                       - self.length_S1[1]
            elif Curve == 'B':
                return -974.036 * np.float_power(x,3) \
                       + 96.7092 * np.float_power(x,2) \
                       - 4.10473 * x \
                       + 0.461716  \
                       - self.length_S1[1]
            elif Curve == 'C':
                return -1365.36 * np.float_power(x,3) \
                       + 122.013 * np.float_power(x,2) \
                       - 4.56032 * x \
                       + 0.460434  \
                       - self.length_S1[1]
            elif Curve == 'D':
                return -1204.02 * np.float_power(x,3) \
                    + 112.893 * np.float_power(x,2) \
                    - 4.45069 * x \
                    + 0.45545   \
                    - self.length_S1[1]
            elif Curve == 'E':
                return -1184.46 * np.float_power(x,3) + 110.911 * np.float_power(x,2) - 4.45133 * x + 0.451263  - self.length_S1[1]
            elif Curve == 'R1':
                return 0.46068 - 0.00440181 * np.log(x)                                                         - self.length_S1[1]
            elif Curve == 'R2':
                return 0.483 - 0.5 * x
        
            
        def funktion_D2(x):
            Curve = self.Curve
            if Curve == 'A':
                return -1159.38 * np.float_power(x,3) + 98.156 * np.float_power(x,2) - 3.722 * x + 0.468        - self.length_S1[2]
            elif Curve == 'B':
                return -974.036 * np.float_power(x,3) + 96.7092 * np.float_power(x,2) - 4.10473 * x + 0.461716  - self.length_S1[2]
            elif Curve == 'C':
                return -1365.36 * np.float_power(x,3) + 122.013 * np.float_power(x,2) - 4.56032 * x + 0.460434  - self.length_S1[2]
            elif Curve == 'D':
                return -1204.02 * np.float_power(x,3) + 112.893 * np.float_power(x,2) - 4.45069 * x + 0.45545   - self.length_S1[2]
            elif Curve == 'E':
                return -1184.46 * np.float_power(x,3) + 110.911 * np.float_power(x,2) - 4.45133 * x + 0.451263  - self.length_S1[2]
            elif Curve == 'R1':
                return 0.46068 - 0.00440181 * np.log(x)                                                         - self.length_S1[2]
            elif Curve == 'R2':
                return 0.483 - 0.5 * x
        
        x_start = 0.001
        
        d_Lamb_D1 = fsolve(funktion_D1, x_start)
        d_Lamb_D2 = fsolve(funktion_D2, x_start)
        delta_d_Lamb = d_Lamb_D2-d_Lamb_D1
        delta_length = self.length_S1[1] - self.length_S1[2]
        #Ansatz ueber Pythagoras
        radius = np.sqrt(np.float_power(delta_d_Lamb,2)+np.float_power(delta_length,2)) 
        return radius

    def step_1(self):
        #Source Table 1 - 4 Elemente Yagi-Uda-Antenne
        #Table 1 or Fig.09 contains an error according to the usage/naming of the curves B) and C)
        #For further usage B) and C) are used as given in Fig.09
        self.E_Space = 0.2 * self.Lamb  #Spacing Length
        self.O_Length = 0.8 * self.Lamb #Overall Length
        self.Curve = 'C'
        self.Curve_Ref = 'R1'
        
        #Values from Table 1
        self.length_S1[0] = 0.482 #* self.Lamb #Reflector
        self.length_S1[1] = 0.428 #* self.Lamb #Director 1
        self.length_S1[2] = 0.424 #* self.Lamb #Director 2
        self.length_S1[3] = 0.428 #* self.Lamb #Director 3
        
        self.gain = 9.2
        
        return
    
    def step_2(self):
        """
        
        """
        self.L_D1 = self.parasicitic_element_length(self.Curve, self.d_Lamb) #* self.Lamb
        self.L_D3 = self.L_D1 #* self.Lamb
        return
    
    def step_3(self):
        """
        Bestimmung der unkompensierten Laenge des Reflektors ueber Fig. 9 mit d/Lamb
        """
        self.L_R = self.parasicitic_element_length(self.Curve_Ref, self.d_Lamb)
        self.L_R = self.L_R #* self.Lamb
        return
    
    def step_4(self):
        """
        English-->German
        Mit einem Zirkel den Abstand zwischen, den Urspruenglich aus der Tabelle abgelesenen Werten,
        fuer D1 = D3 und D2 bestimmen. (Aus Schritt 1)
        Diese Distanz dann auf den unkompensierten Punkt D1=D3 uebertragen.
        Das ergibt den unkompensierten D2-Wert
        ----------------------------
        Ansatz:
        Der D1=D3 Punkt wird als Mittelpunkt fuer den Kreis K1 mit dem Radius des Abstandes von 
        den kompensierten Punkten D1=D3 und D2 (Schritt 1)
        Danach werden die Schnittpunkte von K1 mit parasitic_element_length() gebildet, 
        der Schnittpunkt mit x<d/Lambda wird verworfen
        """
        
        #Bestimmung der Funktion nach der Gesucht wird.
        function = lambda x: self.parasicitic_element_length(self.Curve, x)

        #Bestimmung der Kreisparameter
        self.center = (self.d_Lamb, self.L_D1)
        self.radius = self.radius_Step4()
        
        intersection_points = self.find_intersection_points(function, self.circle_equation)
        for wert in intersection_points:
            if wert <=0.05 and wert >= 0.001:
                LD2 = self.parasicitic_element_length(self.Curve, wert)
            else:
                LD2 = 0.424 #Wert aus Tabelle 1
                
        self.L_D2 = LD2
        return    
    
    def step_5(self):
        cor_f = self.parasicitic_element_length('Boom', self.D_Boom)
        self.L_D1 = self.L_D1 + cor_f
        self.L_D2 = self.L_D2 + cor_f
        self.L_D3 = self.L_D3 + cor_f
        self.L_R = self.L_R   + cor_f

        self.L_D1 = self.L_D1 * self.Lamb
        self.L_D2 = self.L_D2 * self.Lamb
        self.L_D3 = self.L_D3 * self.Lamb
        self.L_R = self.L_R   * self.Lamb

    def Res_yagi_uda(self, input1, input2, input3): #Frequenz in MHz #Durchmesser in mm #Boom Diam in cm
        #Gegebene Werte
        self.Freq = float(input1) * 1e6 #MHz in Hz
        self.Diam = float(input2) * 1e-3 #mm in m
        self.Boom = float(input3) * 1e-2 #cm in m
        
        #Abgeleitete Werte
        self.Lamb = const.c/self.Freq
        self.d_Lamb = self.Diam/self.Lamb
        self.D_Boom = self.Boom/self.Lamb
        
        
        #Step 1:
        self.step_1()
        #Step 2:
        self.step_2()
        #Step 3:
        self.step_3()
        #Step 4:
        self.step_4()
        #Step 5:
        self.step_5()

        #Toleranz
        self.Toleranz = 0.003*self.Lamb
        res_text = f"Fuer die Werte: \n Freqeunz: {str(self.Freq)} Hz \n Durchmesser der Draehte: {str(self.Diam)} m \n"
        res_text = res_text + f"Durchmesser des Booms: {str(self.Boom)} m \n Lambda: {str(self.Lamb)} \n"
        res_text = res_text + f"Toleranz: {str(self.Toleranz)} m \n"
        res_text = res_text + f"Die Laenge der Elemente betraegt: \nReflektor: {str(self.L_R)} m\nDirektor 1: {str(self.L_D1)}m"
        res_text = res_text + f"\nDirektor 2: {str(self.L_D2)} m\nDirektor 3: {str(self.L_D3)} m\n\n"
        
        length = (self.L_R, self.L_D1, self.L_D2, self.L_D3)
        #Ausgabe
        self.l = length
        return length, res_text
    def set_radius (self, rad):
        
        return
    
    def get_antenna_name(self):
        return "Yagi-Uda 4 Elemente"
    