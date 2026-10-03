import pandas as pd
import plotly.express as px

# Chargement
try:
    df = pd.read_csv("data/africa_cleaned.csv")
except:
    df = pd.read_csv("data/africa.csv")

print("=== ÉTAPE 2 - ANALYSE EXPLORATOIRE FOR10A26-404 ===\n")

# 1. Statistiques descriptives
print("1. STATISTIQUES DESCRIPTIVES")
num_cols = df.select_dtypes(include='number').columns
desc = df[num_cols].describe().T
desc['median'] = df[num_cols].median()
print(desc[['count','min','max','mean','median','std']].to_string())
print("\n")

# 2. Matrice de corrélation
print("2. CORRELATIONS")
corr = df[num_cols].corr()
print(corr.to_string())
# Graphique heatmap correlation
fig_corr = px.imshow(corr, text_auto=True, title="Matrice de corrélation - Variables numériques")
fig_corr.write_html("correlation.html")
print("-> correlation.html créé\n")

# 3. Top 10 et Flop 10 (sur PIB_hab)
print("3. TOP 10 et FLOP 10 selon PIB_hab")
if 'PIB_hab' in df.columns:
    top10 = df.sort_values('PIB_hab', ascending=False).head(10)[['pays','annee','PIB_hab','region']]
    flop10 = df.sort_values('PIB_hab', ascending=True).head(10)[['pays','annee','PIB_hab','region']]
    print("TOP 10:\n", top10.to_string(index=False))
    print("\nFLOP 10:\n", flop10.to_string(index=False))
    top10.to_csv("top10.csv", index=False)
    flop10.to_csv("flop10.csv", index=False)
print("\n")

# 4. Évolution temporelle
print("4. EVOLUTION TEMPORELLE")
evol = df.groupby('annee')[['PIB_hab','esperance_vie','IDH']].mean().reset_index()
print(evol.tail(10).to_string(index=False))
fig_evol = px.line(evol, x='annee', y=['PIB_hab','esperance_vie'], title="Évolution moyenne PIB_hab et Espérance de vie 1975-2024")
fig_evol.write_html("evolution_temporelle.html")
print("-> evolution_temporelle.html créé\n")

# 5. Comparaisons régionales
print("5. COMPARAISONS REGIONALES")
regional = df.groupby('region')[['PIB_hab','esperance_vie','IDH','taux_alphabetisation']].mean()
print(regional.to_string())
fig_reg = px.bar(regional.reset_index(), x='region', y='PIB_hab', color='region', title="Comparaison PIB/hab moyen par région (Ouest vs Est vs Nord etc.)")
fig_reg.write_html("comparaison_regionale.html")
print("-> comparaison_regionale.html créé\n")

print("=== FIN ÉTAPE 2 - Tous les fichiers générés ===")