from Fonctions import *
from tkinter import *

#La Fenêtre
window =Tk()
window.title("Abscence IAGI-1")
window.geometry("500x300")
window.iconbitmap("ico.ico")
window.config(background="#CACAFF")
wdt=210
hgt=95
picture = PhotoImage(file ="Logo_ensam.png").zoom(1).subsample(2)
canvas = Canvas( width = wdt, height = hgt,bg="#CACAFF" , highlightthickness = 0)
canvas.create_image(wdt/2, hgt/2, image = picture)
canvas.place(x=140,y=0)

#Bouton Saisir de Date de Séance
saisir=StringVar()
saisir.set(Aujourdhui())
label_date=Label(window,text='Entrer la date de la séance :',font=("courrier",12),bg="#CACAFF",fg='black')
label_date.place(x=60,y=150)
saisie=Entry(textvariable=saisir,justify=CENTER)
saisie.place(x=280,y=152)

def Saisir_Date_Seance():
    date_saisie=saisir.get()
    expression = re.compile("([0-3]?[0-9]/[0-1]?[0-9]/[0-2]?[0-9]?[0-9][0-9])")
    res = expression.findall(date_saisie)
    if res == []:
        showerror(title="error", message="la forme de la date n'est pas valide: dd/mm/yyyy",icon='error')
    else:
        global Date
        Date=date_saisie
        global liste_etudiants
        liste_etudiants=Construire_Liste()
        Nouvelle_Seance(liste_etudiants,date_saisie)
        #Destroy
        saisie.place_forget()
        btn.place_forget()
        label_date.place_forget()
        Rest()


btn=Button(window, width=10,height=2,text="Entrer",command=Saisir_Date_Seance)
btn.place(x=215,y=210)

def Rest():
    #Bouton Valider
    num=StringVar()
    num.set(1)
    label_id = Label(window, text='Entrer l\'id de l\'étudiant :', font=("courrier", 11), bg="#CACAFF", fg='black')
    label_id.place(x=25, y=150)
    saisie_id=Entry(textvariable=num,justify=CENTER)
    saisie_id.place(x=220,y=152)

    def Saisir_Absence():
        numero_test = num.get()
        i = check_user_input(numero_test)
        if (i == 0):
            showerror(title="error", message="La forme de l'id n'est pas valide ",icon='error')
        else:
            numero = int(numero_test)
            if (numero <= 0 or numero >= 11):
                showerror(title="error", message="Le numéro d'id ne convient à aucun étudiant de la liste ",icon='error')
            else:
                result = askquestion("Vérification", "Etes-vous sure de marquer l'abscence?", icon='warning')
                if result == 'yes':
                    global liste_etudiants
                    global numero_etudiant
                    numero_etudiant = numero
                    Etudiant_Absent(liste_etudiants, numero)
                    showinfo("Validé", "L'abscence est marquée")

                    #Destroy et ajouter nv bouton pour le totale et impression
                    label_id.place_forget()
                    saisie_id.place_forget()
                    btn_id.place_forget()
                    Rest2()
                else:
                    showinfo("Echec","L'abscence n'est pas marquée")

    btn_id=Button(window, height=1,text="Valider" ,width=10,command=Saisir_Absence)
    btn_id.place(x=380,y=152)

    def Rest2():
        #Bouton Afficher Totale
        def Afficher_Totale():
            absence_totale=Absence_Totale(liste_etudiants,numero_etudiant)
            nom=Nom(liste_etudiants,numero_etudiant)
            global texte
            texte=Label(window,bg='red', text=f"Absence Totale de ({numero_etudiant}) {nom} est: {absence_totale}")
            texte.place(x=25,y=160)

        label_total = Label(window, text='Le nombre totale d\'abscence de cet étudiant:', font=("courrier", 11), bg="#CACAFF", fg='black')
        label_total.place(x=25, y=120)
        btn_totale=Button(window, height=1,width=12,text="Afficher Totale",command=Afficher_Totale)
        btn_totale.place(x=350,y=120)

        #Pour marqué l'abscence d'un autre étudiant
        def ajouter():
            if texte!="":
                texte.place_forget()
            label_total.place_forget()
            btn_totale.place_forget()
            btn_Add.place_forget()
            label_Ajou.place_forget()
            btn_impression.place_forget()
            label_impression.place_forget()
            Rest() #fait appel à la fonction rest pour afficher le bouton de validation d'abscence

        label_Ajou=Label(window, text='Marquer l\'abscence d\'un autre étudiant:', font=("courrier", 11), bg="#CACAFF", fg='black')
        label_Ajou.place(x=25,y=200)
        btn_Add= Button(window, height=1, width=10, text="Ajouter", command=ajouter)
        btn_Add.place(x=350, y=200)


        #Bouton D'impression du fichier en EXCEL
        def Impression_Liste():
            Reconstruction_Liste_Initiale(liste_etudiants)
            Reconstruction_Fichier()
            global impression
            impression=1
            Liste_Absence_Aujourdhui(Date)
            window.destroy()

        label_impression = Label(window, text='Imprimer la liste dans un fichier excel:', font=("courrier", 11),     bg="#CACAFF", fg='black')
        label_impression.place(x=25, y=250)
        btn_impression=Button(window, height=1,text="Imprimer la liste",command=Impression_Liste)
        btn_impression.place(x=340,y=250)

#Afficher l'interface

window.mainloop()

if impression==0:
    Reconstruction_Liste_Initiale(liste_etudiants)
    Reconstruction_Fichier()
