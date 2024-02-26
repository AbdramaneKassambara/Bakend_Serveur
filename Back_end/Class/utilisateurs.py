from datetime import datetime
from Config import crud


def utilisateur_id_existe(cursor, utilisateur_id, nom_table):
    try:
        cursor.execute(f"SELECT * FROM {nom_table} WHERE utilisateur_id = %s", (utilisateur_id,))
        result = cursor.fetchone()
        return result is not None
    except Exception as e:
        print(f"Erreur lors de la vérification de l'existence de l'utilisateur_id : {e}")
        return False
class Utilisateur:
    def __init__(self, nom_utilisateur, mot_de_passe, role_utilisateur, nom_complet=None, email=None,genre=None):
        self.__nom_utilisateur = nom_utilisateur
        self.__mot_de_passe = mot_de_passe
        self.__role_utilisateur = role_utilisateur
        self.__nom_complet = nom_complet
        self.__email = email
        self.__compte_active = True
        self.__genre = genre

    def get_compte_active(self):
        return self.__compte_active
    
    def desactiver_compte(self):
        self.__compte_active = False

    def get_nom_utilisateur(self):
        return self.__nom_utilisateur

    def get_mot_de_passe(self):
        return self.__mot_de_passe

    def get_role_utilisateur(self):
        return self.__role_utilisateur

    def get_nom_complet(self):
        return self.__nom_complet

    def get_email(self):
        return self.__email
    def get_genre(self):
        return self.__genre
    
    @staticmethod
    def recuperer_utilisateur_par_nom(cursor, nom_utilisateur):
        try:
            cursor.execute("""
                SELECT * FROM Utilisateurs
                WHERE nom_utilisateur=%s
            """, (nom_utilisateur,))
            row = cursor.fetchone()
            if row:
                return row
        except Exception as e:
            print(f"Erreur lors de la récupération de l'utilisateur par nom : {e}")
        return None
    
    def recuperer_utilisateurs_par_role(cursor, role_utilisateur):
        try:
            cursor.execute("""
                SELECT * FROM Utilisateurs
                WHERE role_utilisateur = %s
            """, (role_utilisateur,))
            rows = cursor.fetchall()
            if rows:
                #print(rows)
                return rows
        except Exception as e:
            print(f"Erreur lors de la récupération des utilisateurs par rôle : {e}")
        return None
    
    def create(self, cursor):
        try:
            existing_user = Utilisateur.recuperer_utilisateur_par_nom(cursor, self.get_nom_utilisateur())
            if existing_user:
                print("L'utilisateur existe déjà.")
            else:
                # L'utilisateur n'existe pas
                cursor.execute("""
                    INSERT INTO Utilisateurs (nom_utilisateur, mot_de_passe, role_utilisateur, nom_complet, email, genre, compte_active)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (self.get_nom_utilisateur(), self.get_mot_de_passe(), self.get_role_utilisateur(),
                    self.get_nom_complet(), self.get_email(), self.get_genre(), self.get_compte_active()))
                cursor.connection.commit()
                print("Utilisateur ajouté avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'ajout de l'utilisateur dans la base de données : {e}")

# la class de chef departement est une sous-classe de la class Utilisateur
class ChefDepartement(Utilisateur):
    def __init__(self, nom_utilisateur, mot_de_passe, nom_complet=None, email=None, departement=None,genre=None):
        super().__init__(nom_utilisateur, mot_de_passe, "ChefDepartement", nom_complet, email)
        self.__departement = departement
        self.__genre = genre

    def get_departement(self):
        return self.__departement
    def get_genre(self):
        return self.__genre
    def Sign_In_Chef_departement(cursor, nom_utilisateur, mot_de_passe):
        try:
            # Informations du chef de département
            cursor.execute("""
                SELECT Chef_Departements.chef_id, Utilisateurs.utilisateur_id, Utilisateurs.email, Utilisateurs.nom_complet, Utilisateurs.nom_utilisateur, Utilisateurs.mot_de_passe
                FROM Chef_Departements
                INNER JOIN Utilisateurs ON Chef_Departements.utilisateur_id = Utilisateurs.utilisateur_id
                WHERE Utilisateurs.nom_utilisateur = %s AND Utilisateurs.mot_de_passe = %s
            """, (nom_utilisateur, mot_de_passe))
            chef_info = cursor.fetchone()
            if chef_info:
                chef_id, utilisateur_id, email, nom_complet, nom_utilisateur, mot_de_passe = chef_info
                chef_info ={
                    'chef_id': chef_id,
                    "utilisateur_id" : utilisateur_id,
                    "email":email,
                    "nom_complet": nom_complet,
                    "nom_utilisateur": nom_utilisateur,
                    "mot_de_passe": mot_de_passe,
                }
                
                return chef_info
            else:
                print("Chef de département non trouvé.")
                return None
        except Exception as e:
            print(f"Erreur lors de l'identification du chef de département : {e}")
            return None

    def create(self, cursor,utilisateur_id):
        try:
            # Vérifier si l'utilisateur existe déjà
            if utilisateur_id_existe(cursor,utilisateur_id,"Chef_Departements"):
                print("L'Chef existe déjà.")
            else:
                # Insérer les informations spécifiques au professeur
                cursor.execute("""
                    INSERT INTO Chef_Departements (utilisateur_id, departement) 
                    VALUES (%s, %s)
                """,(int(utilisateur_id), self.get_departement()))
                cursor.connection.commit()
        except Exception as e:
            print(f"Erreur lors de l'ajout du Chef_Departements dans la base de données : {e}")
            return None

class Professeur(Utilisateur):
    def __init__(self, nom_utilisateur, mot_de_passe, nom_complet=None, email=None , genre=None, cours_enseignes=None):
        super().__init__(nom_utilisateur, mot_de_passe, "Professeur", nom_complet, email,genre)
        self.__cours_enseignes = cours_enseignes or []

    def get_cours_enseignes(self):
        return self.__cours_enseignes
    
    def create(self, cursor,utilisateur_id):
        try:
            # Vérifier si l'utilisateur existe déjà
            if utilisateur_id_existe(cursor,utilisateur_id,"Professeurs"):
                print("L'Professeurs existe déjà.")
            else:
                # Insérer les informations spécifiques au professeur
                cursor.execute("""
                    INSERT INTO Professeurs (utilisateur_id)
                    VALUES (%s)
                """,(int(utilisateur_id),))
                cursor.connection.commit()
                #print("utilisateur_id")
                # Récupérer l'ID du tuteur nouvellement inséré
                cursor.execute("SELECT professeur_id FROM Professeurs WHERE utilisateur_id = %s", (utilisateur_id,))
                professeur_id = cursor.fetchone()[0]
                #print(professeur_id)
                for cour in self.get_cours_enseignes():
                    # Ajouter le lien entre le prof et son cours
                    cursor.execute("""
                        INSERT INTO Cours_Professeurs (professeur_id, cours_id)
                        VALUES (%s, %s)
                    """,(professeur_id,cour,))
                    cursor.connection.commit()
                    print("Professeur ajouté avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'ajout du professeur dans la base de données : {e}")
            return None

    def Sign_In_Prof(cursor, nom_utilisateur, mot_de_passe):
        try:
            #informations du professeur
            cursor.execute("""
                SELECT professeur_id, Utilisateurs.utilisateur_id, Utilisateurs.email, Utilisateurs.nom_complet ,Utilisateurs.nom_utilisateur,Utilisateurs.mot_de_passe
                FROM Professeurs
                INNER JOIN Utilisateurs ON Professeurs.utilisateur_id = Utilisateurs.utilisateur_id
                WHERE Utilisateurs.nom_utilisateur = %s AND Utilisateurs.mot_de_passe = %s
            """, (nom_utilisateur, mot_de_passe))
            prof = cursor.fetchone()
            if prof:
               # print(prof)
                # les cours associés au professeur
                cursor.execute(""" 
                    SELECT cours_id FROM Cours_Professeurs WHERE professeur_id = %s 
                """, (prof[0],))
                cours_ids = [t[0] for t in cursor.fetchall()]
                names_cours = []
                #les noms des cours
                for cours_id in cours_ids:
                    name_cours = crud.get_cours(cursor, cours_id)
                    names_cours.append(name_cours)
                # les informations du professeur et les noms des cours
                return {
                    'professeur_info': {'id-prof':prof[0],'id-utilisateur':prof[1],'prof-email':prof[2],'prof-nom':prof[3],'prof-nom_utilisateur':prof[4],'prof-password':prof[5]},
                    'cours_names': names_cours
                }
            else:
                return None 
        except Exception as e:
            print(f"Erreur lors de l'identification du professeur : {e}")
            return None


class Etudiant(Utilisateur):
    def __init__(self, nom_utilisateur, mot_de_passe, nom_complet=None, email=None,genre=None, cours_inscrits=None):
        super().__init__(nom_utilisateur, mot_de_passe, "Etudiant", nom_complet, email,genre)
        self.__cours_inscrits = cours_inscrits or []

    def get_cours_inscrits(self):
        return self.__cours_inscrits
    
    def create(self, cursor, utilisateur_id):
        try:
            if utilisateur_id_existe(cursor, utilisateur_id, "Etudiants"):
                print("L'étudiant existe déjà.")
            else:
                if utilisateur_id_existe(cursor, utilisateur_id, "Utilisateurs"):
                    cursor.execute("""
                        INSERT INTO Etudiants (utilisateur_id)
                        VALUES (%s)
                    """, (int(utilisateur_id),))
                    cursor.connection.commit()
                    print("Étudiant ajouté avec succès.")
                    # Récupérer l'ID du nouvel étudiant inséré
                    cursor.execute("SELECT etudiant_id FROM Etudiants WHERE utilisateur_id = %s", (utilisateur_id,))
                    etudiant_id = cursor.fetchone()[0]
                    print(etudiant_id)
                    # Ajouter les cours inscrits dans la table Cours_Etudiants
                    for cours in self.get_cours_inscrits():
                        cursor.execute("""
                            INSERT INTO Cours_Etudiants (etudiant_id, cours_id)
                            VALUES (%s, %s)
                        """, (etudiant_id, cours))
                        cursor.connection.commit()
                        print("Cours ajouté pour l'étudiant avec succès.")
                else:
                    print(f"L'utilisateur avec l'ID {utilisateur_id} n'existe pas dans la table Utilisateurs.")
        except Exception as e:
            print(f"Erreur lors de l'ajout de l'étudiant dans la base de données : {e}")


    def Sign_In_Etudiant(cursor, nom_utilisateur, mot_de_passe):
        try:
            #informations du etudiant
            cursor.execute("""
                SELECT etudiant_id, Utilisateurs.utilisateur_id, Utilisateurs.email, Utilisateurs.nom_complet ,Utilisateurs.genre
                FROM Etudiants
                INNER JOIN Utilisateurs ON Etudiants.utilisateur_id = Utilisateurs.utilisateur_id
                WHERE Utilisateurs.nom_utilisateur = %s AND Utilisateurs.mot_de_passe = %s
            """, (nom_utilisateur, mot_de_passe))
            etudiant = cursor.fetchone()
            #print(etudiant)
            if etudiant:
                try:
                    cursor.execute(""" 
                        SELECT cours_id FROM Cours_Etudiants WHERE etudiant_id = %s 
                    """, (etudiant[0],))
                    cours_ids = [t[0] for t in cursor.fetchall()]
                    names_cours = []
                    #  for cours_id in cours_ids:
                    #     name_cours = crud.get_cours(cursor, cours_id)
                    # names_cours.append(name_cours)
                    for cours_id in cours_ids:
                        cursor.execute("""
                        SELECT nom_cours, Utilisateurs.nom_complet
                        FROM Cours
                        INNER JOIN Cours_Professeurs ON Cours.cours_id = Cours_Professeurs.cours_id
                        INNER JOIN Utilisateurs ON Cours_Professeurs.professeur_id = Utilisateurs.utilisateur_id
                        WHERE Cours.cours_id = %s
                    """, (cours_id,))
                        result = cursor.fetchone()
                        print (result)
                        if result:
                            cours_nom, professeur_nom = result
                            names_cours.append({ "cours":cours_nom,"Professeur": professeur_nom})
                        else:
                            names_cours.append(f"Nom du cours non trouvé pour l'ID {cours_id}")
                except Exception as e:
                    print(f"Erreur lors de la récupération des cours associés à l'étudiant : {e}")
                # les informations du etudiant et les noms des cours
                return {
                    'etudiant_info': {'id-etudiant':etudiant[0],'id-utilisateur':etudiant[1],'etudiant-email':etudiant[2],'etudiant-nom':etudiant[3],'genre':etudiant[4]},
                    'cours_names': names_cours
                }
            else:
                return None 
        except Exception as e:
            print(f"Erreur lors de l'identification du etudiant : {e}")
            return None

class Tuteur(Utilisateur):
    def __init__(self, nom_utilisateur, mot_de_passe, nom_complet=None, email=None,genre=None,cours_tutorat=None, disponibilites=None):
        super().__init__(nom_utilisateur, mot_de_passe, "Tuteur", nom_complet, email,genre)
        self.__cours_tutorat = cours_tutorat or []
        self.__disponibilites = disponibilites or []

    def get_cours_tutorat(self):
        return self.__cours_tutorat

    def get_disponibilites(self):
        return self.__disponibilites

    def ajouter_matiere_tutorat(self, matiere):
        self.__cours_tutorat.append(matiere)

    def ajouter_disponibilite(self, disponibilite):
        self.__disponibilites.append(disponibilite)
        
    def create(self, cursor, utilisateur_id):
        try:
            if utilisateur_id_existe(cursor, utilisateur_id,"Tuteurs"):
                print("Le tuteur existe déjà.")
            else:
                # Ajouter l'entrée dans la table Tuteurs
                cursor.execute("""
                    INSERT INTO Tuteurs (utilisateur_id)
                    VALUES (%s)
                """, (utilisateur_id,))
                cursor.connection.commit()
                # Récupérer l'ID du tuteur nouvellement inséré
                cursor.execute("SELECT tuteur_id FROM Tuteurs WHERE utilisateur_id = %s", (utilisateur_id,))
                tuteur_id = cursor.fetchone()[0]
                # Ajouter les matières enseignées dans Matieres_Tuteurs
                for matiere in self.get_cours_tutorat():
                    cursor.execute("""
                        INSERT INTO Cours_Tuteurs (tuteur_id, cours_id)
                        VALUES (%s, %s)
                    """, (tuteur_id, matiere))
                    cursor.connection.commit()
                # Ajouter les disponibilités dans Disponibilites_Tuteurs
                for disponibilite in self.get_disponibilites():
                    cursor.execute("""
                        INSERT INTO Disponibilites_Tuteurs (tuteur_id, jour, heure_debut, heure_fin)
                        VALUES (%s, %s, %s, %s)
                    """, (tuteur_id, disponibilite["jour"], disponibilite["heure_debut"], disponibilite["heure_fin"]))
                    cursor.connection.commit()
                print("Tuteur ajouté avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'ajout du tuteur dans la base de données : {e}")

    def Sign_In_Tuteur(cursor, nom_utilisateur, mot_de_passe):
        try:
            #informations du etudiant
            cursor.execute("""
                SELECT tuteur_id, Utilisateurs.utilisateur_id, Utilisateurs.email, Utilisateurs.nom_complet,Utilisateurs.genre
                FROM Tuteurs
                INNER JOIN Utilisateurs ON Tuteurs.utilisateur_id = Utilisateurs.utilisateur_id
                WHERE Utilisateurs.nom_utilisateur = %s AND Utilisateurs.mot_de_passe = %s
            """, (nom_utilisateur, mot_de_passe))
            cursor.connection.commit()
            tuteur = cursor.fetchone()
            #print(tuteur)
            if tuteur:
                # les cours associés au etudiant
                cursor.execute(""" 
                    SELECT cours_id FROM Cours_Tuteurs WHERE tuteur_id = %s 
                """, (tuteur[0],))
                cours_ids = [t[0] for t in cursor.fetchall()]
                name_cours = []
                #les noms des cours
                for cours_id in cours_ids:
                    cours_info = crud.get_cours(cursor, cours_id)
                    name_cours.append(cours_info)
                cursor.execute(""" 
                    SELECT * FROM Disponibilites_Tuteurs WHERE tuteur_id = %s 
                """, (tuteur[0],))
                dispo_info = []
                for disponibilite in cursor.fetchall():
                    id_disponibilite, tuteur_id, jour, heure_debut, heure_fin = disponibilite
                    heure_debut_dt = datetime.strptime(str(heure_debut), '%H:%M:%S')
                    heure_fin_dt = datetime.strptime(str(heure_fin), '%H:%M:%S')
                    dispo_info.append({
                        "Jour": jour,
                        "Heures": {
                            "heure_debut": f"{heure_debut_dt.hour}:{heure_debut_dt.minute:02}",
                            "heure_fin": f"{heure_fin_dt.hour}:{heure_fin_dt.minute:02}"
                        },
                        "disponi-id": id_disponibilite
                    })
                # les informations du etudiant et les noms des cours
                return {
                    'tuteur_info': {'id-tuteur':tuteur[0],'id-utilisateur':tuteur[1],'tuteur-email':tuteur[2],'tuteur-nom':tuteur[3],"genre":tuteur[4]},
                    'name_cours': name_cours,
                    'disponibilite': dispo_info
                }
            else:
                return None 
        except Exception as e:
            print(f"Erreur lors de l'identification du tuteur : {e}")
            return None
