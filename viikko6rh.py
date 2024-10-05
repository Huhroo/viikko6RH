import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.colors as mcolors
import random
import threading
import time
import winsound

root = tk.Tk()
root.title("Allaskaivuu")
root.geometry("1200x800+200+200")


# Luo uima-allas ja oja-matriisit
uimaAllas = np.zeros((20, 60))   
eOja = np.ones((100, 1))
kOja = np.ones((100, 1))
tiedot={}
tiedot = {"apinat": []}   
kaivuutila = 0
allaslippu = 0
merilippu = 0
VAIKENE = 0

def luoapinat(num_monkeys=1000):
    global tiedot
    
    for i in range(1, num_monkeys + 1):
        apina = {
            'id': i,
            'paikka': 'metsä',
            'väsymys': 1,
            'x': None,
            'y': None,
            'lukko': threading.Lock()
        }
        tiedot["apinat"].append(apina)   

def allasTarkkailija():
    global allaslippu, merilippu
    def allasloop():
        while allaslippu == 0:
            allastarkkailu()
            time.sleep(1)
    threading.Thread(target=allasloop).start()        #tämän tavan tehdä threadejä opin teköälyltä, 

def allastarkkailu():
    global eOja, kOja , uimaAllas, allaslippu
    if eOja[99] <= -100 or kOja[99] <= - 100:
        allaslippu = 1
        uimaAllas = np.ones((20, 60))
        c.set_array(uimaAllas)
        uimaallas_canvas.draw()
        if eOja[99] <= -100:
            time.sleep(5)
            winsound.Beep(344,10000)
        else:
            time.sleep(5)
            winsound.Beep(744,10000)
    else:
        print("kaikki hiljaista allas rintamalla")                

def ernestiHakee():
    global tiedot, eOja
    
    
    for apina in tiedot["apinat"]:
        if apina['paikka'] == 'metsä':
            max_y_index = len(eOja) - 1
            attempts = 0   
            
             
            while attempts < max_y_index:
                 
                random_y = random.randint(100, 199)
                y_index = random_y - 100   

                if eOja[y_index][0] == 1:  # Jos paikkaa ei ole kaivettu
                    y = random_y   
                    break
                else:
                    attempts += 1
                    print(f"Paikka ({random_y}) on jo kaivettu, etsitään uusi paikka.")
            else:
                # Jos kaikki paikat on kaivettu, valitaan satunnainen y-koordinaatti ilman ehtoja
                y = random.randint(100, 199)
                print("Kaikki paikat on kaivettu, sijoitetaan apina satunnaiseen paikkaan.")
                break
            apina['paikka'] = 'ernesti'
            apina['esine'] = 'Lapio'
            print(apina)
            x = 353
            
            
            
            
          
            apina['x'] = x
            apina['y'] = y
            
           
            apinaleima = tk.Label(root, text="", bg='brown', width=1, height=1,padx=0, pady=0)
            apinaleima.place(x=x, y=y) 
            apina['leima']=apinaleima
            
            print(f"Apina {apina['id']} siirretty metsästä ernestille.")
            break 

def kernestiHakee():
    global tiedot, kOja
    
  
    for apina in tiedot["apinat"]:
        if apina['paikka'] == 'metsä':
            max_y_index = len(kOja) - 1
            attempts = 0   
            
            # Yritä löytää satunnainen paikka, jota ei ole vielä kaivettu
            while attempts < max_y_index:
                 
                random_y = random.randint(100, 199)
                y_index = random_y - 100   

                if eOja[y_index][0] == 1:  # Jos paikkaa ei ole kaivettu
                    y = random_y   
                    break
                else:
                    attempts += 1
                    print(f"Paikka ({random_y}) on jo kaivettu, etsitään uusi paikka.")
            else:
                # Jos kaikki paikat on kaivettu, valitaan satunnainen y-koordinaatti ilman ehtoja
                y = random.randint(100, 199)
                print("Kaikki paikat on kaivettu, sijoitetaan apina satunnaiseen paikkaan.")
                break
            apina['paikka'] = 'kernesti'
            apina['esine'] = 'Lapio'
            print(apina)
            x = 428 
            
           
            apina['x'] = x
            apina['y'] = y
            
           
            apinaleima = tk.Label(root, text="", bg='brown', width=1, height=1,padx=0, pady=0)
            apinaleima.place(x=x, y=y)  
            apina['leima']=apinaleima
            
            print(f"Apina {apina['id']} siirretty metsästä ernestille.")
            break  

def eHakeeThread():
    kahvaEHaku= threading.Thread(target=ernestiHakee)
    kahvaEHaku.start()       

def kHakeeThread():
    kahvaKHaku= threading.Thread(target=kernestiHakee)
    kahvaKHaku.start()                


luoapinat()  


def kaiva_ojia():
    global tiedot, eOja, kOja
    
   
    for apina in tiedot["apinat"]:
        if apina['paikka'] == 'ernesti':
            Ernekaivuu(apina)
        if apina['paikka'] == 'kernesti':
            Kernekaivuu(apina)
    

      
def apinakaivaaErne(apina):
    global VAIKENE
    if apina['lukko'].acquire(blocking=False):  # Varmistetaan, että apinaa ei jo käytetä
        try:
            
            y_value = apina['y'] 
            y_index = int(-100 + y_value)  
            
            if 0 <= y_index < len(eOja):

                time.sleep(apina['väsymys'])
                apina['väsymys'] = apina['väsymys'] * 2    
                        
                if VAIKENE == 0:    
                   winsound.Beep(500, 500)    
                eOja[y_index] = eOja[y_index] - 1   
                print(f"eOja[{y_index}]: {eOja[y_index][0]}")  
                apina['y'] -= 1  
                c_eOja.set_array(eOja)
                eOja_canvas.draw()
            else:
                print(f"Y index {y_index} is out of bounds.")
            
            
            x = apina['x']
            y = apina['y']
            apina['x'] = x
            apina['y'] = y
            
   
            if apina['leima'] is not None:  
                apina['leima'].place(x=x, y=y)  
            
            print(f"Ernen Apina {apina['id']} kaivoi ojan ja siirretty y-koordinaattiin {apina['y']}.")
        
        finally:
            apina['lukko'].release()  # Vapautetaan lukko, kun apina on valmis kaivamaan
    else:
        print(f"Apina {apina['id']} on jo kaivamassa.")

def apinakaivaaKerne(apina):
    global VAIKENE
    if apina['lukko'].acquire(blocking=False):  # Varmistetaan, että apinaa ei jo käytetä
        try:
           
            y_value = apina['y'] 
            y_index = int(-100 + y_value)  
            
            if 0 <= y_index < len(kOja):
                time.sleep(apina['väsymys'])
                apina['väsymys'] = apina['väsymys'] * 2
                
                if VAIKENE == 0:     
                    winsound.Beep(500, 500)    
                kOja[y_index] = kOja[y_index] - 1  
                print(f"kOja[{y_index}]: {kOja[y_index][0]}")   
                apina['y'] -= 1 
                c_kOja.set_array(kOja)
                kOja_canvas.draw()
            else:
                print(f"Y index {y_index} is out of bounds.")
            
        
            x = apina['x']
            y = apina['y']
            apina['x'] = x
            apina['y'] = y
            
           
            if apina['leima'] is not None: 
                apina['leima'].place(x=x, y=y) 
            
            print(f"Kernen Apina {apina['id']} kaivoi ojan ja siirretty y-koordinaattiin {apina['y']}.")
        
        finally:
            apina['lukko'].release()  # Vapautetaan lukko, kun apina on valmis kaivamaan
    else:
        print(f"Apina {apina['id']} on jo kaivamassa.")

def Ernekaivuu(apina):
    ekaivuukahva = threading.Thread(target=apinakaivaaErne,args=(apina,))
    ekaivuukahva.start()

def Kernekaivuu(apina):
    kkaivuukahva = threading.Thread(target=apinakaivaaKerne,args=(apina,))
    kkaivuukahva.start()

def toggle_tila():
    global kaivuutila
    kaivuutila = 1 - kaivuutila  # Vaihdetaan tilan arvo välillä 0 ja 1
    print(f"Tila: {kaivuutila}")

def start_kaiva_ojia_loop():
    global kaivuutila
    
    def loop():
        if kaivuutila == 1:
            kaiva_ojia()   
        root.after(1000, loop)   
    
    loop()   

start_kaiva_ojia_loop()    

def reset_ojat():
    global eOja, kOja
    
    
    eOja = np.ones((100, 1))
    kOja = np.ones((100, 1))
    c_eOja.set_array(eOja)
    c_kOja.set_array(kOja)
    kOja_canvas.draw()
    eOja_canvas.draw()

    for apina in tiedot["apinat"]:
        apina['paikka'] = 'metsä'
        apina['väsymys'] = 1
        
         
        if apina.get('leima') is not None:
            apina['leima'].place_forget()   
            apina['leima'] = None   
        
    print("Ojat on täytetty ja apinat siirretty takaisin metsään.")

def ernestiHakeeFiksusti():
    global tiedot, kaivuutila
    
    position = 199

    for apina in tiedot["apinat"]:
        if apina['paikka'] == 'metsä':
                
            apina['paikka'] = 'ernesti'
            apina['esine'] = 'Lapio'
            
            x = 353
            y = random.randint(100, 199) 
            apina['x'] = x
            apina['y'] = y
            
            apinaleima = tk.Label(root, text="", bg='brown', width=1, height=1,padx=0, pady=0)
            apinaleima.place(x=x, y=y) 
            apina['leima']=apinaleima
            print(f"Apina {apina['id']} siirretty metsästä ernestille.")
            kaivuutila = 1
            time.sleep(1)
            break 
    
    for i in range(9):
       for apina in tiedot["apinat"]:
           if apina['paikka'] == 'metsä':
                
                apina['paikka'] = 'ernesti'
                apina['esine'] = 'Lapio'
            
                x = 353
                y = position   
                apina['x'] = x
                apina['y'] = y
            
                apinaleima = tk.Label(root, text="", bg='brown', width=1, height=1,padx=0, pady=0)
                apinaleima.place(x=x, y=y) 
                apina['leima']=apinaleima
                position -= 11
                print(f"Apina {apina['id']} siirretty metsästä ernestille.")
                kaivuutila = 1
                time.sleep(1)
                break 

def kernestiHakeeFiksusti():
    global tiedot,kaivuutila
    
    position = 199

    for apina in tiedot["apinat"]:
        if apina['paikka'] == 'metsä':
                
            apina['paikka'] = 'ernesti'
            apina['esine'] = 'Lapio'
            
            x = 428
            y = random.randint(100, 199) 
            apina['x'] = x
            apina['y'] = y
            
            apinaleima = tk.Label(root, text="", bg='brown', width=1, height=1,padx=0, pady=0)
            apinaleima.place(x=x, y=y) 
            apina['leima']=apinaleima
            print(f"Apina {apina['id']} siirretty metsästä ernestille.")
            kaivuutila = 1
            time.sleep(1)
            break 
    
    for i in range(10):
       for apina in tiedot["apinat"]:
           if apina['paikka'] == 'metsä':
                
                apina['paikka'] = 'kernesti'
            
                x = 428
                y = position   
            
                apina['x'] = x
                apina['y'] = y
            
                apinaleima = tk.Label(root, text="", bg='brown', width=1, height=1,padx=0, pady=0)
                apinaleima.place(x=x, y=y) 
                apina['leima']=apinaleima
                position -= 11
                kaivuutila = 1
                time.sleep(1)   
                print(f"Apina {apina['id']} siirretty metsästä ernestille.")
                break  
           
def meriTarkkailuE():
    global eOja, VAIKENE
    
    for i in range(len(eOja)):
         
        if eOja[0] <= -100:
            VAIKENE = 1 
        if eOja[i][0] <= 0:
            if eOja[i][0] > -100:
                eOja[i][0] = -100
                time.sleep(0.25)
                winsound.Beep(244,500)
                print(f"eOja[{i}] on nyt täynnä vettä (-100).")
            
                  
                c_eOja.set_array(eOja)
                eOja_canvas.draw()
            else:
                continue    
        else:
             
            print(f"eOja[{i}] ei ole valmis vettä varten.")
            break
def meriTarkkailuK():
    global  kOja, VAIKENE
    
    
    for i in range(len(kOja)):
         
        if eOja[0] <= -100:
            VAIKENE = 1 
        if kOja[i][0] <= 0:
            if kOja[i][0] > -100:
                kOja[i][0] = -100
                time.sleep(0.25)
                winsound.Beep(744,500)
                print(f"eOja[{i}] on nyt täynnä vettä (-100).")
            
                 
                c_kOja.set_array(kOja)
                kOja_canvas.draw()
            else:
                continue    

        else:
             
            print(f"kOja[{i}] ei ole valmis vettä varten.")
            break               

def aloita_vesisimulaatio():
    global merilippu
    def simulaatiolooppi():
        while merilippu == 0:
             
            
            threading.Thread(target=meriTarkkailuE).start()
            threading.Thread(target=meriTarkkailuK).start()
            time.sleep(1)   
    
     
    threading.Thread(target=simulaatiolooppi).start()


            

     
                            
        
           
def eFiksuThread():
    eFiksuKahva=threading.Thread(target=ernestiHakeeFiksusti)
    eFiksuKahva.start()        

def kFiksuThread():
    kFiksuKahva=threading.Thread(target=kernestiHakeeFiksusti)
    kFiksuKahva.start()         
    

 
ojavarit = ['blue','brown','yellow']
allasvarit = ['brown', 'blue']

 
cmap_oja = mcolors.LinearSegmentedColormap.from_list("custom", [ #tämä on teköäly koodia
    (0/100, ojavarit[0]),       
    (99/100, ojavarit[1]),      
    (100/100, ojavarit[2])      
])
cmapallas = mcolors.ListedColormap(allasvarit)

 
 
 
oja_boundaries = [-100, 0, 1]   
allas_boundaries = [0, 1]   

 
norm_oja = mcolors.Normalize(vmin=-100, vmax=1)
allas_norm = mcolors.BoundaryNorm(allas_boundaries, cmapallas.N)

 


 
canvas = tk.Canvas(root, width=800, height=600, bg='blue')
canvas.place(x=0, y=0)

 
canvas.create_rectangle(100, 100, 700, 500, fill='yellow')
canvas.create_rectangle(150, 400, 200, 200, fill="green")

 
fig, ax = plt.subplots(figsize=(1, 0.34))
c = ax.imshow(uimaAllas, cmap=cmapallas, norm=allas_norm)
ax.axis('off')   
fig.patch.set_alpha(0)
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)


 
uimaallas_canvas = FigureCanvasTkAgg(fig, master=root)
uimaallas_canvas.draw()

 
uimaallas_canvas.get_tk_widget().place(x=340, y=200)   

 
fig_eOja, ax_eOja = plt.subplots(figsize=(0.01, 1))
c_eOja = ax_eOja.imshow(eOja, cmap=cmap_oja, norm=norm_oja)
ax_eOja.axis('off')   
fig_eOja.patch.set_alpha(0)
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

 
eOja_canvas = FigureCanvasTkAgg(fig_eOja, master=root)
eOja_canvas.draw()
eOja_canvas.get_tk_widget().place(x=350, y=100)   

 
fig_kOja, ax_kOja = plt.subplots(figsize=(0.01, 1))
c_kOja = ax_kOja.imshow(kOja, cmap=cmap_oja, norm=norm_oja)
ax_kOja.axis('off')
fig_kOja.patch.set_alpha(0)
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

kOja_canvas = FigureCanvasTkAgg(fig_kOja, master=root)
kOja_canvas.draw()
kOja_canvas.get_tk_widget().place(x=425, y=100)   

ernesti_lahettaa=tk.Button(text='Ernestin hakee apinan',command=eHakeeThread, bg='green')
ernesti_lahettaa.place(x=10,y=650)
ernesti_kaivaa=tk.Button(text='Ernestin kaivaa',command=kaiva_ojia, bg='green')
ernesti_kaivaa.place(x=10,y=675)

kernesti_lahettaa=tk.Button(text='Kernestin hakee apinan',command=kHakeeThread, bg='blue')
kernesti_lahettaa.place(x=160,y=650)
kernesti_kaivaa=tk.Button(text='Kernestin kaivaa',command=kaiva_ojia, bg='blue')
kernesti_kaivaa.place(x=160,y=675)

tayta_ojat=tk.Button(text="Täytä ojat",command=reset_ojat,bg='orange')
tayta_ojat.place(x=310,y=650)

ernesti_fiksu=tk.Button(text="Ernestin viisaat apinat",command=eFiksuThread,bg='orange')
ernesti_fiksu.place(x=310,y=675)

kernesti_fiksu=tk.Button(text="Kernestin viisaat apinat",command=kFiksuThread,bg='orange')
kernesti_fiksu.place(x=310,y=700)

merinappi=tk.Button(text="aloita meri",command=aloita_vesisimulaatio,bg='yellow')
merinappi.place(x=460,y=650)

allasnappi=tk.Button(text="aloita allas vahti",command=allasTarkkailija,bg='yellow')
allasnappi.place(x=460,y=675)



tyot=tk.Button(text='Toggle työt',command=toggle_tila, bg='blue')
tyot.place(x=160,y=700)


 
root.protocol("WM_DELETE_WINDOW", root.quit) #tämä on teköälykoodia

 
root.mainloop()
