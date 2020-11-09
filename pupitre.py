from tkinter import *
      
class Pupitre(Frame) :
    """Pupitre de réglage associé à un canon"""
    def __init__(self, boss, canon):
        Frame.__init__(self, bd=3, relief=GROOVE)
        self.score = 0
        self.appli = boss        #Ref de l'application
        self.canon = canon       #Ref du canon
        # Système de réglage de l'angle de tir
        self.reglAngle = Scale(self, from_=85, to=-15, troughcolor=canon.coul,
                    command=self.orienter, showvalue=0)
        self.reglAngle.set(45)    #Angle initial de tir
        self.reglAngle.pack(side=LEFT)
        # Système de réglage de la dose
        self.reglDose = Scale(self, from_=30, to=5, troughcolor='red',
                    command=self.doser, showvalue=0)
        self.reglDose.set(15)    #Dose initiale de poudre
        self.reglDose.pack(side=LEFT)
        # Identification du canon
        Label(self, text = canon.id).pack(side=TOP, anchor=W, pady=5)
        # Bouton de charge
        self.bCharge = Button(self, text='Charge', command=self.charger, state=DISABLED)
        self.bCharge.pack(side=BOTTOM, padx=5, pady=5)
        # Bouton de tir
        self.bTir = Button(self, text='Feu !', command=self.tirer, state=DISABLED)
        self.bTir.pack(side=BOTTOM, padx=5, pady=5)
        Label(self, text='points').pack()
        self.points = Label(self, text='0', bg='white')
        self.points.pack()
        # positionner à droite ou à gauche selon le sens du canon
        if canon.sens == -1 :
            self.pack(padx=10, pady=10, side=RIGHT)
        else :            
            self.pack(padx=10, pady=10, side=LEFT)        
    
    def tirer(self) :
        "Déclencher le tir du canon associé"
        self.canon.feu()
        self.bTir.configure(state=DISABLED)
#        self.bCharge.configure(state=NORMAL)
        self.appli.changerJoueur()
        
    def charger(self) :
        "Déclencher le tir du canon associé"
        self.canon.charger()
        self.bTir.configure(state=NORMAL)
        self.bCharge.configure(state=DISABLED)
    
    def orienter(self, angle) :
        "Ajuster la hausse du canon"
        self.canon.orienter(angle)
        
    def doser(self, dose) :
        "Ajuster le dosage de poudre"
        self.canon.doser(dose)
        
    def attribuerPoint(self, p) :
        "Incrémenter ou décrémenter le score"
        self.score += p
        self.points.configure(text=' {} '.format(self.score))
