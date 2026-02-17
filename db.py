import mysql.connector
import os
class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
        #self.conn = mysql.connector.connect(
         #   host="localhost",
          #  user="root",
           # password="Lokesh@04",
            #database="blog_db"
        #)
        self.cursor = self.conn.cursor(dictionary=True)
        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(50),
            email VARCHAR(100) UNIQUE,
            password VARCHAR(255),
            user_type VARCHAR(20)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts(
            id INT PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(200),
            content TEXT,
            author_id INT,
            FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments(
            id INT PRIMARY KEY AUTO_INCREMENT,
            comment TEXT,
            user_id INT,
            post_id INT,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
        )
        """)

        self.conn.commit()
        
    def insert(self,name,email,password,user_type):
        try:
            self.cursor.execute(
                "INSERT INTO users(name,email,password,user_type) VALUES (%s,%s,%s,%s)",
                (name,email,password,user_type)
            )
            self.conn.commit()
            return True
        except:
            return False
        
        
    def login(self,email,password):
        self.cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email,password)
        )    
        return self.cursor.fetchone()
    
    def get_user(self,user_id):
        self.cursor.execute("SELECT * FROM users WHERE id=%s",(user_id,))
        return self.cursor.fetchone()
    
    def insert_post(self,title,content,Author_id):
        self.cursor.execute(
            "INSERT INTO posts(title,content,author_id) VALUES(%s,%s,%s)",
            (title,content,Author_id)
            
        )
        self.conn.commit()
        
    def get_all_posts(self):
        self.cursor.execute(
            """
            SELECT posts.*,users.name
            FROM posts JOIN users ON posts.author_id=users.id
            ORDER BY id DESC
            """
        )
        return self.cursor.fetchall()
    
    def get_post_by_id(self,post_id):
        self.cursor.execute("SELECT * FROM posts WHERE id=%s",(post_id,))
        return self.cursor.fetchone()

    def update_post(self,post_id,title,content):
        self.cursor.execute(
            "UPDATE posts SET title=%s, content=%s WHERE id=%s",
            (title,content,post_id)
        )
        self.conn.commit()

    def delete_post(self,post_id):
        self.cursor.execute("DELETE FROM posts WHERE id=%s",(post_id,))
        self.conn.commit()

    def get_user_posts(self,user_id):
        self.cursor.execute("SELECT * FROM posts WHERE author_id=%s",(user_id,))
        return self.cursor.fetchall()

    # ---------------- COMMENTS ----------------

    def insert_comment(self,comment,user_id,post_id):
        self.cursor.execute(
            "INSERT INTO comments(comment,user_id,post_id) VALUES(%s,%s,%s)",
            (comment,user_id,post_id)
        )
        self.conn.commit()

    def get_comments(self,post_id):
        self.cursor.execute("""
            SELECT comments.*, users.name
            FROM comments JOIN users ON comments.user_id = users.id
            WHERE post_id=%s
            ORDER BY id DESC
        """,(post_id,))
        return self.cursor.fetchall()

        