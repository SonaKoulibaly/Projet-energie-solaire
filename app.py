# =============================================================================
# APP.PY — Cœur de l'application Dash | Projet Énergie Solaire
# Auteur : Sona KOULIBALY (SK) | Parc Photovoltaïque — Analyse & Monitoring
# Python 3.12 | Dash + Plotly + Bootstrap
# =============================================================================

import os
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

# ─── CHARGEMENT DES VARIABLES D'ENVIRONNEMENT ─────────────────────────────────
# En local  : lit depuis .env via python-dotenv
# En production Render : lit depuis les variables configurées dans le dashboard Render
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv optionnel — ignoré en production

# ─── CONFIGURATION ────────────────────────────────────────────────────────────
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-prod")
DEBUG      = os.environ.get("DEBUG", "True").lower() == "true"
PORT       = int(os.environ.get("PORT", 8472))
DATA_PATH  = os.environ.get(
    "DATA_PATH",
    os.path.join(os.path.dirname(__file__), "data", "salar_data.csv")
)

# ─── INITIALISATION DE L'APPLICATION ─────────────────────────────────────────
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css",
    ],
    assets_folder="assets",
    suppress_callback_exceptions=True,
    title="SolarDash - Parc Photovoltaique",
    meta_tags=[
        {"name": "viewport",    "content": "width=device-width, initial-scale=1"},
        {"name": "description", "content": "Dashboard monitoring parc photovoltaique"},
    ],
)

# ─── SERVEUR FLASK — EXPOSÉ POUR GUNICORN (RENDER) ───────────────────────────
server = app.server
server.secret_key = SECRET_KEY


# ─── CHARGEMENT ET PRÉPARATION DES DONNÉES ───────────────────────────────────
def load_data():
    """Charge et prépare le dataset solaire."""
    df = pd.read_csv(DATA_PATH, sep=";")

    df["DateTime"] = pd.to_datetime(df["DateTime"], format="%d/%m/%Y %H:%M", errors="coerce")
    df["Date"]     = pd.to_datetime(df["Date"],     format="%d/%m/%Y",        errors="coerce")
    df = df.dropna(subset=["DateTime"]).sort_values("DateTime").reset_index(drop=True)

    # Features dérivées
    df["Efficiency"] = np.where(
        df["DC_Power"] > 0,
        (df["AC_Power"] / df["DC_Power"] * 100).round(2),
        np.nan
    )
    df["Conversion_Loss"] = (df["DC_Power"] - df["AC_Power"]).round(3)

    def get_tranche(h):
        if   0 <= h < 6:  return "Nuit (0h-6h)"
        elif 6 <= h < 10: return "Matin (6h-10h)"
        elif 10<= h < 14: return "Midi (10h-14h)"
        elif 14<= h < 18: return "Apres-midi (14h-18h)"
        else:              return "Soir (18h-24h)"
    df["Tranche_Horaire"] = df["Hour"].apply(get_tranche)

    def get_saison(m):
        if   m in [12, 1, 2]: return "Hiver"
        elif m in [3, 4, 5]:  return "Printemps"
        elif m in [6, 7, 8]:  return "Ete"
        else:                  return "Automne"
    df["Saison"]   = df["Month"].apply(get_saison)
    df["Anomalie"] = (df["Hour"] >= 8) & (df["Hour"] <= 18) & (df["DC_Power"] == 0)
    df["DateStr"]  = df["Date"].dt.strftime("%d/%m/%Y")

    return df


# ─── CHARGEMENT GLOBAL ───────────────────────────────────────────────────────
df = load_data()

# ─── CONSTANTES ──────────────────────────────────────────────────────────────
COUNTRIES   = sorted(df["Country"].unique().tolist())
MONTH_NAMES = {
    1:"Janvier", 2:"Fevrier",  3:"Mars",      4:"Avril",
    5:"Mai",     6:"Juin",     7:"Juillet",   8:"Aout",
    9:"Septembre",10:"Octobre",11:"Novembre", 12:"Decembre"
}
COUNTRY_FLAGS = {
    "Norway":    "Norvege",
    "Brazil":    "Bresil",
    "India":     "Inde",
    "Australia": "Australie",
}
COLORS = {
    "primary":  "#F97316",
    "secondary":"#0F172A",
    "accent":   "#3B82F6",
    "success":  "#10B981",
    "warning":  "#FBBF24",
    "danger":   "#EF4444",
    "light":    "#F8FAFC",
    "card_bg":  "#1E293B",
    "text":     "#E2E8F0",
    "muted":    "#94A3B8",
}

# ─── LAYOUT & CALLBACKS ───────────────────────────────────────────────────────
from layout import layout
from callbacks import register_callbacks

app.layout = layout
register_callbacks(app, df)

# ─── LANCEMENT ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=DEBUG, port=PORT)