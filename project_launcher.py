"""
Script per eseguire il progetto:
-genera dataset sintetico
-addestra modelli e calcola metriche
-salva grafici e CSV predizioni
-se specificato avvia interfaccia Streamlit
"""

import subprocess
import sys

def run_script(script_name):
    print(f"\nEsecuzione di: {script_name}")
    #.run è l'evoluzione di checkCall, gestisce parametri più complessi
    result = subprocess.run([sys.executable, script_name], capture_output=False)
    if result.returncode != 0:
        print(f"Errore durante {script_name}")
        sys.exit(1)

if __name__ == "__main__":
    #Genera dataset
    run_script('dataset_generator.py')
    #Addestra modelli e valuta
    run_script('train_pipeline.py')
    #Avvia Streamlit (opzionale)
    launch_app = input("\nVuoi avviare l'interfaccia grafica Streamlit per usare il modello e predire recensioni? (s/n): \n").lower()
    if launch_app == 's':
        try:
            subprocess.run([sys.executable, "-m", "streamlit", "run", "gui.py"], check=True)
        except subprocess.CalledProcessError:
            print("Errore nell'avvio di Streamlit. Assicurati che sia installato nell'ambiente virtuale.")
