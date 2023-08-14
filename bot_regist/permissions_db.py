import sqlite3

class PermissionsDatabase:
    def __init__(self, database_name='permissions.db'):
        self.database_name = database_name
        self.conn = sqlite3.connect(self.database_name)
        self.cursor = self.conn.cursor()
        self._create_table_if_not_exists()

    def _create_table_if_not_exists(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS id_table (id INTEGER PRIMARY KEY)''')
            self.conn.commit()
        except sqlite3.Error as e:
            print("Ошибка при создании таблицы:", e)

    def check_id_in_database(self, id):
        try:
            self.cursor.execute('''SELECT id FROM id_table WHERE id = ?''', (id,))
            result = self.cursor.fetchone()
            return result is not None
        except sqlite3.Error as e:
            print("Error executing query:", e)
            return False
        

    def add_id_to_database(self, id):
        try:
            self.cursor.execute('''INSERT INTO id_table (id) VALUES (?)''', (id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print("Error adding ID to database:", e)
            return False
        

    def remove_id_from_database(self, id):
        try:
            self.cursor.execute('''DELETE FROM id_table WHERE id = ?''', (id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print("Error removing ID from database:", e)
            return False
        
    
    def close_connection(self):
        self.conn.close()
    

        


