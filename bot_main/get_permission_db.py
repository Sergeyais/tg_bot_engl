import sqlite3

class DatabasePer:
    def __init__(self, db_file='../bot_refistpermissions.db'):
        self.db_file = db_file

    def check_id_in_database(self, user_id):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        try:
            cursor.execute('''SELECT id FROM id_table WHERE id = ?''', (user_id,))
            result = cursor.fetchone()

            if result is not None:
                return True
            else:
                return False
        except sqlite3.Error as e:
            print("Ошибка при выполнении запроса:", e)
        finally:
            conn.close()
