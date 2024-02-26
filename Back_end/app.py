# Importez la classe Flask
from flask import Flask,request, jsonify, render_template
from flask_cors import CORS
from Config import crud as crd
from Config.connexion import connect_to_snowflake,connect_to_database_Mysql
from Class.utilisateurs import Etudiant, Professeur,Tuteur,ChefDepartement
from datetime import datetime, time
# Initialisez l'application Flask
app = Flask(__name__)
CORS(app, supports_credentials=True)
#cursor = connect_to_snowflake()
connection, cursor = connect_to_database_Mysql()
def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return wrapper
def get_json_data():
    return request.get_json() or {}

@app.route('/sign_in', methods=['POST'])
def Sign_In():
    """
    login de user connect  """
    try:
        data = request.get_json()
        role = data.get('role')
        username = data.get('username')
        password = data.get('password')
        if crd.utilisateur_exists(cursor,username,password,role):
            if role == "Professeur":
                prof = Professeur.Sign_In_Prof(cursor, username, password)
            # print(prof)
                return jsonify({"professeur_info": prof,"Role":"Professeur"})
            elif role == "Etudiant":
                etudiant = Etudiant.Sign_In_Etudiant(cursor, username, password)
                #print(etudiant)
                return jsonify({"student_info": etudiant,"Role":"Etudiant"})
            elif role == "Tuteur":
                tuteur = Tuteur.Sign_In_Tuteur(cursor,username,password)
                #print(tuteur)
                return jsonify({"Tuteur": tuteur,"Role":"Tuteur"})
            elif role == "ChefDepartement":
                chefs = ChefDepartement.Sign_In_Chef_departement(cursor,username,password)
            # print(chefs)
                return jsonify({"chef":chefs,"Role":"ChefDepartement"})
            else:
                return jsonify({"error": "Rôle non pris en charge"}), 400
        return jsonify({"error": "Nom d'utilisateur ou mot de passe incorrect"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/update_user', methods=["PUT"])
def updateUserInfo():
    """
    Modifier utilisateur par son id
    """
    try:
        data = request.get_json()
        id_data = data.get("id")
        nom_complet = data.get("nom")
        email = data.get("email")
        password = data.get("password")
        nom_utilisateur = data.get("nom_utilisateur")
        # Récupérer l'utilisateur à mettre à jour
        utilisateur_a_modifier = crd.get_utilisateur_par_id(cursor,id_data)
        #print(utilisateur_a_modifier)
        # Vérifier si l'utilisateur existe
        if utilisateur_a_modifier:
            # Appliquer les modifications
            udpdate = crd.modifier_utilisateur_par_id(
                cursor,
                id_data,
                nom_complet if nom_complet else utilisateur_a_modifier["nom_complet"],
                email if email else utilisateur_a_modifier["email"],
                password if password else utilisateur_a_modifier["password"],
                nom_utilisateur if nom_utilisateur else utilisateur_a_modifier["nom_utilisateur"]
            )
            # print(udpdate)
            return jsonify({"data": True}), 200
        else:
            return jsonify({"error": "Utilisateur non trouvé"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/etudiant', methods=['GET'])
def get_all_students():
    """
    Récupère tous les étudiants d'un professeur
    """
    try:
        id_data = request.args.get('id')
        cours_data = crd.get_cours_by_professeur_id(cursor, id_data)
        cours_dict = {}
        liste_cours = []
        for cours_id, cours_nom in cours_data:
            cours_existe = False
            for cours_item in liste_cours:
                if cours_item["cours_id"] == cours_id:
                    cours_existe = True
                    cours_dict = cours_item
                    break
            if not cours_existe:
                cours_dict = {"cours": cours_nom, "cours_id": cours_id, "etudiants": []}
            etudiants = crd.get_etudiants_by_cours(cursor, cours_id)
            for etudiant_id, nom_etudiant in etudiants:
                cours_dict["etudiants"].append({"nom": nom_etudiant, "etudiant_id": etudiant_id})
            if not cours_existe:
                liste_cours.append(cours_dict)
                response_data = {'data': liste_cours}
        #print(response_data)
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'Erreur': "cours_liste"})

@app.route('/prof', methods=['GET'])
def get_all_prof():
    """
    recuper tout les professeur  d'un etudiant """
    try:
        id_data = request.args.get('id')
        cours_data = crd.get_cours_by_etudiant_id(cursor,id_data)
        prof_dict = {}
        # Récupérer les données des étudiants pour chaque cours
        for cours_id, cours_nom in cours_data:
            profs = crd.get_professors_for_course(cursor, cours_id)
            for prof_id, nom_prof,utilisateur_id in profs:
                if nom_prof not in prof_dict:
                   prof_dict[nom_prof] = {'utilisateur_id': utilisateur_id,"nom_prof":nom_prof}
        noms_id_professeurs = []
        for nom_prof, info in prof_dict.items():
            utilisateur_id = info['utilisateur_id']
            nom_professeur = info['nom_prof']
            noms_id_professeurs.append({
                'utilisateur_id': utilisateur_id,
                'nom': nom_professeur
            })

        #print(noms_id_professeurs )
        response_data = {'data': noms_id_professeurs}
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'Erreur': "cours_liste"})
    
@app.route('/message', methods=['POST'])
def NewMessage():
    """
    issertion de nouveau message"""
    try:
        data = request.get_json()
        titre = data["titre"]
        contenu = data["message"]
        destinataire = data["destinateur"]
        expediteur = data["expediteur"]
        #print(f"titre {titre}  \ncontenu {contenu}\ndestination {destinataire}  \nexpéditeur {expéditeur}")
        msg = crd.insert_message(cursor,expediteur_id=expediteur,destinataire_id=destinataire,titre=titre,contenu=contenu)
        if msg:
            return jsonify({"data": True}), 200
        else :
            return jsonify({"data": False}),400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/message', methods=['GET'])
def get_message():
    """
    recuper les message d' utilisateur connect  """
    try:
        id_data = request.args.get('id')
        #print(id_data)
        #response_data = {'data': noms_id_professeurs}
        return jsonify("response_data"), 200
    except Exception as e:
        return jsonify({'Erreur': "cours_liste"})
    
@app.route('/add_disponibilite', methods=['POST'])
def Add_disponibilite():
    """
    issertion de nouveau disponibilite"""
    try:
        data = request.get_json()
        id_dispo_modifier = data.get("id_modifier")
        if id_dispo_modifier is not None:
            jour = data["jour"]
            heure_debut = data["heure_debut"]
            heure_fin = data["heure_fin"]
            datanew = crd.modifier_disponibilite(cursor,id_dispo_modifier,jour,heure_debut,heure_fin)
           # print(data)
            return jsonify({"data": True}),200
        else:
            jour = data["jour"]
            heure_debut = data["heure_debut"]
            heure_fin = data["heure_fin"]
            tuteur_id = data["tuteur_id"]
            newdisp = crd.ajouter_disponibilite(cursor,tuteur_id=tuteur_id,jour=jour,heure_fin=heure_fin,heure_debut=heure_debut)
        return jsonify({"data": True}),200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/get_disponibilite',methods=["GET"])
def get_disponibility():
    """
    Recuperation des disponibiltés par un tuteur ou par une date"""
    try:
        id_data = request.args.get('id')
        data = crd.get_disponibilites_by_tuteur_id(cursor,id_data)
        dispo_info = []
        for disponibilite in data:
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
        #print(dispo_info) 
        return jsonify({"data": dispo_info}),200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/delete_disponibilite',methods=["DELETE"])
def delete_disponibilite():
    """
    supprimer des disponibiltés par un tuteur"""
    try:
        id_data = request.args.get('id')
        data = crd.delete_disponibilite_by_id(cursor,id_data)

        return jsonify({"data": True}),200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/demande_tutorat', methods=["POST"])
def demande_tutorat():
    """
    assigne les Demande de Tutorat
    """
    try:
        data = request.get_json()
        list_etudiants = data.get("liste_etudiants")
        cours_id = data.get("cours_id")
        success, id_demande = crd.insert_demande_tutorat(cursor, cours_id)
        if success:
            try:
                for etudiant_id in list_etudiants:
                    data = crd.insert_into_Liste_Etudiants_Demandes(cursor, id_demande, etudiant_id)
                return jsonify({"data": True}), 200
            except Exception as e:
                cursor.rollback()
                return jsonify({"error": str(e)}), 500
        else:
            cursor.rollback()
            return jsonify({"data": False}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/list_demande_tuteur',methods=["GET"])
def demande():
    """
    Recuperation la liste des demande de tuteur connect  """
    try:
        id_tuteur = request.args.get('id')
        liste_demande = crd.get_demandes_tuteur_cours(cursor,id_tuteur)
        return jsonify({"data": liste_demande}),200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_tuteur',methods=["GET"])
def get_tuteur():
    """
    Recuperation la liste des tuteur"""
    try:
        id_data = request.args.get('id')
        data = crd.get_disponibilites_by_tuteur_id(cursor,id_data)
        # dispo_info = []
        # for disponibilite in data:
        #     id_disponibilite, tuteur_id, jour, heure_debut, heure_fin = disponibilite
        #     dispo_info.append({
        #         "Jour": jour,
        #         "Heures": {
        #             "heure_debut": f"{heure_debut.hour}:{heure_debut.minute:02}",
        #             "heure_fin": f"{heure_fin.hour}:{heure_fin.minute:02}"
        #         },
        #         "disponi-id": id_disponibilite
        #     })
        #print(dispo_info) 
        return jsonify({"data": "dispo_info"}),200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/set_cadidature',methods=["POST"])
def set_Cadidature():
    """
    Envoie de la cadidature de tuteur """
    try:
        data = request.get_json()
        sucess,set_cadidat = crd.insert_candidature_and_demande_postuler(cursor,data["id_tuteur"],data["id_demande"])
        if sucess:
           return jsonify({"data": {"sucess" : sucess,"statut_info":set_cadidat}}),200 
        else :
          return jsonify({"data": sucess}),401 
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_info_cadidature',methods=["GET"])
def get_info_cadidature():
    """
    Récupère les informations sur une candidature les donnes d'un tuteur  en fonction de son id """
    try:
        id_data = request.args.get('id')
        data =  crd.get_tutor_data_and_courses(cursor,id_data)
        #print(data)
        return jsonify({"data": data}),200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/liste_candidature',methods=["GET"])
def liste_candidature():
    """
    liste des candidature  """
    try:
        id_chef = request.args.get('id[id_chef]')
        data = crd.get_candidatures_with_info(cursor)
        #print(data)
        return jsonify({"liste_cadidature": data}),200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/liste_demande',methods=["GET"])
def liste_demande():
    """
    liste des Desmandes  """
    try:
        id_chef = request.args.get('id[chef_id]')
        data = crd.get_demandes_tutorat(cursor)
        #print(data)
        return jsonify({"liste_cadidature":data}),200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


