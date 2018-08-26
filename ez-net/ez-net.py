#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
EZ-NET 1.4
Klemek 2016

INFO EN:

        Ez-net is a simple tool that help you divide a network easily.
        Work in both Python 2 and 3.

	Instructions :
		3 ways to use ez-net :

		1) (Windows only)
			Double-click on the "ez-net.py" file

		2) (With IDLE)
			Open the "ez-net.py" file with IDLE
			Press F5 or go to menu "Run">"Run Module"

		3) (In command line)
			Go to the folder where the file is with CD
			(On Windows you can do SHIFT+right-clic>"Open command window here")
			(On Linux you can do right-clic>"Open in terminal")
			Execute "python ez-net.py"


	Change language :
		You can change the language by changing the value of LANG
		(Right after this introduction)
		0 = English
		1 = Francais

	Text only:
		ez-net is available in text only by adding the parameter
		"-noGUI" in command line :
		"python ez-net.py -noGUI"

INFO FR:

        Ez-net est un outil simple qui vous permet de diviser un réseau facilement.
        Fonctionne aussi bien sur Python 2 que 3.
        
	Instructions :
		3 méthodes pour utiliser ez-net :

		1) (Windows seulement)
			Double-cliquez sur le fichier "ez-net.py"

		2) (Avec IDLE)
			Ouvrez avec IDLE le fichier "ez-net.py"
			Appuyez sur F5 ou ouvrez le menu "Run">"Run Module"

		3) (En ligne de commande)
			Placez vous dans le dossier du fichier avec CD
			(Sous Windows vous pouvez faire MAJ+clic-droit>"Ouvrir une
			fenêtre de commande içi")
			(Sous Linux vous pouvez faire clic-droit>"Ouvrir dans un
			terminal")
			Executez "python ez-net.py"


	Changer la langue :
		Vous pouvez changer la langue en modifiant la valeur de LANG
		(Juste après cette introduction)
		0 = English
		1 = Francais

	Utilisation textuelle:
		ez-net est disponible en version textuelle en rajoutant "-noGUI"
		comme argument en ligne de commande
		"python ez-net.py -noGUI"

'''

LANG = 0


try:
    from math import log2
    PYTH3 = True
except ImportError:
    from math import log

    def log2(a):
        return log(a) / log(2)
    PYTH3 = False

try:
    if PYTH3:
        import tkinter as tk
        import tkinter.filedialog as fd
    else:
        import Tkinter as tk
        import tkFileDialog as fd
    TK = True
except ImportError:
    TK = False

import os
import sys

VER = "1.4"
STRINGS = {"inputadd": ["Enter the network's address to divide : ",
                        "Entrez l'adresse du réseau à diviser : "],
           "inputmsk": ["Enter the mask : ",
                        "Entrez le masque : "],
           "txtact0": ["Divide the network into n sub-networks",
                       "Diviser le réseau en n sous-réseaux"],
           "txtact1": ["Divide the network into sub-networks with /n masks",
                       "Diviser le réseau en sous-réseaux de masque /n"],
           "txtact2": ["Divide the network into sub-networks with n addresses",
                       "Diviser le réseau en sous-réseaux de n adresses"],
           "newb": ["New",
                    "Nouveau"],
           "openb": ["Open",
                     "Ouvrir"],
           "saveb": ["Save",
                     "Sauver"],
           "act0b": ["Divide into n",
                     "Diviser en n"],
           "act1b": ["Divide into /n",
                     "Diviser en /n"],
           "act2b": ["Divide into size n",
                     "Diviser en taille n"],
           "act3b": ["Clean",
                     "Nettoyer"],
           "act4b1": ["Show",
                      "Montrer"],
           "act4b2": ["Hide",
                      "Cacher"],
           "act5b": ["Name",
                     "Nommer"],
           "act0t": ["Enter how many sub-network to create (<={}) : ",
                     "Entrez combien de sous-réseaux à créer (<={}) : "],
           "act1t": ["Enter the mask number (>/{}) : ",
                     "Entrez le nombre du masque (>/{}) : "],
           "act2t": ["Enter the maximum number of addresses in a sub-network (<={}) : ",
                     "Entrez le nombre maximum d'adresses dans un sous-réseau (<={}) : "],
           "act5t": ["Enter a name for this sub-network (leave blank for none) : ",
                     "Entrez un nom pour ce réseau (laissez vide pour aucun) : "],
           "desc0": ["Address\t: {}\n",
                     "Adresse\t: {}\n"],
           "desc1": ["Mask   \t: {} (/{})\n",
                     "Masque \t: {} (/{})\n"],
           "desc2": ["Number of addresses :\n{}\n",
                     "Nombre d'adresses :\n{}\n"],
           "desc3": ["Broadcast: {}\n",
                     "Diffusion: {}\n"],
           "desc4": ["Name  \t: {}",
                     "Nom   \t: {}"],
           "error0": ["Error",
                      "Erreur"],
           "error1": ["Invalid address",
                      "Adresse invalide"],
           "error2": ["Invalid mask",
                      "Masque invalide"],
           "error3": ["Invalid value",
                      "Valeur invalide"],
           "msg0": ["{} sub-networks created",
                    "{} sous-réseaux créés"],
           "txtmsg0": ["Dividing into {} sub-networks /{} ({}) ({} addresses):",
                       "Division en {} sous-réseaux /{} ({}) ({} adresses):"],
           "txtadd": ["add:{}/{} msk:{} -> {} addresses",
                      "adr:{}/{} msq:{} -> {} adresses"],
           "ok": ["OK",
                  "OK"],
           "cancel": ["Cancel",
                      "Annuler"],
           "definput": ["Value : ",
                        "Valeur : "],
           "files": [[("Network file", ".ezn")],
                     [("Fichier réseau", ".ezn")]]}

CANCEL = "CANCEL"
MONOSPACE = ("Consolas", "10")
# util


def power2(a):
    '''
    To know if a number is a power of 2
    input : a the number to check
    example:
    power2(5)=False
    power2(128)=True
    '''
    n = log2(a)
    return n == int(n)

# network math


def addtobin(a):
    '''
    Returns the binary value of an address
    input : the address in array
    example :
    addtobin([192,168,1,2])='11000000101010000000000100000010'
    '''
    return "".join(["{:0>8}".format(bin(i)[2:])for i in a])


def bintoadd(b):
    '''
    Reverse operation as addtobin
    input : the address in binary
    example :
    bintoadd('11000000101010000000000100000010')=[192,168,1,2]
    '''
    return [int(b[i * 8:i * 8 + 8], 2) for i in range(len(b) // 8)]


def mask(n):
    '''
    Returns the mask associated with a number
    input : the number of the mask
    example :
    mask(19)=[255, 255, 224, 0]
    '''
    return bintoadd('1' * n + '0' * (32 - n))


def masknum(m):
    '''
    Returns the number of a mask
    input : the mask in array
    example :
    masknum([255, 255, 224, 0]) = 19
    '''
    return addtobin(m).count("1")


def netadd(a, m):
    '''
    Returns the network address for a given address
    inputs : -the address in array
    -the mask in array
    example :
    netadd([192,61,196,10],[255,255,128,0])=[192, 61, 128, 0]
    '''
    return [a[i] & m[i] for i in range(4)]


def broadadd(a, m):
    '''
    Returns the broadcast address for a given address
    inputs : -the address in array
    -the mask in array
    example :
    broadadd([192,61,196,10],[255,255,128,0])=[192, 61, 255, 255]
    '''
    ba = addtobin(netadd(a, m))
    bm = addtobin(m)
    ba2 = ""
    for i in range(len(ba)):
        if bm[i] == '1':
            ba2 += ba[i]
        else:
            ba2 += '1'
    return bintoadd(ba2)


def nextnetadd(a, m):
    '''
    Returns the address of the next network
    inputs : -the address in array
    -the mask in array
    example :
    nextnetadd([192,61,196,10],[255,255,128,0])=[192, 62, 0, 0]
    '''
    ba = addtobin(netadd(a, m))
    n = masknum(m)
    ba2 = "{:0>32}".format(bin(int(ba[:n], 2) + 1)[2:] + '0' * (32 - n))
    return bintoadd(ba2)


def nadd(m):
    '''
    Returns the number of available addresses in a network
    input : the mask in array
    example :
    nadd([255,255,128,0])=32766
    '''
    n = masknum(m)
    return 2**(32 - n) - 2


def div(a, m, n):
    '''
    Divide a network with mask /a into subnetwork /a+n
    input : -the address in array
    -the mask in array
    -the mask number difference
    example :
    div([199,168,1,0],[255,255,255,0],2)=[[[199, 168, 1, 0], [255, 255, 255, 192]],
                                        [[199, 168, 1, 64], [255, 255, 255, 192]],
                                        [[199, 168, 1, 128], [255, 255, 255, 192]],
                                        [[199, 168, 1, 192], [255, 255, 255, 192]]]
    '''
    nmsk = masknum(m) + n
    m2 = mask(nmsk)
    a = netadd(a, m2)
    out = []
    for i in range(2**n):
        out += [[a, m2]]
        a = nextnetadd(a, m2)
    return out

# string parsing


def stringadd(a):
    '''
    Returns a string value of an address
    input : the address in array
    example :
    stringadd([192,168,1,1])="192.168.1.1"
    '''
    return ".".join([str(i) for i in a])


def formatnumber(n):
    '''
    Returns a formated string of a number
    input : the number to format
    example :
    formatnumber(81681681)="81,681,681"
    '''
    sn = str(n)
    out = ""
    for i in range(len(sn)):
        if i != 0 and i % 3 == 0:
            out += ","
        out += sn[-i - 1]
    return out[::-1]


def wraptext(txt, nchar):
    '''
    Wrap a text to fit in a given width
    input : -the text to wrap
    -the width to fit in
    example :
    wraptext("this is a very very long text !",10)="this is a\nvery very\nlong text !"
    '''
    k = 0
    lst = None
    for i in range(len(txt)):
        if txt[i] == " ":
            lst = i
        if k >= nchar:
            if lst is not None:
                txt = txt[:lst] + "\n" + txt[lst + 1:]
                k -= lst
        k += 1
    return txt


def checkadd(add):
    '''
    Check if an address is valid
    input : the string of the address
    example :
    checkadd("192.168.1.1")=True
    checkadd("287.168.1.1")=False
    checkadd("192.168,1.1")=False
    '''
    if add.count(".") == 3:
        try:
            for sadd in add.split("/")[0].split("."):
                if not 0 <= int(sadd) < 256:
                    return False
            if "/" in add:
                msk = int(add.split("/")[1])
                if not 0 <= msk <= 30:
                    return False
        except ValueError:
            return False
    else:
        return False
    return True


def parseadd(add):
    '''
    Parse a given valid address and return the mask if given
    input : the string of the address
    example :
    parseadd("192.168.1.1")=([192,168,1,1],None)
    parseadd("192.168.1.1/21")=([192,168,1,1],21)
    '''
    a = []
    msk = None
    for sadd in add.split("/")[0].split("."):
        a += [int(sadd)]
    if "/" in add:
        msk = int(add.split("/")[1])
    return a, msk


def checkmsk(msk, mmin=0, mmax=30):
    '''
    Check if a mask is valid or in a range
    input : -the string of the mask
    -(opt) mmin, the minimum mask number
    -(opt) mmax, the maximum mask number
    example :
    checkmsk("255.255.128.0")=True
    checkadd("255.128.255.0")=False
    checkadd("/25")=True
    checkadd("/31")=False
    checkadd("2")=True
    checkadd("-1")=False
    checkadd("25",mmax=22)=False
    checkadd("255.128.0.0",mmin=12)=False
    '''
    try:
        if "." in msk:
            m = []
            for smsk in msk.split("."):
                if not 0 <= int(smsk) < 256:
                    return False
                else:
                    m += [int(smsk)]
            bm = addtobin(m)
            f0 = False
            for i in bm:
                if f0 and i == '1':
                    return False
                if i == '0':
                    f0 = True
            if not mmin <= masknum(m) <= mmax:
                return False
        else:
            n = int(msk.replace("/", ""))
            if not mmin <= n <= mmax:
                return False
    except ValueError:
        return False
    return True


def parsemsk(msk):
    '''
    Parse a given valid mask
    input : the string of the mask
    example :
    parsemsk("255.255.128.0")=[255,255,128,0]
    parsemsk("/17")=[255,255,128,0]
    parsemsk("17")=[255,255,128,0]
    '''
    if "." in msk:
        m = []
        for smsk in msk.split("."):
            m += [int(smsk)]
    else:
        n = int(msk.replace("/", ""))
        m = mask(n)
    return m

# I/O console


def inputadd(txt, txtfalse=STRINGS["error1"][LANG]):
    '''
    Ask for an address in terminal while it isn't valid
    input : -the text of the question
    -(opt) txtfalse, the text of error when not valid
    returns the same as parseadd
    '''
    cont = False
    while not cont:
        add = input(txt).strip()
        cont = checkadd(add)
        if not cont:
            print(txtfalse)
    return parseadd(add)


def inputmsk(txt, txtfalse=STRINGS["error2"][LANG], mmin=0, mmax=30):
    '''
    Ask for a mask in terminal while it isn't valid
    input : -the text of the question
    -(opt) txtfalse, the text of error when not valid
    -(opt) mmin, the minimum mask number
    -(opt) mmax, the maximum mask number
    returns the same as parsemsk
    '''
    cont = False
    while not cont:
        msk = input(txt)
        cont = checkmsk(msk, mmin, mmax)
        if not cont:
            print(txtfalse)
    return parsemsk(msk)


def inputselect(txt, mi, ma, txtfalse=STRINGS["error3"][LANG]):
    '''
    Ask for an integer input while it isn't valid
    input : -the text of the question
    -the minimum value included
    -the maximum value included
    -(opt) txtfalse, the text of error when not valid
    returns the valid integer input
    '''
    cont = False
    while not cont:
        s = input(txt)
        cont = True
        try:
            n = int(s)
            if not mi <= n <= ma:
                cont = False
        except ValueError:
            cont = False
        if not cont:
            print(txtfalse)
    return n


def printnet(a, m):
    '''
    Print a network with a default format
    input : -the address in array
    -the mask in array
    '''
    print(STRINGS["txtadd"][LANG].format(
        stringadd(netadd(a, m)), masknum(m), stringadd(m), nadd(m)))

# I/O tkinter


class EntryDialog:
    '''
    Pop-up that ask for an input
    arguments : -the master window
    -(opt) text, the text of the question
    -(opt) size, the width of the window in font-size
    -(opt) default, the text already put on the entry
    -(opt) allowcancel, show the cancel button
    use:
    entry = EntryDialog(master, text="some question")
    master.wait_window(entry.top)
    value = entry.get()
    #if the user quit the window or hit cancel, the CANCEL value is given
    '''
    
    def __init__(self, parent, text=STRINGS["definput"][LANG], size=25, default="", allowcancel=True):
        self.top = tk.Toplevel(parent)
        tk.Label(self.top, text=wraptext(text, size), width=size).grid(
            row=0, column=0, columnspan=2, padx=5)
        self.top.title("")
        self.top.protocol("WM_DELETE_WINDOW", self.cancel)
        self.top.resizable(False, False)
        self.v = tk.StringVar()
        self.v.set(default)
        self.e = tk.Entry(self.top, textvariable=self.v)
        self.e.grid(row=1, column=0, columnspan=2, padx=5, sticky=(tk.E, tk.W))
        self.e.focus_set()
        tk.Button(self.top, text=STRINGS["ok"][LANG], command=self.ok, width=6).grid(
            row=2, column=0, pady=5, padx=2, sticky=(tk.E))
        if allowcancel:
            tk.Button(self.top, text=STRINGS["cancel"][LANG], command=self.cancel, width=6).grid(
                row=2, column=1, pady=5, padx=2, sticky=(tk.W))
            self.top.bind("<Escape>", self.cancel)
        self.top.bind("<Return>", self.ok)

    def cancel(self, *args):
        self.v.set(CANCEL)
        self.top.destroy()

    def ok(self, *args):
        self.top.destroy()

    def get(self):
        return self.v.get()


class MessageDialog:
    '''
    Pop-up that show a message
    arguments : -the master window
    -(opt) text, the text shown
    -(opt) size, the width of the window in font-size
    use:
    msg = MessageDialog(master, text="some message")
    master.wait_window(msg.top)
    '''
    
    def __init__(self, parent, text=STRINGS["error0"][LANG], size=25):
        top = self.top = tk.Toplevel(parent)
        self.top.title("")
        self.top.resizable(False, False)
        tk.Label(top, text=wraptext(text, size), width=size).pack(padx=5)
        b = tk.Button(top, text=STRINGS["ok"][LANG], width=6, command=self.ok)
        b.pack(pady=5, padx=5)
        b.focus_set()
        self.top.bind("<Return>", self.ok)

    def ok(self, *args):
        self.top.destroy()


def input_tk(master, txt, allowcancel=True, default=""):
    '''
    ask the user a value with a pop-up and return it if
    no other pop-up is opened
    input : -the master window
    -the text of the question
    -(opt) default, the text already put on the entry
    -(opt) allowcancel, show the cancel button
    returns the string input or CANCEL
    '''
    global inpwin
    if not inpwin:
        inpwin = True
        entry = EntryDialog(master, text=txt, default=default,
                            allowcancel=allowcancel)
        master.wait_window(entry.top)
        inpwin = False
        return entry.get()
    else:
        return CANCEL


def message_tk(master, txt):
    '''
    show the user a given message
    input : -the master window
    -the text shown
    '''
    msg = MessageDialog(master, text=txt)
    master.wait_window(msg.top)


def inputadd_tk(master, txt, txtfalse=STRINGS["error1"][LANG], allowcancel=False):
    '''
    ask the user an address one time and give an error message if not valid
    if the address is invalid
    input : -the master window
    -the text of the question
    -(opt) txtfalse, the text of error when not valid
    -(opt) allowcancel, allow user to cancel (then can return (None, None))
    returns the same as parseadd
    '''
    cont = False
    while not cont:
        add = input_tk(master, txt, allowcancel).strip()
        if add == CANCEL and allowcancel:
            return None, None
        cont = checkadd(add)
        if not cont:
            message_tk(master, txtfalse)
    return parseadd(add)


def inputmsk_tk(master, txt, txtfalse=STRINGS["error2"][LANG], mmin=0, mmax=30, allowcancel=False):
    '''
    ask the user a mask one time and give an error message if not valid
    input : -the master window
    -the text of the question
    -(opt) txtfalse, the text of error when not valid
    -(opt) mmin, the minimum mask number
    -(opt) mmax, the maximum mask number
    -(opt) allowcancel, allow user to cancel (then can return (None, None))
    returns the same as parsemsk
    '''
    cont = False
    while not cont:
        msk = input_tk(master, txt, allowcancel).strip()
        if msk == CANCEL and allowcancel:
            return None
        cont = checkmsk(msk, mmin, mmax)
        if not cont:
            message_tk(master, txtfalse)
    return parsemsk(msk)


def inputselect_tk(master, txt, mi, ma, txtfalse=STRINGS["error3"][LANG]):
    '''
    ask the user an integer value one time and give an error message if not valid
    input : -the master window
    -the text of the question
    -the minimum value included
    -the maximum value included
    -(opt) txtfalse, the text of error when not valid
    returns the valid integer value
    '''
    cont = False
    while not cont:
        s = input_tk(master, txt).strip()
        if s == CANCEL:
            return None
        cont = True
        try:
            n = int(s)
            if not mi <= n <= ma:
                cont = False
        except ValueError:
            cont = False
        if not cont:
            message_tk(master, txtfalse)
    return n

# main functions


def init_cons():
    '''
    launch the console version of ez-net
    '''
    print("=" * 10 + "EZ-NET " + VER + "=" * 10)
    a, msk = inputadd(STRINGS["inputadd"][LANG])
    if msk is None:
        m = inputmsk(STRINGS["inputmsk"][LANG])
    else:
        m = mask(msk)
    a = netadd(a, m)
    printnet(a, m)
    print("0:" + STRINGS["txtact0"][LANG])
    print("1:" + STRINGS["txtact1"][LANG])
    print("2:" + STRINGS["txtact2"][LANG])
    rep = inputselect("> ", mi=0, ma=2)
    if rep == 0:
        k = inputselect(STRINGS["act0t"][LANG].format(
            2**(30 - masknum(m))), mi=1, ma=2**(30 - masknum(m)))
        if power2(k):
            n = int(log2(k))
        else:
            n = int(log2(k)) + 1
        d = div(a, m, n)
        nmsk = masknum(d[0][1])
    if rep == 1:
        m2 = inputmsk(STRINGS["act1t"][LANG].format(
            masknum(m)), mmin=masknum(m) + 1)
        d = div(a, m, masknum(m2) - masknum(m))
        nmsk = masknum(d[0][1])
    if rep == 2:
        k = inputselect(STRINGS["act2t"][LANG].format(formatnumber(
            2**(30 - masknum(m) + 1) - 2)), mi=1, ma=2**(30 - masknum(m) + 1) - 2) + 2
        if power2(k):
            n = int(log2(k))
        else:
            n = int(log2(k)) + 1
        d = div(a, m, 30 - n - masknum(m))
        nmsk = masknum(d[0][1])
    print(STRINGS["txtmsg0"][LANG].format(len(d), nmsk,
                                          stringadd(d[0][1]), formatnumber(nadd(d[0][1]))))
    input()
    for i in range(len(d)):
        print(str(i) + ": " + stringadd(d[i][0]) + "/" + str(nmsk) +
              " (->" + stringadd(broadadd(d[i][0], d[i][1])) + ")")


def init_tk():
    '''
    launch the window version of ez-net
    '''
    global win, li, l, txtbox, inpwin, b1, b2, b3, b4, b5, b6, bs, bo, bn
    inpwin = False
    win = tk.Tk()
    win.resizable(False, False)
    win.title("ez-net " + VER)
    l = tk.Listbox(win, height=16, width=26, activestyle='none',)
    s = tk.Scrollbar(win, orient=tk.VERTICAL, command=l.yview)
    l.configure(yscrollcommand=s.set,font=MONOSPACE)
    l.grid(row=1, column=0, columnspan=3, rowspan=10)
    l.bind("<<ListboxSelect>>", onselect)
    s.grid(row=1, column=3, rowspan=10, sticky=(tk.N, tk.S))
    frb = tk.Frame(win)
    frb.grid(row=0, column=0, sticky=(tk.N))
    bn = tk.Button(frb, text=STRINGS["newb"][LANG], command=netnew, width=7)
    bn.grid(row=0,column=0)
    bo = tk.Button(frb, text=STRINGS["openb"][LANG], command=netopen, width=7)
    bo.grid(row=0,column=1)
    bs = tk.Button(frb, text=STRINGS["saveb"][
                   LANG], command=netsave, width=7, state=tk.DISABLED)
    bs.grid(row=0,column=2) 
    txtbox = tk.Label(win, text="\n\n\n\n\n", width=30,
                      anchor=tk.W, justify=tk.LEFT)
    txtbox.grid(row=0, rowspan=2, column=4)
    b1 = tk.Button(win, text=STRINGS["act0b"][LANG],
                   command=lambda: action(0), width=25, state=tk.DISABLED)
    b1.grid(row=2, column=4, sticky=(tk.N, tk.S))
    b2 = tk.Button(win, text=STRINGS["act1b"][LANG],
                   command=lambda: action(1), width=25, state=tk.DISABLED)
    b2.grid(row=3, column=4, sticky=(tk.N, tk.S))
    b3 = tk.Button(win, text=STRINGS["act2b"][LANG],
                   command=lambda: action(2), width=25, state=tk.DISABLED)
    b3.grid(row=4, column=4, sticky=(tk.N, tk.S))
    b4 = tk.Button(win, text=STRINGS["act3b"][LANG],
                   command=lambda: action(3), width=25, state=tk.DISABLED)
    b4.grid(row=5, column=4, sticky=(tk.N, tk.S))
    b5 = tk.Button(win, text=STRINGS["act4b1"][LANG] + "/" + STRINGS["act4b2"][LANG],
                   command=lambda: action(4), width=25, state=tk.DISABLED)
    b5.grid(row=6, column=4, sticky=(tk.N, tk.S))
    b6 = tk.Button(win, text=STRINGS["act5b"][LANG],
                   command=lambda: action(5), width=25, state=tk.DISABLED)
    b6.grid(row=7, column=4, sticky=(tk.N, tk.S))
    win.bind("<Control-o>", netopen)
    win.bind("<Control-n>", netnew)
    win.mainloop()


def action(typ):
    '''
    callback for button press
    do the action on the current selection
    input : -the action to do
    '''
    global li
    i = getselection()
    if i != -1:
        if typ <= 3:
            a, m, lvl = li[i][0], li[i][1], li[i][2]
            mnum = masknum(m)
            if mnum >= 30:
                return
            d = None
            if typ == 0:  # divide n
                k = inputselect_tk(win, STRINGS["act0t"][LANG].format(
                    2**(30 - mnum)), mi=1, ma=2**(30 - mnum))
                if k is None:
                    return
                if power2(k):
                    n = int(log2(k))
                else:
                    n = int(log2(k)) + 1
                d = div(a, m, n)
                nmsk = masknum(d[0][1])
            if typ == 1:  # divide /n
                m2 = inputmsk_tk(win, STRINGS["act1t"][LANG].format(
                    mnum), mmin=mnum + 1, allowcancel=True)
                if m2 is None:
                    return
                d = div(a, m, masknum(m2) - mnum)
                nmsk = masknum(d[0][1])
            if typ == 2:  # divide size n
                k = inputselect_tk(win, STRINGS["act2t"][LANG].format(
                    formatnumber(2**(30 - mnum + 1) - 2)), mi=1, ma=2**(30 - mnum + 1) - 2)
                if k is None:
                    return
                k += 2
                if power2(k):
                    n = int(log2(k))
                else:
                    n = int(log2(k)) + 1
                d = div(a, m, 32 - n - mnum)
                nmsk = masknum(d[0][1])
            # clean
            k = i + 1
            remove = []
            while k < len(li) and li[k][2] > lvl:
                remove += [k]
                k += 1
            li = [li[k] for k in range(len(li)) if k not in remove]
            if d is not None:
                message_tk(win, STRINGS["msg0"][LANG].format(len(d)))
                li = li[:i + 1] + [[e[0], e[1], lvl + 1, True, ""]
                                   for e in d] + li[i + 1:]
        if typ == 4:
            k = i + 1
            state = not li[k][3]
            while k < len(li) and li[k][2] > li[i][2]:
                if li[k][3] or li[k][2] == li[i][2] + 1:
                    li[k][3] = state
                k += 1
        if typ == 5:
            name = input_tk(win, STRINGS["act5t"][LANG], default=li[i][4])
            if name != CANCEL:
                li[i][4] = name
        updatelist(pos=i)


def onselect(*args):
    '''
    callback for listbox selection change
    update the right description and buttons
    '''
    txtbox.config(text="\n\n\n\n\n")
    i = getselection()
    if i != -1:
        e = li[i]
        text = STRINGS["desc0"][LANG].format(stringadd(e[0]))
        text += STRINGS["desc1"][LANG].format(stringadd(e[1]), masknum(e[1]))
        text += STRINGS["desc2"][LANG].format(formatnumber(nadd(e[1])))
        text += STRINGS["desc3"][LANG].format(stringadd(broadadd(e[0], e[1])))
        if e[4] != "":
            text += STRINGS["desc4"][LANG].format(e[4])
        txtbox.config(text=text)
        if i < len(li) - 1 and li[i + 1][2] > e[2]:
            b4.config(state=tk.NORMAL)
            if li[i + 1][3]:
                b5.config(text=STRINGS["act4b2"][LANG], state=tk.NORMAL)
            else:
                b5.config(text=STRINGS["act4b1"][LANG], state=tk.NORMAL)
        else:
            b4.config(state=tk.DISABLED)
            b5.config(text=STRINGS["act4b1"][LANG] + "/" +
                      STRINGS["act4b2"][LANG], state=tk.DISABLED)
        if masknum(e[1]) >= 30:
            b1.config(state=tk.DISABLED)
            b2.config(state=tk.DISABLED)
            b3.config(state=tk.DISABLED)
        else:
            b1.config(state=tk.NORMAL)
            b2.config(state=tk.NORMAL)
            b3.config(state=tk.NORMAL)
        b6.config(state=tk.NORMAL)
    else:
        b1.config(state=tk.DISABLED)
        b2.config(state=tk.DISABLED)
        b3.config(state=tk.DISABLED)
        b4.config(state=tk.DISABLED)
        b5.config(state=tk.DISABLED)
        b6.config(state=tk.DISABLED)


def getselection():
    '''
    returns the current selection id in the complete list
    '''
    if len(l.curselection()) > 0 and 0 <= l.curselection()[0] < len(li):
        i, k = 0, 0
        while k < l.curselection()[0]:
            i += 1
            if li[i][3]:
                k += 1
        return i
    else:
        return -1


def updatelist(pos=0):
    ''''
    update the listbox list to fit as the current list
    input : -the first value to show on top of the listbox
    '''
    global li, l
    offset = l.yview()[0]
    l.delete(0, tk.END)
    maxlen = 0
    for i in range(len(li)):
        e = li[i]
        if e[3]:
            txt = ""
            if e[2] != 0:
                txt += "  " * (e[2] - 1) + " ↳"
            if i < len(li) - 1 and li[i + 1][2] > e[2] and not li[i + 1][3]:
                txt += "(+)"
            txt += stringadd(e[0]) + " /" + str(masknum(e[1]))
            if e[4] != "":
                if len(e[4]) > 25:
                    txt += "(" + e[4][:22] + "...)"
                else:
                    txt += " (" + e[4] + ")"
            if len(txt) > maxlen:
                maxlen = len(txt)
            
            l.insert(tk.END, txt)
    l.config(width=max(26,maxlen+1))
    l.select_set(pos)
    l.yview_moveto(offset)
    l.event_generate("<<ListboxSelect>>")


def netnew(*args):
    '''
    callback for the new button press or <ctrl-n>
    ask for address then mask if not given with the address
    then start a new list with these
    '''
    global li
    a, msk = inputadd_tk(win, STRINGS["inputadd"][LANG], allowcancel=True)
    if a is not None:
        if msk is None:
            m = inputmsk_tk(win, STRINGS["inputmsk"][LANG])
        else:
            m = mask(msk)
        a = netadd(a, m)
        li = [[a, m, 0, True, ""]]
        updatelist()
        bs.config(state=tk.NORMAL)
        win.bind("<Control-s>", netsave)


def netsave(*args):
    '''
    callback for the save button press or <ctrl-s>
    open a dialog to ask a location to save
    then save the list as .ezn
    '''
    global inpwin
    if not inpwin:
        inpwin = True
        try:
            with fd.asksaveasfile(defaultextension=".ezn", initialfile="network", filetypes=STRINGS["files"][LANG]) as f:
                for e in li:
                    f.write(" ".join([stringadd(e[0]), stringadd(
                        e[1]), str(e[2]), str(e[3]), str(e[4]), "\n"]))
        except AttributeError:
            pass
        inpwin = False


def netopen(*args):
    '''
    callback for the open button press or <ctrl-o>
    open a dialog to ask a .ezn file to open
    then open the file and load the list
    '''
    global li, inpwin
    if not inpwin:
        inpwin = True
        try:
            with fd.askopenfile(filetypes=STRINGS["files"][LANG]) as f:
                li = []
                for line in f:
                    cut = line.strip().split(" ", 4)
                    if len(cut) == 4:
                        cut += [""]
                    li += [[parseadd(cut[0])[0], parsemsk(cut[1]),
                            int(cut[2]), cut[3] == str(True), cut[4]]]
                updatelist()
            bs.config(state=tk.NORMAL)
            win.bind("<Control-s>", netsave)
        except AttributeError:
            pass
        inpwin = False


if __name__ == '__main__':
    if '-help' in [a.lower() for a in sys.argv]:
        print('Use "python ez-net.py" for window, add "-noGUI" for text only')
    elif not TK or '-nogui' in [a.lower() for a in sys.argv]:
        print(TK, str(sys.argv))
        init_cons()
    else:
        init_tk()
