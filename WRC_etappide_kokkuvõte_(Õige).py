import tkinter as tk
from tkinter.ttk import Progressbar, Treeview, Scrollbar
import time
from webscrape import rallyList, rallyResults
import threading

ui = tk.Tk()
ui.geometry("400x200")

temp_list = []
hooaeg_label = tk.Label()

soitja_button = tk.Button()
etapp_button = tk.Button()

def valju():
   ui.destroy()

def hooaeg():

    global hooaeg_label

    h = ("2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017",
    "2018", "2019", "2020")

    hooaeg_label = tk.Label(ui, text="Vali hooaeg:")
    hooaeg_label.pack()

    hooaeg = tk.StringVar(ui)
    hooaeg.set(h[-1])

    w_hooaeg = tk.OptionMenu(ui, hooaeg, *h)
    w_hooaeg.pack()

    valju_button = tk.Button(ui, text="Välju", command=valju)
    valju_button.pack()

    def edasi(default = hooaeg):

        global soitja_button, etapp_button

        temp_list.append(default.get())

        hooaeg_label.configure(text="Kas soovid vaadata etappide tulemusi?")

        w_hooaeg.destroy()
        valju_button.destroy()
        edasi_button.destroy()

        soitja_button = tk.Button(ui, text="Ei", command=quit)
        soitja_button.pack()

        etapp_button = tk.Button(ui, text="Jah", command=etapp)
        etapp_button.pack()


    edasi_button = tk.Button(ui, text="Edasi", command=edasi)
    edasi_button.pack()

def etapp():
    global etapp_

    etapp_ = tk.StringVar(ui)

    progressbar = Progressbar(ui, mode='indeterminate')
    progressbar.pack()

    def getRallyData():
        global edasi_button, w_etapp

        valikud = rallyList(temp_list[0])
        w_etapp = tk.OptionMenu(ui, etapp_, *valikud.keys())
        w_etapp.pack()
        hooaeg_label.configure(text="Vali etapp:")
        progressbar.destroy()

        edasi_button = tk.Button(ui, text="Edasi", command=etapiTulemused)
        edasi_button.pack()
    
    def etapiTulemused(default = etapp_):
        edasi_button.destroy()
        w_etapp.destroy()

        andmed = rallyResults(etapp_.get(), temp_list[0])

        pealkirjad = ('Nimi', 'Auto', 'Aeg')

        hooaeg_label.configure(text="Etapi tulemused:")
        results = Treeview(ui, columns=pealkirjad, show='headings')

        for pealkiri in pealkirjad:
            results.heading(pealkiri, text=pealkiri)

        scroll = Scrollbar(ui, orient="vertical", command=results.yview)
        scroll.pack(side='right', fill='y')
        results.configure(yscrollcommand=scroll.set)

        for key in andmed:
            results.insert("", "end", values=(andmed[key]["Nimi"], andmed[key]["Auto"], andmed[key]["Aeg"]))
        results.pack()

    soitja_button.destroy()
    etapp_button.destroy()

    thread = threading.Thread(target=getRallyData)
    progressbar.start()
    thread.start()
    hooaeg_label.configure(text="Laen andmeid")
    pass

hooaeg()
ui.mainloop()