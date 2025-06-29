'''
metodi usati per convertire i valori letti dall'obd nelle varie informazioni

tutti i metodi richiedono l'intero valore letto tramite obd
'''

def conv_rmp(value):
    A, B = int(value[0:2], 16), int(value[2:4], 16)
    rpm = ((A * 256) + B) / 4
    return rpm

def conv_gas(value):
    gas = value[8:10]
    perc_gas = 100 / 255 * int(gas, 16)
    return perc_gas

def conv_vel(value):
    vel = int(value[4:8], 16)/100
    return vel

def conv_temp(value):
    temp = int(value[:2], 16)-40
    return temp

def conv_freno(value):
    freno = int(value[:2], 16)-40
    return freno

def conv_luci(value):
    luci = {
        "C0": 0,  # 'Spenti'
        "AA": 1,  # 'Anabbaglianti'
        "D0": 2,  # 'Abbaglianti'
    }

    frecce = {
        "00": 'off',  # Spente
        "10": 'sx',   # Freccia sinistra
        "20": 'dx',   # Freccia destra
        "AA": 'all',  # 4 frecce
                }
    return luci.get(value[:2], 'Sconosciuto'), frecce.get(value[2:4], 'off')

def conv_marcie(value):
    marce = {
        "AA": 'R',   
        "1C": 1,  
        "1F": 2,  
        "22": 3,  
        "24": 4,  
        "26": 5,  
        "29": 6,  
    }
    print(value)
    print(value[-4:-2])
    return marce.get(value[-4:-2], 'Sconosciuto')