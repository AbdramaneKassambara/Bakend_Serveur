from Config.crud import get_all_cours,get_etudiants_by_cours, insert_cours
from Config.connexion import connect_to_database_Mysql, connect_to_snowflake
#from Config.table import create_all_tables
from Config.table_mysql import create_all_tables
from data import utilisateurs
#from Back_end.Config.crud import insert_cours,insert_matiere
from Class.utilisateurs import Etudiant, Professeur, Utilisateur,Tuteur,ChefDepartement
import random
#cursor = connect_to_snowflake()
connection,cursor = connect_to_database_Mysql()
create_all_tables(cursor)
# insert_cours(cursor, "Mathématiques")
# insert_cours(cursor, "Intelligence Artificiel")
# insert_cours(cursor, "Physique")
# insert_cours(cursor, "Chimie")
# insert_cours(cursor, "Mobile")
# insert_cours(cursor, "Histoire")
# insert_cours(cursor, "Biologie")
# insert_cours(cursor, "Géographie")
# insert_cours(cursor, "Économie")
# insert_cours(cursor, "Philosophie")
# insert_cours(cursor, "Francais")
# insert_cours(cursor, "Psychologie")
# insert_cours(cursor, "Sociologie")
# insert_cours(cursor, "Médecine")
# insert_cours(cursor, "Anglais")
# insert_cours(cursor,"RCW")
# insert_cours(cursor,"L.Programmation")

#isser user 
for user in utilisateurs:
    user.create(cursor)



#print(f"{'Cours':_^50}")
# cours = get_all_cours(cursor)
# #print(cours)
# list_id_cours = []
# for cour in cours:
#    list_id_cours.append(cour[0])
#print(list_id_cours)
# print(f"{'Etudiant':_^50}")
# etudiants = Utilisateur.recuperer_utilisateurs_par_role(cursor, "Etudiant")
# for etudiant in etudiants:
#     id_utilisateur = etudiant[0]
#     nom_utilisateur = etudiant[1]
#     mdp = etudiant[2]
#     role = etudiant[3]
#     nom_com = etudiant[4]
#     email = etudiant[5]
#     genre = etudiant[6]
#     cours_assignes = random.sample(list_id_cours, min(8, len(list_id_cours)))
#     chaque_Etudiant  = Etudiant(nom_utilisateur,mdp,nom_com,email,genre,cours_inscrits=cours_assignes)
#     #print(chaque_Etudiant.get_genre())
#     #print(chaque_Etudiant.get_cours_inscrits())
#     chaque_Etudiant.create(cursor,id_utilisateur)
# print(f"{'Professeur':_^50}")
# professeurs = Utilisateur.recuperer_utilisateurs_par_role(cursor,"Professeur")
# for professeur in professeurs:
#     #print(professeur)
#     id_utilisateur = professeur[0]
#     nom_utilisateur = professeur[1]
#     mdp = professeur[2]
#     role = professeur[3]
#     nom_com = professeur[4]
#     email = professeur[5]
#     genre = professeur[6]
#     cours_assignes = random.sample(list_id_cours, min(8, len(list_id_cours)))
    #print(cours_assignes)
   # print(cours_assignes)
    #chaque_professeur  = Professeur(nom_utilisateur,mdp,nom_utilisateur,email,genre,cours_enseignes=cours_assignes)
    # print(chaque_Etudiant.get_nom_utilisateur())
    # print(chaque_Etudiant.get_cours_inscrits())
    # chaque_professeur.create(cursor,id_utilisateur)
# seteve = Professeur("Seteve","Seteve_mdp")
# seteves = seteve.get_cours_prof(cursor,"16")
# # Si vous souhaitez simplement afficher les noms des cours
# # for cours in seteves:
# #     print("Cours enseignés par Steve : ", cours)
# fode = Professeur("Fode","Fode_mdp")
# fode = fode.get_cours_prof(cursor,"33")
    
# print(f"{'Tuteur':_^50}")
# tuteurs = Utilisateur.recuperer_utilisateurs_par_role(cursor,"Tuteur")
# def selection_disponibilites(disponibilites, nombre_choix=1):
#     if not disponibilites or nombre_choix <= 0:
#         return [] 
#     disponibilites_aleatoires = random.sample(disponibilites, min(nombre_choix, len(disponibilites)))
#     return disponibilites_aleatoires
# disponibilites = [
#     {"jour": "Lundi", "heure_debut": "09:00", "heure_fin": "12:00"},
#     {"jour": "Mardi", "heure_debut": "14:00", "heure_fin": "17:00"},
#     {"jour": "Mercredi", "heure_debut": "10:30", "heure_fin": "13:30"},
#     {"jour": "Jeudi", "heure_debut":"10:30","heure_fin": "13:30"},
#     {"jour": "Vendredi", "heure_debut":"10:30","heure_fin": "13:30"},
#     {"jour":"Samedi","heure_debut":"11:30","heure_fin": "13:30"},
#     {"jour":"Dimache","heure_debut":"16:30","heure_fin": "19:30"},
# ]
# for tuteur in tuteurs:
#         #print(professeur)
#     id_utilisateur = tuteur[0]
#     nom_utilisateur = tuteur[1]
#     mdp = tuteur[2]
#     role = tuteur[3]
#     nom_com = tuteur[4]
#     email = tuteur[5]
#     genre =  tuteur[6]
#     cours_assignes = random.sample(list_id_cours, min(8, len(list_id_cours)))
#     nombre_choix = random.choice([1, 2, 3, 4,7])
#     disponibilites_selectionnees = selection_disponibilites(disponibilites, nombre_choix)
#     chaque_tuteur  = Tuteur(nom_utilisateur,mdp,nom_utilisateur,email,genre,cours_tutorat=cours_assignes,disponibilites=disponibilites_selectionnees)
#     chaque_tuteur.create(cursor,id_utilisateur)
# #print(tuteurs)
#print(f"{'ChefDepartement':_^50}")
chefs = Utilisateur.recuperer_utilisateurs_par_role(cursor,"ChefDepartement")
for chef in chefs:
    id_utilisateur = chef[0]
    nom_utilisateur = chef[1]
    mdp = chef[2]
    role = chef[3]
    nom_com = chef[4]
    email = chef[5]
    genre =  chef[6]
    chaque_chef  = ChefDepartement(nom_utilisateur,mdp,nom_com,email,"depart +223",genre)
    chaque_chef.create(cursor,id_utilisateur)

# print(f"{'Etudiant dans le Cours ':_^50}")
# cours = get_all_cours(cursor)
# for cours_nom in cours:
#     print(f"Étudiants dans le cours '{cours_nom}':")
#     etudiants = get_etudiants_by_cours(cursor, cours_nom)
#     for etudiant in etudiants:
#         print(f"ID de l'étudiant : {etudiant[0]}, Nom de l'étudiant : {etudiant[1]}")
#     print("\n")