"""
Script che contiene l'implementazione dell'interfaccia grafica facoltativa
"""

import streamlit as st
import joblib
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title='Dashboard', layout='centered') #layout pagina
st.header('Dashboard - Smistamento recensioni hotel e analisi sentimento con machine learning', divider='orange')

#Cache delle risorse: i modelli vengono caricati una sola volta
#per evitare ricaricamenti inutili ad ogni interazione
@st.cache_resource 
def load_models():
    dep = joblib.load(os.path.join('generated_files', 'model_department.pkl')) 
    sent = joblib.load(os.path.join('generated_files', 'model_sentiment.pkl'))
    return dep, sent

try:
    dep_model, sent_model = load_models() #caricamento dei modelli
except Exception as e: #in caso di problemi viene visualizzato questo messaggio e tutto si interrompe
    st.error("Modelli non trovati: esegui prima train_pipeline.py. Errore: " + str(e))
    st.stop()

st.subheader('Predizione singola:')
title = st.text_input('Titolo:') #campi input
body = st.text_area('Testo recensione:')
if st.button('Analizza recensione'): #click del bottone
    if not title.strip() or not body.strip(): #.strip rimuove spazi all'inizio e alla fine
        st.warning('Inserisci sia il titolo che il testo della recensione!')
    else:
        text = (title) + '. ' + (body) #creazione della recensione mettendo titolo e body assieme
        #[0] perchè predict anche se passi un solo elemento restituisce un array
        dep_pred = dep_model.predict([text])[0] 
        sent_pred = sent_model.predict([text])[0]
        #.max prende la probabilità più alta, predict_proba restituisce infatti la probabilità per tutte le classi, es. [[0.10, 0.80, 0.10]]
        dep_prob = dep_model.predict_proba([text]).max() 
        sent_prob = sent_model.predict_proba([text]).max()
        st.success(f"Reparto consigliato: {dep_pred} (conf. {dep_prob:.2f})") #.2f per prendere solo due cifre dopo la virgola
        st.success(f"Sentiment: {'positive' if sent_pred==1 else 'negative'} (conf. {sent_prob:.2f})")
st.divider()

st.subheader('Predizione batch (CSV):')
uploaded = st.file_uploader('Carica CSV con colonne id,title,body:', type=['csv'])
if uploaded is not None:
    try: 
        df = pd.read_csv(uploaded)
        required_cols = {'id', 'title', 'body'} 
        if not required_cols.issubset(df.columns): #nel caso in cui il csv avesse le colonne sbagliate mostro un errore
            st.error(f"Il file CSV deve contenere le colonne: {', '.join(required_cols)}")
        else:
            df['text'] = df['title'].fillna('') + '. ' + df['body'].fillna('')
            preds_dep = dep_model.predict(df['text'])
            #axis=1 farà prendere il massimo per riga (per ogni recensione)
            #per esempio da: [[0.10, 0.80, 0.10], [0.60, 0.20, 0.20], [0.05, 0.15, 0.80]]
            #prenderà: [0.80, 0.60, 0.80]
            probs_dep = dep_model.predict_proba(df['text']).max(axis=1) 
            preds_sent = sent_model.predict(df['text'])
            probs_sent = sent_model.predict_proba(df['text']).max(axis=1)
            df_out = df.copy()
            df_out['department_pred'] = preds_dep #aggiunta delle colonne con i risultati delle predizioni
            df_out['department_confidence'] = probs_dep
            df_out['sentiment_pred'] = ['positive' if p==1 else 'negative' for p in preds_sent]
            df_out['sentiment_confidence'] = probs_sent
            st.dataframe(df_out[['id','title','department_pred','department_confidence','sentiment_pred','sentiment_confidence']])
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S') #.strftime formatta oggetto datetime in stringa
            out_name = f'generated_files/predictions_batch_{timestamp}.csv' #f per indicare che non è semplice testo, ma ci sono variabili
            df_out.to_csv(out_name, index=False) #tolgo l'indice automatico che mette Pandas con index=False
            st.markdown(f"Risultati salvati in: `{out_name}`")
    except Exception as e:
        st.error(f"Errore nel caricamento del file: {e}")