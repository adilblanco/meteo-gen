#!/usr/bin/env python3
"""
Script principal pour générer des données météorologiques simulées
Utilisation simple pour un projet universitaire
"""

from meteo_generator import MeteoGenerator

def main():
    # Créer le générateur
    generator = MeteoGenerator()
    
    print("Générateur de données météorologiques")
    print("=" * 50)
    
    # Générer 5 stations météo
    print("\n1. Génération des stations météo...")
    stations = generator.generer_stations(5)
    print(f"{len(stations)} stations générées")
    
    # Générer des mesures de température
    print("\n2. Génération des mesures de température...")
    mesures = generator.generer_temperatures(500)  # 500 mesures pour les analyses Spark
    print(f"{len(mesures)} mesures générées")
    
    # Exporter en CSV
    print("\n3. Export des données en .data...")
    generator.exporter_stations_csv('stations.data')
    generator.exporter_temperatures_csv(mesures, 'temperatures.data')
    print("Fichiers générés: stations.data, temperatures.data")
    
    print("\nGénération terminée!")

if __name__ == "__main__":
    main()