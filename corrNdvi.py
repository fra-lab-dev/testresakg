"""
Script per l'analisi statistica tra raster risultato del kriging e NDVI
Dipendenze: pip install rasterio numpy scipy matplotlib seaborn

N.B.: script non testato perchè non avevo a disposizione un dato multispettrale 
su cui calcolare l'indice NDVI
"""

import rasterio
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression

def analisi_statistica(raster_resa, raster_ndvi):
    """
    Esegue l'analisi statistica tra due raster
    
    Args:
        raster_resa (str): Percorso del raster della resa
        raster_ndvi (str): Percorso del raster NDVI
    """
    # Carica i raster
    with rasterio.open(raster_resa) as src1, rasterio.open(raster_ndvi) as src2:
        resa = src1.read(1)
        ndvi = src2.read(1)
    
    # Prepara i dati
    mask = ~(np.isnan(resa) | np.isnan(ndvi))
    x = ndvi[mask].reshape(-1, 1)  # NDVI come variabile indipendente
    y = resa[mask]  # Resa come variabile dipendente
    
    # Calcola statistiche descrittive
    print("\nStatistiche descrittive:")
    print(f"NDVI - Media: {np.mean(x):.3f}, Dev.Std: {np.std(x):.3f}")
    print(f"Resa - Media: {np.mean(y):.3f}, Dev.Std: {np.std(y):.3f}")
    
    # Calcola correlazione
    r, p = stats.pearsonr(x.flatten(), y)
    print("\nAnalisi di correlazione:")
    print(f"Coefficiente di correlazione di Pearson: {r:.3f}")
    print(f"P-value: {p:.3e}")
    
    # Calcola R² e regressione lineare
    model = LinearRegression()
    model.fit(x, y)
    r_squared = model.score(x, y)
    
    print("\nModello di regressione lineare:")
    print(f"R²: {r_squared:.3f}")
    print(f"Coefficiente: {model.coef_[0]:.3f}")
    print(f"Intercetta: {model.intercept_:.3f}")
    print(f"Equazione: y = {model.coef_[0]:.3f}x + {model.intercept_:.3f}")

def main():
    """
    Funzione principale
    """
    # Parametri
    raster_resa = "resa_girasole_2022_kriging_prediction.tiff"
    raster_ndvi = "ndvi.tiff"
    
    # Esegue l'analisi
    analisi_statistica(raster_resa, raster_ndvi)

if __name__ == "__main__":
    main()