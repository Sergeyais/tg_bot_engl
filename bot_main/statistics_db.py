import sqlite3

class DatabaseStatistics:
    def __init__(self, db_file='statistics.db'):
        self.db_file = db_file
        self.create_user_requests_table()

    def create_user_requests_table(self):
        query = '''CREATE TABLE IF NOT EXISTS user_requests (id INTEGER PRIMARY KEY, requests INTEGER DEFAULT 0)'''
        self.execute_query(query)

    def execute_query(self, query, parameters=None):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        result = None

        try:
            if parameters is None:
                cursor.execute(query)
            else:
                cursor.execute(query, parameters)
            conn.commit()

            if query.strip().startswith("SELECT"):
                result = cursor.fetchone()  
            
        except sqlite3.Error as e:
            print("Ошибка при выполнении запроса:", e)
        finally:
            conn.close()
        return result

    def increment_requests_count(self, user_id):
        query = '''UPDATE user_requests SET requests=requests+1 WHERE id=?'''
        self.execute_query(query, (user_id,))

    def check_id_in_stat_database(self, user_id):
        query = '''CREATE TABLE IF NOT EXISTS user_requests (id INTEGER PRIMARY KEY, requests INTEGER DEFAULT 0)'''
        self.execute_query(query)

        query = '''SELECT id FROM user_requests WHERE id = ?'''
        result = self.execute_query(query, (user_id,))
        return result is not None

    def add_id_to_database(self, user_id):
        query = '''CREATE TABLE IF NOT EXISTS user_requests (id INTEGER PRIMARY KEY, requests INTEGER DEFAULT 0)'''
        self.execute_query(query)

        query = '''INSERT OR IGNORE INTO user_requests (id, requests) VALUES (?, 0)'''
        self.execute_query(query, (user_id,))

    def get_requests_count(self, user_id):
        query = '''SELECT requests FROM user_requests WHERE id=?'''
        result = self.execute_query(query, (user_id,))
        return result[0] if result else None
    

