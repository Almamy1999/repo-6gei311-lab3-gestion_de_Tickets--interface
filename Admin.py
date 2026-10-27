from Ticket import ASSIGNE, VALIDATION, TERMINE, FERME


class Admin:
    def __init__(self, admin_id, name, email):
        self.adminID = admin_id
        self.name = name
        self.email = email
        self._tickets = []          
        self._prochain_id = 1       

    

    def nextTicketId(self):
        
        numero = self._prochain_id
        self._prochain_id = self._prochain_id + 1
        return numero

    def getTicket(self, ticket_id):
       
        for ticket in self._tickets:
            if ticket.ticketID == ticket_id:
                return ticket
        return None

    def registerTicket(self, ticket):
       
        if self.getTicket(ticket.ticketID) is not None:
            raise ValueError("Le ticket #" + str(ticket.ticketID) + " existe déjà.")
        self._tickets.append(ticket)

        
        if ticket.ticketID >= self._prochain_id:
            self._prochain_id = ticket.ticketID + 1

    def createTicket(self, user, ticket):
        user.createTicket(ticket)
        self.registerTicket(ticket)
        return ticket

    def viewAllTickets(self):
       
        return list(self._tickets)

    

    def viewTicket(self, user, ticket):
        return user.viewTicket(ticket)

    def updateTicket(self, user, ticket, title=None, priority=None, description=None):
        return user.updateTicket(ticket, title, priority, description)

    def addComment(self, ticket, texte):
        return ticket.addComment(texte, self)

   

    def assignTicket(self, ticket, user):
        
        if not user.isDeveloper():
            raise PermissionError(user.name + " n'est pas un développeur.")
        ticket.assignTo(user)

    def validateTicket(self, ticket):
       
        if ticket.status != VALIDATION:
            raise ValueError("Le ticket doit être en VALIDATION pour être validé.")
        ticket.updateStatus(TERMINE)

    def rejectTicket(self, ticket, raison=""):
        
        if ticket.status != VALIDATION:
            raise ValueError("Le ticket doit être en VALIDATION pour être rejeté.")
        ticket.updateStatus(ASSIGNE)
        if raison.strip() != "":
            ticket.addComment("Rejeté : " + raison, self)

    def closeTicket(self, ticket):
        
        if ticket.isClosed():
            raise ValueError("Ce ticket est déjà fermé.")
        ticket.updateStatus(FERME)

    def __str__(self):
        return self.name + " (Admin)" 
