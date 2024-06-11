from database.connection import get_db_connection

class Magazine:
    all = {}
    
    def __init__(self, id, name=None, category=None):
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

    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, new_category):
        if isinstance(new_category, str) and new_category:
            self._category = new_category

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO magazines (name, category) VALUES (?, ?)",
            (self.name, self.category)
        )
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, category):
        magazine = cls(None, name, category)
        magazine.save()
        return magazine
    
    def get_magazine_id(self):
        return self.id
    
    def articles(self):
        from models.article import Article
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT ar.* FROM articles ar INNER JOIN magazines m ON ar.magazine = m.id WHERE m.id = ?",
            (self.id,)
        )
        articles = [Article(*row) for row in cursor.fetchall()]
        conn.close()
        return articles

    def contributors(self):
        from models.author import Author
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT DISTINCT a.* FROM authors a "
            "INNER JOIN articles ar ON ar.author = a.id "
            "INNER JOIN magazines m ON ar.magazine = m.id WHERE m.id = ?",
            (self.id,)
        )
        authors = [Author(*row) for row in cursor.fetchall()]
        conn.close()
        return authors

    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT ar.title FROM articles ar INNER JOIN magazines m ON ar.magazine = m.id WHERE m.id = ?",
            (self.id,)
        )
        titles = [row[0] for row in cursor.fetchall()]
        conn.close()
        return titles

    def contributing_authors(self):
        from models.author import Author
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT DISTINCT a.* FROM authors a "
            "INNER JOIN articles ar ON ar.author = a.id "
            "INNER JOIN magazines m ON ar.magazine = m.id WHERE m.id = ? "
            "GROUP BY a.id HAVING COUNT(ar.id) > 2",
            (self.id,)
        )
        authors = [Author(*row) for row in cursor.fetchall()]
        conn.close()
        return authors

    @classmethod
    def find_by_id(cls, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(*row)
        return None
