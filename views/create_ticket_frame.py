
import os
import tkinter as tk
from tkinter import ttk, filedialog          # [MODIFIÉ] ajout de filedialog


class CreateTicketFrame(tk.LabelFrame):
    def __init__(self, parent, on_create):
        super().__init__( 
            parent,
            text="Créer un ticket",
            font=("Arial", 11, "bold"),
            padx=18,
            pady=15,
            bg="white",
            fg="#243247"
        )

        self.on_create = on_create
        self.images = []          # [NOUVEAU] chemins des images choisies

        self.columnconfigure(1, weight=1)

        # Titre
        tk.Label(
            self,
            text="Titre :",
            bg="white"
        ).grid(row=0, column=0, sticky="w", pady=6)

        self.champ_titre = ttk.Entry(self)
        self.champ_titre.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(15, 0),
            pady=6
        )

        # Description
        tk.Label(
            self,
            text="Description :",
            bg="white"
        ).grid(row=1, column=0, sticky="nw", pady=6)

        self.champ_description = tk.Text(
            self,
            height=4,
            wrap="word",
            font=("Arial", 10),
            relief="solid",
            borderwidth=1
        )
        self.champ_description.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(15, 0),
            pady=6
        )

        # [NOUVEAU] Images de la description
        tk.Label(
            self,
            text="Images :",
            bg="white"
        ).grid(row=2, column=0, sticky="w", pady=6)

        zone_images = tk.Frame(self, bg="white")
        zone_images.grid(row=2, column=1, sticky="ew", padx=(15, 0), pady=6)

        ttk.Button(
            zone_images,
            text="Ajouter une image...",
            command=self.choisir_image
        ).pack(side="left")

        self.label_images = tk.Label(
            zone_images,
            text="Aucune image",
            bg="white",
            fg="#667085"
        )
        self.label_images.pack(side="left", padx=10)

        # Priorité
        tk.Label(
            self,
            text="Priorité :",
            bg="white"
        ).grid(row=3, column=0, sticky="w", pady=6)

        self.priorite = tk.StringVar(value="Moyenne")

        self.champ_priorite = ttk.Combobox(
            self,
            textvariable=self.priorite,
            values=["Basse", "Moyenne", "Haute"],
            state="readonly"
        )
        self.champ_priorite.grid(
            row=3,
            column=1,
            sticky="ew",
            padx=(15, 0),
            pady=6
        )

        # Bouton de création
        ttk.Button(
            self,
            text="Créer le ticket",
            command=self.creer_ticket
        ).grid(
            row=4,
            column=1,
            sticky="e",
            pady=(12, 0)
        )

    # [NOUVEAU]
    def choisir_image(self):
        # Ouvre la fenêtre Windows pour choisir un fichier.
        # tkinter sait afficher seulement les PNG et les GIF.
        chemin = filedialog.askopenfilename(
            title="Choisir une image",
            filetypes=[("Images", "*.png *.gif")]
        )
        if chemin == "":
            return        # l'utilisateur a cliqué sur Annuler

        self.images.append(chemin)

        # Afficher les noms des images choisies
        noms = []
        for image in self.images:
            noms.append(os.path.basename(image))
        self.label_images.config(text=", ".join(noms))

    def creer_ticket(self):
        donnees = {
            "titre": self.champ_titre.get(),
            "description": self.champ_description.get(
                "1.0", "end-1c"
            ),
            "priorite": self.priorite.get(),
            "images": list(self.images)        # [NOUVEAU]
        }

        self.on_create(donnees)

    def vider_champs(self):
        self.champ_titre.delete(0, tk.END)
        self.champ_description.delete("1.0", tk.END)
        self.priorite.set("Moyenne")
        self.images = []                                  # [NOUVEAU]
        self.label_images.config(text="Aucune image")     # [NOUVEAU]