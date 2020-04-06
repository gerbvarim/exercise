import sqlite3
import threading

class DataBaseWrapper(object):
    
    def __init__(self, file_name, table_name, conversion_function):
        self.conversion_function = conversion_function
        self.conn = sqlite3.connect(file_name, check_same_thread = False)
        self.cursor = self.conn.cursor()
        self.table_name = table_name
        try:
            self.cursor.execute('CREATE TABLE '+table_name+' (key, val)')
        except sqlite3.OperationalError:#the tabel may already exist, in this case it can not be created
            pass
        self.lock = threading.Lock()
    
    def __getitem__(self, key):
        with self.lock:#access db with lock to avoid chance of data corruption
            self.cursor.execute('SELECT * FROM '+self.table_name+' WHERE key=\''+str(key)+'\' ')
            result = self.cursor.fetchall()
        if len(result) == 0:
            return None
        return self.conversion_function(result[0][1])
    
    def __setitem__(self, key, val):
        with self.lock:#access db with lock to avoid chance of data corruption
            self.cursor.execute('DELETE FROM '+self.table_name+' WHERE key=\''+str(key)+'\' ')
            self.cursor.execute('INSERT into '+self.table_name+' VALUES (\''+str(key)+'\', \''+str(val)+'\')')
            self.conn.commit()
    
    def key_in_db(self, key):
        return self[key] != None