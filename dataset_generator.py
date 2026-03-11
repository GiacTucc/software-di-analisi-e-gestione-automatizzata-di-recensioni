"""
    Generatore di dataset di recensioni, salva tutto sotto il percorso generated_file/reviews_dataset.csv 
    in un file CSV con queste colonne: (id, title, body, department, sentiment)
"""

import csv #Libreria che legge e scrive file CSV
import random #Libreria per generare numeri casuali
import uuid #Libreria per generare identificatori univoci universali (UUID)
import os #Libreria per interagire con il sistema operativo


DEPARTMENTS = ['Housekeeping', 'Reception', 'F&B']
TEMPLATES = {
    'Housekeeping': {
        'positive': [
            {
                "title": "Pulizia impeccabile",
                "body": "Bagno sempre impeccabile, tutto a posto."
            },
            {
                "title": "Camera perfettamente curata",
                "body": "Camera pulita e ordinata, con tutti i comfort. Torneremo volentieri."
            },
            {
                "title": "Pulizia eccellente",
                "body": "Lenzuola fresche e profumate, ottima pulizia."
            },
            {
                "title": "Stanza confortevole",
                "body": "Stanza confortevole, perfettamente curata."
            },
            {
                "title": "Servizio pulizie al top",
                "body": "Il personale delle pulizie è stato impeccabile."
            },
            {
                "title": "Pulizie quotidiane perfette",
                "body": "Pulizie quotidiane accurate e precise."
            },
            {
                "title": "Pulizia buona",
                "body": "Tutto pulito, ottimo."
            },
        ],
        'negative': [
            {
                "title": "Scarsa pulizia",
                "body": "Stanza sporca, polvere ovunque e cattivo odore."
            },
            {
                "title": "Che schifo!",
                "body": "Tutto sporco. Veramente deludente."
            },
            {
                "title": "Bagno sporco",
                "body": "Bagno maleodorante e non pulito. Orrendo!"
            },
            {
                "title": "Pulizie superficiali",
                "body": "Pulizie superficiali, niente è a posto."
            },
            {
                "title": "Disordine all'arrivo",
                "body": "Stanza disordinata e sporca al mio arrivo. Non ci tornerò."
            },
            {
                "title": "Scarsa attenzione ai dettagli",
                "body": "Poca attenzione alla pulizia e ai dettagli."
            },
            {
                "title": "Esperienza negativa",
                "body": "Non tornerò per la scarsa pulizia. Mi sono trovato malissimo."
            },
        ]
    },
    'Reception': {
        'positive': [
            {
                "title": "Check-in veloce",
                "body": "Check-in rapido e staff gentile e disponibile."
            },
            {
                "title": "Ottimo",
                "body": "Reception cordiale."
            },
            {
                "title": "Staff accogliente",
                "body": "Reception sempre pronta ad aiutare con un sorriso."
            },
            {
                "title": "Servizio eccellente",
                "body": "Personale cortese, molto professionale."
            },
            {
                "title": "Esperienza positiva",
                "body": "Reception efficiente, check-out senza attese."
            },
            {
                "title": "Personale disponibile",
                "body": "Aiuto immediato per ogni richiesta."
            },
            {
                "title": "Reception impeccabile",
                "body": "Servizio rapido e preciso, ottima esperienza! Torneremo volentieri."
            },
        ],
        'negative': [
            {
                "title": "Reception lenta",
                "body": "Reception lenta e scortese, check-in lungo."
            },
            {
                "title": "Reception oscena",
                "body": "Tempi di attesa lunghissimi e personale arrogante."
            },
            {
                "title": "Staff poco professionale",
                "body": "Staff poco professionale e scortese. Maleducati."
            },
            {
                "title": "Esperienza negativa",
                "body": "Servizio lento e confusionario alla reception."
            },
            {
                "title": "Problemi al check-in",
                "body": "Check-in molto disorganizzato e caotico."
            },
            {
                "title": "Maleducazione del personale",
                "body": "Reception inefficiente e mal organizzata. Ci abbiamo messo ore per entrare in camera."
            },
            {
                "title": "Servizio scadente",
                "body": "Esperienza deludente con lo staff della reception. Non lo consiglierei."
            },
        ]
    },
    'F&B': {
        'positive': [
            {
                "title": "Colazione eccellente",
                "body": "Colazione abbondante e variegata."
            },
            {
                "title": "Il cibo era squisito",
                "body": "Il cibo era squisito e ben presentato."
            },
            {
                "title": "Cena deliziosa",
                "body": "Cena ottima e servizio rapido."
            },
            {
                "title": "Servizio impeccabile",
                "body": "Cibo di qualità e servizio impeccabile. A pranzo era sempre tutto fantastico"
            },
            {
                "title": "Esperienza culinaria perfetta",
                "body": "Ottima esperienza culinaria, tutto delizioso."
            },
            {
                "title": "Menù vario e gustoso",
                "body": "Menù molto vario e soddisfacente. Che buono."
            },
            {
                "title": "Staff del ristorante cordiale",
                "body": "Staff del ristorante cordiale e professionale."
            },
        ],
        'negative': [
            {
                "title": "Colazione deludente",
                "body": "Colazione scarsa e poco varia. Pranzo e cena ancora peggio."
            },
            {
                "title": "Cibo pessimo",
                "body": "Il cibo aveva un sapore terribile."
            },
            {
                "title": "Cibo senza sapore",
                "body": "Cibo freddo e senza sapore. Pessimo."
            },
            {
                "title": "Ristorante lento",
                "body": "Ristorante lento e disorganizzato."
            },
            {
                "title": "Qualità bassa",
                "body": "Poca scelta e qualità bassa."
            },
            {
                "title": "Esperienza culinaria negativa",
                "body": "Cibo poco appetibile e mal presentato. Bleah"
            },
            {
                "title": "Pessima cucina",
                "body": "Servizio confuso e disorganizzato, non consiglierei questo posto."
            },
        ]
    }
}
AMBIGUOUS = [
    ("Personale ok", "Il personale è stato gentile ma la camera non era ancora pronta.", 'Reception', 'positive'),
    ("Check-in e colazione", "Arrivati tardi, il check-in è stato rapido ma la colazione era già finita.", 'Reception', 'positive'),
    ("Tutto sommato bene", "Reception gentile, anche se la stanza era un po' fredda.", 'Reception', 'positive'),
    ("Accoglienza così così", "Personale cordiale ma attesa lunga al check-in.", 'Reception', 'negative'),
    ("Esperienza mista", "Servizio accogliente ma confusione al momento del pagamento.", 'Reception', 'negative'),
    ("Pulizia nella media", "La stanza era pulita ma il bagno aveva un cattivo odore.", 'Housekeeping', 'negative'),
    ("Servizio misto", "Staff accogliente ma il letto non era per niente comodo.", 'Housekeeping', 'negative'),
    ("Tutto normale", "Camera tranquilla ma la polvere sui mobili era evidente.", 'Housekeeping', 'negative'),
    ("Discreto soggiorno", "Pulizia buona ma mancavano gli asciugamani. Staff cortese.", 'Housekeeping', 'positive'),
    ("Niente di speciale", "Camera ordinata ma il pavimento era molto sporco.", 'Housekeeping', 'negative'),
    ("Buona sistemazione", "Struttura curata ma il ristorante era troppo affollato.", 'F&B', 'positive'),
    ("Esperienza contrastante", "Pulizia ottima, ma il ristorante chiudeva troppo presto.", 'F&B', 'positive'),
    ("Colazione discreta", "Buona scelta di prodotti ma il tavolo non era stato pulito.", 'F&B', 'negative'),
    ("Cena tra alti e bassi", "Cibo buono ma il servizio molto lento.", 'F&B', 'negative'),
    ("Ristorante e camera", "Cena fantastica ma la stanza aveva un cattivo odore.", 'F&B', 'negative'),
]
DATASET_PATH = os.path.join('generated_file', 'reviews_dataset.csv') #percorso di salvataggio del dataset generato

#(In totale (di default) saranno 300 recensioni non ambigue + 15 ambigue)
def generate(non_ambiguous=300, ambiguous=15, out_path=DATASET_PATH): 
    rows = [] #lista che conterrà tutte le righe del dataset
    per_combo = non_ambiguous // (len(DEPARTMENTS) * 2)  #300 / (3*2) = 50, quindi 50 recensioni per ogni 
                                                            #combinazione di reparto e sentiment

    #Genera recensioni non ambigue
    for department in DEPARTMENTS: #Per ogni reparto
        for sentiment in ['positive', 'negative']: #Per ogni sentiment
            template = TEMPLATES[department][sentiment] #Prende il template corrispondente 
            #(template sarebbe la lista di recensioni per quel reparto e sentiment che si sta ciclando)
            for i in range(per_combo): #(Genera 50 recensioni)
                review = random.choice(template) #Prendo una recensione a caso dal template
                title, body = review['title'], review['body']

                rows.append({ #aggiungo la recensione processata al dataset
                    'id': str(uuid.uuid4()), #creo con la libreria uuid un id univoco
                    'title': title,
                    'body': body,
                    'department': department,
                    'sentiment': sentiment
                })

    #Genera recensioni ambigue, ho fatto una lista e un ciclo a parte per garantire che vengano incluse 
    for review in AMBIGUOUS[:ambiguous]:
        rows.append({
            'id': str(uuid.uuid4()),
            'title': review[0], #le recensioni ambigue sono tuple e non dizionari, quindi accedo agli elementi con gli indici
            'body': review[1],
            'department': review[2],
            'sentiment': review[3]
        })

    random.shuffle(rows) #mescolo tutte le recensioni

    keys = ['id', 'title', 'body', 'department', 'sentiment'] #colonne del file CSV
    with open(out_path, 'w', newline='', encoding='utf-8') as f: #apro il csv in scrittura
        writer = csv.DictWriter(f, fieldnames=keys) #creo un writer che scrive dizionari, indicando le colonne
        writer.writeheader() #scrivo l'intestazione del csv
        for r in rows: #per ogni recensione..
            writer.writerow(r) #..scrivo la riga nel csv
    print(f"Generato {len(rows)} record in {out_path}.")

if __name__ == '__main__': #quando si esegue questo file direttamente, faccio partire generate()
    generate() 
