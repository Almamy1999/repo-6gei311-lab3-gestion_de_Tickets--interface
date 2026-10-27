import tkinter as tk
from tkinter import ttk, messagebox


class EditTicketFrame(tk.Toplevel):
    def __init__(self, parent, ticket, on_save):
        super().__init__(parent)
        self.title('Modifier un ticket')
        self.geometry('520x400')
        self.ticket = ticket
        self.on_save = on_save

        tk.Label(self, text='Titre :').pack(pady=5)
        self.entry_titre = tk.Entry(self, width=48)
        self.entry_titre.pack()
        self.entry_titre.insert(0, ticket['titre'])

        tk.Label(self, text='Description :').pack(pady=5)
        self.entry_description = tk.Text(self, width=48, height=5)
        self.entry_description.pack()
        self.entry_description.insert('1.0', ticket['description'])

        tk.Label(self, text='Priorité :').pack(pady=5)
        self.combo_priorite = ttk.Combobox(self, values=['Basse', 'Moyenne', 'Haute'], state='readonly')
        self.combo_priorite.pack()
        self.combo_priorite.set(ticket['priorite'])

        tk.Button(self, text='Enregistrer', command=self.enregistrer_modifications).pack(pady=20)

    def enregistrer_modifications(self):
        donnees = {
            'titre': self.entry_titre.get().strip(),
            'description': self.entry_description.get('1.0', tk.END).strip(),
            'priorite': self.combo_priorite.get(),
        }
        if not donnees['titre'] or not donnees['description']:
            messagebox.showwarning('Champs obligatoires', 'Veuillez remplir tous les champs.', parent=self)
            return
        self.on_save(self.ticket, donnees)
        self.destroy()
