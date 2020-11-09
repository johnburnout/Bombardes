from tkinter import *
from math import sin, cos, pi
from random import randrange

class Canon(object) :
    """Petit canon graphique"""
    def __init__(self, boss, ident, x, y, sens, coul="midnight blue", lBuse=30):
        self.boss = boss           #Référence du canevas
        self.appli = boss.master   #Référence de la fenêtre de l'application
        self.id = ident            #Id du canon
        self.coul = coul           #Couleur associée au canon
        self.x1, self.y1 = x, y    #Axe de rotation du canon
        self.sens = sens           #Sens de tir (-1 : gauche, +1 : droite)
        self.lBuse = lBuse         #Longueur du canon
        self.angle = 0             #Hausse par défaut
        # Largeur ey hauteur du canevas :
        self.xMax, self.yMax = int(boss.cget('width')), int(boss.cget('height'))
        # Dessiner la buse du canon
        self.x2, self.y2 = x + lBuse*self.sens, y
        self.buse = boss.create_line(self.x1, self.y1, self.x2, self.y2, fill=coul, width=lBuse//3)
        self.rc = 5*lBuse//10
        self.v = 5
        self.corps = boss.create_oval(x-self.rc, y-self.rc, x+self.rc, y+self.rc, fill=coul, width=0)
        self.charge = FALSE
        self.anim = FALSE
        self.explo = FALSE
        # Dessiner un obus "caché"
        self.obus = boss.create_oval(-10, -10,
                            -10, -10, fill='red')
        
    def orienter(self, angle) :
        """Choisir l'angle de tir"""
        self.angle = float(angle)*pi/180
        self.x2, self.y2 = int(self.x1 + self.lBuse*cos(self.angle)*self.sens), int(self.y1 - self.lBuse*sin(self.angle))
        self.boss.coords(self.buse, self.x1, self.y1, self.x2, self.y2)
        
    def doser(self, v=15) :
        self.v = float(v)*self.lBuse/50
        if self.v > 30 :
            self.v = 30
        elif self.v < 5 :
            self.v = 5
#        if self.charge :
#            self.boss.coords(self.obus, int(self.x1-self.v*self.lBuse//40), int(self.y1-self.v*self.lBuse//40),
#                                int(self.x1+self.v*self.lBuse//40), int(self.y1+self.v*self.lBuse//40))
        
    def charger(self, v=15) :
        """Charger le canon"""
#        print('en charge')
        if not self.charge :
#            print('chargé !')
            self.charge = TRUE
#            self.boss.coords(self.obus, int(self.x1-self.v*self.lBuse//40), int(self.y1-self.v*self.lBuse//40),
#                                int(self.x1+self.v*self.lBuse//40), int(self.y1+self.v*self.lBuse//40))
        
    def deplacer(self, x, y) :
        """Amener le canon dans une nouvelle position x,y"""
        dx, dy = x - self.x1, y - self.y1
        self.boss.move(self.buse, dx, dy)
        self.boss.move(self.corps, dx, dy)
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy
        
    def feu(self) :
        """Déclencher le tir"""
        if not (self.anim or self.explo) and self.charge :
#            print('feu !')
            self.anim = TRUE
            # Récuperer la description des canons présents
            self.guns = self.appli.dictionnaireCanons()            
            self.boss.coords(self.obus, self.x2-3*self.lBuse//30, self.y2-3*self.lBuse//30,
                            self.x2+3*self.lBuse//30, self.y2+3*self.lBuse//30)
            self.vx, self.vy = self.v*cos(self.angle)*self.sens, -self.v*sin(self.angle)
            self.charge = FALSE
            self.animer_obus()
            return TRUE #-> Signaler que le coup est parti
        else :
            return FALSE #-> le coup n'a pu être tiré
            
    def animer_obus(self) :
        """Animation de l'obus"""
        if self.anim :
            self.boss.move(self.obus, int(self.vx), int(self.vy))
            c = tuple(self.boss.coords(self.obus))
            x0, y0 = c[0] + 3*self.lBuse//50, c[1] + 3*self.lBuse//50 #Coordonnées du centre de l'obus
            self.test_obstacle(x0, y0)
            self.vy += .4
#            print(x0,y0)
            self.boss.after(20, self.animer_obus)
        else :   
            # animation terminée - cacher l'obus et déplacer les canons
            self.fin_animation()
    
    def test_obstacle(self, x0, y0) :
        "Evaluer si l'obus a atteint une cible ou les limites du terrain"
        if x0 < -self.lBuse//10 or x0 > self.xMax + self.lBuse//10 or y0 > self.yMax + self.lBuse//10 :
            self.anim = FALSE
            return
        # Analyser le dictionnaire des canons pour voir si les coords
        # de l'un d'entre eux sont proches de celles de l'obus
        for cle in self.guns :      # cle : clé dans le dictionnaire
            gun = self.guns[cle]    # valeur correspondante
            if x0  < gun.x1 + self.rc and x0 > gun.x1 - self.rc \
                    and y0  < gun.y1 + self.rc and y0 > gun.y1 - self.rc :
                self.anim = FALSE
                #Dessiner l'explosion de l'obus
                self.explo = self.boss.create_oval(x0-12, y0-12, x0+12,
                    y0+12, fill='yellow', width=0)
                self.hit = cle
                self.boss.after(150, self.fin_explosion)
                break
            
    def fin_explosion(self) :
        "Effacer l'explosion, réinitialiser l'obus, gérer le score"
        self.boss.delete(self.explo)
        self.explo = FALSE
        #Signaler le succès à la fenetre maitresse
        self.appli.goal(self.id, self.hit)
#        print(self.id, self.hit)
        #Déplacer les canons
        self.appli.disperser()    
        
    def fin_animation(self) :
        "Actions à accomplir lorsque l'obus à terminer sa trajectoire"
        # Cacher le canon
        self.boss.coords(self.obus, -10, -10, -10, -10)
