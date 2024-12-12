"""
nome: Lucarelli
cognome: Sebastiano
matricola: 0001090126
"""

"""
Progetto Python: Simulazione di Protocollo di Routing
"""
DISTANZA_MAX = float('inf')  # Imposta una costante per rappresentare la distanza massima

class Nodo:
    def __init__(self, nome):
        self.nome = nome  # Assegna il nome del nodo
        self.vicini = {}  # Dizionario che conterrà i vicini del nodo
        self.tabella_routing = {}  # Tabella di routing che conterrà la distanza verso ciascun nodo

    def inizializza_tabella(self):
        # Configura inizialmente la tabella di routing con i vicini diretti
        self.tabella_routing = {
            dest: (costo, dest) for dest, costo in self.vicini.items()  # Per ogni vicino, costo e se stesso come prossimo hop
        }
        self.tabella_routing[self.nome] = (0, None)  # La distanza da se stesso è 0, e non c'è prossimo hop

    def calcola_aggiornamenti(self, tabella_vicino, costo_vicino):
        # Calcola gli aggiornamenti nella tabella di routing in base alla tabella di un vicino
        modifiche = False  # Flag per determinare se ci sono stati cambiamenti
        for destinazione, costo in tabella_vicino.items():
            if destinazione == self.nome:  # Non consideriamo il nodo stesso
                continue
            nuovo_costo = costo + costo_vicino  # Calcola il nuovo costo verso la destinazione attraverso il vicino
            # Se non esiste una tabella per la destinazione o il nuovo costo è più basso
            if destinazione not in self.tabella_routing or nuovo_costo < self.tabella_routing[destinazione][0]:
                self.tabella_routing[destinazione] = (nuovo_costo, list(self.vicini.keys())[0])  # Aggiorna la tabella
                modifiche = True  # Segna che c'è stato un cambiamento
        return modifiche  # Restituisce True se ci sono stati cambiamenti, altrimenti False

    def stato_attuale(self):
        # Restituisce lo stato attuale della tabella di routing (solo i costi, senza i prossimi hop)
        return {
            dest: costo for dest, (costo, _) in self.tabella_routing.items()  # Esclude il prossimo hop e restituisce solo i costi
        }

    def __str__(self):
        # Rappresenta il nodo come stringa per una visualizzazione chiara
        descrizione = ", ".join(
            f"{dest}: {costo if costo < DISTANZA_MAX else 'inf'} (via {hop or '-'})"  # Mostra il costo e il prossimo hop
            for dest, (costo, hop) in sorted(self.tabella_routing.items())  # Ordina per destinazione
        )
        return f"Nodo {self.nome}: [{descrizione}]"  # Restituisce la rappresentazione del nodo

def crea_nodi(architettura_grafo):
    # Crea i nodi a partire dalla rappresentazione del grafo
    nodi = {}
    for nome, vicinato in architettura_grafo.items():
        nodo = Nodo(nome)  # Crea un nodo per ciascun nome nel grafo
        nodo.vicini = vicinato  # Assegna i vicini del nodo
        nodi[nome] = nodo  # Aggiungi il nodo al dizionario dei nodi
    for nodo in nodi.values():
        nodo.inizializza_tabella()  # Inizializza la tabella di routing per ogni nodo
    return nodi  # Restituisce il dizionario dei nodi

def aggiorna_tabelle(nodi):
    # Aggiorna le tabelle di routing di tutti i nodi
    cambiamenti = False  # Flag per sapere se c'è stato un cambiamento
    for nodo in nodi.values():
        for vicino, costo in nodo.vicini.items():  # Per ogni vicino di un nodo
            nodo_vicino = nodi[vicino]  # Ottieni il nodo vicino
            stato_vicino = nodo_vicino.stato_attuale()  # Ottieni la tabella di routing del vicino
            modificato = nodo.calcola_aggiornamenti(stato_vicino, costo)  # Calcola gli aggiornamenti della tabella di routing
            cambiamenti = cambiamenti or modificato  # Se c'è stato almeno un cambiamento, flagga come True
    return cambiamenti  # Restituisce True se ci sono stati cambiamenti nelle tabelle, altrimenti False

def mostra_stato_rete(nodi, titolo, file, a_video=True):
    # Stampa lo stato della rete nel file e a video se richiesto
    if a_video:
        print(f"\n{titolo}")
    file.write(f"\n{titolo}\n")
    for nodo in nodi.values():
        if a_video:
            print(nodo)  # Stampa a video
        file.write(str(nodo) + "\n")  # Scrive nel file

def simula_propagazione_routing(architettura_grafo):
    # Simula la propagazione del protocollo di routing
    nodi = crea_nodi(architettura_grafo)  # Crea i nodi a partire dal grafo

    # Creazione e apertura del file per scrivere i risultati
    with open("progetto.txt", "w") as file:  # Assicurati di aprire il file in modalità scrittura
        # Mostra stato iniziale nel file e a video
        mostra_stato_rete(nodi, "Tabelle di routing iniziali", file)

        iterazione = 0
        while True:
            iterazione += 1  # Incrementa il contatore delle iterazioni
            print(f"\nIterazione {iterazione}:")  # Stampa a video
            file.write(f"\nIterazione {iterazione}:\n")  # Scrive nel file
            cambiamenti = aggiorna_tabelle(nodi)  # Aggiorna le tabelle dei nodi
            mostra_stato_rete(nodi, f"Stato dopo l'iterazione {iterazione}", file)  # Scrive lo stato nel file

            if not cambiamenti:  # Se non ci sono stati cambiamenti, la simulazione è terminata
                break

        mostra_stato_rete(nodi, "Convergenza raggiunta - Tabelle finali", file)  # Scrive il risultato finale nel file

if __name__ == "__main__":
    grafo = {
        'A': {'B': 2, 'C': 4, 'E': 1},
        'B': {'A': 2, 'C': 1, 'D': 4, "E": 7},
        'C': {'A': 4, 'B': 1},
        'D': {'B': 4, 'E': 2},
        'E': {'A': 1, 'B': 7, 'D': 2},
    }
    simula_propagazione_routing(grafo)  # Esegue la simulazione di propagazione del routing