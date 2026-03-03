# ☀️ SolarDash — Dashboard de Monitoring Photovoltaïque

<div align="center">
## 🌐 Démo Live
👉 [Voir le dashboard en ligne](https://solardash-tghb.onrender.com)
![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Dash](https://img.shields.io/badge/Dash-2.17-orange?style=for-the-badge&logo=plotly)
![Plotly](https://img.shields.io/badge/Plotly-5.22-green?style=for-the-badge&logo=plotly)
![Pandas](https://img.shields.io/badge/Pandas-2.2-yellow?style=for-the-badge&logo=pandas)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

**Tableau de bord interactif pour le suivi et l'analyse de la production d'énergie solaire**

*Réalisé par **Sona KOULIBALY (SK)** — Mastère 2 Big Data & Data Strategy*

</div>

---

## 📋 Table des Matières

1. [Contexte & Problématique](#-contexte--problématique)
2. [Objectifs du Projet](#-objectifs-du-projet)
3. [Dataset](#-dataset)
4. [Architecture du Projet](#-architecture-du-projet)
5. [Fonctionnalités](#-fonctionnalités)
6. [Visualisations](#-visualisations)
7. [Installation](#-installation)
8. [Lancement](#-lancement)
9. [Utilisation](#-utilisation)
10. [Export & Rapports](#-export--rapports)
11. [Stack Technique](#-stack-technique)
12. [Auteur](#-auteur)

---

## 🌍 Contexte & Problématique

> **"Suivi et analyse de la production d'énergie solaire d'un parc photovoltaïque"**

La transition énergétique impose une gestion rigoureuse des parcs solaires. Ce projet répond à un besoin concret : **monitorer en temps réel la production d'un parc PV multi-sites**, détecter les anomalies, analyser l'impact des conditions environnementales et optimiser le rendement global.

Le dataset couvre **4 sites internationaux** (Norvège, Brésil, Inde, Australie) sur l'**année complète 2024**, avec une granularité horaire, soit **35 136 mesures** exploitées.

---

## 🎯 Objectifs du Projet

| # | Objectif | Statut |
|---|----------|--------|
| 1 | Suivre la production **horaire et journalière** des panneaux PV | ✅ |
| 2 | Détecter les **anomalies** (production nulle, écart réel vs théorique) | ✅ |
| 3 | Visualiser l'effet des **conditions environnementales** sur la production | ✅ |
| 4 | Comparer la production **DC vs AC** pour analyser l'efficacité | ✅ |
| 5 | Créer un **tableau de bord interactif** Plotly/Dash | ✅ |

---

## 📊 Dataset

**Fichier :** `data/salar_data.csv` — Séparateur `;`

**Dimensions :** 35 136 lignes × 14 colonnes

| Variable | Type | Description |
|----------|------|-------------|
| `Date` | date | Jour de mesure |
| `Time` | int | Heure de mesure (0–23) |
| `DateTime` | datetime | Combinaison Date + Time |
| `Country` | string | Pays du site (Norway, Brazil, India, Australia) |
| `DC_Power` | float | Puissance directe générée (kW) — avant conversion |
| `AC_Power` | float | Puissance après conversion (kW) — rendement réel |
| `Ambient_Temperature` | float | Température ambiante (°C) |
| `Module_Temperature` | float | Température des panneaux (°C) |
| `Irradiation` | float | Irradiation solaire (kW/m²) |
| `Day` | int | Jour du mois |
| `Month` | int | Mois (1–12) |
| `Hour` | int | Heure (0–23) |
| `Daily_Yield` | float | Production cumulée du jour (kWh) |
| `Total_Yield` | float | Production totale depuis début d'année (kWh) |

**Variables dérivées (calculées dans `app.py`) :**
- `Efficiency` = `AC_Power / DC_Power × 100` (rendement %)
- `Anomalie` = `DC_Power == 0` entre 8h–18h (booléen)
- `Tranche_Horaire` : Nuit / Matin / Midi / Après-midi / Soir
- `Saison` : Hiver / Printemps / Été / Automne

**Statistiques clés :**
- DC_Power moyen : **18.3 kW** | max : **83.5 kW** | Pic à **12h**
- Rendement AC/DC moyen : **~90.5%**
- Anomalies détectées (8h–18h) : **1 201** (dont 593 en Norvège)
- Irradiation moyenne : **0.303 kW/m²**

---

## 🗂️ Architecture du Projet

```
PROJET_ENERGIE/
│
├── 📄 app.py               # Cœur de l'application Dash
│                           # Chargement data, features dérivées, routing
│
├── 📄 layout.py            # Interface utilisateur complète
│                           # Navbar, Hero, Filtres, KPIs, Graphes, Export
│
├── 📄 callbacks.py         # Logique interactive (15+ callbacks)
│                           # Filtres, graphes, anomalies, exports
│
├── 📁 assets/
│   ├── 🖼️  logo.png        # Logo SolarDash
│   └── 🎨 style.css        # Thème dark solar (CSS complet)
│
├── 📁 data/
│   └── 📊 salar_data.csv   # Dataset principal (35 136 lignes)
│
├── 📁 docs/
│   └── 📁 screenshots/     # Captures d'écran du dashboard
│
├── 📋 requirements.txt     # Dépendances Python 3.12
├── 📋 README.md            # Documentation du projet
└── 🚫 .gitignore           # Fichiers exclus de Git
```

### Flux de données

```
salar_data.csv
      │
      ▼
   app.py ──── Chargement + Features dérivées (Efficiency, Anomalie...)
      │
      ▼
   layout.py ── Interface (Filtres → dcc.Store → Callbacks)
      │
      ▼
callbacks.py ── read_store() → Graphes Plotly + KPIs + Exports
      │
      ▼
   Navigateur ── Dashboard interactif http://127.0.0.1:8472
```

---

## ✨ Fonctionnalités

### 🎛️ Filtres Interactifs
- **Filtre Pays** : multi-sélection (Norvège, Brésil, Inde, Australie)
- **Filtre Mois** : multi-sélection (Janvier → Décembre)
- **RangeSlider Heure** : plage 0h–23h avec affichage dynamique
- **Bouton Réinitialiser** : retour aux valeurs par défaut en un clic

> Tous les filtres mettent à jour **simultanément** : KPIs, graphes, tableaux et alertes.

### 📈 KPI Cards (8 indicateurs)
- ⚡ Production DC Totale (kWh)
- 🔌 Production AC Totale (kWh)
- 📊 Rendement AC/DC Moyen (%)
- ☀️ Irradiation Moyenne (kW/m²)
- 🌡️ Température Module Moyenne (°C)
- ⚠️ Nombre d'Anomalies Détectées
- 🕐 Heure de Pic (DC max)
- 🏆 Meilleur Site (pays le plus productif)

### 🔍 Détection d'Anomalies
- Identification automatique des heures avec `DC_Power = 0` entre **8h et 18h**
- Alerte colorée (🟢 Normal / 🟡 Attention / 🔴 Critique)
- Tableau détaillé avec tri et filtres natifs
- Scatter chart annoté avec zone solaire surlignée

### 📥 Export Triple Format
- **Excel (.xlsx)** : 4 onglets (Données brutes, KPIs, Anomalies, Agrégation horaire)
- **PDF** : Rapport structuré avec KPIs, tableau comparatif et synthèse
- **HTML interactif** : 3 graphes Plotly embarqués, partageable sans installation

---

## 📊 Visualisations

| # | Graphe | Type | Ce qu'on voit |
|---|--------|------|---------------|
| 1 | **DC vs AC par Heure** | Line chart + fill | Tendance production + pertes conversion |
| 2 | **Production Cumulée Journalière** | Area chart | Progression Daily_Yield dans la journée |
| 3 | **Rendement AC/DC par Mois** | Bar groupé | Saisonnalité du rendement |
| 4 | **Production Totale par Pays** | Bar horizontal | Comparaison DC vs AC par site |
| 5 | **Total Yield — Tendance Annuelle** | Area chart | Croissance cumulative par pays |
| 6 | **Heatmap Irradiation × Production** | Heatmap | Intensité solaire Mois × Heure |
| 7 | **Température Module vs DC Power** | Scatter + tendance | Relation chaleur/production |
| 8 | **Profil d'Irradiation Horaire** | Line + plage | Ensoleillement moyen ± variance |
| 9 | **Température Ambiante vs Module** | Multi-axes | ΔT ambiant/panneau par heure |
| 10 | **Anomalies Scatter** | Scatter annoté | Points rouges = anomalies détectées |
| 11 | **Anomalies par Pays & Mois** | Bar empilé | Distribution temporelle des anomalies |

---

## ⚙️ Installation

### Prérequis
- Python **3.12** minimum
- pip à jour

### Étapes

```bash
# 1. Cloner le dépôt
git clone https://github.com/SonaKoulibaly/projet-energie-solaire.git
cd projet-energie-solaire

# 2. Créer l'environnement virtuel
python -m venv .venv

# 3. Activer l'environnement
# Windows :
.venv\Scripts\activate
# macOS / Linux :
source .venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt
```

### Dépendances principales

```
dash==2.17.1
dash-bootstrap-components==1.6.0
plotly==5.22.0
pandas==2.2.2
numpy==1.26.4
openpyxl==3.1.3
reportlab==4.2.2
gunicorn==22.0.0
```

---

## 🚀 Lancement

```bash
# Mode développement (debug activé)
python app.py

# Ouvrir dans le navigateur :
# http://127.0.0.1:8472
```

> **Port :** `8472` (rarement utilisé, peu de conflits)
>
> **Mode production :** `gunicorn app:server -b 0.0.0.0:8472`

---

## 🖥️ Utilisation

### Navigation
Le dashboard est divisé en **5 sections** accessibles via la navbar :

| Section | Contenu |
|---------|---------|
| **Vue Globale** | Hero banner + 8 KPI cards |
| **Production** | 5 graphes production DC/AC |
| **Environnement** | 4 graphes conditions climatiques |
| **Anomalies** | Alerte + scatter + tableau détaillé |
| **Rapport** | Exports Excel / PDF / HTML + tableau preview |

### Workflow recommandé
1. Sélectionner un **pays** dans le filtre
2. Affiner par **mois** (ex: été vs hiver)
3. Ajuster la **plage horaire** (ex: 8h–18h uniquement)
4. Observer les **KPIs** et les **graphes** se mettre à jour
5. Consulter les **anomalies** détectées
6. **Exporter** les résultats en Excel / PDF / HTML

---

## 📤 Export & Rapports

### Export Excel
Téléchargement direct sur le PC avec **4 onglets** :
- `Données_Brutes` — toutes les colonnes filtrées
- `KPIs_par_Pays` — DC total, AC total, rendement, température
- `Anomalies` — uniquement les heures anormales
- `Agrégation_Horaire` — moyennes par pays × mois × heure

### Export PDF (ReportLab)
Rapport structuré A4 avec :
- Tableau des 8 KPIs
- Tableau comparatif par pays (DC, AC, rendement, anomalies)
- Synthèse & interprétation narrative

### Export HTML Interactif
Fichier `.html` autonome avec **3 graphes Plotly embarqués** :
- DC vs AC par heure
- Heatmap DC Power
- Évolution Total Yield par pays

---

## 🛠️ Stack Technique

| Catégorie | Technologie | Usage |
|-----------|-------------|-------|
| **Language** | Python 3.12 | Backend & data processing |
| **Framework** | Dash 2.17 | Application web interactive |
| **Visualisation** | Plotly 5.22 | 11 graphes interactifs |
| **UI Components** | Dash Bootstrap Components | Layout responsive |
| **Data** | Pandas 2.2, NumPy 1.26 | Manipulation & calculs |
| **Export Excel** | openpyxl 3.1 | Génération .xlsx multi-onglets |
| **Export PDF** | ReportLab 4.2 | Rapport PDF structuré |
| **Style** | CSS3 custom | Thème dark solar |
| **Fonts** | Poppins (Google Fonts) | Typographie |
| **Icons** | Font Awesome 6.4 | Icônes UI |
| **Déploiement** | Gunicorn | Serveur production |

---

## 📸 Captures d'Écran

> Captures disponibles dans `docs/screenshots/`

| Fichier | Description |
|---------|-------------|
| `01_hero_kpis.png` | Vue globale — Hero banner + 8 KPI cards |
| `02_filtres.png` | Panel de filtres — pays, mois, slider heure |
| `03_production_dc_ac.png` | Courbe DC vs AC par heure |
| `04_heatmap.png` | Heatmap Irradiation × Production |
| `05_scatter_temperature.png` | Nuage de points Température vs DC |
| `06_anomalies.png` | Section anomalies — alerte + scatter |
| `07_export.png` | Section export — 3 boutons |
| `08_tableau_preview.png` | Tableau de prévisualisation des données |

---

## 👤 Auteur

<div align="center">

**Sona KOULIBALY**
*alias* **SK**

Mastère 2 Big Data & Data Strategy

📧 GitHub : [@SonaKoulibaly](https://github.com/Sonakoulibaly)

*"Faire parler les données pour éclairer les décisions énergétiques"*

---

**Réalisé avec :** Python 3.12 · Dash · Plotly · Pandas · ReportLab

</div>

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

<div align="center">
☀️ <em>SolarDash — Monitoring Parc Photovoltaïque · 2024</em> ☀️

</div>
