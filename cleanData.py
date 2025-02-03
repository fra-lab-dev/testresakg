# -*- coding: utf-8 -*-
"""
Script per la pulizia dei dati da geopackage
Lo script carica un geopackage, analizza la distribuzione spaziale
dei valori di raccolto e area, applica le regole di pulizia e salva
il dataframe finale in un geopackage in uscita

Per utilizzo installare le seguenti dipendenze:
pip install geopandas pandas matplotlib seaborn

Consigliabile l'utilizzo di un venv python 

N.B.: una volta lanciato lo script è necessario chiudere la finestra di matplotlib per
        poter proseguire con i passi successivi dell'elaborazione
"""

# Importazione delle librerie necessarie
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def carica_dati(percorso_file):
    """
    Carica i dati dal file geopackage
    
    Args:
        percorso_file (str): Percorso del file geopackage
        
    Returns:
        GeoDataFrame: Dataset caricato
    """
    try:
        # Carica il geopackage in un GeoDataFrame
        gdf = gpd.read_file(percorso_file)
        print(f"Dati caricati con successo. Shape iniziale: {gdf.shape}")
        return gdf
    except Exception as e:
        print(f"Errore durante il caricamento del file: {str(e)}")
        return None

def visualizza_statistiche_iniziali(gdf):
    """
    Mostra le statistiche iniziali del dataset
    
    Args:
        gdf (GeoDataFrame): Dataset da analizzare
    """
    print("\nStatistiche iniziali:")
    print("-" * 50)
    print("\nInformazioni sul dataset:")
    print(gdf.info())
    print("\nStatistiche descrittive:")
    print(gdf.describe())
    print("\nValori nulli per colonna:")
    print(gdf.isnull().sum())

def visualizza_distribuzione(gdf, colonna):
    """
    Crea un grafico della distribuzione dei valori per una colonna
    
    Args:
        gdf (GeoDataFrame): Dataset da analizzare
        colonna (str): Nome della colonna da visualizzare
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(data=gdf, x=colonna)
    plt.title(f'Distribuzione di {colonna}')
    plt.show()

def pulisci_dati(gdf):
    """
    Applica le regole di pulizia dei dati. Le regole utilizzate, a titolo
    puramente esemplificativo sono le seguenti:
    1. rimuovere valori minori o uguali a zero per RESAKG
    2. rimuovere record con valori di area minori o uguali a zero
    3. rimuovere i record con valori NULL in tutti i campi
    
    Args:
        gdf (GeoDataFrame): Dataset da pulire
        
    Returns:
        GeoDataFrame: Dataset pulito
    """
    # Salva il numero di righe iniziale
    righe_iniziali = len(gdf)
    
    # 1. Rimuove i valori minori o uguali a zero per RESAKG
    gdf = gdf[gdf['RESAKG'] > 0]
    print(f"Rimossi {righe_iniziali - len(gdf)} record con RESAKG <= 0")
    
    # Aggiorna il conteggio delle righe
    righe_iniziali = len(gdf)
    
    # 2. Rimuove record con valori di area minori o uguali a zero
    gdf = gdf[gdf['AREA'] > 0]
    print(f"Rimossi {righe_iniziali - len(gdf)} record con AREA <= 0")
    
    # Aggiorna il conteggio delle righe
    righe_iniziali = len(gdf)
    
    # 3. Rimuove i record con valori NULL di tutti i campi
    gdf = gdf.dropna()
    print(f"Rimossi {righe_iniziali - len(gdf)} record con valori NULL")
    
    return gdf

def salva_dati_puliti(gdf, percorso_output):
    """
    Salva i dati puliti in un nuovo file
    
    Args:
        gdf (GeoDataFrame): Dataset da salvare
        percorso_output (str): Percorso dove salvare il file
    """
    try:
        gdf.to_file(percorso_output, driver='GPKG')
        print(f"Dati salvati con successo in: {percorso_output}")
    except Exception as e:
        print(f"Errore durante il salvataggio del file: {str(e)}")

def main():
    """
    Funzione principale che esegue la pipeline di pulizia dati
    """
    # Percorso del file di input e di output
    input_file = "resa_girasole_2022.gpkg"
    output_file = "resa_girasole_2022_cleaned.gpkg"
    
    # Carica i dati
    gdf = carica_dati(input_file)
    if gdf is None:
        return
    
    # Visualizza statistiche iniziali
    visualizza_statistiche_iniziali(gdf)
    
    # Visualizza distribuzione dei valori chiave
    visualizza_distribuzione(gdf, 'RESAKG')
    visualizza_distribuzione(gdf, 'AREA')
    
    # Pulisci i dati
    gdf_pulito = pulisci_dati(gdf)
    
    # Visualizza statistiche finali
    print("\nStatistiche dopo la pulizia:")
    print("-" * 50)
    print(f"Righe originali: {len(gdf)}")
    print(f"Righe dopo la pulizia: {len(gdf_pulito)}")
    print(f"Righe rimosse: {len(gdf) - len(gdf_pulito)}")
    
    # Salva i dati puliti
    salva_dati_puliti(gdf_pulito, output_file)

if __name__ == "__main__":
    main()