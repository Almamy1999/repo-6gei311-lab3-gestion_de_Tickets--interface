
import tkinter as tk
from tkinter import ttk


class TicketListFrame(tk.LabelFrame):
    def __init__(self, parent, on_view, on_edit):
        super().__init__(parent, text="Mes tickets", padx=12, pady=12)

        # Tableau des tickets
        colonnes = ("id", "titre", "priorite", "statut")

        self.table_tickets = ttk.Treeview(
            self,
            columns=colonnes,
            show="headings",
            height=8,
            selectmode="browse"
        )

        for colonne, titre in [
            ("id", "ID"),
            ("titre", "Titre"),
            ("priorite", "Priorité"),
            ("statut", "Statut")
        ]:
            self.table_tickets.heading(colonne, text=titre)

        self.table_tickets.column("id", width=60, anchor="center")
        self.table_tickets.column("titre", width=350)
        self.table_tickets.column("priorite", width=120, anchor="center")
        self.table_tickets.column("statut", width=120, anchor="center")

        self.table_tickets.pack(fill="both", expand=True)

        # Boutons d'action
        actions = tk.Frame(self)
        actions.pack(pady=10)

        tk.Button(
            actions,
            text="Consulter",
            command=on_view
        ).pack(side="left", padx=5)

        tk.Button(
            actions,
            text="Modifier",
            command=on_edit
        ).pack(side="left", padx=5)

        # Double-clic pour consulter un ticket
        self.table_tickets.bind(
            "<Double-1>",
            lambda event: on_view()
        )

    def ajouter_ticket(self, ticket):
        self.table_tickets.insert(
            "",
            tk.END,
            iid=str(ticket["id"]),
            values=self._valeurs(ticket)
        )

    def actualiser_ticket(self, ticket):
        self.table_tickets.item(
            str(ticket["id"]),
            values=self._valeurs(ticket)
        )

    def obtenir_selection(self):
        selection = self.table_tickets.selection()

        if not selection:
            return None

        return int(selection[0])

    @staticmethod
    def _valeurs(ticket):
        return (
            ticket["id"],
            ticket["titre"],
            ticket["priorite"],
            ticket["statut"]
        )
