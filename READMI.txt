Ho scritto 3 script Python di esempio per le 3 elaborazioni richieste
1. Pulizia dati (cleanData.py)
2. Interpolazione dati (kriging.py)
3. Correlazione con indice NDVI (corrNdvi.py)

Gli script sono configurabili modificano i parametri nell'apposita sezione in ciascun metodo main()
I primi due script sono stati testati con successo, il terzo non ho avuto modo di verificarlo perchè non ho a disposizione un dato multispettrale su cui calcolare l'indice NDVI.

Per il deploy degli script si consiglia di utilizzare un venv python.

ISTRUZIONI

#Installare le librerie venv per Python 3
pip install virtualenv

#Creazione dell'ambiente virtuale 
python -m venv myenv

#attivazione (sotto windows)
.\Scripts\Activate.ps1

#attivazione (sotto Linux)
source myenv/bin/activate

#Successivamente copiare il file zip all'interno della cartella dell'ambiente virtuale e procedere all'installazione delle dipendenze
pip install geopandas pandas matplotlib seaborn numpy pykrige rasterio scipy

lanciare in sequenza gli script:
1. cleanData.py (N.B: è necessario chiudere le finestre matplotlib che mostrano le distribuzione di frequenza per procedere con le elaborazioni)
2. kriging.py
3. corrNdvi.py

 
