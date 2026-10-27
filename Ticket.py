from datetime import datetime
from Attachment import Attachment


# Les statuts possibles d'un ticket
OUVERT = "OUVERT"
ASSIGNE = "ASSIGNÉ"
VALIDATION = "VALIDATION"
TERMINE = "TERMINÉ"
FERME = "FERMÉ"


PRIORITES = ["Basse", "Moyenne", "Haute"]

# les transitions possible

TRANSITIONS = {
    OUVERT: [ASSIGNE, FERME],
    ASSIGNE: [VALIDATION, FERME],
    VALIDATION: [TERMINE, ASSIGNE, FERME],
    TERMINE: [],
    FERME: [],
}


class Comment:
    def __init__(self, auteur, texte):
        texte = texte.strip()
        if texte == "":
            raise ValueError("Le commentaire est vide.")
        self.auteur = auteur
        self.texte = texte
        self.date = datetime.now()

    def __str__(self):
        if self.auteur is None:
            nom = "Anonyme"
        else:
            nom = self.auteur.name
        return nom + " : " + self.texte


class Ticket:
    def __init__(self, ticket_id, title, priority="Moyenne", description=""):
       
        if title.strip() == "":
            raise ValueError("Le titre est obligatoire.")

       
        if priority not in PRIORITES:
            raise ValueError("Priorité invalide : " + priority)

        self.ticketID = ticket_id
        self.title = title.strip()
        self.priority = priority
        self.description = description.strip()
        self.status = OUVERT
        self.creationDate = datetime.now()
        self.updateDate = datetime.now()

        self.creator = None
        self.assignedTo = None
        self.comments = [] 
        self.attachments = [] 

    def isClosed(self):
       
        return self.status == TERMINE or self.status == FERME

    def updateInfo(self, title=None, priority=None, description=None):
        if self.isClosed():
            raise PermissionError("Ce ticket est fermé, on ne peut plus le modifier.")

        if title is not None:
            if title.strip() == "":
                raise ValueError("Le titre est obligatoire.")
            self.title = title.strip()

        if priority is not None:
            if priority not in PRIORITES:
                raise ValueError("Priorité invalide : " + priority)
            self.priority = priority

        if description is not None:
            self.description = description.strip()

        self.updateDate = datetime.now()

    def updateStatus(self, nouveau_statut):
        statuts_permis = TRANSITIONS[self.status]
        if nouveau_statut not in statuts_permis:
            raise ValueError("Transition interdite : " + self.status + " -> " + nouveau_statut)

        self.status = nouveau_statut
        self.updateDate = datetime.now()

    def assignTo(self, user):
       
        if self.status != ASSIGNE:
            self.updateStatus(ASSIGNE)
        self.assignedTo = user
        self.updateDate = datetime.now()

    def addComment(self, texte, auteur=None):
        commentaire = Comment(auteur, texte)
        self.comments.append(commentaire)
        self.updateDate = datetime.now()
        return commentaire

    def addAttachment(self, attachment):
        if not isinstance(attachment, Attachment):
            raise TypeError("Ce n'est pas une pièce jointe valide.")
        if self.isClosed():
            raise PermissionError("Ce ticket est fermé, on ne peut plus ajouter de pièce jointe.")

        self.attachments.append(attachment)
        self.updateDate = datetime.now()

    def toDict(self):
        
        liste_commentaires = []
        for commentaire in self.comments:
            liste_commentaires.append(str(commentaire))

        return {
            "id": self.ticketID,
            "titre": self.title,
            "description": self.description,
            "priorite": self.priority,
            "statut": self.status,
            "commentaires": liste_commentaires,
            "pieces_jointes": self.attachments,
        }

    def __str__(self):
        return "Ticket #" + str(self.ticketID) + " - " + self.title + " [" + self.status + "]"