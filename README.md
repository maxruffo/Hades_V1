# MultiInputLSTM für die Vorhersage von Preiskursen mit ResidualBlocks und AttentionLayers

Dieses Projekt untersucht die Anwendung verschiedener LSTM-Modelle zur Vorhersage von Zeitreihen mit Finanzdaten. Durch die Kombination von **ResidualBlocks** und **Attention Layers** werden Modellarchitekturen getestet, die sowohl Trends als auch Details in Daten erfassen können.

## Inhaltsverzeichnis

1. [Projektübersicht](#projektübersicht)
2. [Dateistruktur](#dateistruktur)
3. [Features](#features)
4. [Modellarchitekturen](#modellarchitekturen)
5. [Training und Optimierung](#training-und-optimierung)
6. [Evaluation](#evaluation)
7. [Zukünftige Arbeit](#zukünftige-arbeit)

---

## Projektübersicht

Dieses Projekt basiert auf Finanzdaten von BTCUSDT und beinhaltet folgende Schritte:
- Datenextraktion und -vorbereitung mithilfe der Binance-API.
- Berechnung und Visualisierung technischer Indikatoren.
- Entwicklung und Testen von LSTM-Architekturen mit unterschiedlichen Erweiterungen.
- Evaluation der Modelle auf neuen Daten.

---

## Dateistruktur

Die wichtigsten Verzeichnisse und Dateien des Projekts:

- `Data Analysis and Visualization`: Skripte zur Datenanalyse und Visualisierung.
- `Evaluation_PNGs`: Ergebnisse und Grafiken für die Modellbewertung.
- `Experiment 1`: Basismodell (MultiInputLSTM).
- `Experiment 2`: Erweiterung um ResidualBlocks.
- `Experiment 3`: Kombination von ResidualBlocks und Attention Layers.
- `src/main/data_preprocessing`: Code für Datenvorverarbeitung und Signalberechnung.
- `config.json`: Konfiguration für die Datenextraktion.
- `requirements.txt`: Abhängigkeiten des Projekts.

---

## Features

Die berechneten Indikatoren umfassen:
- **SMA/EMA**: Erkennung von Trends (50/200-Tage-Gleitender Durchschnitt).
- **MACD**: Momentum-Indikator.

---

## Modellarchitekturen

### 1. Basismodell: MultiInputLSTM
Ein LSTM-Modell, das mehrere Eingaben berücksichtigt und direkt Preisvorhersagen trifft.

### 2. Erweiterung: ResidualBlocks
- **Vorteil**: Reduzierte Probleme wie vanishing gradients.
- **Implementierung**: Lineare Transformationen, Normalisierung, Aktivierung und Skip-Verbindungen.

### 3. Erweiterung: Attention Layers
- Fokus auf relevante Teile der Sequenzdaten.
- Kombiniert mit ResidualBlocks für detaillierte Vorhersagen.

---

## Training und Optimierung

- **Loss-Funktion**: Mean Squared Error (MSE) zur Bestrafung kleiner Fehler.
- **Optimierer**: Adam (adaptives Lernen).
- **Learning Rate Scheduler**: ReduceLROnPlateau zur Effizienzsteigerung.
- **Early Stopping**: Vermeidung von Overfitting durch frühzeitiges Beenden des Trainings.

---

## Evaluation

- **Testdaten**: BTCUSDT-Daten vom 01.11.2024 bis 25.11.2024.
- **Ergebnisse**:
  - Das Modell zeigt hohe Robustheit gegenüber kleinen Datenabweichungen.
  - Erfassung von Langzeittrends, jedoch Glättung von schnellen Preisspitzen.
- **MSE vs. Trendvarianz**:
  - MSE < Quadratische Varianz: Modell erfasst Gesamttrends erfolgreich.

---

## Zukünftige Arbeit

- Erweiterung der Features (z. B. Sentiment-Analysen).
- Optimierung der Architektur zur Erfassung kurzfristiger Preisschwankungen.
- Integration weiterer Datenquellen zur Verbesserung der Vorhersagequalität.
- Scaler Verbesserungen

---

## Vielen Dank