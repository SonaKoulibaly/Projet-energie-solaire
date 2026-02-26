# =============================================================================
# APP.PY — Cœur de l'application Dash | Projet Énergie Solaire
# Auteur : SK | Parc Photovoltaïque — Analyse & Monitoring
# Python 3.12 | Dash + Plotly + Bootstrap
# =============================================================================

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import os

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
    title="☀️ SolarDash — Parc Photovoltaïque",
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {"name": "description", "content": "Dashboard de monitoring du parc photovoltaïque"},
    ],
)

server = app.server  # Pour déploiement Gunicorn / Heroku / Render

# ─── CHARGEMENT ET PRÉPARATION DES DONNÉES ───────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "salar_data.csv")

def load_data():
    """Charge et prépare le dataset solaire."""
    df = pd.read_csv(DATA_PATH, sep=";")

    # Conversion datetime
    df["DateTime"] = pd.to_datetime(df["DateTime"], format="%d/%m/%Y %H:%M", errors="coerce")
    df["Date"]     = pd.to_datetime(df["Date"], format="%d/%m/%Y", errors="coerce")

    # ── Nettoyage ────────────────────────────────────────────────────────────
    df = df.dropna(subset=["DateTime"])
    df = df.sort_values("DateTime").reset_index(drop=True)

    # ── Features dérivées ────────────────────────────────────────────────────
    # Rendement AC/DC (%)
    df["Efficiency"] = np.where(
        df["DC_Power"] > 0,
        (df["AC_Power"] / df["DC_Power"] * 100).round(2),
        np.nan
    )

    # Perte de conversion
    df["Conversion_Loss"] = (df["DC_Power"] - df["AC_Power"]).round(3)

    # Tranche horaire
    def get_tranche(h):
        if   0 <= h < 6:  return "🌙 Nuit (0h–6h)"
        elif 6 <= h < 10: return "🌅 Matin (6h–10h)"
        elif 10<= h < 14: return "☀️ Midi (10h–14h)"
        elif 14<= h < 18: return "🌤️ Après-midi (14h–18h)"
        else:              return "🌆 Soir (18h–24h)"
    df["Tranche_Horaire"] = df["Hour"].apply(get_tranche)

    # Anomalie : DC = 0 pendant les heures solaires (8h–18h)
    df["Anomalie"] = (
        (df["Hour"] >= 8) & (df["Hour"] <= 18) & (df["DC_Power"] == 0)
    )

    # Saison
    def get_saison(m):
        if   m in [12, 1, 2]: return "❄️ Hiver"
        elif m in [3, 4, 5]:  return "🌸 Printemps"
        elif m in [6, 7, 8]:  return "☀️ Été"
        else:                  return "🍂 Automne"
    df["Saison"] = df["Month"].apply(get_saison)

    # Semaine du mois
    df["Week"] = df["DateTime"].dt.isocalendar().week.astype(int)
    df["DateStr"] = df["Date"].dt.strftime("%d/%m/%Y")

    return df


# ─── CHARGEMENT GLOBAL ───────────────────────────────────────────────────────
df = load_data()

# ─── CONSTANTES UTILES ───────────────────────────────────────────────────────
COUNTRIES   = sorted(df["Country"].unique().tolist())
MONTHS      = sorted(df["Month"].unique().tolist())
MONTH_NAMES = {
    1: "Janvier", 2: "Février",  3: "Mars",     4: "Avril",
    5: "Mai",     6: "Juin",     7: "Juillet",  8: "Août",
    9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"
}
COUNTRY_FLAGS = {
    "Norway":    "🇳🇴 Norvège",
    "Brazil":    "🇧🇷 Brésil",
    "India":     "🇮🇳 Inde",
    "Australia": "🇦🇺 Australie",
}

# ─── PALETTE COULEURS ────────────────────────────────────────────────────────
COLORS = {
    "primary":    "#F97316",   # Orange solaire
    "secondary":  "#0F172A",   # Bleu nuit
    "accent":     "#3B82F6",   # Bleu électrique
    "success":    "#10B981",   # Vert
    "warning":    "#FBBF24",   # Jaune
    "danger":     "#EF4444",   # Rouge
    "light":      "#F8FAFC",
    "card_bg":    "#1E293B",
    "text":       "#E2E8F0",
    "muted":      "#94A3B8",
}

# ─── LANCEMENT ───────────────────────────────────────────────────────────────
from layout import layout
from callbacks import register_callbacks

app.layout = layout
register_callbacks(app, df)

if __name__ == "__main__":
    app.run(debug=True, port=8472)
    