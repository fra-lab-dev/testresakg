"""
Script per l'interpolazione Kriging di dati usando PyKrige

Dipendenze:
pip install geopandas numpy pykrige rasterio

"""

import geopandas as gpd
import numpy as np
from pykrige.ok import OrdinaryKriging
import rasterio
from rasterio.transform import from_origin

def carica_dati(file_path):
    """
    Carica i dati dal geopackage pulito e restituisce anche il CRS
    
    Args:
        file_path (str): Percorso del file geopackage
    Returns:
        tuple: (GeoDataFrame, CRS)
    """
    try:
        gdf = gpd.read_file(file_path)
        print(f"Dati caricati con successo. Numero di punti: {len(gdf)}")
        print(f"Sistema di riferimento: {gdf.crs}")
        print(f"Campi disponibili: {list(gdf.columns)}")
        return gdf, gdf.crs
    except Exception as e:
        print(f"Errore nel caricamento dei dati: {str(e)}")
        return None, None

def prepara_griglia(gdf, risoluzione=5):
    """
    Prepara la griglia per l'interpolazione
    
    Args:
        gdf (GeoDataFrame): Dataset dei punti
        risoluzione (float): Risoluzione della griglia in metri
    Returns:
        tuple: (x_grid, y_grid, bounds)
    """
    # Ottiene i bounds del dataset
    bounds = gdf.total_bounds
    
    # Crea la griglia con la risoluzione specificata
    x = np.arange(bounds[0], bounds[2], risoluzione)
    y = np.arange(bounds[1], bounds[3], risoluzione)
    
    return x, y, bounds

def esegui_kriging(gdf, x, y, campo_valore='RESAKG', variogram_model='gaussian'):
    """
    Esegue l'interpolazione kriging usando PyKrige
    
    Args:
        gdf (GeoDataFrame): Dataset dei punti
        x (numpy.array): Coordinate X della griglia
        y (numpy.array): Coordinate Y della griglia
        campo_valore (str): Nome del campo da interpolare
        variogram_model (str): Modello di variogramma da utilizzare
    Returns:
        numpy.array: Valori interpolati e varianza
    """
    # Verifica che il campo esista
    if campo_valore not in gdf.columns:
        raise ValueError(f"Il campo {campo_valore} non esiste nel dataset")
    
    # Estrae le coordinate e i valori
    data_x = gdf.geometry.x.values
    data_y = gdf.geometry.y.values
    values = gdf[campo_valore].values
    
    print(f"Esecuzione kriging sul campo: {campo_valore}")
    print(f"Modello variogramma: {variogram_model}")
    
    # Crea e configura il kriging
    OK = OrdinaryKriging(
        data_x,
        data_y,
        values,
        variogram_model=variogram_model,
        verbose=False,
        enable_plotting=False
    )
    
    # Esegue il kriging
    z, ss = OK.execute('grid', x, y)
    
    return z, ss

def salva_raster(result, bounds, risoluzione, output_path, crs, suffix=''):
    """
    Salva il risultato come GeoTiff
    
    Args:
        result (numpy.array): Risultato del kriging
        bounds (tuple): Bounds del dataset
        risoluzione (float): Risoluzione della griglia
        output_path (str): Percorso del file di output
        crs: Sistema di riferimento dei dati originali
        suffix (str): Suffisso da aggiungere al nome del file
    """
    # Modifica il nome del file per includere il suffisso
    if suffix:
        nome_file = output_path.replace('.tiff', f'_{suffix}.tiff')
    else:
        nome_file = output_path
    
    transform = from_origin(
        bounds[0],
        bounds[3],
        risoluzione,
        risoluzione
    )
    
    with rasterio.open(
        nome_file,
        'w',
        driver='GTiff',
        height=result.shape[0],
        width=result.shape[1],
        count=1,
        dtype=result.dtype,
        crs=crs,
        transform=transform,
    ) as dst:
        dst.write(result, 1)
    
    print(f"Salvato il file: {nome_file}")

def main():
    """
    Funzione principale
    """
    # Parametri configurabili
    input_file = "resa_girasole_2022_cleaned.gpkg"
    output_file = "resa_girasole_2022_kriging.tiff"
    campo_valore = 'RESAKG'  # Campo su cui effettuare il kriging
    risoluzione = 5  # metri
    variogram_model = 'gaussian'  # Modello del variogramma
    
    # Carica i dati
    gdf, crs = carica_dati(input_file)
    if gdf is None:
        return
        
    # Prepara la griglia
    print("Preparazione della griglia di interpolazione...")
    x, y, bounds = prepara_griglia(gdf, risoluzione)
    
    # Esegue il kriging
    print("Esecuzione del kriging...")
    try:
        z, ss = esegui_kriging(gdf, x, y, campo_valore, variogram_model)
        
        # Salva i risultati
        print("Salvataggio dei raster...")
        #salvataggio file predizione e varianza
        salva_raster(z, bounds, risoluzione, output_file, crs, 'pred')
        salva_raster(ss, bounds, risoluzione, output_file, crs, 'var')
        
        print("Processo completato con successo!")
        
    except ValueError as e:
        print(f"Errore: {str(e)}")
        return

if __name__ == "__main__":
    main()