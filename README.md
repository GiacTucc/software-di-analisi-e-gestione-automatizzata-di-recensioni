**Machine Learning per Processi Aziendali**
**Smistamento recensioni hotel e analisi del sentiment**

N.B. 
I test sull'intero applicativo, compresi quelli sugli script di avvio e configurazione automatica, sono stati eseguiti solo su piattaforma Windows.

Per motivi di riproducibilità, il set di dati che ho utilizzato per l'addestramento e i test nello sviluppo è incluso nel repository, sotto la directory "dataset".

**Descrizione**
Il progetto realizza un sistema di classificazione automatica delle recensioni di una struttura con due obiettivi:
- **Assegnare il reparto corretto** (*Housekeeping, Reception, F&B*)
- **Determinare il sentiment** (*positivo o negativo*)

Il sistema comprende:
- Generazione automatica del dataset
- Pipeline di preprocessing
- Addestramento e valutazione dei modelli (train/test split 80/20)
- Interfaccia grafica opzionale per predizioni singole e batch

---

**Struttura del progetto**
- `dataset_generator.py`: Genera il dataset sintetico ed esporta il CSV
- `train_pipeline.py`: Addestra i modelli e calcola le metriche
- `gui.py`: Dashboard Streamlit per utilizzare i modelli
- `project_launcher.py`: Configura l'ambiente virtuale e installa le dipendenze necessarie
- `run_all.py`: Avvio completo automatico
- `requirements.txt`: Dipendenze

Tutti i file generati vengono salvati nella cartella:
`generated_files/`

Le librerie e le dipendenze necessarie per l’esecuzione del progetto verranno installate nella cartella: 
`venv/`

---

**Requisiti**

- Python 3.10 o superiore

---

**Esecuzione**
Metodo automatico (consigliato):
`python run_all.py`

Questo comando:
- Installa le dipendenze
- Genera il dataset
- Addestra i modelli
- Mostra le metriche
- Consente di avviare la dashboard

Metodo manuale:
- Installare le dipendenze:
`pip install -r requirements.txt`
- Generare il dataset:
`python dataset_generator.py`
- Addestrare i modelli:
`python train_pipeline.py`
- Avviare l’interfaccia grafica (opzionale):
`streamlit run gui.py`

---

**Output principali**
All’interno della cartella `generated_files/` vengono salvati:
- Dataset sintetico (CSV)
- Modelli addestrati (.pkl)
- Matrici di confusione
- Report delle metriche
- File delle predizioni batch (con timestamp)
