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

# Dictionnaire de correspondance des numéros de statut aux chaînes de caractères
statut_mapping = {
    1: 'En cours',
    2: 'Terminé',
    3: 'En attente'
}

def ajouter_une_tache():
    mycursor = mydb.cursor(dictionary=True)
    nom_tache = input("Nom de la tache a inserer: ")
    date_obje = input("Entrez la date objéctif au format 'YYYY-MM-DD HH:mm:ss': ")
    tache_query =("INSERT INTO TACHES (nom_tache, date_creation, date_objectif) VALUES (%s, NOW(), %s)")
    tache_values = (nom_tache, date_obje)
    mycursor.execute(tache_query, tache_values)
    mycursor.execute("SELECT LAST_INSERT_ID() as last_id")
    last_tache_id = mycursor.fetchone()['last_id']
    print("Les differents statuts :")
    print("1: En cours")
    print("2: Terminé")
    print("3: En attente")
    id_statut = input("Entrez l'identifiant du statut pour la nouvelle tâche : ")
    statut_query = "UPDATE TACHES SET Id_STATUT = %s WHERE Id_TACHES = %s"
    statut_values = (id_statut, last_tache_id)
    mycursor.execute(statut_query, statut_values)
    mydb.commit()
    print("L'ajout a bien etais realiser !")

def changement_statut():
    mycursor = mydb.cursor(dictionary=True)

    # Demandez à l'utilisateur d'entrer l'ID de la tâche
    choix_tache_utilisateur = input("Entrez l'ID de la tâche à modifier : ")

    # Demandez à l'utilisateur d'entrer le nouveau statut
    choix_statut = input("Entrez le nouveau statut pour cette tâche : ")

    # Exécutez la requête SQL pour mettre à jour le statut de la tâche
    update_query = "UPDATE TACHES SET Id_STATUT = %s WHERE Id_TACHES = %s"
    update_values = (choix_statut, choix_tache_utilisateur)

    mycursor.execute(update_query, update_values)
    mydb.commit()

    print(f"Le statut de la tâche {choix_tache_utilisateur} a bien été mis à jour !")

def menu_modif():
    print("*" * 30)
    print("Que voulez vous modifiez ?")
    print("-" * 30)
    print("Tapez 1 pour modifier le Nom d'une tache.")
    print("-" * 30)
    print("Tapez 2 pour modifier la date objectif.")
    print("-" * 30)
    print("Tapez 3 pour modifier la date de realisation.")
    print("-" * 30)
    print("Tapez 4 pour modifier le statut.")
    print("-" * 30)

def modif_nom():
    mycursor = mydb.cursor(dictionary=True)
    id_a_modif = int(input("Quel est l'ID de la tache a modifier ?: "))
    modif = str(input(f"Quel nom voulez vous lui attribuer ?: "))
    nom_query = "UPDATE taches SET nom_tache = %s WHERE Id_TACHES = %s"
    nom_values = (modif, id_a_modif)
    mycursor.execute(nom_query, nom_values)
    mydb.commit()

    print(f"La modification de la tache portant L'ID: {id_a_modif} a bien etais effectuée !")

def modif_date_ojectif():
    mycursor = mydb.cursor(dictionary=True)
    id_a_modif = int(input("Quel est l'ID de la tache a modifier ?: "))
    date_a_update = input("Entrez la date objéctif au format 'YYYY-MM-DD HH:mm:ss': ")
    date_obj_query = "UPDATE taches SET date_objectif = %s WHERE Id_TACHES = %s"
    date_values = (date_a_update, id_a_modif)
    mycursor.execute(date_obj_query, date_values)
    mydb.commit()
    
    print(f"La date objectif de la tache portant l'ID : {id_a_modif} à bien etais modifier !")

def modif_date_realisation():
    mycursor = mydb.cursor(dictionary=True)
    realisation_now = input(f"Si la date de realisation est aujourd'hui taper 1, sinon tapez 2:")

    if realisation_now == "1":
        afficher_taches(),
        id_a_modif = int(input("Quel est l'ID de la tache a modifier ?: "))
        date_rea_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        date_rea_query = "UPDATE taches SET date_realisation = %s WHERE Id_TACHES = %s"
        date_rea_values = (date_rea_now, id_a_modif)
        mycursor.execute(date_rea_query, date_rea_values)
        mydb.commit()

        print(f"La date de réalisation de la tâche portant l'ID : {id_a_modif} a bien été modifiée a la date du jour !")
    
    else:
        id_a_modif = int(input("Quel est l'ID de la tache a modifier ?: "))
        date_a_update = input("Entrez la date objéctif au format 'YYYY-MM-DD HH:mm:ss': ")
        date_rea_query = "UPDATE taches SET date_realisation = %s WHERE Id_TACHES = %s"
        date_values = (date_a_update, id_a_modif)
        mycursor.execute(date_rea_query, date_values)
        mydb.commit()
    
        print(f"La date de realisation de la tache portant l'ID : {id_a_modif} à bien etais modifier !")

def choix_statut():
    global choix_statut
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM statut")
    statuts = mycursor.fetchall()

    for statut in statuts:
        print(f"{statut['Id_STATUT']}, {statut['statut']}")

    choix_statut = input(f"Quel est votre choix de statut ?:")

def affichage_statut():
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM statut")
    statuts = mycursor.fetchall()

    for statut in statuts:
        print(f"{statut['Id_STATUT']}: {statut['statut']}")

def supprimer_tache():
    mycursor = mydb.cursor(dictionary=True)
    tache_a_supprimer = int(input("Entre l'ID de la tache a supprimer:"))
    delete_query = ("DELETE FROM taches WHERE id_TACHES = %s")
    delete_values = (tache_a_supprimer,)
    mycursor.execute(delete_query, delete_values)
    mydb.commit()
    print(f"La tache portant l'ID: {tache_a_supprimer} a bien etais supprimée !")

def choix_taches():
    global choix_tache_utilisateur
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT TACHES.*, STATUT.statut FROM TACHES LEFT JOIN STATUT ON TACHES.Id_STATUT = STATUT.Id_STATUT")
    taches = mycursor.fetchall()

    if not taches:
        print("La liste de tâches est vide.")
    else:
        print("Voici la To Do List :")
        for tache in taches:
             # Récupérer le statut à partir du dictionnaire de correspondance
            statut = statut_mapping.get(tache['Id_STATUT'], 'Statut inconnu')

            print("*" * 30)
            print(f"ID de la tache : {tache['Id_TACHES']}")
            print(f"Nom de la tâche: {tache['nom_tache']}")
            print(f"Date de création: {tache['date_creation']}")
            print(f"Date objectif: {tache['date_objectif']}")
            print(f"Date de réalisation: {tache['date_realisation']}")
            print(f"Statut: {statut}")
            print("-" * 30)
    
    choix_tache_utilisateur = input(f"Quel est le choix de la tache a modifier ?:")

def afficher_taches():
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT TACHES.*, STATUT.statut FROM TACHES LEFT JOIN STATUT ON TACHES.Id_STATUT = STATUT.Id_STATUT")
    taches = mycursor.fetchall()

    if not taches:
        print("La liste de tâches est vide.")
    else:
        print("Voici la To Do List :")
        for tache in taches:
             # Récupérer le statut à partir du dictionnaire de correspondance
            statut = statut_mapping.get(tache['Id_STATUT'], 'Statut inconnu')

            print("*" * 30)
            print(f"ID de la tache : {tache['Id_TACHES']}")
            print(f"Nom de la tâche: {tache['nom_tache']}")
            print(f"Date de création: {tache['date_creation']}")
            print(f"Date objectif: {tache['date_objectif']}")
            print(f"Date de réalisation: {tache['date_realisation']}")
            print(f"Statut: {statut}")
            print("-" * 30)

def afficher_menu():
    print("*" * 30)
    print("Bonjour est bienvenue sur TO DO BENG, BANG BANG")
    print("-" * 30)
    print("Tapez 1 pour ajouter une nouvelle tache")
    print("-" * 30)
    print("Tapez 2 pour modifier le statut d'une tache")
    print("-" * 30)
    print("Tapez 3 pour supprimer une tache")
    print("-" * 30)
    print("Tapez 4 pour modifier une tache")
    print("-" * 30)
    print("Tapez 5 pour afficher la liste des taches")


while True:
    afficher_menu()
    print("*" * 30)
    choix = input(f"Veuillez choisir l'option desirez: ")

    if choix == "5":
        afficher_taches()

    elif choix == "1":
        ajouter_une_tache()

    elif choix == "2":
        afficher_taches(),
        affichage_statut(),
        changement_statut()

    elif choix == "3":
        afficher_taches(),
        supprimer_tache()

    elif choix == "4":
        menu_modif()
        choix_modif = int(input(f"Que voulez vous modifiez ?: "))

        if choix_modif == 1:
            afficher_taches(),
            modif_nom()

        elif choix_modif == 2: 
            afficher_taches(),
            modif_date_ojectif()

        elif choix_modif == 3:
            afficher_taches(),
            modif_date_realisation()

        elif choix_modif == 4:
            afficher_taches(),
            affichage_statut(),
            changement_statut()

        else:
            print("Commande inconnue veuillez reessayez.")
        
    else:
        print("Commande inconnue, veuillez reessayez.")






    