
from datetime import datetime


def cours_existe(cursor, nom_cours):
    cursor.execute("SELECT COUNT(*) FROM Cours WHERE nom_cours = %s", (nom_cours,))
    count = cursor.fetchone()[0]
    return count > 0
def matiere_existe(cursor, nom_matiere):
    cursor.execute("SELECT COUNT(*) FROM Matieres WHERE nom_matiere = %s", (nom_matiere,))
    count = cursor.fetchone()[0]
    return count > 0
def modifier_utilisateur_par_id(cursor, id_utilisateur, nom_complet=None, email=None, password=None, nom_utilisateur=None):
    cursor.execute("""UPDATE Utilisateurs
                      SET nom_complet = %s, email = %s, mot_de_passe = %s, nom_utilisateur = %s
                      WHERE utilisateur_id = %s;""",
                   (nom_complet, email, password, nom_utilisateur, id_utilisateur))
    if cursor.rowcount > 0:
        cursor.connection.commit()
        return True
    else:
        return False
def get_utilisateur_par_id(cursor, id_utilisateur):
    """
    Récupère un utilisateur par son ID dans la base de données.
    Arguments :
        cursor : Cursor de la base de données.
        id_utilisateur (int) : L'ID de l'utilisateur à récupérer.
    Returns :
        dict : Dictionnaire contenant les informations de l'utilisateur, ou None si l'utilisateur n'est pas trouvé.
    """
    cursor.execute("SELECT * FROM Utilisateurs WHERE utilisateur_id = %s", (id_utilisateur,))
    utilisateur = cursor.fetchone()
    #print(utilisateur)
    if utilisateur:
        return {
            "utilisateur_id": utilisateur[0],
            "nom_complet": utilisateur[4],
            "email": utilisateur[5],
            "mot_de_passe": utilisateur[2],
            "nom_utilisateur": utilisateur[1],
        }
    else:
        return None
def utilisateur_exists(cursor, nom_utilisateur, mot_de_passe, role_utilisateur):
    try:
        cursor.execute("""
            SELECT COUNT(*) FROM Utilisateurs
            WHERE nom_utilisateur = %s AND mot_de_passe = %s AND role_utilisateur = %s
        """, (nom_utilisateur, mot_de_passe, role_utilisateur))
        count = cursor.fetchone()[0]
        if count == 1:
            return True
        elif count > 1:
            print("Erreur: Plusieurs utilisateurs correspondent aux informations fournies.")
            return False
        else:
            return False
    except Exception as e:
        print(f"Erreur lors de la vérification de l'existence de l'utilisateur : {e}")
        return False
def insert_demande_tutorat(cursor, cours_id):
    try:
        cursor.execute(
            "INSERT INTO Demandes_Tutorat (cours_id) VALUES (%s)",
            (cours_id,)
        )
        insertion_id = cursor.lastrowid
        if cursor.rowcount > 0:
            cursor = cursor.connection.commit()
            return True, insertion_id
        return False, None
    except Exception as e:
        print(f"Erreur lors de l'insertion de la demande de tutorat : {e}")
        return False, None
def insert_into_Liste_Etudiants_Demandes(cursor, demande_id, etudiant_id):
    try:
        cursor.execute("""
            SELECT COUNT(*)
            FROM Cours_Etudiants_Demandes_Tutorat AS cedt
            INNER JOIN Demandes_Tutorat AS dt ON cedt.demande_id = dt.demande_id
            WHERE dt.cours_id = (
                SELECT cours_id
                FROM Demandes_Tutorat
                WHERE demande_id = %s
            )
            AND cedt.etudiant_id = %s
        """, (demande_id, etudiant_id))
        existing_count = cursor.fetchone()[0]
        if existing_count == 0:
            cursor.execute("""
                INSERT INTO Cours_Etudiants_Demandes_Tutorat (demande_id, etudiant_id)
                VALUES (%s, %s)
            """, (demande_id, etudiant_id))
            if cursor.rowcount > 0:
                cursor.connection.commit()
                return True
        else:
            print("L'étudiant existe déjà pour cette demande.")
            return False
    except Exception as e:
        print(f"Erreur lors de l'insertion de données dans la table Cours_Etudiants_Demandes_Tutorat : {e}")
        return False
def insert_candidature_tutorat(cursor, tuteur_id, demande_id):
    try:
        cursor.execute("""
            INSERT INTO Candidatures_Tuteurats (tuteur_id, demande_id)
            VALUES (%s, %s)
        """, (tuteur_id, demande_id))
        cursor.connection.commit()
        return True
    except Exception as e:
        print(f"Erreur lors de l'insertion de la candidature de tutorat : {e}")
        return False
def insert_cours(cursor, nom_cours):
    try:
        if not cours_existe(cursor, nom_cours):
            cursor.execute("INSERT INTO Cours (nom_cours) VALUES (%s)", (nom_cours,))
            print(f"Cours '{nom_cours}' ajouté avec succès.")
            cursor.connection.commit()
        else:
            print(f"Le cours '{nom_cours}' existe déjà.")
    except Exception as e:
        print(f"Erreur lors de l'insertion du cours : {e}")
def get_cours(cursor, id_cours):
    try:
        cursor.execute("SELECT nom_cours FROM Cours WHERE cours_id = %s", (id_cours,))
        result = cursor.fetchone()
        if result:
            nom_cours = result[0]
            return nom_cours
        else:
            return "Cours non trouvé"
    
    except Exception as e:
        print(f"Erreur lors de la récupération du cours : {e}")
        return None
def get_all_cours(cursor):
    try:
        cursor.execute("SELECT * FROM Cours ORDER BY cours_id")
        cours = cursor.fetchall()
        if cours:
            return cours
        else:
            print(f"Aucun cours trouvé.")
            return []
    except Exception as e:
        print(f"Erreur lors de la récupération des cours : {e}")
        return []
def get_cours_by_professeur_id(cursor, id_professeur):
    try:
        cursor.execute("""
            SELECT Cours.cours_id, Cours.nom_cours
            FROM Cours
            JOIN Cours_Professeurs ON Cours.cours_id = Cours_Professeurs.cours_id
            WHERE Cours_Professeurs.professeur_id = %s
        """, (id_professeur,))
        result = cursor.fetchall()
        cours_info = [(r[0], r[1]) for r in result]
        #print(cours_info)
        return cours_info
    except Exception as e:
        print(f"Erreur lors de la récupération des cours : {e}")   
def get_etudiants_by_cours(cursor, id_cours):
    try:
        cursor.execute("""
            SELECT Etudiants.etudiant_id, Utilisateurs.nom_complet
            FROM Etudiants
            INNER JOIN Cours_Etudiants ON Etudiants.etudiant_id = Cours_Etudiants.etudiant_id
            INNER JOIN Cours ON Cours_Etudiants.cours_id = Cours.cours_id
            INNER JOIN Utilisateurs ON Etudiants.utilisateur_id = Utilisateurs.utilisateur_id
            WHERE Cours.cours_id = %s
        """, (id_cours,))
        result = cursor.fetchall()
        resultats_ids_noms = [(id_etudiant, nom_etudiant) for (id_etudiant, nom_etudiant) in result]
        # Retourner la liste des étudiants dans le cours avec le nom du cours
        return resultats_ids_noms
    except Exception as e:
        print(f"Erreur lors de la récupération des étudiants par cours : {e}")
def get_cours_by_etudiant_id(cursor, id_etudiant):
    try:
        cursor.execute("""
            SELECT Cours.cours_id, Cours.nom_cours
            FROM Cours
            JOIN Cours_Etudiants ON Cours.cours_id = Cours_Etudiants.cours_id
            WHERE Cours_Etudiants.etudiant_id = %s
        """, (id_etudiant,))
        result = cursor.fetchall()
        cours_info = [(r[0], r[1]) for r in result]
        return cours_info
    except Exception as e:
        print(f"Erreur lors de la récupération des cours : {e}")
def get_professors_for_course(cursor, course_id):
    try:
        cursor.execute("""
            SELECT DISTINCT Professeurs.professeur_id, Utilisateurs.nom_complet,Utilisateurs.utilisateur_id
            FROM Professeurs
            JOIN Utilisateurs ON Professeurs.utilisateur_id = Utilisateurs.utilisateur_id
            JOIN Cours_Professeurs ON Professeurs.professeur_id = Cours_Professeurs.professeur_id
            WHERE Cours_Professeurs.cours_id = %s
        """, (course_id,))
        professors_for_course = cursor.fetchall()
        return professors_for_course
    except Exception as e:
        print(f"Erreur lors de la récupération des professeurs pour le cours {course_id} : {e}")
        return []
def insert_message(cursor, expediteur_id, destinataire_id, titre, contenu):
    try:
        cursor.execute("""
            INSERT INTO Messages (expediteur_id, destinataire_id, titre, contenu)
            VALUES (%s, %s, %s, %s)
        """, (expediteur_id, destinataire_id, titre, contenu))
        if cursor.rowcount > 0:
            cursor.connection.commit()
            return True
        else:
            return False
    except Exception as e:
        print(f"Erreur lors de l'insertion du message : {e}")
def get_disponibilites_by_tuteur_id(cursor, tuteur_id):
    try:
        cursor.execute("""
            SELECT * FROM Disponibilites_Tuteurs
            WHERE tuteur_id = %s
        """, (tuteur_id,))
        disponibilites = cursor.fetchall()
        return disponibilites
    except Exception as e:
        print(f"Erreur lors de la récupération des disponibilités : {e}")
        return None  
def disponibilite_existe(cursor, tuteur_id, jour, heure_debut, heure_fin):
    try:
        cursor.execute("""
            SELECT * FROM Disponibilites_Tuteurs
            WHERE tuteur_id = %s
            AND jour = %s
            AND heure_debut = %s
            AND heure_fin = %s
        """, (tuteur_id, jour, heure_debut, heure_fin))
        
        disponibilite = cursor.fetchone()
        return disponibilite is not None

    except Exception as e:
        print(f"Erreur lors de la vérification de l'existence de la disponibilité : {e}")
        return False
def ajouter_disponibilite(cursor, tuteur_id, jour, heure_debut, heure_fin):
    try:
        if not disponibilite_existe(cursor, tuteur_id, jour, heure_debut, heure_fin):
            cursor.execute("""
                INSERT INTO Disponibilites_Tuteurs (tuteur_id, jour, heure_debut, heure_fin)
                VALUES (%s, %s, %s, %s)
            """, (tuteur_id, jour, heure_debut, heure_fin))
            if cursor.rowcount > 0:
                print(f"Disponibilité ajoutée avec succès pour le tuteur ID {tuteur_id}.")
                return True
            else:
                print(f"Aucune disponibilité ajoutée pour le tuteur ID {tuteur_id}. Vérifiez les données.")
                return False
        else:
            print(f"La disponibilité pour le tuteur ID {tuteur_id} existe déjà.")
            return False
    except Exception as e:
        print(f"Erreur lors de l'insertion de la disponibilité : {e}")
        return False
def modifier_disponibilite(cursor, disponibilite_id, nouveau_jour, nouvelle_heure_debut, nouvelle_heure_fin):
    try:
            cursor.execute("""
                UPDATE Disponibilites_Tuteurs
                SET jour = %s, heure_debut = %s, heure_fin = %s
                WHERE disponibilite_id = %s
            """, (nouveau_jour, nouvelle_heure_debut, nouvelle_heure_fin, disponibilite_id))
            print(f"Disponibilité avec ID {disponibilite_id} modifiée avec succès.")
    except Exception as e:
        print(f"Erreur lors de la modification de la disponibilité : {e}")
def delete_disponibilite_by_id(cursor, disponibilite_id):
    try:
            print(f"Suppression de la disponibilité avec l'ID {disponibilite_id}")
            cursor.execute("""
                DELETE FROM Disponibilites_Tuteurs
                WHERE disponibilite_id = %s
            """, (disponibilite_id,))
            if cursor.rowcount > 0:
                print(f"La disponibilité avec l'ID {disponibilite_id} a été supprimée avec succès.")
            else:
                print(f"Aucune disponibilité trouvée avec l'ID {disponibilite_id}. Aucune suppression effectuée.")
    except Exception as e:
        print(f"Erreur lors de la suppression de la disponibilité : {e}")
def get_demandes_tuteur_cours(cursor, tuteur_id):
    try:
        cursor.execute("""
            SELECT
                dt.demande_id,
                c.nom_cours,
                u.nom_complet AS etudiant,
                dp.statut
            FROM Demandes_Tutorat dt
            JOIN Cours_Etudiants_Demandes_Tutorat cedt ON dt.demande_id = cedt.demande_id
            JOIN Etudiants et ON cedt.etudiant_id = et.etudiant_id
            JOIN Utilisateurs u ON et.utilisateur_id = u.utilisateur_id
            JOIN Cours_Tuteurs ct ON dt.cours_id = ct.cours_id
            JOIN Cours c ON dt.cours_id = c.cours_id
            LEFT JOIN Demandes_Postuler dp ON dt.demande_id = dp.demande_id AND ct.tuteur_id = dp.tuteur_id
            WHERE ct.tuteur_id = %s
        """, (tuteur_id,))
        result = cursor.fetchall()
        demande_info = {}
        for row in result:
            demande_id, nom_cours, etudiant, statut = row
            if demande_id not in demande_info:
                demande_info[demande_id] = {"nom_cours": nom_cours, "etudiants": [], "statut_tuteur": statut}
            demande_info[demande_id]["etudiants"].append(etudiant)
        liste_demandes = [{"demande_id": demande_id, "data": data} for demande_id, data in demande_info.items()]
        return liste_demandes
    except Exception as e:
        print(f"Erreur : {e}")
def insert_candidature_and_demande_postuler(cursor, tuteur_id, demande_id):
    try:
        cursor.execute("""
            SELECT COUNT(*) FROM Candidatures_Tuteurats 
            WHERE tuteur_id = %s AND demande_id = %s
        """, (tuteur_id, demande_id))
        existing_count = cursor.fetchone()[0]
        if existing_count == 0:
            cursor.execute("""
                INSERT INTO Candidatures_Tuteurats (tuteur_id, demande_id)
                VALUES (%s, %s)
            """, (tuteur_id, demande_id))
            cursor.execute("""
                INSERT INTO Demandes_Postuler (tuteur_id, demande_id, statut)
                VALUES (%s, %s, %s)
            """, (tuteur_id, demande_id, True))
            cursor.connection.commit()
            cursor.execute("""
                SELECT statut FROM Demandes_Postuler
                WHERE tuteur_id = %s AND demande_id = %s
            """, (tuteur_id, demande_id))
            statut_postuler = cursor.fetchone()[0]
            return True, statut_postuler
        else:
            print("Le tuteur a déjà une candidature pour cette demande.")
            return False, None
    except Exception as e:
        print(f"Erreur lors de l'insertion de la candidature et de la demande postuler : {e}")
        return False, None
def get_tutor_data_and_courses(cursor, tuteur_id):
    try:
        # Requête pour récupérer les données du tuteur
        query = """
            SELECT 
                Utilisateurs.nom_complet, 
                Utilisateurs.email,
                Tuteurs.tuteur_id, 
                Tuteurs.utilisateur_id,
                Cours.nom_cours
            FROM Tuteurs
            INNER JOIN Utilisateurs ON Tuteurs.utilisateur_id = Utilisateurs.utilisateur_id
            LEFT JOIN Cours_Tuteurs ON Tuteurs.tuteur_id = Cours_Tuteurs.tuteur_id
            LEFT JOIN Cours ON Cours_Tuteurs.cours_id = Cours.cours_id
            WHERE Tuteurs.tuteur_id = %s
        """
        cursor.execute(query, (tuteur_id,))
        tutor_data_and_courses = cursor.fetchall()
        tutors = {}
        list_disponibilite = get_disponibilites_by_tuteur_id(cursor,tuteur_id=tuteur_id)
        dispo_info = []
        for disponibilite in list_disponibilite:
            id_disponibilite, tuteur_id, jour, heure_debut, heure_fin = disponibilite
            heure_debut_dt = datetime.strptime(str(heure_debut), '%H:%M:%S')
            heure_fin_dt = datetime.strptime(str(heure_fin), '%H:%M:%S')
            dispo_info.append({
                "Jour": jour,
                "Heures": {
                    "heure_debut": f"{heure_debut_dt.hour}:{heure_debut_dt.minute:02}",
                    "heure_fin": f"{heure_fin_dt.hour}:{heure_fin_dt.minute:02}"
                },
            })
        for tutor_data in tutor_data_and_courses:
            nom_complet, email, tuteur_id, utilisateur_id, cours = tutor_data
            if tuteur_id not in tutors:
                tutors[tuteur_id] = {'nom_complet': nom_complet, 'email': email, 'cours': [cours], 'disponibility': dispo_info}
            else:
                tutors[tuteur_id]['cours'].append(cours)
        resultat = list(tutors.values())
        return resultat 
    except Exception as e:
        print(f"Erreur lors de la récupération des données du tuteur et des cours qu'il donne : {e}")
        return None

def delete_candidature(cursor, tuteur_id, demande_id):
    try:
        cursor.execute("""
            DELETE FROM Candidatures_Tuteurat
            WHERE tuteur_id = %s AND demande_id = %s
        """, (tuteur_id, demande_id))
        cursor.connection.commit()
        print("La candidature a bien été supprimée.")
    except Exception as e:
        print(f"Une erreur est survenue lors de la suppression de la candidature : {e}")
def get_candidatures_with_info(cursor):
    try:
        cursor.execute("""
            SELECT 
                ct.candidature_id AS id_candidature,
                c.nom_cours AS nom_cours,
                ct.demande_id AS id_demande,
                t.tuteur_id AS id_tuteur,
                u.nom_complet AS nom_tuteur
            FROM Candidatures_Tuteurats ct
            INNER JOIN Tuteurs t ON ct.tuteur_id = t.tuteur_id
            INNER JOIN Utilisateurs u ON t.utilisateur_id = u.utilisateur_id
            INNER JOIN Demandes_Tutorat dt ON ct.demande_id = dt.demande_id
            INNER JOIN Cours c ON dt.cours_id = c.cours_id
        """)
        list_candidatures = cursor.fetchall()
        candidatures = {}
        for item in list_candidatures:
            id_candidature, nom_cours, _, id_tuteur, nom_tuteur = item
            if nom_cours not in candidatures:
                candidatures[nom_cours] = {
                    'id_candidature': id_candidature,
                    'nom_cours': nom_cours,
                    'Tuteurs': [{'nom': nom_tuteur, 'id_tuteur': id_tuteur}]
                }
            else:
                candidatures[nom_cours]['Tuteurs'].append({'nom': nom_tuteur, 'id_tuteur': id_tuteur})
        resultat = list(candidatures.values())
       # print(resultat)
        return resultat
    except Exception as e:
        print(f"Erreur lors de la récupération des candidatures : {e}")
        return None

    except Exception as e:
        print(f"Erreur lors de la récupération des candidatures : {e}")
        return None
def get_demandes_tutorat(cursor):
    try:
        demandes = []
        cursor.execute("""
            SELECT d.demande_id, c.nom_cours, d.statut_demande
            FROM Demandes_Tutorat d
            INNER JOIN Cours c ON d.cours_id = c.cours_id
        """)
        demandes_rows = cursor.fetchall()
        for demande_row in demandes_rows:
            demande_id = demande_row[0]
            nom_cours = demande_row[1]
            statut_demande = demande_row[2]
            cursor.execute("""
                SELECT u.nom_complet
                FROM Cours_Etudiants_Demandes_Tutorat ce
                INNER JOIN Utilisateurs u ON ce.etudiant_id = u.utilisateur_id
                WHERE ce.demande_id = %s
            """, (demande_id,))
            etudiants_rows = cursor.fetchall()
            etudiants = [etudiant_row[0] for etudiant_row in etudiants_rows]
            demandes.append({
                'demande_id': demande_id,
                'nom_cours': nom_cours,
                'statut_demande': statut_demande,
                'etudiants': etudiants
            })
        return demandes
    except Exception as e:
        print(f"Erreur lors de la récupération des demandes de tutorat : {e}")
        return None
