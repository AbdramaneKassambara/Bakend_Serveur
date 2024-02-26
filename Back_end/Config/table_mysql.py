# Table pour les Utilisateurs
def create_tables_Utilisateurs(cursor):
    try:
        print("Création de la table Utilisateurs")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Utilisateurs (
                utilisateur_id INT AUTO_INCREMENT PRIMARY KEY,
                nom_utilisateur VARCHAR(255) NOT NULL UNIQUE,
                mot_de_passe VARCHAR(255) NOT NULL,
                role_utilisateur VARCHAR(50) NOT NULL,
                nom_complet VARCHAR(255),
                email VARCHAR(255),
                genre VARCHAR(10),
                compte_active BOOLEAN DEFAULT TRUE
            )
        """)
    except Exception as e:
        print(f"Erreur lors de la création de la table Utilisateurs : {e}")

# Table pour les Chef_Departements
def create_tables_Chef_Departements(cursor):
    try:
        print("Création de la table Chef_Departements")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Chef_Departements (
                chef_id INT AUTO_INCREMENT PRIMARY KEY,
                utilisateur_id INT UNIQUE,
                departement VARCHAR(255),
                FOREIGN KEY (utilisateur_id) REFERENCES Utilisateurs(utilisateur_id)
            )
        """)
    except Exception as e:
        print(f"Erreur lors de la création de la table Chef_Departements : {e}")

# Table pour les Professeurs
def create_tables_Professeurs(cursor):
    try:
        print("Création de la table Professeurs")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Professeurs (
                professeur_id INT AUTO_INCREMENT PRIMARY KEY,
                utilisateur_id INT UNIQUE
            )
        """)
    except Exception as e:
        print(f"Erreur lors de la création de la table Professeurs : {e}")

# Table pour les Cours
def create_tables_Cours(cursor):
    try:
        print("Création de la table Cours")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Cours (
                cours_id INT AUTO_INCREMENT PRIMARY KEY,
                nom_cours VARCHAR(255) UNIQUE
            )
        """)
    except Exception as e:
        print(f"Erreur lors de la création de la table Cours : {e}")

# Table pour les Etudiants
def create_tables_Etudiants(cursor):
    try:
        print("Création de la table Etudiants")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Etudiants (
                etudiant_id INT AUTO_INCREMENT PRIMARY KEY,
                utilisateur_id INT UNIQUE
            )
        """)
    except Exception as e:
        print(f"Erreur lors de la création de la table Etudiants : {e}")

# Table pour les Tuteurs
def create_tables_Tuteurs(cursor):
    try:
        print("Création de la table Tuteurs")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Tuteurs (
                tuteur_id INT AUTO_INCREMENT PRIMARY KEY,
                utilisateur_id INT UNIQUE
            )
        """)
    except Exception as e:
        print(f"Erreur lors de la création de la table Tuteurs : {e}")

# Table de liaison pour les cours enseignés par les professeurs
def create_tables_Cours_Professeurs(cursor):
    try:
        print("Création de la table Cours_Professeurs")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Cours_Professeurs (
                professeur_id INT,
                cours_id INT,
                PRIMARY KEY (professeur_id, cours_id),
                FOREIGN KEY (professeur_id) REFERENCES Professeurs(professeur_id),
                FOREIGN KEY (cours_id) REFERENCES Cours(cours_id)
            )
        """)
    except Exception as e:
        print(f"Erreur lors de la création de la table Cours_Professeurs : {e}")

# Table de liaison pour les cours inscrits par les étudiants
def create_tables_Cours_Etudiants(cursor):
    try:
        print("Création de la table Cours_Etudiants")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Cours_Etudiants (
                etudiant_id INT,
                cours_id INT,
                PRIMARY KEY (etudiant_id, cours_id),
                FOREIGN KEY (etudiant_id) REFERENCES Etudiants(etudiant_id),
                FOREIGN KEY (cours_id) REFERENCES Cours(cours_id)
            )
        """)
    except Exception as e:
        print(f"Erreur lors de la création de la table Cours_Etudiants : {e}")

# Table pour les Sessions de Tutorat
def create_tables_Sessions_Tutorats(cursor):
    try:
        print("Création de la table Sessions_Tutorats")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Sessions_Tutorats (
                session_id INT AUTO_INCREMENT PRIMARY KEY,
                etudiant_id INT,
                tuteur_id INT,
                cours VARCHAR(255),
                date_session TIMESTAMP,
                duree_session INT,
                FOREIGN KEY (etudiant_id) REFERENCES Etudiants(etudiant_id),
                FOREIGN KEY (tuteur_id) REFERENCES Tuteurs(tuteur_id)
            )
        """)
    except Exception as e:
        print(f"Erreur lors de la création de la table Sessions_Tutorats : {e}")

# Table pour les Demandes de Tutorat
def create_tables_Demandes_Tutorat(cursor):
    try:
        print("Création de la table Demandes_Tutorat")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Demandes_Tutorat (
                demande_id INT AUTO_INCREMENT PRIMARY KEY,
                cours_id INT,
                date_demande TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                statut_demande VARCHAR(50) DEFAULT 'En attente',
                FOREIGN KEY (cours_id) REFERENCES Cours(cours_id)
            )
        """)
    except Exception as e:
        print(f"Erreur lors de la création de la table Demandes_Tutorat : {e}")
def create_tables_Demandes_Postuler(cursor):
    try:
        print("Création de la table Demandes_Postuler")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Demandes_Postuler (
                demande_id INT,
                tuteur_id INT,
                statut BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (demande_id) REFERENCES Demandes_Tutorat(demande_id),
                FOREIGN KEY (tuteur_id) REFERENCES Tuteurs(tuteur_id)
            )
        """)
    except Exception as e:
        print(f"Erreur lors de la création de la table Demandes_Postuler : {e}")
def create_tables_Cours_Etudiants_Demandes_Tutorat(cursor):
    try:
        print("Création de la table Cours_Etudiants_Demandes_Tutorat")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Cours_Etudiants_Demandes_Tutorat (
                demande_id INT,
                etudiant_id INT,
                FOREIGN KEY (etudiant_id) REFERENCES Etudiants(etudiant_id),
                FOREIGN KEY (demande_id) REFERENCES Demandes_Tutorat(demande_id)
            )
        """)
    except Exception as e:
        print(f"Erreur lors de la création de la table Cours_Etudiants_Demandes_Tutorat : {e}")


# Table pour les Notifications
def create_tables_Notifications(cursor):
    try:
        print("Création de la table Notifications")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Notifications (
                notification_id INT AUTO_INCREMENT PRIMARY KEY,
                utilisateur_id INT,
                message TEXT,
                date_notification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                lu BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (utilisateur_id) REFERENCES Utilisateurs(utilisateur_id)
            )
        """)
    except Exception as e:
        print(f"Erreur lors de la création de la table Notifications : {e}")

# Table pour les Commentaires
def create_tables_Commentaires(cursor):
    try:
        print("Création de la table Commentaires")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Commentaires (
                commentaire_id INT AUTO_INCREMENT PRIMARY KEY,
                utilisateur_id INT,
                session_id INT,
                commentaire TEXT,
                date_commentaire TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (utilisateur_id) REFERENCES Utilisateurs(utilisateur_id),
                FOREIGN KEY (session_id) REFERENCES Sessions_Tutorats(session_id)
            )
        """)
    except Exception as e:
        print(f"Erreur lors de la création de la table Commentaires : {e}")

# Table pour les Rapports de Session
def create_tables_Rapports_Session(cursor):
    try:
        print("Création de la table Rapports_Session")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Rapports_Session (
                rapport_id INT AUTO_INCREMENT PRIMARY KEY,
                session_id INT,
                contenu_rapport TEXT,
                date_rapport TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES Sessions_Tutorats(session_id)
            )
        """)
    except Exception as e:
        print(f"Erreur lors de la création de la table Rapports_Session : {e}")

# Table pour les Disponibilités des Tuteurs
def create_tables_Disponibilites_Tuteurs(cursor):
    try:
        print("Création de la table Disponibilites_Tuteurs")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Disponibilites_Tuteurs (
                disponibilite_id INT AUTO_INCREMENT PRIMARY KEY,
                tuteur_id INT,
                jour VARCHAR(10),
                heure_debut TIME,
                heure_fin TIME,
                FOREIGN KEY (tuteur_id) REFERENCES Tuteurs(tuteur_id)
            )
        """)
    except Exception as e:
        print(f"Erreur lors de la création de la table Disponibilites_Tuteurs : {e}")

# Table pour les Evenements
def create_tables_Evenements(cursor):
    try:
        print("Création de la table Evenements")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Evenements (
                evenement_id INT AUTO_INCREMENT PRIMARY KEY,
                titre_evenement VARCHAR(255),
                description_evenement TEXT,
                date_evenement TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    except Exception as e:
        print(f"Erreur lors de la création de la table Evenements : {e}")
#tuteur
def create_tables_Cours_Tuteurs(cursor):
    try:
        print("Création de la table Cours_Professeurs")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Cours_Tuteurs (
                tuteur_id INT,
                cours_id INT,
                PRIMARY KEY (tuteur_id, cours_id),
                FOREIGN KEY (tuteur_id) REFERENCES Tuteurs(tuteur_id),
                FOREIGN KEY (cours_id) REFERENCES Cours(cours_id)
            )
        """)
    except Exception as e:
        print(f"Erreur lors de la création de la table Cours_Tuteurs : {e}")

# Table pour les Messages
def create_table_Messages(cursor):
    try:
        print("Création de la table Messages")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Messages (
                message_id INT AUTO_INCREMENT PRIMARY KEY,
                expediteur_id INT,
                destinataire_id INT,
                titre VARCHAR(255),
                contenu TEXT,
                date_envoi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                lu BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (expediteur_id) REFERENCES Utilisateurs(utilisateur_id),
                FOREIGN KEY (destinataire_id) REFERENCES Utilisateurs(utilisateur_id)
            )
        """)
    except Exception as e:
        print(f"Erreur lors de la création de la table Messages : {e}")
def create_table_Candidatures_Tuteurat(cursor):
    try:
        print("Création de la table Candidatures_Tuteurat")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Candidatures_Tuteurats (
                candidature_id INT AUTO_INCREMENT PRIMARY KEY,
                tuteur_id INT,
                demande_id INT,
                statut_candidature VARCHAR(50) DEFAULT 'En attente',
                FOREIGN KEY (tuteur_id) REFERENCES Tuteurs(tuteur_id),
                FOREIGN KEY (demande_id) REFERENCES Demandes_Tutorat(demande_id)
            )
        """)
    except Exception as e:
        print(f"Erreur lors de la création de la table Candidatures_Tuteurat : {e}")
# Fonction pour créer toutes les tables
def create_all_tables(cursor):
    create_tables_Utilisateurs(cursor)
    create_tables_Chef_Departements(cursor)
    create_tables_Professeurs(cursor)
    create_tables_Cours(cursor)
    create_tables_Etudiants(cursor)
    create_tables_Tuteurs(cursor)
    create_tables_Cours_Professeurs(cursor)
    create_tables_Cours_Etudiants(cursor)
    create_tables_Sessions_Tutorats(cursor)
    create_tables_Cours_Tuteurs(cursor)
    create_tables_Demandes_Tutorat(cursor)
    create_tables_Cours_Etudiants_Demandes_Tutorat(cursor)
    create_tables_Notifications(cursor)
    create_tables_Commentaires(cursor)
    create_tables_Rapports_Session(cursor)
    create_tables_Disponibilites_Tuteurs(cursor)
    create_tables_Evenements(cursor)
    create_table_Messages(cursor)
    create_tables_Demandes_Postuler(cursor)
    create_table_Candidatures_Tuteurat(cursor)