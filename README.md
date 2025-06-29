# car3bus

**car3bus** è un progetto Python per la visualizzazione e il monitoraggio di dati automotive tramite dashboard grafiche personalizzate, pensato per Raspberry Pi e sistemi embedded.

## Funzionalità principali

- Dashboard grafiche in tempo reale (giri motore, velocità, ecc.)
- Visualizzazione con display a 7 segmenti simulati
- Interfaccia utente con PyQt5
- Aggiornamento dati tramite bus CAN o simulazione

## Requisiti

- Python 3.7+
- PyQt5
- (Opzionale) librerie per CAN bus (es. python-can)

## Installazione

1. Clona la repository:
    ```bash
    git clone https://github.com/M4M0M3N/car3bus
    cd car3bus
    ```

2. Installa le dipendenze:
    ```bash
    pip install -r requirements.txt
    ```

## Avvio

Per avviare la dashboard:
```bash
python gui_script.py
```

## Struttura del progetto

- `gui/` — Componenti grafici delle dashboard
- `gui_script.py` — Script principale per lanciare l’interfaccia
- `README.md` — Questo file

## Note

- Personalizza le posizioni e le dimensioni dei widget modificando i parametri nei file delle dashboard.
- Il progetto è pensato per essere facilmente adattabile a diverse esigenze di visualizzazione dati automotive.

## Licenza

MIT

---

**Autore:** [Il tuo nome]