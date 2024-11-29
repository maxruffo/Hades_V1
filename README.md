# Hades V1

## How does the Code Work?

### 1. Data Acquisition
- Firstly the User decides the Ticker-Pair of the Currecy he wants to trade.
- He chooses the Timeframe of the Data he wants to use.
- The Data is then downloaded from the Binance API. -> binance_utils.py (DataDownloader)
- The Code sends a get request to the API for every single Day, becuase there is a limit of 1000 candles per request.
- For Performance reasons the request are parallelized with the help of the ThreadPoolExecutor.
- All the CSV Files are then stored in the Data Folder.
- the Data is then loaded into a Pandas DataFrame.
- The data is merged to a single DataFrame and stored in a CSV File.
- Then the Trading Signals (SMA_50, SMA_200, EMA_50, EMA_200, MACD, MACD_Signal, MACD_Hist, RSI, BB_upper, BB_middle, BB_lower, Slowk, Slowd, ADX, STDDEV, Ichimoku_Conversion, Ichimoku_Base, Ichimoku_SpanA, Ichimoku_SpanB) are calculated and added to the DataFrame
- The Dataframe is stored in a CSV File.

### 2. LTSM Training
- The Data is loaded from the CSV File.


- reinforcment_learning.py
- q learning
- sequentz demension 



### Encountered Problems
#### Binance
- The Binance API has a limit of 1000 candles per request. To get the data for a longer timeframe, the requests have to be parallelized.
- The Data is stored in CSV Files, which is not the most efficient way to store the data. A better way would be to store the data in a Database.
#### Training
- The Training of the LSTM Model is very slow. The Model has to be trained on a GPU to get reasonable results.
- The Model has to be trained on a lot of Data to get reasonable results.
- There were to many features at the beginning, which slowed down the training process. The features had to be reduced to get reasonable results.
- Training ist gerade sehr langsam, da es auf der CPU läuft.

## Todo
1. Custom_layer und Attention Layer erstellen
2. Bestes Model evaluiren -> varianz und mean quadrieren und vergleichen
3. Code aufräumen
4. Sowas wie Adapative Learning Rate einbauen und EarlyStopping
5. 



# Testen ob es ein Tren ist oder nicht durchschnittliche Änderung mean und varianz quadriereung wäre
# Wie durchscnittliche Veränderung und die Varianz ich quadriere die Varianz und vergleiche die MSE
# Custom Layer machen Standard Layers von Papers
# Sauber evaluiren
# Strukturierte Aufbau der Präsentation
# Smaple nehmen wie die Input daten sind
# Modell Architektur
# Qualtität der Evaluation