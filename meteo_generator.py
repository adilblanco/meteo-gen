import csv
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('fr_CA')  # Utilise le locale canadien français

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
            # Limite: distribution uniforme (20% pour chaque valeur) peu réaliste
            nb_temperatures = random.choices([0, 1, 2, 3, 4], weights=[2, 4, 4, 10, 80])[0]
            
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
    
    def exporter_temperatures_csv(self, mesures, fichier='temperatures.data'):
        """Exporte les mesures de température en CSV"""
        with open(fichier, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['dateMesure', 'codeStation', 'typeStation', 'precipitation', 'nbrPolluants', 'temperature']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for mesure in mesures:
                # Convertit la liste de températures en string avec points-virgules (selon l'exemple)
                mesure_csv = mesure.copy()
                mesure_csv['temperature'] = ';'.join(map(str, mesure['temperature'])) if mesure['temperature'] else ''
                writer.writerow(mesure_csv)