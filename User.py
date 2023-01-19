class User:
    def __init__(self):
        self.firstName = None
        self.lastName = None
        self.pseudo = None
        self.nCard = None
        self.password = None
        self.token = None

    def setFirstName(self, firstName):
        self.firstName = firstName

    def setLastName(self, lastName):
        self.lastName = lastName

    def setPseudo(self, pseudo):
        self.pseudo = pseudo

    def setNCard(self, nCard):
        self.nCard = nCard

    def setPassword(self, password):
        self.password = password

    def setToken(self, token):
        self.token = token

    def show(self):
        print("Welcome " + self.firstName + " " + self.lastName + " !")
