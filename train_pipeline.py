"""
    Script di addestramento per il modello di machine learning, che classifica le recensioni in base al
    reparto di riferimento (Housekeeping, Reception, F&B) e sentiment (positivo/negativo).
    Tutti i file generati (modelli, grafici, report sugli errori) sono salvati nella cartella generated_files/.
"""

import matplotlib.pyplot as pyplot #serve per creare grafici e visualizzazioni
import os #libreria per interagire con il sistema operativo
from datetime import datetime #per gestire date e orari
import pandas as pandas #libreria per la manipolazione e l'analisi dei dati
import numpy as numpy #libreria per il calcolo scientifico
import joblib #libreria per salvare e caricare oggetti in modo molto veloce

#sklearn è una libreria di machine learning, permette di creare, addestrare e valutare modelli di ML senza 
#dover implementare tutti i vari algoritmi da zero. Da essa importo varie funzioni e classi:
from sklearn.model_selection import train_test_split #per dividere il dataset in training set e test set
#(Training set: dati su cui il modello impara. Test set: dati su cui verifichi se il modello funziona bene 
# su dati mai visti).
from sklearn.feature_extraction.text import TfidfVectorizer #per convertire il testo in una rappresentazione numerica, in modo che il modello di ML possa elaborarlo
from sklearn.linear_model import LogisticRegression #algoritmo di classificazione, che uso per predire le classi (reparto e sentiment)
from sklearn.pipeline import Pipeline #per concatenare più passaggi in un'unica catena
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report #funzioni varie per valutare le performance del modello


#Costanti e percorsi file:
CSV_PATH = 'generated_files/reviews_dataset.csv'
RANDOM_STATE = 42
TEST_SIZE = 0.2
MODEL_DEP_PATH = os.path.join('generated_files', 'model_department.pkl') 
MODEL_SENT_PATH = os.path.join('generated_files', 'model_sentiment.pkl')

#Organizzo i dati:
dataframe = pandas.read_csv(CSV_PATH) #leggo il file .csv che ho generato con il dataset al suo interno, in pandas si chiama DataFrame
dataframe['complete_review'] = dataframe['title'].fillna('') + '. ' + dataframe['body'].fillna('') #creo una nuova colonna 'complete_review' nel dataframe che unisce titolo e corpo della recensione, gestendo i valori vuoti

#Convenzione nel ML e nella statistica:
#X indica le variabili indipendenti, ovvero gli input per addestrare il modello (nel mio caso le recensioni)
#y indica le variabili dipendenti, ovvero le etichette che il modello deve predire (nel mio caso reparto e sentiment)
X = dataframe['complete_review'] #lista delle recensioni (titolo + corpo)
y_department = dataframe['department'] #lista delle etichette di reparto per ogni recensione
y_sentiment = (dataframe['sentiment'] == 'positive').astype(int) #lista delle etichette di sentiment (1=positivo, 0=negativo) per ogni recensione

#Split del dataset in training set e test set:
#test_size indica la percentuale di dati che voglio riservare al test set (0.2 è 20% in questo caso, come richiesto da traccia)
#random_state fissa la casualità, così la divisione in train e test resta sempre uguale.
#stratify serve per mantenere la stessa proporzione di reparto sia nel training set che nel test set,
#gli stai dicendo, quando dividi i dati assicurati che nel train e nel test set ci siano le stesse proporzioni di reparto del 
# dataset originale, eviterà quindi che nel test ci siano solo recensioni del reparto Reception.
X_train, X_test, y_department_train, y_department_test, y_sentiment_train, y_sentiment_test = train_test_split(
    X, y_department, y_sentiment, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y_department
)

#Pipeline per dedurre il reparto:
#Una pipeline è una catena di passaggi che trasformano i dati e li passano al modello di ML.
#In questo caso, la pipeline ha due passaggi:
#1.TfidfVectorizer: converte il testo delle recensioni in numeri usando TF-IDF (Term Frequency-Inverse Document Frequency),
# che aiuta a evidenziare le parole più importanti in ogni recensione.
#2.LogisticRegression: è l'algoritmo di classificazione che userò per predire il reparto basandomi 
# sulle caratteristiche estratte dal testo.
pipe_dep = Pipeline([
    ('tfidataframe', TfidfVectorizer(
        lowercase=True, 
        token_pattern=r"(?u)\b\w+\b", #token_pattern accetta una regEx, qui gli sto dicendo di accettare parole accentate e singoli caratteri.
        ngram_range=(1,2), #ngram_range=(1,2) significa che considera sia singole parole (unigrammi) che coppie di parole (bigrammi).
        # utile per essere più preciso, altrimenti potrebbe scambiare "buono" per positivo anche se in realtà si trova con un "non" davanti.
        max_features=5000 #max_features=5000 limita il numero di caratteristiche a 5000, per evitare lentezza e inefficienza.
            # Per caratteristiche (o features) si intendono le parole o combinazioni di parole estratte dal testo 
            # che il modello userà per fare previsioni.
        )
    ),
    ('clf', LogisticRegression(
        max_iter=1000, #numero massimo di iterazioni per l'algoritmo di ottimizzazione
        solver='lbfgs' #algoritmo di ottimizzazione usato per calcolare i pesi del modello in modo efficiente.
            #è usato per classificazioni multiclasse (come in questo caso, visto che noi abbiamo 3 dipartimenti)
        )
    )
])

#Pipeline per dedurre il sentiment:
pipe_sent = Pipeline([
    ('tfidataframe', TfidfVectorizer(
        lowercase=True, 
        token_pattern=r"(?u)\b\w+\b", 
        ngram_range=(1,2), 
        max_features=5000)),
    ('clf', LogisticRegression(
        max_iter=1000, 
        solver='liblinear' #algoritmo di ottimizzazione adatto per classificazioni binarie (positivo/negativo in questo caso)
        )
    )
])

#Addestro i modelli:
#.fit fa partire l'addestramento del modello vero e proprio, usiamo ovviamente il training set creato prima per questo scopo
pipe_dep.fit(X_train, y_department_train)
pipe_sent.fit(X_train, y_sentiment_train)

#---------
#Salva modelli:
joblib.dump(pipe_dep, MODEL_DEP_PATH)
joblib.dump(pipe_sent, MODEL_SENT_PATH)
print(f"Modelli salvati in {MODEL_DEP_PATH} e {MODEL_SENT_PATH}")

#Predizioni test set:
y_department_pred = pipe_dep.predict(X_test)
y_sentiment_pred = pipe_sent.predict(X_test)

#Funzione comune per creare e salvare il grafico degli F1-Score:
def generate_f1_score_graph(y_true, y_pred, labels, title='', save_path='', figsize=(5,3)):
    report = classification_report(y_true, y_pred, output_dict=True)
    f1_scores = {label: report[str(label)]['f1-score'] for label in labels}

    pyplot.figure(figsize=figsize)
    pyplot.bar(f1_scores.keys(), f1_scores.values())
    pyplot.ylim(0, 1)
    pyplot.ylabel('F1-Score')
    pyplot.title(title)
    pyplot.tight_layout()
    pyplot.savefig(os.path.join('generated_files', save_path))
    pyplot.close()
    print(f"Salvato: {save_path}")

#Funzione comune per generare e salvare la matrice di confusione come grafico:
def generate_confusion_matrix_graph(conf_matr, labels, target_name='', save_path='', figsize=(6,4)):
    pyplot.figure(figsize=figsize)
    pyplot.imshow(conf_matr, interpolation='nearest', cmap=pyplot.cm.Blues)
    pyplot.title(target_name)
    pyplot.colorbar()
    tick_marks = numpy.arange(len(labels))
    pyplot.xticks(tick_marks, labels, rotation=45)
    pyplot.yticks(tick_marks, labels)
    thresh = conf_matr.max() / 2.
    for i, j in numpy.ndindex(conf_matr.shape):
        pyplot.text(j, i, format(conf_matr[i, j], 'd'),
                 horizontalalignment="center",
                 color="white" if conf_matr[i, j] > thresh else "black")
    pyplot.ylabel('True label')
    pyplot.xlabel('Predicted label')
    pyplot.tight_layout()
    pyplot.savefig(os.path.join('generated_files', save_path)) 
    pyplot.close()
    print("Salvato: " + save_path)

#Funzione che gestisce tutte le metriche e i report:
def metrics_report(y_true, y_pred, labels=None, target_name='', save_path='', figsize=(6,4)):
    acc = accuracy_score(y_true, y_pred)
    f1_macro = f1_score(y_true, y_pred, average='macro')
    conf_matr = confusion_matrix(y_true, y_pred, labels=labels)

    #Stampa nel prompt le metriche e il report di classificazione:
    print(f"\n*===* {target_name} *===*")
    print(f"Accuracy: {acc:.4f}")
    print(f"F1-(macro): {f1_macro:.4f}")

    #Genera e salva i grafici:
    generate_f1_score_graph(
        y_true,
        y_pred,
        labels=labels,
        title=target_name,
        save_path='f1-score' + save_path
    )
    generate_confusion_matrix_graph(
        conf_matr,
        labels,
        target_name=target_name,
        save_path='confusion_matrix' + save_path,
        figsize=figsize
    )


labels_dep = sorted(dataframe['department'].unique()) #labels per il reparto
labels_sent = sorted(dataframe['sentiment'].unique()) #labels per il sentiment
label_number_sent = [1 if s == 'positive' else 0 for s in labels_sent] #etichette di sentiment in numeri (1=positivo, 0=negativo)
#faccio partire il gestore delle metriche e dei report sia per il reparto che per il sentiment:
metrics_report(
    y_true=y_department_test,
    y_pred=y_department_pred,
    labels=labels_dep,
    target_name='Department',
    save_path='_department.png',
    figsize=(6, 4)
)    
metrics_report(
    y_true=y_sentiment_test,
    y_pred=y_sentiment_pred,
    labels=label_number_sent, #(1=positivo, quindi recensioni positive, 0=negativo, quindi recensioni negative)
    target_name='Sentiment',
    save_path='_sentiment.png',
    figsize=(4, 3)
)

#Funzione generica per salvare gli errori in un file CSV:
def save_errors(X_test, y_true, y_pred, label_name, filename, dataframe):
    #Creazione DataFrame degli errori
    errors = pandas.DataFrame({
        'id': dataframe.loc[X_test.index, 'id'],
        'complete_review': X_test,
        f'{label_name}_true': y_true.values,
        f'{label_name}_pred': y_pred
    })
    #Filtra solo gli errori
    errs = errors[errors[f'{label_name}_true'] != errors[f'{label_name}_pred']]
    #Salva su CSV
    errs.to_csv(os.path.join('generated_files', filename), index=False)
    print(f"Salvata lista errori: {filename} (n={len(errs)})")

print("")
#Errori department
save_errors(X_test, y_department_test, y_department_pred, 'dep', 'department_errors.csv', dataframe)
#Errori sentiment
save_errors(X_test, y_sentiment_test, y_sentiment_pred, 'sent', 'sentiment_errors.csv', dataframe)

#Export predizioni test set:
out = pandas.DataFrame({
    'id': dataframe.loc[X_test.index, 'id'],
    'title': dataframe.loc[X_test.index, 'title'],
    'body': dataframe.loc[X_test.index, 'body'],
    'complete_review': X_test,
    'department_true': y_department_test.values,
    'department_pred': y_department_pred,
    'sentiment_true': ['positive' if s==1 else 'negative' for s in y_sentiment_test],
    'sentiment_pred': ['positive' if s==1 else 'negative' for s in y_sentiment_pred],
})
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S') #timestamp per rendere unico il nome del file
out_name = f'predictions_sample_{timestamp}.csv'
out.to_csv(os.path.join('generated_files', out_name), index=False)
print(f"Predizioni esportate in {out_name}")
