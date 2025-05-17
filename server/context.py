from server.database.database import DatabaseClient


class ApplicationContext:

    def __init__(self):
        self.databaseClient = DatabaseClient()
        self.closeFlag = False

    def close(self):
        self.databaseClient.close()
        self.closeFlag = True


applicationContext = ApplicationContext()


def close():
    if applicationContext is not None and applicationContext.closeFlag is False:
        applicationContext.close()