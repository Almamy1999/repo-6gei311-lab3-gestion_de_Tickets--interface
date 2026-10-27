
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

# Permet d'importer Ticket.py, User.py, Admin.py qui sont dans le dossier parent
dossier_projet = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dossier_projet)

from Ticket import Ticket          
from User import User              
from Admin import Admin            

from create_ticket_frame import CreateTicketFrame
from ticket_list_frame import TicketListFrame
from ticket_details_frame import TicketDetailsFrame
from edit_ticket_frame import EditTicketFrame


class UserInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des tickets")
        self.root.geometry("1000x700")
        self.root.minsize(800, 550)
        self.root.configure(bg="#f3f5f9")

        
        
        self.admin = Admin(1, "Admin", "admin@uqac.ca")
        self.utilisateur = User(1, "Bamba", "bamba@uqac.ca", "Utilisateur")

        # Style général
        style = ttk.Style()
        style.configure(
            "Titre.TLabel",
            font=("Arial", 20, "bold"),
            background="#f3f5f9",
            foreground="#243247"
        )
        style.configure(
            "SousTitre.TLabel",
            font=("Arial", 10),
            background="#f3f5f9",
            foreground="#667085"
        )

        # Conteneur principal
        contenu = tk.Frame(
            self.root,
            bg="#f3f5f9"
        )
        contenu.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        # En-tête
        ttk.Label(
            contenu,
            text="Système de gestion des tickets",
            style="Titre.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            contenu,
            text="Créer, consulter et modifier vos tickets.",
            style="SousTitre.TLabel"
        ).pack(anchor="w", pady=(5, 20))

        # Formulaire de création
        self.formulaire = CreateTicketFrame(
            contenu,
            on_create=self.creer_ticket
        )
        self.formulaire.pack(
            fill="x",
            pady=(0, 18)
        )

        # Liste des tickets
        self.liste = TicketListFrame(
            contenu,
            on_view=self.consulter_ticket,
            on_edit=self.modifier_ticket
        )
        self.liste.pack(
            fill="both",
            expand=True
        )

        # Barre d'information
        self.info = tk.Label(
            contenu,
            text="0 ticket enregistré",
            bg="#f3f5f9",
            fg="#667085",
            anchor="w",
            font=("Arial", 9)
        )
        self.info.pack(fill="x", pady=(10, 0))

    def actualiser_compteur(self):
        # [MODIFIÉ] On compte les tickets enregistrés chez l'Admin
        nombre = len(self.admin.viewAllTickets())
        mot = "ticket" if nombre == 1 else "tickets"
        self.info.config(
            text=f"{nombre} {mot} enregistré{'s' if nombre > 1 else ''}"
        )

    def creer_ticket(self, donnees):
        # [MODIFIÉ] On crée un vrai objet Ticket au lieu d'un dictionnaire
        try:
            ticket = Ticket(
                self.admin.nextTicketId(),
                donnees["titre"],
                donnees["priorite"],
                donnees["description"]
            )
            self.admin.createTicket(self.utilisateur, ticket)
        except Exception as erreur:
            messagebox.showwarning("Erreur", str(erreur))
            return

        # [NOUVEAU] Ajouter les images choisies comme pièces jointes du ticket
        for chemin in donnees["images"]:
            try:
                self.utilisateur.addAttachment(ticket, chemin)
            except Exception as erreur:
                messagebox.showwarning("Image refusée", str(erreur))

        self.liste.ajouter_ticket(ticket.toDict())
        self.formulaire.vider_champs()
        self.actualiser_compteur()

        messagebox.showinfo(
            "Succès",
            "Le ticket a été créé avec succès."
        )

    def obtenir_ticket_selectionne(self):
        identifiant = self.liste.obtenir_selection()

        if identifiant is None:
            messagebox.showwarning(
                "Sélection",
                "Veuillez sélectionner un ticket."
            )
            return None

        #  On demande le ticket à l'Admin 
        ticket = self.admin.getTicket(identifiant)

        if ticket is None:
            messagebox.showerror(
                "Erreur",
                "Le ticket sélectionné est introuvable."
            )
        return ticket

    def consulter_ticket(self):
        ticket = self.obtenir_ticket_selectionne()

        if ticket is None:
            return

        #  La fenêtre de détails reçoit le dictionnaire du ticket
        TicketDetailsFrame(
            self.root,
            ticket.toDict(),
            on_add_comment=self.ajouter_commentaire
        )

    def ajouter_commentaire(self, donnees_ticket, commentaire):
        # [MODIFIÉ] On retrouve le vrai ticket, puis l'utilisateur commente
        ticket = self.admin.getTicket(donnees_ticket["id"])

        try:
            nouveau = self.utilisateur.addComment(ticket, commentaire)
        except Exception as erreur:
            messagebox.showwarning("Commentaire", str(erreur))
            return None

        messagebox.showinfo(
            "Succès",
            "Le commentaire a été ajouté avec succès."
        )
        # [NOUVEAU] Renvoyer le texte à afficher (ex. : "Babacar : mon commentaire")
        return str(nouveau)

    def modifier_ticket(self):
        ticket = self.obtenir_ticket_selectionne()

        if ticket is None:
            return

        #  La fenêtre de modification reçoit le dictionnaire du ticket
        EditTicketFrame(
            self.root,
            ticket.toDict(),
            on_save=self.enregistrer_modifications
        )

    def enregistrer_modifications(self, donnees_ticket, donnees):
        #  On retrouve le vrai ticket puis on le modifie avec updateTicket
        ticket = self.admin.getTicket(donnees_ticket["id"])

        try:
            self.utilisateur.updateTicket(
                ticket,
                donnees["titre"],
                donnees["priorite"],
                donnees["description"]
            )
        except Exception as erreur:
            messagebox.showwarning("Erreur", str(erreur))
            return

        self.liste.actualiser_ticket(ticket.toDict())

        messagebox.showinfo(
            "Succès",
            "Le ticket a été modifié avec succès."
        )


if __name__ == "__main__":
    root = tk.Tk()
    interface = UserInterface(root)
    root.mainloop()