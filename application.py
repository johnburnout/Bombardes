from tkinter import *
from random import randrange
from canon import *
from pupitre import *
        
class Application(Frame) :
    """Fenêtre principale de l'application"""
    def __init__(self, width=600, height=400, joueurs=["Jean", "Soaz"]) :
        Frame.__init__(self)
        self.master.title("Jeu des bombardes !")
        self.pack()
        self.joueurs=joueurs
        self.jeu = Canvas(self, width=600, height=400, bg="#6edc95", bd=3, relief=SUNKEN)
        self.largeur, self.hauteur = width, height
        self.jeu.pack(padx=8, pady=8)
        self.guns={}     #Dictionnaire des canons présents
        self.pupi={}     #Dictionnaire des pupitres présents
        #instanciation de deux canons opposés
        self.guns[joueurs[0]] = Canon(self.jeu, joueurs[0], 30, self.hauteur-50, 1, "#006b6b")        
        self.guns[joueurs[1]] = Canon(self.jeu, joueurs[1], width-30, self.hauteur-50, -1, "#2f486b")
        # instanciation des pupitres
        self.pupi[joueurs[0]] = Pupitre(self, self.guns[joueurs[0]])        
        self.pupi[joueurs[1]] = Pupitre(self, self.guns[joueurs[1]])
        self.joueurActif = randrange(0,2)
        self.pupi[joueurs[self.joueurActif]].bCharge.configure(state=NORMAL)
        
    def disperser(self) :
        for iden in self.guns :
            gun = self.guns[iden]
            #Positionner à droite ou à gauche
            if gun.sens == 1 :
                x = randrange(20, 80)
            else :
                x = randrange(self.largeur-80, self.largeur-20)
            gun.deplacer(x,randrange(self.hauteur/2, self.hauteur-10))
            
    def goal(self, i, j) :
        "La canon 'i' signale qu'il a touché l'adversaire 'j'"
        if i != j :
            self.pupi[i].attribuerPoint(1)
        else :            
            self.pupi[i].attribuerPoint(-1)
            
    def changerJoueur(self) :
        self.joueurActif = (self.joueurActif + 1) % 2        
        self.pupi[self.joueurs[self.joueurActif]].bCharge.configure(state=NORMAL)
            
    def dictionnaireCanons(self) :
        "Revoyer le dictionnaire des canons présents"
        return self.guns