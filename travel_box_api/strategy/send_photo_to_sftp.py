#!/bin/python3

"""
Date time cluster
"""

import json
import sys
import copy
import paramiko
import re

from travel_box_api.group.country_code import UNUSE_WORDS

clusters = {}

with sys.stdin as database:
    clusters = json.load(database)


def sort_cluster(clusters: dict) -> list: 
    list_of_path = {}
    for cluster_id, cluster in clusters.items():
        path = f"{cluster["contient"]}/{cluster["country"]}"
        path += f"/{cluster["region"]}"
        path += f"/{cluster["place"]}"
        for unuse_word in UNUSE_WORDS:
            path = path.replace(unuse_word, "")
        path = path.strip()
        path = path.replace(" /", "/")
        path = path.replace(" ", "_")
        path = re.sub(r"[^A-Za-z]*$", "", path)
        path = path.rstrip("-_")
        for photo_local_path in cluster["photos"].values():
            list_of_path.setdefault(path, []).append(photo_local_path["path"])
    return list_of_path


def upload_file_sftp(hostname, port, username, password, local_file, remote_path):
    """
    Envoie un fichier local vers un serveur SFTP.

    :param hostname: Adresse du serveur SFTP
    :param port: Port du serveur SFTP (par défaut : 22)
    :param username: Nom d'utilisateur
    :param password: Mot de passe
    :param local_file: Chemin du fichier local à envoyer
    :param remote_path: Chemin de destination sur le serveur
    """
    try:
        # Création de la connexion SFTP
        transport = paramiko.Transport((hostname, port))
        transport.connect(username=username, password=password)
        
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        # Envoi du fichier
        sftp.put(local_file, remote_path)
        print(f"Fichier {local_file} envoyé avec succès à {remote_path} sur {hostname}")
        
        # Fermeture de la connexion SFTP
        sftp.close()
        transport.close()
    except Exception as e:
        print(f"Erreur lors de l'envoi du fichier : {e}")

# Exemple d'utilisation
hostname = "aigyre.fr"
port = 22
username = ""
password = ""
remote_path = "/mnt/disk1/gallery/galleries/{}"

list_of_path_file = sort_cluster(clusters)
print(list_of_path_file)

for sorted_path, local_paths in list_of_path_file.items():
    print(remote_path.format(sorted_path))
    for local_path in local_paths:
        print(local_path)
    

#upload_file_sftp(hostname, port, username, password, local_file, remote_path)
