\# Dashboard Afrique 1975-2024 - FOR10A26-404

Projet Formuloo - Victus - Douala



\## Démo publique

URL Streamlit : https://\[ton-nom]-afrique.streamlit.app (à remplacer après déploiement)



\## Structure

\- `data/africa\_cleaned.csv` : 1000 lignes nettoyées

\- `app.py` : Dashboard 5+ visualisations Streamlit

\- `etape2.py` : Analyse exploratoire

\- `INSIGHTS.md` : 5 conclusions

\- Captures : dossier /screenshots



\## Lancement local

pip install -r requirements.txt

python -m streamlit run app.py



\## 5 Visualisations

1\. Vue d'ensemble KPIs (st.metric)

2\. Analyse temporelle (line Plotly)

3\. Comparaison géographique (bar)

4\. Corrélations (scatter)

5\. Distribution (histogramme + box plot)



Qualité : st.cache\_data <5s, layout=wide mobile, titres + descriptions, source citée.

