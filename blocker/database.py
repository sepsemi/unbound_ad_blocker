import sqlite3

class Database:
    
    def __init__(self):
        path = '/usr/local/etc/unbound/blocker/etc/database.db'
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
    
    def table_create(self, table):
        sql = """
            CREATE TABLE IF NOT EXISTS {} (
                domain TEXT NOT NULL,
                tld TEXT NOT NULL,
                lenght INTEGER NOT NULL,
                PRIMARY KEY(domain)
            );
        """

        self.cursor.execute(sql.format(table))

    def table_insert(self, table, **data):
        tld = data['tld']
        lenght = data['lenght'] 
        domain = data['domain']
        
        sql = """
            INSERT OR IGNORE INTO {} (domain, tld, lenght)
            VALUES (?, ?, ?)
        """
        self.cursor.execute(sql.format(table), (domain, tld, lenght))

    def table_fetch_one(self, table, **data):        
        tld = data['tld']
        lenght = data['lenght'] 
        domain = data['domain']

        sql = """
            SELECT tld, lenght, domain 
            FROM {}
            WHERE tld = ? and lenght = ? and domain = ?
        """

        self.cursor.execute(sql.format(table), (tld, lenght, domain))
        return self.cursor.fetchone()


    
