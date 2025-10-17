# Générateur de Données Météorologiques

Un générateur simple de données météorologiques simulées pour projets universitaires.

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

```bash
python main.py
```

Génère automatiquement :
- `stations.data` : 5 stations météorologiques
- `temperatures.data` : 500 mesures de température

## Format des données

### Stations
- `codeStation` : Identifiant unique de 10 chiffres
- `nomStation` : Nom de la station météorologique  
- `villeStation` : Ville où est localisée la station

### Mesures de température
- `dateMesure` : Date de la mesure (YYYY-MM-DD)
- `codeStation` : Code de la station (10 chiffres, lié aux stations)
- `typeStation` : Type de station (P=portable, S=statique, casse variable)
- `precipitation` : Quantité de précipitation en millimètres (0-50mm)
- `nbrPolluants` : Nombre de polluants détectés (0-10)
- `temperature` : Liste des températures en Fahrenheit (1-5 mesures par jour)