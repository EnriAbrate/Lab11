import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []
        self._selectedProduct = None

    def fillDD(self):
        for i in range(2015, 2019):
            self._view._ddyear.options.append(ft.dropdown.Option(str(i)))

        colors = self._model.getColors()
        for c in colors:
            self._view._ddcolor.options.append(ft.dropdown.Option(str(c)))

        self._view.update_page()


    def handle_graph(self, e):
        color = self._view._ddcolor.value
        year = self._view._ddyear.value
        self._model.buildGraph(color, year)

        self._view.txtOut.controls.clear()
        self._view.txtOut.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumNodes()}, Numero di archi: {self._model.getNumEdges()}."))

        archi = self._model.getArchiPesoMaggiore()

        for a in archi:
            self._view.txtOut.controls.append(ft.Text(f"Arco da {a[0]} a {a[1]}, con peso = {a[2]}"))

        self.fillDDProduct()

        self._view.update_page()


    def fillDDProduct(self):
        prodotti = self._model._allProducts

        for p in prodotti:
            self._view._ddnode.options.append(ft.dropdown.Option(data=p, text=p.Product_number, on_click=self.readDDProduct))

        self._view.update_page()

    def readDDProduct(self, e):
        if e.control.data is None:
            self._selectedProduct = None
        else:
            self._selectedProduct = e.control.data

    def handle_search(self, e):
        if self._selectedProduct is None:
            self._view.txtOut2.controls.clear()
            self._view.txtOut2.controls.append(ft.Text(f"Selezionare un prodotto!"))
            self._view.update_page()
            return

        numeroArchi = self._model.getPercorso(self._selectedProduct)

        self._view.txtOut2.controls.clear()
        self._view.txtOut2.controls.append(ft.Text(f"Il percorso con numero archi maggiore è: {numeroArchi}"))

        self._view.update_page()

