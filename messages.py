class Message:
    def __init__(self, connection):
        self.connection = connection
    
    def create(self):
        create_table = '''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            symbol TEXT,
            data TEXT
        )
        '''
        cursor = self.connection.cursor()
        cursor.execute(create_table)
        self.connection.commit()