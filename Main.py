from tkinter import mainloop
import sici
import GUI


gui=GUI.Gui()


#TODE GET RID OF:
ant=sici.dipole_lam2()
gui.set_antenna_class(ant)
#

mainloop()