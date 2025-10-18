import csv
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('en_CA')  # Utilise le locale anglais canadien

class MeteoGenerator:
    """Générateur simple de données météorologiques simulées"""
    
    def __init__(self, seed=42):
        """
        Initialise le générateur avec un seed pour la reproductibilité
        """
        self.stations = []
        random.seed(seed)
        fake.seed_instance(seed)
        
    def generer_stations(self, nombre=10):
        """Génère un nombre donné de stations météo"""
        self.stations = []
        for _ in range(nombre):
            station = {
                'codeStation': str(random.randint(1000000000, 9999999999)),  # 10 chiffres
                'nomStation': f"Station {fake.city()}",
                'villeStation': fake.city()
            }
            self.stations.append(station)
        return self.stations
    
    def generer_temperatures(self, nombre_mesures=100):
        """Génère des mesures de température pour une année"""
        if not self.stations:
            self.generer_stations(5)  # Génère des stations par défaut
            
        mesures = []
        date_debut = datetime(2024, 1, 1)
        
        for _ in range(nombre_mesures):
            # Date aléatoire dans l'année
            jours_aleatoire = random.randint(0, 365)
            date_mesure = date_debut + timedelta(days=jours_aleatoire)
            
            # Station aléatoire
            station = random.choice(self.stations)
            
            # Génération des autres champs
            type_station = random.choice(['P', 'S', 'p', 's'])  # Peu importe la casse
            precipitation = round(random.uniform(0, 50), 1)  # mm
            nbr_polluants = random.randint(0, 10)
            
            # Températures variables (0 à 4) avec distribution réaliste
            # Ancienne version: nb_temperatures = random.randint(0, 4)
            nb_temperatures = random.randint(1, 4)
            
            temperatures = []
            for _ in range(nb_temperatures):
                # Températures en Fahrenheit (simule le Canada: -40°F à 100°F)
                temp = round(random.uniform(-40, 100), 1)
                temperatures.append(temp)
            
            mesure = {
                'dateMesure': date_mesure.strftime('%Y-%m-%d'),
                'codeStation': station['codeStation'],
                'typeStation': type_station,
                'precipitation': precipitation,
                'nbrPolluants': nbr_polluants,
                'temperature': temperatures
            }
            mesures.append(mesure)
            
        return mesures
    
    def exporter_stations_csv(self, fichier='stations.data'):
        """Exporte les stations en CSV"""
        if not self.stations:
            return
            
        with open(fichier, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['codeStation', 'nomStation', 'villeStation']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for station in self.stations:
                writer.writerow(station)
    
    def generer_donnees_non_conformes(self):
        """Génère des données non-conformes avec le signe '?' pour chaque colonne"""
        donnees_non_conformes = []
        
        # Station valide de référence
        station_ref = self.stations[0] if self.stations else {'codeStation': '1234567890'}
        
        # 1. codeStation: ? (reste des colonnes conforme)
        donnees_non_conformes.append({
            'dateMesure': '2024-06-15',
            'codeStation': '?',
            'typeStation': 'P',
            'precipitation': 25.3,
            'nbrPolluants': 3,
            'temperature': [12.5, 18.2]
        })
        
        # 2. dateMesure: ? (reste des colonnes conforme)
        donnees_non_conformes.append({
            'dateMesure': '?',
            'codeStation': station_ref['codeStation'],
            'typeStation': 'S',
            'precipitation': 18.7,
            'nbrPolluants': 5,
            'temperature': [22.1, 15.8, 19.3]
        })
        
        # 3. typeStation: ? (reste des colonnes conforme)
        donnees_non_conformes.append({
            'dateMesure': '2024-08-20',
            'codeStation': station_ref['codeStation'],
            'typeStation': '?',
            'precipitation': 31.2,
            'nbrPolluants': 2,
            'temperature': [28.4, 26.7]
        })
        
        # 4. precipitation: ? (reste des colonnes conforme)
        donnees_non_conformes.append({
            'dateMesure': '2024-09-10',
            'codeStation': station_ref['codeStation'],
            'typeStation': 'p',
            'precipitation': '?',
            'nbrPolluants': 7,
            'temperature': [16.9, 21.2, 18.5]
        })
        
        # 5. nbrPolluants: ? (reste des colonnes conforme)
        donnees_non_conformes.append({
            'dateMesure': '2024-11-05',
            'codeStation': station_ref['codeStation'],
            'typeStation': 'S',
            'precipitation': 42.8,
            'nbrPolluants': '?',
            'temperature': [8.3, 12.1]
        })
        
        # 6. temperature: ? (reste des colonnes conforme)
        donnees_non_conformes.append({
            'dateMesure': '2024-12-01',
            'codeStation': station_ref['codeStation'],
            'typeStation': 'P',
            'precipitation': 15.6,
            'nbrPolluants': 4,
            'temperature': '?'
        })
        
        return donnees_non_conformes

    def exporter_temperatures_csv(self, mesures, fichier='temperatures.data'):
        """Exporte les mesures de température en CSV"""
        with open(fichier, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['dateMesure', 'codeStation', 'typeStation', 'precipitation', 'nbrPolluants', 'temperature']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            # Écrire les mesures normales
            for mesure in mesures:
                # Convertit la liste de températures en string avec points-virgules (selon l'exemple)
                mesure_csv = mesure.copy()
                mesure_csv['temperature'] = ';'.join(map(str, mesure['temperature'])) if mesure['temperature'] else ''
                writer.writerow(mesure_csv)
            
            # Ajouter les données non-conformes
            donnees_non_conformes = self.generer_donnees_non_conformes()
            for donnee in donnees_non_conformes:
                donnee_csv = donnee.copy()
                # Traiter le champ température pour les données non-conformes
                if isinstance(donnee['temperature'], list):
                    donnee_csv['temperature'] = ';'.join(map(str, donnee['temperature']))
                else:
                    donnee_csv['temperature'] = donnee['temperature']  # Déjà une string "?"
                writer.writerow(donnee_csv)
