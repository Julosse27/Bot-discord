# title: Kenji Battle
# author: Lateurte Jules et Fauchereau Evan
# desc: Un petit jeu d'enfants de 15 ans qui commencent tout juste à programmer
# version: 2

import pyxel as px
from collections import defaultdict
import sqlite3
import os
import sys

Ressources = r"Ressources\Kenji_battle_ressources.pyxres"
Données = os.path.join(os.path.dirname(__file__), r"Ressources\Données.sq3")

lettres = (
           ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"),
           ("a", "b", "c", "d", "e", "f", "h", "i", "k", "l", "m", "n", "o", "r", "s", "t", "u", "v", "w", "x", "z"),
           ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", " "),
           ("é", "è", "à", "ê", "ù", "-", "'", ".", "!", "?", ":", "_", "(", ")", "%", "="),
           ("g", "j", "p", "q", "y", ",", "ç", ";"),
           ("/")
           )

touches = ( (px.KEY_A, "a"), (px.KEY_Z, "z"), (px.KEY_E, "e"), (px.KEY_R, "r"), (px.KEY_T, "t"), (px.KEY_Y, "y"),
            (px.KEY_U, "u"), (px.KEY_I, "i"), (px.KEY_O, "o"), (px.KEY_P, "p"), (px.KEY_Q, "q"), (px.KEY_S, "s"),
            (px.KEY_D, "d"), (px.KEY_F, "f"), (px.KEY_G, "g"), (px.KEY_H, "h"), (px.KEY_J, "j"), (px.KEY_K, "k"),
            (px.KEY_L, "l"), (px.KEY_M, "m"), (px.KEY_W, "w"), (px.KEY_X, "x"), (px.KEY_C, "c"), (px.KEY_V, "v"),
            (px.KEY_B, "b"), (px.KEY_N, "n"), (px.KEY_SPACE, " "), (px.KEY_RIGHTBRACKET, ")"), (px.KEY_COLON, ":"), 
            (px.KEY_1, "1"), (px.KEY_3, "3"))

touches_spé =  ((px.KEY_2, "2", "é"), (px.KEY_4, "4", "'"), (px.KEY_5, "5", "("), (px.KEY_6, "6", "-"),
                (px.KEY_7, "7", "è"), (px.KEY_8, "8", "_"), (px.KEY_9, "9", "ç"), (px.KEY_0, "0", "à"),
                (px.KEY_COMMA, "?", ","), (px.KEY_SEMICOLON, ".", ";")
                )

touches_keypad = ((px.KEY_KP_0, "0"), (px.KEY_KP_1, "1"), (px.KEY_KP_2, "2"), (px.KEY_KP_3, "3"), (px.KEY_KP_4, "4"), (px.KEY_KP_5, "5"), (px.KEY_KP_6, "6"),
                (px.KEY_KP_7, "7"), (px.KEY_KP_8, "8"), (px.KEY_KP_9, "9"))

def ajouter_texte(x, y, taille, txt, couleur, gr_elements: str, type_retour = "Normal"):
    global elements
    elements[gr_elements]["texte"].append(Draw_texte(x, y, taille, txt, couleur, type_retour, len(elements[gr_elements]["texte"])))

def ajouter_bouton(x: int, y: int, width: int, height: int, gr_elements: str, fonction, *paramètres_fonction, modèle = False, coolkey = 15, taille = 1, x_img: int = None, y_img: int = None, x_img_a: int = None, y_img_a: int = None, couleur1 = None, couleur2 = None, bordure: int = 1):
    global elements
    if not (type(fonction) != type(ajouter_bouton) or type(fonction) != type(def_pseudo.chek_touches)):
        raise Exception("L'action demandée n'est pas executable.")
    if modèle:
        if not (x_img or y_img or x_img_a or y_img_a):
            raise ValueError("Les coordonées de l'images doivent être préscisées.")
    else:
        if not (couleur1 or couleur2):
            raise ValueError("Les couleurs doivent être préscisées.")
    elements[gr_elements]["boutons"].append(Bouton(x, y, width, height, fonction, paramètres_fonction, taille, x_img, y_img, x_img_a, y_img_a, coolkey, modèle, (couleur1, couleur2), bordure))

def update_elements(gr_elements, *type_elements):
    if not len(type_elements) == 0:
        for type_element in type_elements:
            for element in elements[gr_elements][type_element]:
                element.update()

def draw_elements(gr_elements, *type_elements):
    if not len(type_elements) == 0:
        for type_element in type_elements:
            for element in elements[gr_elements][type_element]:
                element.draw()

class Perso:
    def __init__(self, x, vies):
        self.x = x
        self.vies = vies
        self.img_b = ((0, 0), (16, 0))
        self.img_m = ((32, 0), (48, 0))
        self.img_att = (64, 0)
        self.imgs_ch = ((96, 0), (96, 16), (128, 0), (208, 48))
        self.img_ult = ((224, 0), (224, 48), (192, 32))
        self.img_mort = (96, 48)

    def update(self):
        if px.btn(px.KEY_LEFT):
            self.mouvement = - base_stats["Vitesse"]
        if px.btn(px.KEY_RIGHT):
            self.mouvement = base_stats["Vitesse"]

class Bouton:
    def __init__(self, x: int, y: int, taille_w: int, taille_h: int, fonction: type[ajouter_bouton], paramètres: tuple, taille: int, x_img, y_img, x_img_a, y_img_a, couleur_transparence, modèle, couleur, bordure):
        self.x = x
        self.y = y
        self.width = taille_w
        self.height = taille_h
        self.fonction = fonction
        self.paramètres = paramètres
        self.modèle = modèle
        self.exclu = False
        self.taille = taille
        if modèle:
            self.x_img = x_img
            self.y_img = y_img
            self.x_img_a = x_img_a
            self.y_img_a = y_img_a
        else:
            global couleurs
            for i in range(len(couleur)):
                if couleur[i] > len(couleurs):
                    if couleur[i] not in couleurs:
                        couleurs.append(couleur[i])
                    couleur[i] = couleurs.index(couleur[i])
            self.couleur1 = couleur[0]
            self.couleur2 = couleur[1]
            self.bordure = bordure
        
        if couleur_transparence > len(couleurs):
            couleur_transparence = couleurs.index(couleur_transparence)
        self.coolkey = couleur_transparence
        self.animation = False

    def exclusion(self, valeur):
        self.exclu = valeur

    def change_y(self, nouveau_y):
        self.y = nouveau_y

    def update(self):
        self.animation = False
        mx = px.mouse_x
        my = px.mouse_y
        
        x1 = self.x - ((self.width / 2) * (self.taille - 1))
        x2 = self.x + self.width + ((self.width / 2) * (self.taille - 1))
        y1 = self.y - ((self.height / 2) * (self.taille - 1))
        y2 = self.y + self.height + ((self.height / 2) * (self.taille - 1))
        if not self.exclu:
            if (mx >= x1 and mx <= x2) and (my >= y1 and my <= y2):
                self.animation = True
                if px.btnp(px.MOUSE_BUTTON_LEFT):
                    if len(self.paramètres) == 0:
                        self.fonction()
                    else:
                        self.fonction(*self.paramètres)
    
    def draw(self):
        if not self.exclu:
            if self.modèle:
                if self.animation and px.frame_count % 40 < 20:
                    px.blt(self.x, self.y, 0, self.x_img_a, self.y_img_a, self.width, self.height, self.coolkey, scale= self.taille)
                else:
                    px.blt(self.x, self.y, 0, self.x_img, self.y_img, self.width, self.height, self.coolkey, scale= self.taille)
            else:
                px.rect(self.x, self.y, self.width, self.height, self.couleur2)
                if self.animation and px.frame_count % 40 < 20:
                    px.rect(self.x + (self.bordure * 2), self.y + (self.bordure * 2), self.width - (3 * self.bordure), self.height - (3 * self.bordure), self.couleur1)
                else:
                    px.rect(self.x + self.bordure, self.y + self.bordure, self.width - (2* self.bordure), self.height - (2* self.bordure), self.couleur1)
            
class Draw_texte:
    class Retour:
        def __init__(self, x, y, taille, texte, couleur, y_img, decallage):
            self.x = x
            self.y = y
            self.taille = taille
            self.couleur = couleur
            self.y_img = y_img
            self.decallage = decallage
            self.positions = []
            for caractère in texte:
                for u in range(len(lettres)):
                    for i in range(len(lettres[u])):
                        if caractère == lettres[u][i]:
                            if u != 5:
                                self.positions.append((i, u))

            self.taille_x = 8 * len(self.positions)

        def draw(self):
            for o in range(len(self.positions)):
                px.tilemaps[7].pset(o + self.decallage, 0 + self.y_img, self.positions[o])
                if self.positions[o][1] == 4:
                    px.tilemaps[7].pset(o + self.decallage, 1 + self.y_img, (self.positions[o][0], self.positions[o][1] + 1))
                else:
                    px.tilemaps[7].pset(o + self.decallage, 1 + self.y_img, (10, 2))
            
            px.bltm(self.x, self.y, 7, 8 * self.decallage, 8 * self.y_img, self.taille_x, 16, 0, scale = self.taille)

    def __init__(self, x, y, taille, texte, couleur, type_retour, index):
        self.x = x
        self.y = y
        self.x_base = x
        self.taille = taille
        self.change_couleur(couleur)
        self.type_retour = type_retour
        self.index = index
        self.change_texte(texte)

    def change_couleur(self, couleur):
        global couleurs
        if couleur > len(couleurs):
            if couleur not in couleurs:
                couleurs.append(couleur)
                px.colors.from_list(couleurs)
            self.couleur = couleurs.index(couleur)
        else:
            self.couleur = couleur
        
    def change_texte(self, nouveau_txt):
        self.x = self.x_base
        nouveau_txt = list(nouveau_txt)
        txt = []
        self.txts_retours = []
        if "/" in nouveau_txt:
            for i in range(len(nouveau_txt)):
                if "/" == nouveau_txt[i]:
                    txt.append(i)
            txt.append(len(nouveau_txt))

        if self.type_retour == "Millieu":
            if len(txt) > 0:
                self.x -= ((txt[0] * 8) / 2)
            else:
                self.x -= ((len(nouveau_txt) * 8) / 2)

        if not len(txt) == 0:
            for u in range(len(txt)):
                if u == 0:
                    txt_base = nouveau_txt[:txt[u]]
                else:
                    if self.type_retour == "Normal":
                        x_retour = self.x_base
                    elif self.type_retour == "Millieu":
                        x_retour = self.x + ((txt[0] * 8) / 2) - (((txt[u] - txt[u - 1]) * 8) / 2)
                    elif self.type_retour == "Inversé":
                        x_retour = self.x_base - (txt[u] * 8)

                    self.txts_retours.append(self.Retour(x_retour, self.y + (16 * u), self.taille, nouveau_txt[txt[u - 1] + 1:txt[u]], self.couleur, 2 * self.index, txt[u - 1]))

            nouveau_txt = txt_base
        
        if self.type_retour == "Inversé":
            self.x = self.x_base - (len(nouveau_txt) * 8)

        positions = []
        for caractère in nouveau_txt:
            for u in range(len(lettres)):
                for i in range(len(lettres[u])):
                    if caractère == lettres[u][i]:
                        if u != 5:
                            positions.append((i, u))
        
        self.taille_x = 8 * len(positions)
        self.positions = positions
        
    def draw(self):
        for o in range(len(self.positions)):
            px.tilemaps[7].pset(o, 0 + (2 * self.index), self.positions[o])
            if self.positions[o][1] == 4:
                px.tilemaps[7].pset(o, 1 + (2 * self.index), (self.positions[o][0], self.positions[o][1] + 1))
            else:
                px.tilemaps[7].pset(o, 1 + (2 * self.index), (10, 2))

        px.pal(7, self.couleur)

        for retour in self.txts_retours:
            retour.draw()
        
        px.bltm(self.x, self.y, 7, 0, 16 * self.index, self.taille_x, 16, 0, scale = self.taille)

        px.pal()

class Def_pseudo:
    def __init__(self, changement_p = False):
        global elements

        elements = defaultdict(lambda: {"boutons": [], "texte": []})
        self.pseudo = ""
        self.ch_p = changement_p
        self.majuscule = True
        self.gr_element = "def_pseudo"

        self.couleur_txt = 0xEEEEEE
        self.x_txt = 197
        self.y_txt = 139

        if not new:
            self.pseudo = Base_données.recup_last_pseudo()
            self.choisi = True
        else:
            self.choisi = False

        if changement_p:
            self.choisi = False
            self.pseudo = ""

        ajouter_texte(256, 100, 1, "Choisit ton/pseudo !", 0xEEEEEE, self.gr_element, "Millieu")
        ajouter_texte(self.x_txt, self.y_txt, 1, self.pseudo, self.couleur_txt, self.gr_element)

        self.limite_taille_pseudo = 15
        
        self.couleur_txt = couleurs.index(self.couleur_txt)

    def chek_touches(self):
        écrit = False
        if len(self.pseudo) < self.limite_taille_pseudo:
            for code, lettre in touches:
                if not écrit:
                    if px.btnp(code, hold= 30, repeat= 3):
                        if self.majuscule:
                            lettre = lettre.upper()
                        self.pseudo += lettre
                    if px.btn(code):
                        écrit = True

            for code, majuscule, minuscule in touches_spé:
                if not écrit:
                    if px.btnp(code, hold= 30, repeat= 3):
                        if self.majuscule:
                            self.pseudo += majuscule
                        else:
                            self.pseudo += minuscule
                    if px.btn(code):
                        écrit = True

            for code, lettre in touches_keypad:
                if not écrit:
                    if px.btnp(code, hold= 30, repeat= 3):
                        self.pseudo += lettre
                    if px.btn(code):
                        écrit = True

        if px.btnp(px.KEY_RSHIFT) or px.btnp(px.KEY_LSHIFT):
            if self.majuscule:
                self.majuscule = False
            else:
                self.majuscule = True

        if not écrit:
            if px.btnp(px.KEY_BACKSPACE, hold = 30, repeat= 3):
                self.pseudo = self.pseudo[:-1]
                écrit = True

        if not écrit:
            if px.btnp(px.KEY_RETURN) or px.btnp(px.KEY_RETURN2) or px.btnp(px.KEY_KP_ENTER):
                self.choisi = True
                init(self.pseudo)
        else:
            elements[self.gr_element]["texte"][1].change_texte(self.pseudo.replace(" ", "$"))        

    def draw(self):
        yL1 = -32
        yL2 = -16
        while yL1 <= px.height:
            yL1 += 32
            yL2 += 32
            px.rect(0, yL1, px.width, 16, 9)
            px.rect(0, yL2, px.width, 16, 10)

        px.blt(px.width / 2 - 32, px.height / 2 - 16, 0, 64, 128, 64, 32, scale= 2)

        draw_elements(self.gr_element, "texte")
        if px.frame_count % 30 < 15:
            px.line(self.x_txt + (8 * len(self.pseudo)), self.y_txt, self.x_txt + (8 * len(self.pseudo)), self.y_txt + 8, self.couleur_txt)

class Lancement_jeu:
    def lancement(self):
        global etat_jeu
        etat_jeu = "Prepa"
        self.timer = 0

    def update(self):
        self.timer += 1

        if self.timer == 300:
            global etat_jeu
            etat_jeu = "Jeu"
    
    def draw(self):
        for i in range(self.timer // 10):
            px.rect(0, 16 * i, px.width, 16, 16)
            if i == (px.height // 16) + 10:
                px.blt(px.width / 2 - 32, px.height / 2 - 16, 0, 128, 96, 64, 32, 15, scale= 8)

class Base_données:
    def ouverture(self):
        conn = sqlite3.connect(Données)
        cur = conn.cursor()
        return conn, cur

    def fermeture(self, conn: sqlite3.Connection, cur: sqlite3.Cursor):
        cur.close()
        conn.close()

    def réinitialisation():
        conn = sqlite3.connect(Données)
        cur = conn.cursor()
        ll = cur.execute("select name from sqlite_master").fetchall()
        l = []
        for i in ll:
            l.append(i[0])

        for name in l:
            if not (name == "Pseudos" or name == "Hscores"):
                cur.execute(f"drop table {name}")

        cur.execute("delete from Pseudos")
        cur.execute("delete from Hscores")
        conn.commit()

        cur.close()
        conn.close()
        
    def création():
        conn = sqlite3.connect(Données)
        cur = conn.cursor()
        cur.execute("create table Pseudos(pseudo text, last bolean default False)")
        cur.execute("create table Hscores(score integer, joueur text)")
        cur.close()
        conn.close()

    def recup_pseudos(self):
        conn, cur = self.ouverture()
        r = cur.execute("select pseudo from Pseudos").fetchall()
        result = []
        for i in range(len(r)):
            result.append(r[i][0])
        self.fermeture(conn, cur)
        return result
    
    def recup_score(self):
        conn, cur = self.ouverture()
        r = cur.execute("select * from Hscores").fetchall()
        self.fermeture(conn, cur)
        return r
    
    def ajouter_score(self, Pseudo: str, Score: int):
        global suchis
        conn, cur = self.ouverture()
        cur.execute(f"insert into Hscores(score, joueur) values({Score}, '{Pseudo}')")
        cur.execute(f"update {pseudo}_generale set suchis = {suchis + (Score // 10 * difficultées[paramètres["Difficultée"]]["rendement"])}")
        conn.commit()
        suchis = self.recup_suchis()
        self.fermeture(conn, cur)

    def chek_new():
        conn = sqlite3.connect(Données)
        cur = conn.cursor()
        if len(cur.execute("select * from Pseudos").fetchall()) == 0:
            i = True
        else:
            i = False
        cur.close()
        conn.close()
        return i
    
    def recup_sqlite_master(self):
        conn, cur = self.ouverture()
        r = cur.execute("select name from sqlite_master").fetchall()
        result = []
        for i in range(len(r)):
            result.append(r[i][0])
        self.fermeture(conn, cur)
        return result
    
    def recup_last_pseudo():
        conn = sqlite3.connect(Données)
        cur = conn.cursor()
        i = cur.execute("select pseudo from Pseudos where last = True").fetchone()[0]
        cur.close()
        conn.close()
        return i
    
    def recup_objets(self):
        conn, cur = self.ouverture()
        r = cur.execute(f"select acheté from {pseudo}_amélioration").fetchall()
        result = []
        for i in range(len(r)):
            result.append(r[i][0])
        self.fermeture(conn, cur)
        return result
    
    def acheter_objet(self, nom: str = None):
        conn, cur = self.ouverture()

        for i in range(len(objets)):
            if objets[i]["nom"] == nom:
                break
        else:
            raise ValueError("Cet amélioration n'éxiste pas.")

        i += 1

        if cur.execute(f"select acheté from {pseudo}_amélioration where rowid = {i}").fetchone()[0]:
            raise Exception("Cet amélioration à déjà été acheté.")
        else:
            cur.execute(f"update {pseudo}_amélioration set acheté = True where rowid = {i}")
            conn.commit()

        r = cur.execute(f"select acheté from {pseudo}_amélioration").fetchall()
        achetés = []
        for i in range(len(r)):
            achetés.append(r[i][0])

        global objets_achetables
        
        objets_achetables = []
        for i in range(len(objets)):
            if not achetés[i]:
                if objets[i]["requirement"] == None or achetés[objets[i]["requirement"]] == True:
                    objets_achetables.append(objets[i].copy())
            
        self.fermeture(conn, cur)
    
    def recup_param(self, paramètre):
        conn, cur = self.ouverture()
        result = cur.execute(f"select {paramètre} from {pseudo}_generale").fetchone()[0]
        self.fermeture(conn, cur)
        return result
    
    def recup_suchis(self):
        conn, cur = self.ouverture()
        result = cur.execute(f"select suchis from {pseudo}_generale").fetchone()[0]
        self.fermeture(conn, cur)
        return result
    
    def changer_paramètre(self, paramètre, valeur):
        conn, cur = self.ouverture()
        global paramètres
        paramètres[paramètre] = valeur
        cur.execute(f"update {pseudo}_generale set {paramètre} = '{valeur}'")
        if paramètre == "Difficultée":
            elements["Params"]["texte"][1].change_texte(difficultées[valeur]["txt"])
            elements["Params"]["texte"][1].change_couleur(difficultées[valeur]["couleur"])
            elements["Params"]["texte"][2].change_texte(valeur)
            elements["Params"]["texte"][2].change_couleur(difficultées[valeur]["couleur"])
        conn.commit()
        self.fermeture(conn, cur)

    def __init__(self, Pseudo: str):
        global pseudo
        conn, cur = self.ouverture()

        pseudo = Pseudo.replace("$", " ")
        
        if Pseudo not in self.recup_pseudos():
            cur.execute(f"create table {Pseudo}_generale(suchis integer, Difficultée text)")
            cur.execute(f"create table {Pseudo}_amélioration(acheté boolean)")
            
            list_objets = []
            for i in range(len(objets)):
                list_objets.append("(False)")
            
            objet = ", ".join(list_objets)
            
            if Pseudo == 'Cheat_test':
                cur.execute("insert into Cheat_test_generale(suchis, Difficultée) values(5000, 'Moyen')")
            else:
                cur.execute(f"insert into {Pseudo}_generale(suchis, Difficultée) values(0, 'Moyen')")
            cur.execute(f'insert into {Pseudo}_amélioration(acheté) values{objet}')

            cur.execute(f"insert into Pseudos(pseudo) values('{Pseudo}')")

            conn.commit()
        
        cur.execute("update Pseudos set last = False")
        cur.execute(f"update Pseudos set last = True where pseudo = '{Pseudo}'")

        conn.commit()

        self.fermeture(conn, cur)

        elements["Menu"]["texte"][0].change_texte(pseudo)

        ouvrir_menu("Menu")
            
def ouvrir_menu(menu):
    global menu_ouvert
    menu_ouvert = menu
    if menu == "Score":
        scores = données.recup_score()
        scores.sort(key= lambda a: a[0], reverse= True)

        for i in range(len(scores)):
            elements["Score"]["texte"][i].change_texte(f"{i + 1}.{scores[i][1]}{"_" * (23 - (len(scores[i][1]) + len(str(scores[i][0]))))}{scores[i][0]}")
    

def change_pseudo():
    global def_pseudo
    def_pseudo = Def_pseudo(True)

def change_upg(nom_upg: str):
    pass

def init(Pseudo: str):
    global données, objets_achetables, suchis, paramètres, etat_jeu

    ajouter_texte(px.width - 5, 5, 1, "", 7, "Menu", type_retour= "Inversé")
    données = Base_données(Pseudo)

    etat_jeu = "Menu"

    achetés = données.recup_objets()
    objets_achetables = []
    for i in range(len(objets)):
        if not achetés[i]:
            if objets[i]["requirement"] == None or achetés[objets[i]["requirement"]] == True:
                objets_achetables.append(objets[i].copy())

    
    suchis = données.recup_suchis()

    paramètres = {"Difficultée": données.recup_param("Difficultée")}

    ### Boutons du Menu principal ###
    ajouter_bouton(100, 50, 64, 32, "Menu", lancement_jeu.lancement, taille= 4, x_img= 0, y_img= 32, x_img_a= 0, y_img_a= 128, modèle= True)
    ajouter_bouton(100, 192, 32, 32, "Menu", ouvrir_menu, "Infos", taille= 2, x_img= 32, y_img= 64, x_img_a= 32, y_img_a= 96, modèle= True)
    ajouter_bouton(200, 192, 32, 32, "Menu", ouvrir_menu, "Params", taille= 2, x_img= 0, x_img_a= 0, y_img= 64, y_img_a= 96, modèle= True)
    ajouter_bouton(300, 200, 16, 16, "Menu", ouvrir_menu, "Shop", taille= 4, coolkey= 16, x_img= 128, x_img_a= 128, y_img= 128, y_img_a= 144, modèle= True)
    ajouter_bouton(400, 200, 16, 16, "Menu", ouvrir_menu, "Score", taille= 4, x_img= 208, x_img_a= 208, y_img= 0, y_img_a= 16, modèle= True)

    ### Croix du menu infos ###
    ajouter_bouton(px.width - 31, 7, 16, 16, "Infos", ouvrir_menu, "Menu", modèle= True, x_img= 80, y_img= 32, x_img_a= 80, y_img_a= 48)

    ### Boutons du menu de la boutique ###
    ajouter_bouton(px.width - 31, 7, 16, 16, "Shop", ouvrir_menu, "Menu", modèle= True, x_img= 80, y_img= 32, x_img_a= 80, y_img_a= 48)
    x_base = 160
    x = x_base
    y = 50
    espacement = 60
    for i in range(len(objets_achetables)):
        if i % 6 == 0:
            y += espacement
            x = x_base
        ajouter_bouton(x, y, 16, 16, "Shop", change_upg, objets_achetables[i]["nom"], taille= 3, modèle= True, x_img= refs_butons_upgs[objets_achetables[i]["nom_modèle"]]["x_img"], y_img= refs_butons_upgs[objets_achetables[i]["nom_modèle"]]["y_img"], x_img_a= refs_butons_upgs[objets_achetables[i]["nom_modèle"]]["x_img_a"], y_img_a= refs_butons_upgs[objets_achetables[i]["nom_modèle"]]["y_img_a"])
        x += espacement
    ### Textes menu de la boutique ###
    ajouter_texte(px.width / 2 + 40, 13, 2, f"{données.recup_suchis()}", 3, "Shop", "Millieu")

    ### Croix du menu des scores ###
    ajouter_bouton(px.width - 31, 7, 16, 16, "Score", ouvrir_menu, "Menu", modèle= True, x_img= 80, y_img= 32, x_img_a= 80, y_img_a= 48)
    ### Textes menu des scores ###
    for i in range(2):
        for u in range(20):
            ajouter_texte(120 + (250 * i), 55 + (10 * u), 1, f"{(20 * i) + (u + 1)}.Score_encore_non_défini", 0, "Score", type_retour= "Millieu")

    ### Boutons du menu paramètres ###
    ajouter_bouton(px.width - 31, 7, 16, 16, "Params", ouvrir_menu, "Menu", modèle= True, x_img= 80, y_img= 32, x_img_a= 80, y_img_a= 48)
    ajouter_bouton(95, 55, 25, 13, "Params", données.changer_paramètre, "Difficultée", "Facile", couleur1= 9, couleur2= 10, bordure= 2)
    ajouter_bouton(125, 55, 25, 13, "Params", données.changer_paramètre, "Difficultée", "Moyen", couleur1= 9, couleur2= 10, bordure= 2)
    ajouter_bouton(155, 55, 25, 13, "Params", données.changer_paramètre, "Difficultée", "Diffiçile", couleur1= 9, couleur2= 10, bordure= 2)
    ajouter_bouton(250, 70, 25, 13, "Params", change_pseudo, couleur1= 9, couleur2= 10, bordure= 2)
    ### Textes du menu paramètres ###
    ajouter_texte(50, 42, 1, "1.Changer la difficultée", 7, "Params")
    ajouter_texte(140, 70, 1, difficultées[paramètres["Difficultée"]]["txt"], difficultées[paramètres["Difficultée"]]["couleur"], "Params", type_retour= "Millieu")
    ajouter_texte(140, 203, 2, paramètres["Difficultée"], difficultées[paramètres["Difficultée"]]["couleur"], "Params", type_retour= "Millieu")

def update():
    if not def_pseudo.choisi:
        def_pseudo.chek_touches()
    else:
        if etat_jeu == "Menu":
            if menu_ouvert == "Shop":
                for boutons in elements["Shop"]["boutons"][1:]:
                    boutons.change_y(boutons.y + px.mouse_wheel)
                    if boutons.y <= 75:
                        boutons.exclusion(True)
                    else:
                        boutons.exclusion(False)

            update_elements(menu_ouvert, "boutons")
            
            for bouton in elements["Params"]["boutons"]:
                if bouton.fonction == données.changer_paramètre:
                    if bouton.paramètres[0] == "Difficultée":
                        if bouton.paramètres[1] == paramètres["Difficultée"]:
                            bouton.couleur2 = 0
                        else:
                            bouton.couleur2 = 10
        elif etat_jeu == "Prepa":
            lancement_jeu.update()
        elif etat_jeu == "Jeu":
            px.quit()
        
        if px.btnp(px.KEY_A):
            px.quit()

def draw():
    if not def_pseudo.choisi:
        def_pseudo.draw()
    else:
        if etat_jeu == "Jeu":
            px.cls(12)
        else:
            yL1 = -32
            yL2 = -16
            while yL1 <= px.height:
                yL1 += 32
                yL2 += 32
                px.rect(0, yL1, px.width, 16, 9)
                px.rect(0, yL2, px.width, 16, 10)
            px.mouse(True)
            if menu_ouvert == "Infos":
                px.blt(px.width / 2 - 16, px.height / 2 - 8, 0, 128, 32, 32, 16, scale= 15)
            elif menu_ouvert == "Params":
                px.blt(px.width / 2 - 16, px.height / 2 - 8, 0, 128, 48, 32, 16, scale= 15)
            
            draw_elements(menu_ouvert, "boutons", "texte")

            if menu_ouvert == "Shop":
                px.rect(0, 0, 128, px.height, 2)
                px.rect(10, 10, 108, px.height - 20, 10)
                px.blt(px.width / 2 + 75, 10, 0, 162, 35, 12, 11, 12, scale= 2)

            if etat_jeu == "Prepa":
                lancement_jeu.draw()

px.init(512, 256, title= "Kenji Battle", fps= 60)
px.load(Ressources)

couleurs = px.colors.to_list()
couleurs.append(0xff2626)
px.colors.from_list(couleurs)

new = Base_données.chek_new()

difficultées =      {"Facile": {"txt":"Vraiment/vous n'arrivez pas/à jouer !!!//- 3 ennemis par vagues/- 2 types d'ennemis/- 5 vies/x0.5 de récompense", "couleur": 0x109837, "rendement": 0.5},
                    "Moyen": {"txt":"Vous êtes tout/juste dans la moyenne//- 4 ennemis par vagues/- 3 type d'ennemis/- 4 vies//x1 de récompenses", "couleur": 0xcb6e05, "rendement": 1},
                    "Diffiçile": {"txt":"La dernière difficultée/???//- 5 ennemis par vagues/- 5 types d'ennemis/- 3 vies//x2 de récompense", "couleur": 0xf50000, "rendement": 2}
                    }

base_stats = {"Vitesse": 1, 
              "Revenus score": 1, 
              "Revenus suchis": 1, 
              "Range ult": 3, 
              "Reload ult": 600, 
              "Att ult": 1, 
              "Parade chance": 5, 
              "Delay 1ere change": 60, 
              "Delay 2eme charge": 90, 
              "Delay 3eme charge": 180, 
              "Reload att": 60, 
              "3eme charge": False,
              "Ult": False,
              "Mini slash": False
              }
refs_butons_upgs = {"vitesse": {"x_img": 64, "y_img": 32, "x_img_a": 64, "y_img_a": 48},
                    "revenus score": {"x_img": 176, "y_img": 0, "x_img_a": 176, "y_img_a": 16},
                    "revenus suchis": {"x_img": 160, "y_img": 32, "x_img_a": 160, "y_img_a": 48},
                    "ult": {"x_img": 176, "y_img": 64, "x_img_a": 176, "y_img_a": 80},
                    "parade": {"x_img": 176, "y_img": 32, "x_img_a": 176, "y_img_a": 48},
                    "delay": {"x_img": 160, "y_img": 0, "x_img_a": 160, "y_img_a": 16},
                    "3charge": {"x_img": 192, "y_img": 64, "x_img_a": 192, "y_img_a": 80}
                    }
objets = (  {"nom": "La première vitesse", "stat": "Vitesse", "valeur": 1.1, "description": "", "prix": 100, "nom_modèle": "vitesse", "requirement": None},
            {"nom": "Adepte du/petit score", "stat": "Revenus score", "valeur": 1.1, "description": "", "prix": 200, "nom_modèle": "revenus score", "requirement": None}, 
            {"nom": "Adepte de la/mini pièce", "stat": "Revenus suchis", "valeur": 1.1, "desciption": "", "prix": 300, "nom_modèle": "revenus suchis", "requirement": None}, 
            {"nom": "Taper qui ?/Tout le monde !", "stat": "Range ult", "valeur": 4, "desciption": "", "prix": 700, "nom_modèle": "ult", "requirement": 11},
            {"nom": "L'ult je l'ai en/permanence !", "stat": "Reload ult", "valeur": 900, "desciption": "", "prix": 500, "nom_modèle": "ult", "requirement": 11},
            {"nom": "On tape 2 fois ici", "stat": "Att ult", "valeur": 2, "desciption": "", "prix": 900, "nom_modèle": "ult", "requirement": 11},
            {"nom": "La parade", "stat": "Parade", "valeur": 10, "desciption": "", "prix": 400, "nom_modèle": "parade", "requirement": None},
            {"nom": "Rapide 1", "stat": "Delay 1ere charge", "valeur": 40, "desciption": "", "prix": 600, "nom_modèle": "delay", "requirement": None},
            {"nom": "Rapide 2", "stat": "Delay 2ere charge", "valeur": 80, "desciption": "", "prix": 800, "nom_modèle": "delay", "requirement": None},
            {"nom": "Rapide 3", "stat": "Delay 3ere charge", "valeur": 170, "desciption": "", "prix": 1000, "nom_modèle": "delay", "requirement": 12},
            {"nom": "Attaquer mais en plus rapide", "stat": "reload att", "valeur": 50, "desciption": "", "prix": 500, "nom_modèle": "delay", "requirement": None},
            {"nom": "Un ult ???", "stat": "3eme charge", "valeur": True, "desciption": "", "prix": 1000, "nom_modèle": "ult", "requirement": None},
            {"nom": "La 3eme", "stat": "3eme charge", "valeur": True, "desciption": "", "prix": 1200, "nom_modèle": "3charge", "requirement": None},
            {"nom": "Un petit bonus", "stat": "Mini slash", "valeur": True, "desciption": "", "prix": 1200, "nom_modèle": "3charge", "requirement": 12}
            )

lancement_jeu = Lancement_jeu()

def_pseudo = Def_pseudo()
if def_pseudo.choisi:
    init(def_pseudo.pseudo)

menu_ouvert = "Menu"

px.run(update, draw)