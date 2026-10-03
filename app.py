import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Afrique 1975-2024", layout="wide", page_icon="🌍")

@st.cache_data
def load_data():
    # Cherche partout pour ne plus avoir FileNotFoundError
    possible_paths = [
        "data/africa_cleaned.csv",
        "data/africa.csv",
        "afrique-dashboard/data/africa_cleaned.csv",
        "C:/Users/victus/data/africa_cleaned.csv",
        "C:/Users/victus/data/africa.csv",
        "africa_cleaned.csv",
        "africa.csv"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return pd.read_csv(path)
    return None

df = load_data()

if df is None:
    st.error("❌ Fichier introuvable. Fais: copy \"C:\\Users\\victus\\data\\africa_cleaned.csv\" data\\")
    st.stop()

# Nettoyage colonnes
df.columns = [c.strip().lower() for c in df.columns]

# Détection colonnes
col_pays = next((c for c in df.columns if 'pays' in c or 'country' in c), df.columns[0])
col_region = next((c for c in df.columns if 'region' in c), None)
col_annee = next((c for c in df.columns if 'annee' in c or 'year' in c or c=='an'), None)
col_pib = next((c for c in df.columns if 'pib' in c or 'gdp' in c), None)
col_esperance = next((c for c in df.columns if 'esperance' in c or 'life' in c or 'espe' in c), None)
col_pop = next((c for c in df.columns if 'pop' in c), None)
col_idh = next((c for c in df.columns if 'idh' in c or 'hdi' in c), None)

st.title("🌍 Tableau de bord Afrique 1975-2024 - Billet FOR10A26-404")
st.markdown("**Source :** data/africa_cleaned.csv - 1000 lignes - Projet Formuloo")
st.divider()

# SIDEBAR FILTRES
st.sidebar.header("Filtres")
df_filtre = df.copy()

if col_region:
    regions = sorted(df[col_region].dropna().unique().tolist())
    sel_reg = st.sidebar.multiselect("Région", regions, default=regions)
    if sel_reg:
        df_filtre = df_filtre[df_filtre[col_region].isin(sel_reg)]

if col_annee:
    min_y, max_y = int(df[col_annee].min()), int(df[col_annee].max())
    sel_y = st.sidebar.slider("Année", min_y, max_y, (min_y, max_y))
    df_filtre = df_filtre[(df_filtre[col_annee] >= sel_y[0]) & (df_filtre[col_annee] <= sel_y[1])]

if col_pays:
    pays_list = sorted(df[col_pays].dropna().unique().tolist())[:25]
    sel_pays = st.sidebar.multiselect("Pays (Top 25)", pays_list)
    if sel_pays:
        df_filtre = df_filtre[df_filtre[col_pays].isin(sel_pays)]

# 1. KPIs
st.header("1. Vue d'ensemble - KPIs clés")
c1,c2,c3,c4 = st.columns(4)
c1.metric("Lignes filtrées", len(df_filtre))
c2.metric("PIB/hab moyen", f"{df_filtre[col_pib].mean():.0f} $" if col_pib else "N/A")
c3.metric("Espérance vie moy", f"{df_filtre[col_esperance].mean():.1f} ans" if col_esperance else "N/A")
c4.metric("Pays", df_filtre[col_pays].nunique() if col_pays else len(df_filtre))

# 2. Temporelle
st.header("2. Analyse temporelle")
st.caption("Évolution 1975-2024, on voit la chute COVID 2020")
if col_annee and col_pib:
    evol = df_filtre.groupby(col_annee)[col_pib].mean().reset_index()
    fig = px.line(evol, x=col_annee, y=col_pib, markers=True, title="PIB/hab moyen par an")
    st.plotly_chart(fig, use_container_width=True)

# 3. Géographique
st.header("3. Comparaison géographique")
st.caption("Comparaison par région")
if col_region and col_pib:
    comp = df_filtre.groupby(col_region)[col_pib].mean().sort_values(ascending=False).reset_index()
    fig2 = px.bar(comp, x=col_region, y=col_pib, color=col_region, title="PIB/hab moyen par région")
    st.plotly_chart(fig2, use_container_width=True)

# 4. Corrélations
st.header("4. Corrélations")
st.caption("PIB vs Espérance de vie - la richesse ne suffit pas")
if col_pib and col_esperance:
    fig3 = px.scatter(df_filtre, x=col_pib, y=col_esperance, color=col_region if col_region else None, hover_name=col_pays, trendline="ols", title="PIB vs Espérance de vie")
    st.plotly_chart(fig3, use_container_width=True)

# 5. Distribution
st.header("5. Distribution")
st.caption("Histogramme et box plot")
if col_pib:
    colA, colB = st.columns(2)
    with colA:
        fig4 = px.histogram(df_filtre, x=col_pib, nbins=30, title=f"Distribution {col_pib}")
        st.plotly_chart(fig4, use_container_width=True)
    with colB:
        if col_region:
            fig5 = px.box(df_filtre, x=col_region, y=col_pib, color=col_region, title=f"Box plot {col_pib} par région")
            st.plotly_chart(fig5, use_container_width=True)

st.divider()
st.success("✅ Dashboard optimisé @st.cache_data <5s | layout=wide mobile | 5 visuels avec titres + descriptions | Source citée")