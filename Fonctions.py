from datetime import date
import csv
import openpyxl
import re
from tkinter import *
from tkinter.messagebox import*

# Variables Globals
liste_etudiants = []
numero_etudiant = 0
nouvelle_liste_etudiants = []
impression = 0
Date = "JJ/MM/AAAA"
texte=""

# La date actuelle sous forme JJ/MM/AAAA
def Aujourdhui():
    to_day = date.today()
    aujourdhui = f"{to_day.day}/{to_day.month}/{to_day.year}"
    return aujourdhui

#Fonction pour verifier si l'utilisateur à entrer la forme int de l'id
def check_user_input(input):
    try:
        # Convert it into integer
        val = int(input)
        return 1
    except ValueError:
        try:
            # Convert it into float
            val = float(input)
            return 0
        except ValueError:
            return 0

# Construire une liste des etudiants de la classe IAGI
def Construire_Liste():
    fichier = open("iagi.txt", "r")
    liste_initiale = fichier.readlines()
    fichier.close()
    nombre_eleves = len(liste_initiale)
    for i in range(nombre_eleves):
        ligne = liste_initiale[i].split(",")
        liste_initiale[i] = ligne
        if i == 0: continue
        liste_initiale[i][-1] = int(liste_initiale[i][-1])
    liste_finale = liste_initiale
    return liste_finale


# Créer une nouvelle Séance
def Nouvelle_Seance(liste, Date):
    liste[0].insert(-1, Date)
    for i in range(1, len(liste)):
        liste[i].insert(-1, "0")


# Marquer une absence
def Etudiant_Absent(liste, numero):
    liste[numero][-2] = "1"
    liste[numero][-1] += 1


# Calcul d'Absence Totale d'un etudiant
def Absence_Totale(liste, numero):
    absence_totale = liste[numero][-1]
    return absence_totale


def Nom(liste, numero):
    nom = liste[numero][1]
    return nom


def Reconstruction_Liste_Initiale(liste):
    if liste==[]:
        liste=Construire_Liste()
    global nouvelle_liste_etudiants
    # Reconstruction_Absence_Totale
    for ligne in liste[1:-1]:
        ligne[-1] = str(ligne[-1]) + "\n"
    liste[-1][-1] = str(liste[-1][-1])

    for ligne in liste:
        new_ligne = ','.join(ligne.copy())
        nouvelle_liste_etudiants.append(new_ligne)


def Reconstruction_Fichier():
    fichier = open("iagi.txt", "w")
    fichier.writelines(nouvelle_liste_etudiants)
    fichier.close()


def Liste_Absence_Aujourdhui(Date):
    input_file='iagi.txt'
    output_file='iagi.xlsx'

    wb=openpyxl.Workbook()
    ws=wb.worksheets[0]

    with open(input_file, 'r') as data:
        reader=csv.reader(data,delimiter=',')
        for row in reader:
            ws.append(row)

            
    wb.save(output_file)
