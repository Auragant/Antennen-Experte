import sici 
import yaud

antenna_list = [
    ('Dipol'),
    ('Yagi-Uda'),
    ]

#Liste mit den Dateien, f�r die einzelnen Antennen:
class_antenna_list = [
    sici.dipole_lam2(),
    #yaud.yagi_uda(),
    ]