import tkinter as tk
from tkinter import messagebox


class TicketDetailsFrame(tk.Toplevel):
    def __init__(self, parent, ticket, on_add_comment):
        super().__init__(parent)
        self.title('Détails du ticket')
        self.geometry('620x680')                 
        self.ticket = ticket
        self.on_add_comment = on_add_comment
        self.images_affichees = []              

        infos = (f"ID : {ticket['id']}\nTitre : {ticket['titre']}\n"
                 f"Description : {ticket['description']}\nPriorité : {ticket['priorite']}\n"
                 f"Statut : {ticket['statut']}")
        tk.Label(self, text=infos, justify='left', wraplength=570).pack(anchor='w', padx=20, pady=15)

        # Images de la description 
        tk.Label(self, text='Images :').pack(anchor='w', padx=20)
        zone_images = tk.Frame(self)
        zone_images.pack(anchor='w', padx=20, pady=5)

        nombre_images = 0
        for piece in ticket['pieces_jointes']:
            chemin = piece.path
            if chemin.lower().endswith('.png') or chemin.lower().endswith('.gif'):
                try:
                    image = tk.PhotoImage(file=chemin)
                except tk.TclError:
                    tk.Label(zone_images, text=piece.getName() + ' (illisible)').pack(side='left', padx=5)
                    continue

                # Réduire l'image pour qu'elle fasse au plus environ 180 pixels de large
                facteur = image.width() // 180 + 1
                image = image.subsample(facteur, facteur)

                # Garder l'image dans une liste
                self.images_affichees.append(image)
                tk.Label(zone_images, image=image).pack(side='left', padx=5)
                nombre_images = nombre_images + 1

        if nombre_images == 0:
            tk.Label(zone_images, text='Aucune image', fg='#667085').pack(side='left')

        # Commentaires
        tk.Label(self, text='Commentaires :').pack(anchor='w', padx=20, pady=(10, 0))
        self.liste_commentaires = tk.Listbox(self, width=75, height=7)
        self.liste_commentaires.pack(fill='both', expand=True, padx=20, pady=5)
        for commentaire in ticket['commentaires']:
            self.liste_commentaires.insert(tk.END, commentaire)

        self.entry_commentaire = tk.Entry(self, width=60)
        self.entry_commentaire.pack(padx=20, pady=5)
        tk.Button(self, text='Ajouter un commentaire', command=self.ajouter_commentaire).pack(pady=10)

    def ajouter_commentaire(self):
        commentaire = self.entry_commentaire.get().strip()
        if not commentaire:
            messagebox.showwarning('Commentaire', 'Veuillez saisir un commentaire.', parent=self)
            return

        # on affiche le texte renvoyé par la logique métier (avec le nom de l'auteur)
        texte_affiche = self.on_add_comment(self.ticket, commentaire)
        if texte_affiche is not None:
            self.liste_commentaires.insert(tk.END, texte_affiche)
            self.entry_commentaire.delete(0, tk.END)