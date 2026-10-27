from Ticket import ASSIGNE, VALIDATION
from Attachment import AttachmentFactory



UTILISATEUR = "Utilisateur"
DEVELOPPEUR = "Développeur"


class User:
    def __init__(self, user_id, name, email, role=UTILISATEUR):
      
        if role != UTILISATEUR and role != DEVELOPPEUR:
            raise ValueError("Rôle invalide : " + role)

        self.userID = user_id
        self.name = name 
        self.email = email
        self.role = role

    def isDeveloper(self):
        return self.role == DEVELOPPEUR

    def createTicket(self, ticket):
       
        if ticket.creator is not None:
            raise ValueError("Ce ticket a déjà un créateur.")
        ticket.creator = self
        return ticket

    def viewTicket(self, ticket):
       
        return ticket.toDict()

    def updateTicket(self, ticket, title=None, priority=None, description=None):
       
        if ticket.creator != self:
            raise PermissionError(self.name + " n'est pas le créateur de ce ticket.")
        ticket.updateInfo(title, priority, description)
        return ticket

    def addComment(self, ticket, texte):
       
        return ticket.addComment(texte, self)

    def addAttachment(self, ticket, chemin):
       
        if ticket.creator != self and ticket.assignedTo != self:
            raise PermissionError(self.name + " ne peut pas ajouter de pièce jointe à ce ticket.")

        fabrique = AttachmentFactory()
        piece = fabrique.create(chemin)
        ticket.addAttachment(piece)
        return piece

    def submitForValidation(self, ticket):
        
        if not self.isDeveloper():
            raise PermissionError("Seul un développeur peut envoyer un ticket en validation.")
        if ticket.assignedTo != self:
            raise PermissionError("Ce ticket n'est pas assigné à " + self.name + ".")
        if ticket.status != ASSIGNE:
            raise ValueError("Le ticket doit être ASSIGNÉ pour être envoyé en validation.")

        ticket.updateStatus(VALIDATION)

    def __str__(self):
        return self.name + " (" + self.role + ")" 
