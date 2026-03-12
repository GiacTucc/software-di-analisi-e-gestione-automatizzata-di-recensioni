"""
Script per configurare il progetto:
-crea ambiente virtuale
-installa dipendenze
-esegue script che avvia il progetto
"""
import os
import sys
import subprocess
import shutil
import platform

VENV_DIR = 'venv' #venv sta per Virtual environment directory

def create_venv():
    if not os.path.exists(VENV_DIR):
        print("Creazione ambiente virtuale...")
        #subprocess.check_call esegue un comando del sistema operativo come se lo stessi lanciando dal terminale.
        #Inoltre blocca il programma finché il comando non termina.
        subprocess.check_call([sys.executable, '-m', 'venv', VENV_DIR])
        #esegue il modulo venv per creare l'ambiente virtuale e lo creerà in VENV_DIR
        #sys.executable da il percorso di python che sta eseguendo questo script, così si evita problemi se hai
        #più versioni scaricate.
        #-m esegui come modulo
    else:
        print("Ambiente virtuale già presente.")

def install_requirements():
    print("Installazione dipendenze...")
    if platform.system() == 'Windows': #windows
        #individua il percorso dell’interprete Python dentro l’ambiente virtuale appena creato.
        python_path = os.path.join(VENV_DIR, 'Scripts', 'python.exe')
        #installa tutte le dipendenze presenti nel file requirements.txt
        subprocess.run(f'"{python_path}" -m pip install -r requirements.txt --quiet --disable-pip-version-check', 
                       shell=True, check=True)
        #-r è per fargli prendere tutte le dipendenze dal file 
        #check=True fa sì che, se il comando fallisce Python lanci un’eccezione.
        #shell=True permette di passare il comando come stringa completa (necessario su Windows).
    else: #mac o linux
        python_path = os.path.join(VENV_DIR, 'bin', 'python') #qui ci sono percorsi diversi
        subprocess.run([python_path, '-m', 'pip', 'install', '-r', 'requirements.txt',
                        '--quiet', '--disable-pip-version-check'], check=True)


def run_project():
    print("Esecuzione progetto completo...")
    if os.path.exists('generated_files'): #ogni volta che viene eseguito da zero ricrea la cartella dei file generati
        shutil.rmtree('generated_files')
    os.makedirs('generated_files', exist_ok=True)

    if platform.system() == 'Windows':
        python_path = os.path.join(VENV_DIR, 'Scripts', 'python.exe')
    else:
        python_path = os.path.join(VENV_DIR, 'bin', 'python')
    subprocess.check_call([python_path, 'project_launcher.py']) #lancio project_launcher.py che avvierà il progetto

if __name__ == '__main__':
    create_venv()
    install_requirements()
    run_project()
    print("\nEsecuzione terminata con successo!")
