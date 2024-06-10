from database.connection import get_db_connection

class Magazine:
    all = {}
    def __init__(self, id, name = None, category = None):
        self._id = id
        self._name = name
        self._category = category

    def __repr__(self):
        return f'<Magazine {self.id} {self.name} {self.category}>'
    
    @property
    def id(self):
        return self._id    
    @id.setter
    def id(self, id):
        if isinstance(id, int):
            self._id = id

    @property
    def name(self):
        return self._name    
    @name.setter
    def name(self, new_name):
        if isinstance(new_name, str) and 2 <= len(new_name) <= 16:
            self._name = new_name

        CURSOR.execute(sql, (self.id,))
        author_data = CURSOR.fetchall()

        if not author_data:
            return None

        authors = []
        for row in author_data:
            authors.append(Author(*row)) 

        return authors
    
    @classmethod
    def find_by_id(cls, id):
        conn = get_db_connection()
        CURSOR = conn.cursor()
        sql = """
            SELECT * FROM magazines
            WHERE id = ?
        """
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        if row:
            return Magazine(*row)
        return None