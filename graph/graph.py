import tkinter
from math import *
from functools import partial

ver="1.1.0"

#Déclaration des variables
#Tailles du menu (minimal pour la hauteur)
WMENU = 200
HMENU = 450

#Couleur des champs de saisie en erreur
WRONG="tomato"

#Les différentes polices d'écritures utilisées dans le programme
t3font = ('Times Roman', 18,'bold')
t2font = ('Times Roman', 14,'bold')
t1font = ('Times Roman', 12,'underline')
pbfont = ('Times Roman',11,'bold')
pfont = ('Times Roman',10)
bfont = ('Times Roman',10)
mfont = ('Times Roman',10,'bold')
b2font = ('Times Roman',12,'bold')

curves=[] #Liste de stockage des courbes
LENCURVES=10 #Nombre de variables d'une courbe
ACTIVE=0 #Clé d'accès à une variable
TYPE=1
EQ=2
XEQ=3
YEQ=4
PARMIN=5
PARMAX=6
PARSTEP=7
CCOLOR=8
SIZE=9

#TYPES
PARAM=0
POLAR=1
YFX=2
XFY=3

ntypes=["Arc parametré","Courbe polaire","y=f(x)","x=f(y)"]
types={ntypes[PARAM]:PARAM,ntypes[POLAR]:POLAR,ntypes[YFX]:YFX,ntypes[XFY]:XFY}

#Idem pour le stockage des variables pour le graphique
graph=[]
LENGRAPH=14
XMIN=0
XMAX=1
YMIN=2
YMAX=3
AXIS1=4
AXIS2=5
AXIS3=6
AXIST1=7
AXIST2=8
AXISA=9
GRID1=10
GRID2=11
GRID3=12
GCOLOR=13

#Idem pour le stockage des variables des options
opts=[]
LENOPTS=4
TX=0
TY=1
ZOOM=2
RND=3

scr=0 #Courbe sélectionnée dans le menu
page=1 #Page du menu

zoombe=False

def start():
    '''Lancement du programme'''
    global win #Définition de la fenetre en variable globale
    win=tkinter.Tk() #Création de la fenetre / démarrage de tkinter

    #Création des variables tkinter (courbes, graph, options)
    tkvars([],[-5,5,-5,5,1,1,0,1,1,1,1,1,1,"white"],[500,500,0,3])
    #tkvars([],[-4.5,4.5,-6,3,0,0,0,0,0,0,0,0,0,"white"],[500,500,0,3])

    #Ajout d'une nouvelle courbe suivant certains paramètres
    #newCurve(1,ntypes[POLAR],"cos(t)/(1-sin(t))","","",0,2*pi,0.1,"red",1)
    #newCurve(1,ntypes[PARAM],"","t**5-(10/3)*t**3","(-t**4+(11/5)*t**2)*3/2",-1.825,1.825,0.01,"red",2)
    #newCurve(1,ntypes[POLAR],"sin(2*t)","","",0,"2*pi",0.1,"red",1)

    #Création des éléments de la fenetre
    paintwin()
    

def paintwin():
    global win,cv #le canvas doit être global pour l'accès d'autres fonctions

    #Création de la fenetre
    width=opts[TX].get()+WMENU #Largeur en fonction du canvas + menu
    #Hauteur en fonction du canvas mais minimum du menu
    if(opts[TY].get()<HMENU): 
        height=HMENU
    else:
        height=opts[TY].get()
    
    win.title("Graph (version "+ver+")") #Titre de la fenetre
    win.resizable(width=False,height=False) #Fenetre non redimensionnable
    #Application des tailles de la fenetre
    win.geometry(""+str(width)+"x"+str(height))

    #Création du canvas
    

    #Création des evenements
    win.bind("<Return>",enter) #La touche entrée appelle la fonction enter
    win.bind("<MouseWheel>",zoom)

    #Cration du menu avec rafraichissement du canvas
    menu(1,True,False)

    #Fin de la création de la fenetre
    win.mainloop()
    

def menu(pagea,repaint,same,*args):
    global menuf
    
    #Si on demande de rafraichir le canvas, on appelle paint
    if(repaint):
        paint()

    #On essaye de détruire l'ancien menu, menuf
    try:
        menuf.destroy()
    except NameError: #Si menuf n'existe pas, on ne fais rien
        pass
    except tkinter.TclError:
        pass

    #On crée un nouveau conteneur d'élements, menuf
    menuf=tkinter.Frame(win)

    #Si on demande juste de rafraichir le menu, on prend page comme réference
    if(same):
        if(page==1):
            page1(menuf) #Ajouts des élements de la page 1 sur menuf
        if(page==2):
            page2(menuf)
        if(page==3):
            page3(menuf)
    else: #Sinon on prend le paramètre pagea pour changer de page
        if(pagea==1):
            page1(menuf)
        if(pagea==2):
            page2(menuf)
        if(pagea==3):
            page3(menuf)

    #On positionne le menu à droite du canvas
    #side LEFT signifie le sens d'ajout des élements
    #fill Y signifie que l'élement doit remplir toute la hauteur disponible
    menuf.grid(column=1,row=0,sticky=tkinter.N)

def menuBar(frame,n):
    #Barre de navigation du menu
    
    men=tkinter.Frame(frame) #Nouveau conteneur ajouté à celui en paramètre
    #Les différents boutons
    #partial permet de rajouter des paramètres à une fonction de commande
    b1=tkinter.Button(men,text="Courbes",font=mfont,command=partial(menu,1,False,False),width=7)
    b2=tkinter.Button(men,text="Graph",font=mfont,command=partial(menu,2,False,False),width=7)
    b3=tkinter.Button(men,text="Options",font=mfont,command=partial(menu,3,False,False),width=7)
    #Modification du bouton de la page actuelle
    if(n==1):
        b1.config(state=tkinter.DISABLED,bg="yellow")
    if(n==2):
        b2.config(state=tkinter.DISABLED,bg="yellow")
    if(n==3):
        b3.config(state=tkinter.DISABLED,bg="yellow")
    #Position des boutons sur une grille
    b1.grid(column=0,row=0)
    b2.grid(column=1,row=0)
    b3.grid(column=2,row=0)
    men.pack(fill=tkinter.X)

def page1(frame):
    global page
    page=1
    
    f=tkinter.Frame(frame) #Nouveau conteneur ajouté à celui en paramètre
    
    menuBar(f,1) #On ajoute les boutons sur f
    
    f1=tkinter.Frame(f) #Conteneur des boutons de navigation des ourbes
    #celui de droite appelle la fonction move(-1)
    #et affiche le nombre de courbes avant
    b1=tkinter.Button(f1,text=("<= ("+str(scr)+")"),font=bfont,command=partial(move,-1),width=11)
    if(scr==0):  #Si il n'y as pas de courbes avant, il est désctivé
        b1.config(state=tkinter.DISABLED)
    b1.grid(column=0,row=0) #on l'ajoute sur une grille
    del b1 #On libère la mémoire
    #le bouton de gauche affiche le nombre de courbes apres
    b2=tkinter.Button(f1,text=("("+str(len(curves)-scr-1)+") =>"),font=bfont,command=partial(move,1),width=11)
    #S'il ni y en a pas, on change son nom et sa commande
    if(scr==len(curves)-1 or len(curves)==0):
        b2.config(text="Nouvelle courbe",command=badd)
    b2.grid(column=1,row=0)
    del b2
    f1.pack(fill=tkinter.X) #on pack l'ensemble des boutons

    #Si scr se trouve dans la liste des courbes
    #Il se peut que non si il n'y a pas de courbes
    if(len(curves)>scr):
        #A chaque element de saisie se trouve une variable de la liste du début
        #la modification s'effectue en instantanée mais pas le rafraichissement
        #du graph ici géré par entrée
        #Cela permet aussi de choisir quand on a finis l'edition
        #pour eviter les erreurs constamment
        f1=tkinter.LabelFrame(f,text=("Courbe "+str(scr+1)),padx=5,pady=5)
        
        f2=tkinter.Frame(f1)
        
        tkinter.Label(f2,text="Type :",font=pfont).grid(column=0,row=0)
        tkinter.OptionMenu(f2,curves[scr][TYPE],*ntypes,command=ctype).grid(column=1,row=0)
        
        f2.pack(fill=tkinter.X)
        
        if(types[curves[scr][TYPE].get()]==PARAM):
            f2=tkinter.LabelFrame(f1,text="Equations paramétriques",padx=5,pady=5)
            tkinter.Label(f2,text="x(t)=",font=pfont).grid(column=0,row=0)
            
            e=tkinter.Entry(f2,textvariable=curves[scr][XEQ],width=19)
            try:
                ft(curves[scr][XEQ].get(),0.01)
            except(ZeroDivisionError):
                pass
            except(NameError):
                e.config(bg=WRONG)
            except:
                e.config(bg=WRONG)
            e.grid(column=1,row=0)
            
            tkinter.Label(f2,text="y(t)=",font=pfont).grid(column=0,row=1)
            
            e=tkinter.Entry(f2,textvariable=curves[scr][YEQ],width=19)
            try:
                ft(curves[scr][YEQ].get(),0.01)
            except(ZeroDivisionError):
                pass
            except(NameError):
                e.config(bg=WRONG)
            except:
                e.config(bg=WRONG)
            e.grid(column=1,row=1)
            
            f2.pack(fill=tkinter.X)
        else:
            f2=tkinter.LabelFrame(f1,text="Equation",padx=5,pady=5)
            if(types[curves[scr][TYPE].get()]==POLAR):
                tkinter.Label(f2,text="ρ(t)=",font=pfont).grid(column=0,row=0)
                
                e=tkinter.Entry(f2,textvariable=curves[scr][EQ],width=19)
                try:
                    ft(curves[scr][EQ].get(),0.01)
                except(ZeroDivisionError):
                    pass
                except(NameError):
                    e.config(bg=WRONG)
                except:
                    e.config(bg=WRONG)
                e.grid(column=1,row=0)
                
            if(types[curves[scr][TYPE].get()]==YFX):
                tkinter.Label(f2,text="y=f(x)=",font=pfont).grid(column=0,row=0)
                
                e=tkinter.Entry(f2,textvariable=curves[scr][EQ],width=19)
                try:
                    x=0.01
                    eval(curves[scr][EQ].get())
                except(ZeroDivisionError):
                    pass
                except(NameError):
                    e.config(bg=WRONG)
                except:
                    e.config(bg=WRONG)
                e.grid(column=1,row=0)
                
            if(types[curves[scr][TYPE].get()]==XFY):
                tkinter.Label(f2,text="x=f(y)=",font=pfont).grid(column=0,row=0)
                
                e=tkinter.Entry(f2,textvariable=curves[scr][EQ],width=19)
                try:
                    y=0.01
                    eval(curves[scr][EQ].get())
                except(ZeroDivisionError):
                    pass
                except(NameError):
                    e.config(bg=WRONG)
                except:
                    e.config(bg=WRONG)
                e.grid(column=1,row=0)
                
            f2.pack(fill=tkinter.X)
        if(types[curves[scr][TYPE].get()]==PARAM or types[curves[scr][TYPE].get()]==POLAR):
            f2=tkinter.LabelFrame(f1,text="Paramètre t",padx=5,pady=5)
            if(types[curves[scr][TYPE].get()]==POLAR):
                f2.config(text="Paramètre t (θ)")
            tkinter.Label(f2,text="Min:",font=pfont).grid(column=0,row=0)
            
            e=tkinter.Entry(f2,textvariable=curves[scr][PARMIN],width=6)
            try:
                int(eval(curves[scr][PARMIN].get()))
            except(NameError):
                e.config(bg=WRONG)
            except:
                e.config(bg=WRONG)
            e.grid(column=1,row=0)
            
            tkinter.Label(f2,text="Max:",font=pfont).grid(column=2,row=0)
            
            e=tkinter.Entry(f2,textvariable=curves[scr][PARMAX],width=6)
            try:
                int(eval(curves[scr][PARMAX].get()))
            except(NameError):
                e.config(bg=WRONG)
            except:
                e.config(bg=WRONG)
            e.grid(column=3,row=0)
            
            tkinter.Label(f2,text="Pas:",font=pfont).grid(column=0,row=1)
            
            e=tkinter.Entry(f2,textvariable=curves[scr][PARSTEP],width=6)
            try:
                int(1/eval(curves[scr][PARSTEP].get()))
            except(NameError):
                e.config(bg=WRONG)
            except:
                e.config(bg=WRONG)
            e.grid(column=1,row=1)
            
            f2.pack(fill=tkinter.X)

        f2=tkinter.LabelFrame(f1,text="Autre",padx=5,pady=5)
        tkinter.Label(f2,text="Couleur:     ",font=pfont).grid(column=0,row=0)
        tkinter.Entry(f2,textvariable=curves[scr][CCOLOR],width=10).grid(column=1,row=0)
        tkinter.Label(f2,text="Epaisseur:",font=pfont).grid(column=0,row=1)
        
        e=tkinter.Entry(f2,textvariable=curves[scr][SIZE],width=10)
        try:
            int(curves[scr][SIZE].get())
        except(NameError):
            e.config(bg=WRONG)
        except:
            e.config(bg=WRONG)
        e.grid(column=1,row=1)
        
        f2.pack(fill=tkinter.X)

        f2=tkinter.Frame(f1,padx=5,pady=5)
        tkinter.Button(f2,text="Supprimer",width=12,command=partial(delCurve,scr),font=bfont).grid(column=0,row=0)
        tkinter.Checkbutton(f2,text="Visible",variable=curves[scr][ACTIVE],command=paint).grid(column=1,row=0)
        f2.pack(fill=tkinter.X)
            
        f2.pack()

        f1.pack(fill=tkinter.Y)
    f.pack(fill=tkinter.BOTH,anchor=tkinter.N)

def page2(frame):
    global page
    page=2
    #mêmes principes que précedemment
    f=tkinter.Frame(frame)
    
    menuBar(f,2)
    
    f1=tkinter.LabelFrame(f,text="Fenêtre",padx=5,pady=5)

    f2=tkinter.Frame(f1)
    
    f3=tkinter.LabelFrame(f2,text="X",padx=5,pady=5)
    tkinter.Label(f3,text="min:",font=pfont).grid(column=0,row=0)
    
    e=tkinter.Entry(f3,textvariable=graph[XMIN],width=7)
    try:
        int(eval(graph[XMIN].get()))
    except(NameError):
        e.config(bg=WRONG)
    except:
        e.config(bg=WRONG)
    e.grid(column=1,row=0)
    
    tkinter.Label(f3,text="max:",font=pfont).grid(column=2,row=0)
    
    e=tkinter.Entry(f3,textvariable=graph[XMAX],width=7)
    try:
        int(eval(graph[XMAX].get()))
    except(NameError):
        e.config(bg=WRONG)
    except:
        e.config(bg=WRONG)
    e.grid(column=3,row=0)
    
    f3.grid(column=0,row=0)
    
    f3=tkinter.LabelFrame(f2,text="Y",padx=5,pady=5)
    tkinter.Label(f3,text="min:",font=pfont).grid(column=0,row=0)
    
    e=tkinter.Entry(f3,textvariable=graph[YMIN],width=7)
    try:
        int(eval(graph[YMIN].get()))
    except(NameError):
        e.config(bg=WRONG)
    except:
        e.config(bg=WRONG)
    e.grid(column=1,row=0)
    
    tkinter.Label(f3,text="max:",font=pfont).grid(column=2,row=0)
    
    e=tkinter.Entry(f3,textvariable=graph[YMAX],width=7)
    try:
        int(eval(graph[YMAX].get()))
    except(NameError):
        e.config(bg=WRONG)
    except:
        e.config(bg=WRONG)
    e.grid(column=3,row=0)
    
    f3.grid(column=0,row=1)

    f2.pack(fill=tkinter.X)

    f2=tkinter.Frame(f1)
    tkinter.Button(f2,text="Orthonormer X",command=orthx).grid(column=0,row=0)
    tkinter.Button(f2,text="Orthonormer Y",command=orthy).grid(column=1,row=0)
    f2.pack(fill=tkinter.X)
    st=tkinter.NORMAL
    if(not(azoomenable)):
        st=tkinter.DISABLED
    tkinter.Button(f1,text="Zoom auto",command=azoom,state=st).pack(fill=tkinter.X)
    
    f1.pack(fill=tkinter.BOTH)

    f1=tkinter.LabelFrame(f,text="Graduation",padx=5,pady=5)

    f2=tkinter.LabelFrame(f1,text="Axes",padx=5,pady=5)
    tkinter.Checkbutton(f2,text="1   ",variable=graph[AXIS1],command=paint,width=7).pack()
    tkinter.Checkbutton(f2,text="0.5",variable=graph[AXIS2],command=paint,width=7).pack()
    tkinter.Checkbutton(f2,text="0.1",variable=graph[AXIS3],command=paint,width=7).pack()
    f2.grid(column=0,row=0)

    f2=tkinter.LabelFrame(f1,text="Grille",padx=5,pady=5)
    tkinter.Checkbutton(f2,text="1   ",variable=graph[GRID1],command=paint,width=7).pack()
    tkinter.Checkbutton(f2,text="0.5",variable=graph[GRID2],command=paint,width=7).pack()
    tkinter.Checkbutton(f2,text="0.1",variable=graph[GRID3],command=paint,width=7).pack()
    f2.grid(column=1,row=0)

    f1.pack(fill=tkinter.BOTH)

    f1=tkinter.LabelFrame(f,text="Autre",padx=5,pady=5)
    f2=tkinter.Frame(f1)
    tkinter.Label(f2,text="Fond:",font=pfont).grid(column=0,row=0)
    tkinter.Entry(f2,textvariable=graph[GCOLOR],width=18).grid(column=1,row=0)
    f2.pack()
    tkinter.Checkbutton(f1,text="Titre des axes",variable=graph[AXIST1],command=paint).pack(anchor=tkinter.NW)
    tkinter.Checkbutton(f1,text="Axes flechés",variable=graph[AXISA],command=paint).pack(anchor=tkinter.NW)
    tkinter.Checkbutton(f1,text="Unités",variable=graph[AXIST2],command=paint).pack(anchor=tkinter.NW)
    f1.pack(fill=tkinter.X)
    
    f.pack(fill=tkinter.BOTH,anchor=tkinter.N)
    

def page3(frame):
    global page
    page=3
    #idem
    f=tkinter.Frame(frame)
    
    menuBar(f,3)
       
    f1=tkinter.LabelFrame(f,text="Taille du graph",padx=5,pady=5)
    tkinter.Label(f1,text="X:",font=pfont).grid(column=0,row=0)
    
    e=tkinter.Entry(f1,textvariable=opts[TX],width=6)
    try:
        int(opts[TX].get())
    except:
        e.config(bg=WRONG)
    e.grid(column=1,row=0)
    
    tkinter.Label(f1,text="Y:",font=pfont).grid(column=2,row=0)
    
    e=tkinter.Entry(f1,textvariable=opts[TY],width=6)
    try:
        int(opts[TX].get())
    except:
        e.config(bg=WRONG)
    e.grid(column=3,row=0)
    
    tkinter.Button(f1,text="changer",font=bfont,command=restart).grid(column=4,row=0)
    f1.pack(fill=tkinter.X)

    f1=tkinter.LabelFrame(f,text="Autre",padx=5,pady=5)
    tkinter.Checkbutton(f1,text="Zoomer localement",variable=opts[ZOOM]).pack(anchor=tkinter.NW)
    f2=tkinter.Frame(f1)
    tkinter.Label(f2,text="Précision déplacements:",font=pfont).grid(column=0,row=0)
    tkinter.Entry(f2,textvariable=opts[RND],width=5).grid(column=1,row=0)
    f2.pack()
    f1.pack(fill=tkinter.X)

    f1=tkinter.LabelFrame(f,text="Informations",padx=5,pady=5)
    tkinter.Label(f1,text="Commandes",font=pbfont).pack()
    tkinter.Label(f1,text="Entrée - Valider les champs\nClic gauche - Déplacer l'origine\nClic droit - Dézoomer\nClic droit (glisser) - Zoomer\nMolette - Zoomer/Dézoomer",font=pfont).pack()
    tkinter.Label(f1,text="Divers",font=pbfont).pack()
    tkinter.Label(f1,text="\"pi\" est valide dans l'écriture\ndes fonctions et valeurs.",font=pfont).pack()
    tkinter.Label(f1,text="A propos",font=pbfont).pack()
    tkinter.Label(f1,text="Graph version "+ver+"\nDéveloppé par : Clément Gouin\nclement.gouin@reseau.eseo.fr",font=pfont).pack()
    f1.pack(fill=tkinter.X)
    
    f.pack(fill=tkinter.BOTH,anchor=tkinter.N)

def paint():
    global cv,autozoom,azoomenable
    try:
        cv.destroy()
    except NameError:
        pass
    except tkinter.TclError:
        pass
    cv=tkinter.Canvas(win,width=opts[TX].get(),height=opts[TY].get())
    cv.grid(column=0,row=0,sticky=tkinter.N)
    cv.bind("<Button-1>",bu1)
    cv.bind("<Button-3>",bu3)
    cv.bind("<B3-Motion>",bu3m)
    cv.bind("<ButtonRelease-3>",bu3r)
    #Une des fonctions principales du programme
    #elle permet le rafraichissement du canvas

    #on crée tout d'abord le fond par un rectangle,
    #on efface rien, on colle juste le fond par dessus le précédent
    cv.create_rectangle(2,2,opts[TX].get(),opts[TY].get()-3,fill=graph[GCOLOR].get())
    #suivant les paramètres, on affiche les grilles et axes ou non
    if(graph[GRID3].get()):
        gridf(0.1,"grey90")
    if(graph[GRID2].get()):
        gridf(0.5,"grey80")
    if(graph[GRID1].get()):
            gridf(1,"grey70")
    #Ici on met en paramètre qui est l'axe maitre,
    #car c'est lui qui affiche les noms des axes, les unités et les fleches
    if(graph[AXIS1].get()):
        axisf(1,"grey40",4,True) #L'axe 1 est toujours maitre s'il est actif
    if(graph[AXIS2].get()):
        axisf(0.5,"grey40",2,(not(graph[AXIS1].get()))) #Sinon c'est le 0.5 etc.
    if(graph[AXIS3].get()):
        axisf(0.1,"grey40",1,(not(graph[AXIS1].get()) and not(graph[AXIS2].get())))
    #enfin on affiche les courbes successivement et si elles sont affichées
    autozoom=[0,0,0,0]
    azoomenable=False
    if(len(curves)>0):
        for k in range(len(curves)):
            if(curves[k][ACTIVE].get()):
                curvef(k,curves[k][CCOLOR].get(),curves[k][SIZE].get())
    if(zoombe):
        cv.create_rectangle(zoomb[0][0],zoomb[0][1],zoomb[1][0],zoomb[1][1],outline="red")
    
    
def gridf(pas,col):
    #On récupère les différentes variables
    try:
        tx,ty,xmax,xmin,ymax,ymin=opts[TX].get(),opts[TY].get(),eval(graph[XMAX].get()),eval(graph[XMIN].get()),eval(graph[YMAX].get()),eval(graph[YMIN].get())
    except:
        pass
    else:
        factx=tx/(abs(xmax-xmin))
        facty=ty/(abs(ymax-ymin))
        n = int((2+abs(ymax-ymin))/pas)
        d=abs(ymin)-abs(int(ymin))
        for k in range(n+1):
            cv.create_line(0,ty-(k*pas+d-1)*facty,tx,ty-(k*pas+d-1)*facty,fill=col)
        n = int((2+abs(xmax-xmin))/pas)
        d=abs(xmin)-abs(int(xmin))
        for k in range(n+1):
            cv.create_line((k*pas+d-1)*factx,0,(k*pas+d-1)*factx,ty,fill=col)

def axisf(pas,col,t1,high):
    try:
        tx,ty,xmax,xmin,ymax,ymin=opts[TX].get(),opts[TY].get(),eval(graph[XMAX].get()),eval(graph[XMIN].get()),eval(graph[YMAX].get()),eval(graph[YMIN].get())
    except:
        pass
    else:
        factx=tx/(abs(xmax-xmin))
        facty=ty/(abs(ymax-ymin))
        if(min(xmin,xmax)<0 and max(xmin,xmax)>0):
            n = int((2+abs(ymax-ymin))/pas)
            d=abs(min(ymin,ymax))-abs(int(min(ymin,ymax)))
            if(high and graph[AXISA].get()):
                if(ymax>ymin):
                    cv.create_line(-sgn(xmin,xmax)*xmin*factx,0,-sgn(xmin,xmax)*xmin*factx,ty,fill=col,arrow=tkinter.FIRST)
                else:
                    cv.create_line(-sgn(xmin,xmax)*xmin*factx,0,-sgn(xmin,xmax)*xmin*factx,ty,fill=col,arrow=tkinter.LAST)
            else:
                cv.create_line(-sgn(xmin,xmax)*xmin*factx,0,-sgn(xmin,xmax)*xmin*factx,tx,fill=col)

            for k in range(n+1):
                cv.create_line(-sgn(xmin,xmax)*xmin*factx-t1,ty-(k*pas+d-1)*facty,-sgn(xmin,xmax)*xmin*factx+t1+1,ty-(k*pas+d-1)*facty,fill=col)
            if(high and graph[AXIST2].get() and min(ymin,ymax)<pas and max(ymin,ymax)>pas):
                cv.create_text(-10-sgn(xmin,xmax)*xmin*factx,ty-(pas-ymin)*facty,text=str(pas),font=pfont,fill=col)
            if(high and graph[AXIST1].get()):
                if(ymax>ymin):
                    cv.create_text(-10-xmin*factx,15,text="y",font=pfont,fill=col)
                else:
                    cv.create_text(-10-xmin*factx,ty-35,text="y",font=pfont,fill=col)
            
        if(min(ymin,ymax)<0 and max(ymin,ymax)>0):
            n = int((2+abs(xmax-xmin))/pas)
            d=abs(min(xmin,xmax))-abs(int(min(xmin,xmax)))
            if(high and graph[AXISA].get()):
                if(xmax>xmin):
                    cv.create_line(0,ty+sgn(ymin,ymax)*ymin*facty,tx,ty+sgn(ymin,ymax)*ymin*facty,fill=col,arrow=tkinter.LAST)
                else:
                    cv.create_line(0,ty+sgn(ymin,ymax)*ymin*facty,tx,ty+sgn(ymin,ymax)*ymin*facty,fill=col,arrow=tkinter.FIRST)
            else:
                cv.create_line(0,ty+sgn(ymin,ymax)*ymin*facty,tx,ty+sgn(ymin,ymax)*ymin*facty,fill=col)
            for k in range(n+1):
                cv.create_line((k*pas+d-1)*factx,ty+sgn(ymin,ymax)*ymin*facty-t1,(k*pas+d-1)*factx,ty+sgn(ymin,ymax)*ymin*facty+t1+1,fill=col)
            if(high and graph[AXIST2].get() and min(xmin,xmax)<pas and max(xmin,xmax)>pas):
                cv.create_text((pas-xmin)*factx,ty+sgn(ymin,ymax)*ymin*facty+15,text=str(pas),font=pfont,fill=col)
            if(high and graph[AXIST1].get()):
                if(xmax>xmin):
                    cv.create_text(tx-10,ty+ymin*facty+15,text="x",font=pfont,fill=col)
                else:
                    cv.create_text(10,ty+ymin*facty+15,text="x",font=pfont,fill=col)

def curvef(k,col,ta):
    global curves,azoomenable,autozoom
    try:
        tx,ty,xmax,xmin,ymax,ymin,parmin,parmax,parstep=opts[TX].get(),opts[TY].get(),eval(graph[XMAX].get()),eval(graph[XMIN].get()),eval(graph[YMAX].get()),eval(graph[YMIN].get()),eval(curves[k][PARMIN].get()),eval(curves[k][PARMAX].get()),eval(curves[k][PARSTEP].get())
        1/parstep
    except:
        pass
    else:
        factx=tx/(xmax-xmin)
        facty=ty/(ymax-ymin)
        if(types[curves[k][TYPE].get()]==PARAM):
            azoomenable=True
        if(types[curves[k][TYPE].get()]==POLAR):
            azoomenable=True
            curves[k][XEQ].set("("+curves[k][EQ].get()+")*cos(t)")
            curves[k][YEQ].set("("+curves[k][EQ].get()+")*sin(t)")
        if(types[curves[k][TYPE].get()]==YFX):
            curves[k][XEQ].set("t")
            curves[k][YEQ].set(curves[k][EQ].get().replace('x','t'))
            curves[k][PARMIN].set(xmin)
            curves[k][PARMAX].set(xmax)
            curves[k][PARSTEP].set(abs(xmax-xmin)/(tx))
        if(types[curves[k][TYPE].get()]==XFY):
            curves[k][YEQ].set("t")
            curves[k][XEQ].set(curves[k][EQ].get().replace("y","t"))
            curves[k][PARMIN].set(ymin)
            curves[k][PARMAX].set(ymax)
            curves[k][PARSTEP].set(abs(ymax-ymin)/(ty))
            
        n = int((parmax-parmin)/parstep)+2
        li=[];
        for k1 in range(n):
            t=parmin+k1*parstep
            try:
                li+=[[ft(curves[k][XEQ].get(),t),ft(curves[k][YEQ].get(),t),True]]
                if(azoomenable):
                    if(li[k1][0]>autozoom[XMAX]):
                        autozoom[XMAX]=li[k1][0]
                    if(li[k1][0]<autozoom[XMIN]):
                        autozoom[XMIN]=li[k1][0]
                    if(li[k1][1]>autozoom[YMAX]):
                        autozoom[YMAX]=li[k1][1]
                    if(li[k1][1]<autozoom[YMIN]):
                        autozoom[YMIN]=li[k1][1]
            except(ZeroDivisionError):
                li+=[[0,0,False]]
        for k1 in range(n):
            li[k1][0]=int((li[k1][0]-xmin)*factx)
            li[k1][1]=ty-int((li[k1][1]-ymin)*facty)
        for k1 in range(n-1):
            if(li[k1][2] and li[k1+1][2] and
               ((0<li[k1][0]<tx and 0<li[k1][1]<ty) or
               (0<li[k1+1][0]<tx and 0<li[k1+1][1]<ty))):
                    cv.create_line(li[k1][0],li[k1][1],li[k1+1][0],li[k1+1][1],fill=col,width=ta)

def restart():
    global win,curves,graph,opts,scr
    #Lorsque l'on veut modifier la fenetre, on doit la détruire
    #et cela détruit toutes les variables tkinter, on les sauvegarde
    #donc dans des listes et on les recrée
    
    if(len(curves)>0):
        savcurves = []
        for k in range(len(curves)):
            temp=[]
            for l in range(len(curves[k])):
                temp+=[curves[k][l].get()]
            savcurves+=[temp[:]]
    savgraph=[]
    for k in range(len(graph)):
        savgraph+=[graph[k].get()]
    savopts=[]
    for k in range(len(opts)):
        savopts+=[opts[k].get()]
    win.destroy()
    win=tkinter.Tk()
    tkvars(savcurves,savgraph,savopts)
    paintwin()
    
    

def tkvars(cu,ax,op):
    global curves,graph,opts
    #Définitions des variables et de leur type
    
    curves=[]
    if(len(cu)>0):
        for k in range(len(cu)):
            newCurve(cu[k][ACTIVE],cu[k][TYPE],cu[k][EQ],cu[k][XEQ],cu[k][YEQ],cu[k][PARMIN],cu[k][PARMAX],cu[k][PARSTEP],cu[k][CCOLOR],cu[k][SIZE])
            
    graph=LENGRAPH*[None]
    graph[XMAX]=tkinter.StringVar()
    graph[XMIN]=tkinter.StringVar()
    graph[YMIN]=tkinter.StringVar()
    graph[YMAX]=tkinter.StringVar()
    graph[AXIS1]=tkinter.IntVar()
    graph[AXIS2]=tkinter.IntVar()
    graph[AXIS3]=tkinter.IntVar()
    graph[AXIST1]=tkinter.IntVar()
    graph[AXIST2]=tkinter.IntVar()
    graph[AXISA]=tkinter.IntVar()
    graph[GRID1]=tkinter.IntVar()
    graph[GRID2]=tkinter.IntVar()
    graph[GRID3]=tkinter.IntVar()
    graph[GCOLOR]=tkinter.StringVar()
    for k in range(len(graph)):
        graph[k].set(ax[k])
        
    opts=LENOPTS*[None]
    opts[TX]=tkinter.IntVar()
    opts[TY]=tkinter.IntVar()
    opts[ZOOM]=tkinter.IntVar()
    opts[RND]=tkinter.IntVar()
    for k in range(len(opts)):
        opts[k].set(op[k])

def newCurve(active,typef,eq,xeq,yeq,tmin,tmax,tstep,color,size):
    global curves,scr
    #Ajout d'une courbe
    
    curves+=[LENCURVES*[None]]
    n=len(curves)-1
    curves[n][ACTIVE]=tkinter.IntVar()
    curves[n][TYPE]=tkinter.StringVar()
    curves[n][EQ]=tkinter.StringVar()
    curves[n][XEQ]=tkinter.StringVar()
    curves[n][YEQ]=tkinter.StringVar()
    curves[n][PARMIN]=tkinter.StringVar()
    curves[n][PARMAX]=tkinter.StringVar()
    curves[n][PARSTEP]=tkinter.StringVar()
    curves[n][CCOLOR]=tkinter.StringVar()
    curves[n][SIZE]=tkinter.IntVar()
    curves[n][ACTIVE].set(active)
    curves[n][TYPE].set(typef)
    curves[n][EQ].set(eq)
    curves[n][XEQ].set(xeq)
    curves[n][YEQ].set(yeq)
    curves[n][PARMIN].set(tmin)
    curves[n][PARMAX].set(tmax)
    curves[n][PARSTEP].set(tstep)
    curves[n][CCOLOR].set(color)
    curves[n][SIZE].set(size)

def delCurve(n):
    global curves,scr
    #Destruction d'une courbe
    
    del curves[n]
    scr-=1
    menu(1,True,False)


def enter(event):
    #Evenement correspondand à l'appui de la touche entrée
    menu(1,True,True)

def bu1(event):
    global graph
    #Evenement du clic de la souris
    #le graph ce centre sur ce clic
    tx,ty,xmax,xmin,ymax,ymin=opts[TX].get(),opts[TY].get(),eval(graph[XMAX].get()),eval(graph[XMIN].get()),eval(graph[YMAX].get()),eval(graph[YMIN].get())
    
    factx=tx/(xmax-xmin)
    facty=ty/(ymax-ymin)
    dx=(event.x-tx/2)/factx
    dy=(event.y-ty/2)/facty
    graph[XMAX].set(rnd(xmax+dx,opts[RND].get()))
    graph[XMIN].set(rnd(xmin+dx,opts[RND].get()))
    graph[YMAX].set(rnd(ymax-dy,opts[RND].get()))
    graph[YMIN].set(rnd(ymin-dy,opts[RND].get()))
    menu(2,True,True)

def bu3(event):
    global zoomb,zoombe,win
    zoombe=True
    zoomb=[[event.x,event.y],[event.x,event.y]]
    win.after(20,paint)

def bu3m(event):
    global zoomb,win
    zoomb[1]=[event.x,event.y]
    win.after(20,paint)
    

def bu3r(event):
    global zoomb,zoombe,graph
    tx,ty,xmax,xmin,ymax,ymin=opts[TX].get(),opts[TY].get(),eval(graph[XMAX].get()),eval(graph[XMIN].get()),eval(graph[YMAX].get()),eval(graph[YMIN].get())
    zoombe=False
    if(abs(zoomb[0][0]-zoomb[1][0])<5 and abs(zoomb[0][1]-zoomb[1][1])<5):
        factx=opts[TX].get()/(abs(xmax-xmin))
        facty=opts[TY].get()/(abs(ymax-ymin))
        factx/=2
        facty/=2
        dx=(opts[TX].get()-(xmax-xmin)*factx)/factx
        dy=(opts[TY].get()-(ymax-ymin)*factx)/factx
        graph[XMAX].set(rnd(xmax+dx/2,opts[RND].get()))
        graph[XMIN].set(rnd(xmin-dx/2,opts[RND].get()))
        graph[YMAX].set(rnd(ymax+dy/2,opts[RND].get()))
        graph[YMIN].set(rnd(ymin-dy/2,opts[RND].get()))
    else:
        factx=opts[TX].get()/(abs(xmax-xmin))
        facty=opts[TY].get()/(abs(ymax-ymin))
        graph[XMIN].set(rnd(xmin+zoomb[0][0]/factx,opts[RND].get()))
        graph[XMAX].set(rnd(xmin+zoomb[1][0]/factx,opts[RND].get()))
        graph[YMIN].set(rnd(ymax-zoomb[0][1]/facty,opts[RND].get()))
        graph[YMAX].set(rnd(ymax-zoomb[1][1]/facty,opts[RND].get()))
    menu(1,True,True)
    

def zoom(event):
    global graph
    #Evenement de la molette de la souris
    tx,ty,xmax,xmin,ymax,ymin=opts[TX].get(),opts[TY].get(),eval(graph[XMAX].get()),eval(graph[XMIN].get()),eval(graph[YMAX].get()),eval(graph[YMIN].get())
    
    zoom = event.delta/120
    factx=opts[TX].get()/(abs(xmax-xmin))
    facty=opts[TY].get()/(abs(ymax-ymin))
    factx+=zoom*2
    facty+=zoom*2
    dx=(opts[TX].get()-(xmax-xmin)*factx)/factx
    dy=(opts[TY].get()-(ymax-ymin)*factx)/factx
    graph[XMAX].set(rnd(xmax+dx/2,opts[RND].get()))
    graph[XMIN].set(rnd(xmin-dx/2,opts[RND].get()))
    graph[YMAX].set(rnd(ymax+dy/2,opts[RND].get()))
    graph[YMIN].set(rnd(ymin-dy/2,opts[RND].get()))
    if(zoom>0 and opts[ZOOM].get()):
        dx=(event.x-opts[TX].get()/2)/factx
        dy=(event.y-opts[TY].get()/2)/facty
        graph[XMAX].set(rnd(graph[XMAX]+dx,opts[RND].get()))
        graph[XMIN].set(rnd(graph[XMIN]+dx,opts[RND].get()))
        graph[YMAX].set(rnd(graph[YMAX]-dy,opts[RND].get()))
        graph[YMIN].set(rnd(graph[YMIN]-dy,opts[RND].get()))
    menu(2,True,True)

def azoom():
    global graph
    graph[XMAX].set(autozoom[XMAX]*1.1)
    graph[XMIN].set(autozoom[XMIN]*1.1)
    graph[YMAX].set(autozoom[YMAX]*1.1)
    graph[YMIN].set(autozoom[YMIN]*1.1)
    menu(2,True,True)

def badd():
    global scr
    #ajout d'une courbe vide avec le bouton "Nouvelle Courbe"
    newCurve(0,ntypes[PARAM],"","","",0,0,0.1,"black",1)
    if(len(curves)>1):
        scr+=1
    menu(1,True,False)

def ctype(*args):
    #TODO
    if(types[curves[scr][TYPE].get()]==POLAR and curves[scr][EQ].get()!=""):
        curves[scr][EQ].set(curves[scr][EQ].get().replace("y","t"))
        curves[scr][EQ].set(curves[scr][EQ].get().replace("x","t"))
    if(types[curves[scr][TYPE].get()]==XFY and curves[scr][EQ].get()!=""):
        curves[scr][EQ].set(curves[scr][EQ].get().replace("t","y"))
        curves[scr][EQ].set(curves[scr][EQ].get().replace("x","y"))
    if(types[curves[scr][TYPE].get()]==YFX and curves[scr][EQ].get()!=""):
        curves[scr][EQ].set(curves[scr][EQ].get().replace("t","x"))
        curves[scr][EQ].set(curves[scr][EQ].get().replace("y","x"))
    menu(1,False,False)

def move(n):
    global scr
    #Changement de courbe dans le menu
    if(n>0 and scr<len(curves)-1):
        scr+=1
    elif(n<0 and scr>0):
        scr-=1
    menu(1,False,False)

def orthx():
    global graph
    #Orthonormalisation de l'axe x en fonction de l'axe y
    tx,ty,xmax,xmin,ymax,ymin=opts[TX].get(),opts[TY].get(),eval(graph[XMAX].get()),eval(graph[XMIN].get()),eval(graph[YMAX].get()),eval(graph[YMIN].get())
    
    if(xmax<xmin):
        i=xmin
        graph[XMIN].set(xmax)
        graph[YMAX].set(i)
    c=xmin+(abs(xmax-xmin))/2
    dx=(abs(ymax-ymin))*tx/ty
    graph[XMAX].set(c+dx/2)
    graph[XMIN].set(c-dx/2)
    menu(2,True,True)
    
def orthy():
    global graph
    #Idem en inversant
    tx,ty,xmax,xmin,ymax,ymin=opts[TX].get(),opts[TY].get(),eval(graph[XMAX].get()),eval(graph[XMIN].get()),eval(graph[YMAX].get()),eval(graph[YMIN].get())
    if(ymax<ymin):
        i=ymin
        graph[YMIN].set(ymax)
        graph[YMAX].set(i)
    c=ymin+(abs(ymax-ymin))/2
    dy=(abs(xmax-xmin))*ty/tx
    graph[YMAX].set(c+dy/2)
    graph[YMIN].set(c-dy/2)
    menu(2,True,True)
    
#fonctions utiles

def ft(text,t):
    #Transformation du texte de f(t) en vraie fonction
    return eval(text)

def rnd(n,p):
    #arrondi de n au p-ième chiffre
    return int(n*10**p+0.5)/(10**p)

def sgn(minv,maxv):
    #signe en fonction de l'inversion des axes
    if(maxv<minv):
        return -1
    return 1

#Démarrage du programme
start()
