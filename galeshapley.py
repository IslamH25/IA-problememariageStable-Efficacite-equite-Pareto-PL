import random
import time

# Commandes utiles:
    # n=int(s) transforme la chaine s en entier.
    # s=str(n) l'inverse
    # Quelques methodes sur les listes:
    # l.append(t) ajoute t a la fin de la liste l
    # l.index(t) renvoie la position de t dans l (s'assurer que t est dans l)
    # for s in l: s vaut successivement chacun des elements de l (pas les indices, les elements)


def lecturePrefSpe(s):# Definition d'une fonction, avec un parametre (s). Ne pas oublier les ":"
    m=[]
    monFichier = open(s, "r") # Ouverture en lecture. Indentation par rapport a la ligne d'avant (<-> bloc).
    contenu = monFichier.readlines() # Contenu contient une liste de chainces de caracteres, chaque chaine correspond a une ligne       
    monFichier.close() #Fermeture du fichier
    for i in range(1,len(contenu)):
        m.append(contenu[i].split())
    
    for i in range(len(m)):
        for j in range(len(m[i])):
            if(i==0 and j==0): 
                continue
            if(j==1 and i!=0):
                continue
            m[i][j]=int(m[i][j])
    
    return m

def lecturePrefEtu(s):# Definition d'une fonction, avec un parametre (s). Ne pas oublier les ":"
    m=[]
    monFichier = open(s, "r") # Ouverture en lecture. Indentation par rapport a la ligne d'avant (<-> bloc).
    contenu = monFichier.readlines() # Contenu contient une liste de chainces de caracteres, chaque chaine correspond a une ligne       
    monFichier.close() #Fermeture du fichier
    for i in range(1,len(contenu)):
        m.append(contenu[i].split())
    
    for i in range(len(m)):
        for j in range(len(m[i])):
            if(j==1):
                continue
            m[i][j]=int(m[i][j])
    
    return m


def affichageMatrice(m):
    for i in range(len(m)):
        print(m[i])
    print("\n")

def GSHoptialEtu(numEtu,Etu_pref,Master_pref,Mastercap):
    EtuLibre=set(range(numEtu))
    match={}
    while EtuLibre:
        Etu=EtuLibre.pop()
        for master in Etu_pref[Etu]:
            if Mastercap[master]>0:
                Mastercap[master]-=1
                match[Etu]=master
                break
            else:
                l=[]
                for cle,valeur in match.items():
                    if(valeur==master):
                        l.append(Master_pref[master].index(cle))
                s=max(l)
                a=Master_pref[master][s]
                if Master_pref[master].index(Etu) < s:
                    del match[a]
                    EtuLibre.add(Master_pref[master][s])
                    match[Etu]=master
                    break
    return match


def GSHopitalMaster(numMaster,Etu_pref,Master_pref,Master_cap):
    unmatched_master = set(range(numMaster))
    match = {}
    while unmatched_master:
        master = unmatched_master.pop()
        while(Master_cap[master]>0):
            for student in Master_pref[master]:
                if student not in match:
                    match[student] = master
                    Master_cap[master] -= 1
                    break
                else:
                    current_match = match[student]
                    if Etu_pref[student].index(master) < Etu_pref[student].index(current_match):
                        unmatched_master.add(current_match)
                        Master_cap[current_match]+=1
                        match[student] = master
                        Master_cap[master] -= 1
                        break
    return match

def PaireInstable(Etu_pref,Master_pref,matchs):
    PI=[]
    for key1,value1 in matchs.items():
        for key2,value2 in matchs.items():
            if(key1==key2):
                continue
            a = False; b = False
            if(Etu_pref[key1].index(value1)>Etu_pref[key1].index(value2)):
                a=True
            if(Master_pref[value2].index(key1)<Master_pref[value2].index(key2)):
                b=True
            if(a and b):
                PI.append((key1,value2))
    return PI

def Etu_Pref_Aleatoire(n):

    Etu_Pref = []
    for i in range (0,n):
        s='Etu'+str(i)
        Etu_Pref.append([i] +[s]+ random.sample(range(0,9),9))

    return Etu_Pref

def Master_Pref_Aleatoire(n):

    Master_Pref = [['Cap']]

    if n > 9 : 
        for i in range(0,9):
            Master_Pref[0].append(n//9)
    else :
        for i in range(0,9):
            Master_Pref[0].append(1)

    siu = sum(Master_Pref[0][1:])
    if(siu<n):
        for i in range(1,10):
            Master_Pref[0][i] = Master_Pref[0][i] + 1
            siu = siu + 1
            if siu == n :
                break 

    masterName = ['ANDROIDE','BIM','DAC','IMA','RES','SAR','SESI','SFPN','STL']

    for i in range (0,9):
        Master_Pref.append([i] +[masterName[i]]+ random.sample(range(0,n),n))

    return Master_Pref

def Temps_Calcul(n):
    m=Master_Pref_Aleatoire(n)
    e=Etu_Pref_Aleatoire(n)
    Master_pref=[]
    Etu_pref=[]
    numEtu=len(e[2])-2
    for i in range(1,len(m)):
        Master_pref.append(m[i][2::])
    for i in range(len(e)):
        Etu_pref.append(e[i][2::])

    Master_cap=m[0][1::]
    GSHoptialEtu(numEtu,Etu_pref,Master_pref,Master_cap)
    t2=time.process_time()
    return t2

m1=lecturePrefSpe("PrefSpe.txt")
m2=lecturePrefEtu("PrefEtu.txt")
affichageMatrice(m1)
affichageMatrice(m2)

numEtu=len(m1[2])-2
numMaster=len(m2[2])-2
Etu_pref=[]
Master_pref=[]
for i in range(1,len(m1)):
    Master_pref.append(m1[i][2::])
for i in range(len(m2)):
    Etu_pref.append(m2[i][2::])

Master_cap=m1[0][1::]

n = 11

affichageMatrice(Etu_Pref_Aleatoire(n))
affichageMatrice(Master_Pref_Aleatoire(n))

#print(PaireInstable(Etu_pref,Master_pref,GSHoptialEtu(numEtu,Etu_pref,Master_pref,Master_cap)))

#print(GSHoptialEtu(numEtu,Etu_pref,Master_pref,Master_cap))
Master_cap=m1[0][1::]
#print(GSHopitalMaster(numMaster,Etu_pref,Master_pref,Master_cap))
n=200
while(n<2000):
    print(Temps_Calcul(n))
    n+=200


def createFichierLPEquite(nomFichier, Etu_pref, Master_pref, k, n, m):
    monFichier = open(nomFichier, "w")
    
    # Écrire la fonction objectif
    monFichier.write("Maximize\n")
    monFichier.write("z\n")
    monFichier.write("st\n")

    #Contraintes de préférences sur les Masters
    for i in range(m):
        monFichier.write("c"+str(i)+":")
        for column in range(k):
            monFichier.write(str(m-column+1)+ "x" + str(Master_pref[i][column]) + "_" + str(i) + " ")
            if column != k - 1:
                monFichier.write(" + ")
        monFichier.write("<= z")
        monFichier.write("\n")

    #Contraintes de préférences sur les Etudiants
    for i in range(n):
        monFichier.write("c"+str(i+m)+":")
        for column in range(k):
            monFichier.write(str(m-column+1)+ "x" +str(i) + "_" + str(Etu_pref[i][column]) + " " )
            if column != k - 1:
                monFichier.write(" + ")
        monFichier.write("<= z")
        monFichier.write("\n")

    #Contraintes sur le mariage côté Etudiant
    for i in range(n):
        monFichier.write("c"+str(i+m+n)+": ")
        for j in range(m):
            monFichier.write("x"+str(i)+ "_" +str(j))
            if j != m - 1:
                monFichier.write(" + ")
        monFichier.write("<= 1")
        monFichier.write("\n")

    #Contraintes sur le mariage côté Maste
    for i in range(m):
        monFichier.write("c"+str(i+m+n+n)+": ")
        for j in range(n):
            monFichier.write("x"+str(j)+ "_" +str(i))
            if j != n - 1:
                monFichier.write(" + ")
        monFichier.write("<= 1")
        monFichier.write("\n")
        
    # Écrire les contraintes de la binarité
    monFichier.write("Binary\n")
    for i in range(n):
        for j in range(m):
            monFichier.write("x" + str(i) + "_" + str(j) + " ")
            monFichier.write("\n")
    
    # Terminer le fichier
    monFichier.write("end\n")
    monFichier.close()



# 0	ANDROIDE	7	9	5	4	3	1	0	10	6	8	2
# 1	BIM	7	5	9	4	3	1	0	10	8	6	2
# 2	DAC	3	9	5	4	7	6	1	0	10	8	2
# 3	IMA	7	9	5	4	3	1	0	6	10	8	2
# 4	RES	10	3	0	4	5	6	7	8	9	1	2
# 5	SAR	1	0	3	4	5	6	7	2	9	10	8
# 6	SESI	0	1	3	4	5	6	7	2	8	10	9
# 7	SFPN	7	6	9	5	4	3	1	0	10	8	2
# 8	STL	1	0	3	4	5	6	7	2	9	10	8


createFichierLPEquite("test4.lp",Etu_pref,Master_pref,4,numEtu,numMaster)
    