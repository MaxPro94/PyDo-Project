import mysql.connector
from datetime import datetime
from tkinter import *


config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'to_do_list'
}

mydb = mysql.connector.connect(**config)

# Creation de la fenetre:
window = Tk()

# Personnalisation de cette fenetre:
window.title("To-do-list")
window.geometry("720x480")
window.config(background='lemonchiffon')

# Creation d'un cadre:
frame = Frame(window, bg='lemonchiffon')

# Creation d'un titre principal:
label_title = Label(window, text="Bienvenue sur la TO-DO-LIST", font=("Roboto", 20), bg = 'lemonchiffon', fg ='#03a9f4')
label_title.pack()

def ajouter_une_tache():
    # Creation d'un curseur pour la BDD:
    mycursor = mydb.cursor(dictionary=True)

    # Demander le nom de la tâche à l'utilisateur:
    label_nom = Label(window, text="Entrez le nom de la tache:", bg="lemonchiffon", fg='#03a9f4')
    label_nom.pack()
    nom_tache = StringVar()
    entrer_nom_tache = Entry(window, textvariable=nom_tache, width=30)
    entrer_nom_tache.pack()

    # Demander la date objectif pour la tache créer: 
    label_date_obj = Label(window, text="Entrez la date objéctif au format 'YYYY-MM-DD HH:mm:ss':", bg="lemonchiffon", fg='#03a9f4')
    label_date_obj.pack()
    date_obje = Entry(window,textvariable=StringVar, width=30)
    date_obje.pack()

    # Demander le statut de la tâche:
    label_statut = Label(window, text= "1: En cours ; 2: Terminé ; 3: En attente", fg='#03a9f4')
    label_statut.pack()
    label = Label(window, text="Entrez le statut de votre tache:")
    id_statut = Entry(window, textvariable=StringVar, width=30)
    id_statut.pack()

    # Definir la fonction pour executer la requete SQL lors du clic sur le bouton "Ajouter":
    def execute_query_ajout_tache():
        nom_tache_value = nom_tache.get()
        date_obje_value = date_obje.get()
        id_statut_value = id_statut.get()
        tache_query = "INSERT INTO TACHES (nom_tache, date_creation, date_objectif, Id_STATUT) VALUES (%s, NOW(), %s, %s)"
        tache_values = (nom_tache_value, date_obje_value, id_statut_value)
        mycursor.execute(tache_query, tache_values)

    ajouter_tache=Button(window, text="Ajouter", command=execute_query_ajout_tache)
    ajouter_tache.pack()

result_text = Text(window, wrap="word", width=40, height=15)
result_text.pack(expand=True, fill="both")
scrollbar = Scrollbar(window, command=result_text.yview)
scrollbar.pack(side="right", fill="y")
result_text.config(yscrollcommand=scrollbar.set)

def afficher_taches():
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT TACHES.*, STATUT.statut FROM TACHES LEFT JOIN STATUT ON TACHES.Id_STATUT = STATUT.Id_STATUT")
    taches = mycursor.fetchall()

    if not taches:
        result_text.config(state="normal")
        result_text.delete(1.0, "end")
        result_text.insert("end", "La liste de tâches est vide.")
        result_text.config(state="disabled")
    else:
        result_text.config(state="normal")
        result_text.delete(1.0, "end")
        result_text.insert("end", "Liste des taches:   ")
        for tache in taches:
             # Récupérer le statut à partir du dictionnaire de correspondance
            statut_text = tache.get('statut', 'Statut inconnu')
            result_text.insert("end",
                            f"ID de la tache : {tache['Id_TACHES']}\n"
                            f"Nom de la tâche: {tache['nom_tache']}\n"
                            f"Date de création: {tache['date_creation']}\n"
                            f"Date objectif: {tache['date_objectif']}\n"
                            f"Date de réalisation: {tache['date_realisation']}\n"
                            f"Statut: {statut_text}\n"
                            f"{'*' * 30}\n"
                            )
        result_text.config(state="disabled")

def modification_tache():
    modif_nom_tache_bouton = Button(window, text="Modifier le nom", command=modif_nom_tache(mydb, window))
    modif_nom_tache_bouton.pack(side="bottom", padx=5, pady=10)
    modif_statut_tache_bouton = Button(window, text="Modifier le nom")
    modif_statut_tache_bouton.pack(side="bottom", padx=5, pady=10)
    modif_date_obje_tache_bouton = Button(window, text="Modifier la date objéctif")
    modif_date_obje_tache_bouton.pack(side="bottom", padx=5, pady=10)
    modif_date_real_tache_bouton = Button(window, text="Modifier la date de réalisation")
    modif_date_real_tache_bouton.pack(side="bottom", padx=5, pady=10)

def modif_nom_tache(mydb, window):
     # Création d'un curseur pour exécuter des requêtes SQL
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM taches")
    taches_liste = mycursor.fetchall()

    # Création d'une Listbox pour afficher les tâches
    listbox = Tk.Listbox(window)
    listbox.pack(pady=10)

    # Ajout des tâches à la Listbox
    for tache in taches_liste:
        listbox.insert(Tk.END, tache['nom_tache'])  # Assurez-vous d'ajuster la clé selon la structure de votre table
    
    # mycursor = mydb.cursor(dictionary=True)
    # id_select = input("Veuillez entrez l'ID de la tache a modifier :")
    # new_nom = input("Veuillez entrer le nouveau nom de la tache :")
    # update_query = "UPDATE taches SET nom_tache = %s WHERE Id_TACHES = %s"
    # update_query_data = (id_select, new_nom)
    # mycursor.execute(update_query, update_query_data)
    # mydb.commit()


    
creation_tache_button = Button(window, text="Créé une tâche", command=ajouter_une_tache)
creation_tache_button.pack(side="left", padx=5, pady=5)
actualiser_button = Button(window, text="Actualiser les tâches", command=afficher_taches)
actualiser_button.pack(side="left", padx=5, pady=5)
modification_tache_button = Button(window, text="Modifier une tâche", command=modification_tache)
modification_tache_button.pack(side="left", padx=5, pady=5)
supprimer_tache_button = Button(window, text="Supprimer une tâche")
supprimer_tache_button.pack(side="left", padx=5, pady=5)

# Fonction qui s'ouvre a l'ouverture de Tkinter
afficher_taches()

# Afficher la fenetre "window":
window.mainloop()