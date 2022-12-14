from tkinter import *

# taille du disque a la base a partir duquel on delimitera la taille des autres disques de plus en plus petit
largeur_cnv = 900
hauteur_cnv = 300

longueur_base = largeur_cnv / 4  # longueur de la base
base = largeur_cnv / 4.2  # longueur des disques
ecart = 20
taille = 40  # hauteur des disques
separation = 2  # separation entre les disques sur une meme tige
base_gauche = largeur_cnv / 25  # longueur de la base a droite de chaques tiges
# longueur du socle a gauche de chaques tiges
base_droite = 9 * largeur_cnv / 9.5
epaisseur = 24  # epaissi la base et les tiges
haut = 4 * hauteur_cnv / 5  # hauteur des tiges
# defini la position du jeu, peu le deplacer a droite
origine = (0, hauteur_cnv)

n = 5  # nombres de disques
longueur_disque = base
disque_base = longueur_base - longueur_disque / 2  # taille du plus gros disque
# taille des autres disques déterminé en divisant par deux le gros disque pour en créer de plus petits
autres_disques = taille / 2 + separation

ids = []

# permet de bouger les disques de la tige "debut" vers la tige "arrivee" en passant par la tige intermédiaire "transition"


def hanoi(L, debut, arrivee, transition, nb_element_tige, done):
    if L:  # si la tige est vide, la fonction ne fait rien
        # déplacement des k−1 plus hauts éléments de la pile, L etant le nombre d'elements dans la pile
        A = hanoi(L[1:], debut, transition, arrivee, nb_element_tige, False)
        B = [(L[0], (debut, nb_element_tige[debut] - 1),
              (arrivee, nb_element_tige[arrivee]))]
        # nb_element_tige désigne la liste des hauteurs des tiges 0, 1 et 2
        # le nombre d'element contenu dans les tiges ont changé alors la liste nb_element_tige est mise à jour
        nb_element_tige[debut] -= 1
        nb_element_tige[arrivee] += 1
        C = hanoi(L[1:], transition, arrivee, debut, nb_element_tige, False)
        if done:
            # la fonction hanoi dessine un déplacement en faisant appel à la fonction deplacer_disques où i est l’indice du déplacement dans la liste moves
            moves = list(enumerate(A + B + C))
            for (i, (nro, orig, dstn)) in moves:
                # Le déplacement a lieu toute les secondes
                # la méthode after est appelée après 1000 * (i + 1) millisecondes
                cnv.after(1000 * (i + 1), deplacer_disques, nro, orig, dstn)
        return A + B + C  # la fonction hanoi renvoie la liste des déplacements
    return []


# les id des disques sont stockées dans une liste ids
# On pourra déplacer le disque souhaité
# orig et destination sont des couples (tige, etage)
def deplacer_disques(indice, orig, destination):
    i, hi = orig
    j, hj = destination
    # avec les indices des tiges espacées les unes des autres on determine le vecteur horizontal de déplacement
    dx = (j - i) * longueur_base
    # les disques ayant tous la même épaisseur, c’est analogue pour le vecteur de déplacement vertical.
    # Attention toutefois que l’axe des ordonnées du canevas étant orienté vers le bas et que les disques sont numérotés de manière
    #  croissante en se dirigeant vers le haut, il faut changer le signe de l’écart.
    dy = -(hj - hi) * taille
    cnv.move(ids[indice], dx, dy)


# fonction qui renvoi l'origine du nouveau repère
def chgt(X, Y, center):
    return (X + center[0], -Y + center[1])


# fonction qui cree les disques
# les autres disques sont obtenus par décalage avec le disque le plus bas
def draw_disk(nb_disque, disque_base, autres_disques, longueur_disque):
    for _ in range(nb_disque):
        A = chgt(disque_base, autres_disques, origine)
        B = chgt(disque_base + longueur_disque,
                 autres_disques + taille, origine)
        # conception de chaque disques avec la méthode create_rectangle
        rect = cnv.create_rectangle(A, B, fill="turquoise", outline="")
        ids.append(rect)
        disque_base += ecart
        autres_disques += taille + separation
        longueur_disque -= 2 * ecart


def button_start_clicked():  # lancement du jeu
    nb = int(nb_disk.get())
    print("C'est parti", nb)
    draw_disk(int(nb), disque_base, autres_disques, longueur_disque)
    hanoi(list(range(nb)), 0, 2, 1, [nb, 0, 0], True)  # tiges 0,1,2


##########################################################################
# Programme principal
##########################################################################


# Conception des disques

fenetre = Tk()

# creation d'une fenetre principale
fenetre.title("Tour de Hanoï")
fenetre.geometry("1024x400")
'''bg = PhotoImage("/LogoSophieBarat.jpg")

mon_label = Label(fenetre, image=bg)
mon_label.place(x=0, y=0)
'''

fenetre['bg'] = 'turquoise'

cnv = Canvas(fenetre, width=largeur_cnv, height=hauteur_cnv,
             bg="ivory")
cnv.pack(side=TOP, padx=5, pady=5)
# ajout des boutons start et stop
Button(fenetre, text='Start', command=button_start_clicked).pack(
    side=LEFT, padx=125, pady=5)
Button(fenetre, text='Stop').pack(side=RIGHT, padx=125, pady=5)
var = StringVar(fenetre)
var.set(str(n))
nb_disk = Spinbox(fenetre, from_=1, to=12, textvariable=var)
nb_disk.pack()


# fonction qui cree les disques
# les autres disques sont obtenus par décalage avec le disque le plus bas
"""
for _ in range(n):
    A = chgt(disque_base, autres_disques, origine)
    B = chgt(disque_base + longueur_disque, autres_disques + taille, origine)
    # conception de chaque disques avec la méthode create_rectangle
    rect = cnv.create_rectangle(A, B, fill="turquoise", outline="")
    ids.append(rect)
    disque_base += ecart
    autres_disques += taille + separation
    longueur_disque -= 2 * ecart


img = PhotoImage(file="E:\\download\\TourHanoi_NSI\\LogoSophieBarat.jpg")
cnv.create_image(140, 20, anchor=NW, image=img)
cnv.place(x=0, y=0)
"""
# cnv.pack()

# Conception et emplacement de la base
G = chgt(base_gauche, 0, origine)  # distance inter-tige a gauche
D = chgt(base_droite, epaisseur, origine)  # distance inter-tige droite
cnv.create_rectangle(G, D, fill="black")

# Conception et emplacement de 3 tiges
for i in range(3):
    x = (i + 1) * longueur_base - epaisseur / 2
    emplacement_tige = chgt(x, 0, origine)  # emplacement des tiges
    # epaisseur et hauteur des tiges
    taille_tige = chgt(x + epaisseur, haut, origine)
    cnv.create_rectangle(emplacement_tige, taille_tige, fill="black")


"""
def start_game():
    # Reset le compteur
    counter['text'] = 'Moves: 0'

    # commence l'animation du jeu en deplacant le disque le plus petit
    deplacer_disques(1, 0, 1)


def reset_game():
    # reset l'animation en deplcant tout les disques sur la tige 0
    deplacer_disques(n, 2, 0)

    # Reset the counter
    counter['text'] = 'Moves: 0'


# Creer des boutons Start pour commencer l'animation et Reset pour reinitialiser l'animation
start_button = Tk.Button(fenetre, text='Start', command=start_game)
start_button.place(x=150, y=100)
start_button.pack()
print(dir(Button()))

reset_button = Tk.Button(fenetre, text='Reset', command=reset_game)
reset_button.pack()

# Creer un compteur qui compte le nombres de fois ou les disques sont déplacé
counter = Tk.Label(fenetre, text='Moves: 0')
counter.pack()
"""

# hanoi(list(range(n)), 0, 2, 1, [n, 0, 0], True)  # tiges 0,1,2

fenetre.mainloop()
