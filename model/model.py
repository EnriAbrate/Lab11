import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._allProducts = []
        self._idMap = {}

        self._bestPath = []
        self._lunghezza = 0

    def getPercorso(self, nodoPartenza):
        self._bestPath = []
        self._lunghezza = 0

        parziale = [nodoPartenza]

        self.ricorsione(parziale)

        return (self._lunghezza - 1)

    def ricorsione(self, parziale):
        if len(parziale) > self._lunghezza:
            self._lunghezza = len(parziale)
            self._bestPath = copy.deepcopy(parziale)

        for v in self._grafo.neighbors(parziale[-1]):
            if v not in parziale and len(parziale) == 1:
                parziale.append(v)
                self.ricorsione(parziale)
                parziale.pop()
            else:
                if v not in parziale:
                    pesoPrecedente = self._grafo[parziale[-2]][parziale[-1]]["weight"]
                    pesoDaAggiungere = self._grafo[parziale[-1]][v]["weight"]
                    if pesoDaAggiungere > pesoPrecedente:
                        parziale.append(v)
                        self.ricorsione(parziale)
                        parziale.pop()

    def buildGraph(self, color, year):
        self._grafo.clear()
        self._allProducts = DAO.getProducts(color)
        self._grafo.add_nodes_from(self._allProducts)

        for p in self._allProducts:
            self._idMap[p.Product_number] = p

        connessa = DAO.getConnessa(self._idMap, color, year)
        for c in connessa:
            c.Peso = DAO.getPeso(c.Product_number1.Product_number, c.Product_number2.Product_number, color, year)
            self._grafo.add_edge(c.Product_number1, c.Product_number2, weight=c.Peso)

    def getArchiPesoMaggiore(self):
        archi = []

        for e in self._grafo.edges:
            archi.append( (e[0].Product_number, e[1].Product_number, self._grafo[e[0]][e[1]]["weight"]) )

        sortedArchi = sorted(archi, key=lambda x: x[2], reverse=True)

        return sortedArchi[0:3]

    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)

    def getColors(self):
        return DAO.getColors()
