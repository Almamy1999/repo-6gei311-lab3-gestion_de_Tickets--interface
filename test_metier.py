import os
import unittest

from Ticket import Ticket, OUVERT, ASSIGNE, VALIDATION, TERMINE, FERME
from User import User
from Admin import Admin
from Attachment import AttachmentFactory, TextAttachment, ImageAttachment


class TestGestionTickets(unittest.TestCase):

    def setUp(self):
       
        self.admin = Admin(1, "Bamba", "bamba@uqac.ca")
        self.client = User(1, "Client", "client@uqac.ca", "Utilisateur")
        self.dev = User(2, "Almamy", "almamy@uqac.ca", "Développeur")
        self.autre = User(3, "Autre", "autre@uqac.ca", "Utilisateur")

        self.ticket = Ticket(self.admin.nextTicketId(), "Bug d'affichage", "Haute", "L'écran reste noir")
        self.admin.createTicket(self.client, self.ticket)

        
        fichier = open("test_notes.txt", "w", encoding="utf-8")
        fichier.write("Étapes pour reproduire le bug")
        fichier.close()

        fichier = open("test_capture.png", "w")
        fichier.write("fausse image")
        fichier.close()

    def tearDown(self):
       
        os.remove("test_notes.txt")
        os.remove("test_capture.png")

   

    def test_creer_ticket(self):
        self.assertEqual(self.ticket.status, OUVERT)
        self.assertEqual(self.ticket.creator, self.client)
        self.assertEqual(self.ticket.description, "L'écran reste noir")
        self.assertEqual(len(self.admin.viewAllTickets()), 1)

    def test_titre_vide_refuse(self):
        with self.assertRaises(ValueError):
            Ticket(99, "   ")

    def test_priorite_invalide_refusee(self):
        with self.assertRaises(ValueError):
            Ticket(99, "Titre", "Urgente")

   

    def test_assigner_a_un_developpeur(self):
        self.admin.assignTicket(self.ticket, self.dev)
        self.assertEqual(self.ticket.status, ASSIGNE)
        self.assertEqual(self.ticket.assignedTo, self.dev)

    def test_assigner_a_un_non_developpeur_refuse(self):
        with self.assertRaises(PermissionError):
            self.admin.assignTicket(self.ticket, self.autre)

    
    def test_cycle_complet(self):
        self.admin.assignTicket(self.ticket, self.dev)
        self.dev.submitForValidation(self.ticket)
        self.assertEqual(self.ticket.status, VALIDATION)
        self.admin.validateTicket(self.ticket)
        self.assertEqual(self.ticket.status, TERMINE)

    def test_rejet_retour_au_developpeur(self):
        self.admin.assignTicket(self.ticket, self.dev)
        self.dev.submitForValidation(self.ticket)
        self.admin.rejectTicket(self.ticket, "Le bug est encore là")
        self.assertEqual(self.ticket.status, ASSIGNE)

    def test_transition_interdite(self):
       
        with self.assertRaises(ValueError):
            self.ticket.updateStatus(TERMINE)

    

    def test_fermeture_directe(self):
        self.admin.closeTicket(self.ticket)
        self.assertEqual(self.ticket.status, FERME)

    def test_fermer_deux_fois_refuse(self):
        self.admin.closeTicket(self.ticket)
        with self.assertRaises(ValueError):
            self.admin.closeTicket(self.ticket)

   

    def test_createur_peut_modifier(self):
        self.client.updateTicket(self.ticket, "Nouveau titre", "Basse", "Nouvelle description")
        self.assertEqual(self.ticket.title, "Nouveau titre")
        self.assertEqual(self.ticket.priority, "Basse")
        self.assertEqual(self.ticket.description, "Nouvelle description")

    def test_autre_utilisateur_ne_peut_pas_modifier(self):
        with self.assertRaises(PermissionError):
            self.autre.updateTicket(self.ticket, "Pirate")

    def test_ticket_ferme_non_modifiable(self):
        self.admin.closeTicket(self.ticket)
        with self.assertRaises(PermissionError):
            self.client.updateTicket(self.ticket, "Trop tard")

    

    def test_ajouter_et_consulter_commentaires(self):
        self.client.addComment(self.ticket, "Ça arrive au démarrage")
        self.admin.addComment(self.ticket, "Pris en charge")
        commentaires = self.client.viewTicket(self.ticket)["commentaires"]
        self.assertEqual(commentaires, ["Client : Ça arrive au démarrage", "Bamba : Pris en charge"])

    def test_commentaire_vide_refuse(self):
        with self.assertRaises(ValueError):
            self.client.addComment(self.ticket, "   ")

   

    def test_fabrique_choisit_le_bon_type(self):
        fabrique = AttachmentFactory()
        self.assertIsInstance(fabrique.create("test_notes.txt"), TextAttachment)
        self.assertIsInstance(fabrique.create("test_capture.png"), ImageAttachment)

    def test_ajouter_et_charger_pieces_jointes(self):
        self.client.addAttachment(self.ticket, "test_notes.txt")
        self.client.addAttachment(self.ticket, "test_capture.png")
        self.assertEqual(len(self.ticket.attachments), 2)
        self.assertEqual(self.ticket.attachments[0].load(), "Étapes pour reproduire le bug")
        self.assertEqual(self.ticket.attachments[1].load(), "test_capture.png")

    def test_extension_non_acceptee(self):
        with self.assertRaises(ValueError):
            AttachmentFactory().create("virus.exe")

    def test_fichier_introuvable(self):
        with self.assertRaises(FileNotFoundError):
            AttachmentFactory().create("absent.png")

    

    def test_seul_le_dev_assigne_envoie_en_validation(self):
        self.admin.assignTicket(self.ticket, self.dev)
        with self.assertRaises(PermissionError):
            self.client.submitForValidation(self.ticket)

    def test_piece_jointe_non_autorisee(self):
        with self.assertRaises(PermissionError):
            self.autre.addAttachment(self.ticket, "test_capture.png")

    def test_role_invalide_refuse(self):
        with self.assertRaises(ValueError):
            User(9, "X", "x@uqac.ca", "Chef")


if __name__ == "__main__":
    unittest.main(verbosity=2)