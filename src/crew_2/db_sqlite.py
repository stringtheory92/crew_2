import sqlite3

class DBHandler:
    def __init__(self, db_path='ai_articles.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    link TEXT,
                    summary TEXT
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS Products (
                    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_name TEXT NOT NULL,
                    product_details TEXT
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS Features (
                    feature_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER,
                    feature_name TEXT NOT NULL,
                    feature_details TEXT,
                    FOREIGN KEY (product_id) REFERENCES Products(product_id)
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS FeatureDetails (
                    detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    feature_id INTEGER,
                    detail_name TEXT NOT NULL,
                    detail_value TEXT,
                    FOREIGN KEY (feature_id) REFERENCES Features(feature_id)
                )
            ''')

    def execute_query(self, query, params=()):
        with self.conn:
            cursor = self.conn.execute(query, params)
        return cursor

    def fetch_all(self, query, params=()):
        cursor = self.conn.execute(query, params)
        return cursor.fetchall()

    def fetch_one(self, query, params=()):
        cursor = self.conn.execute(query, params)
        return cursor.fetchone()

    def close(self):
        self.conn.close()