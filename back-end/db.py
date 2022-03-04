def create_tables(db):
    db.execute("""
        CREATE TABLE movies (
            name VARCHAR(255) NOT NULL PRIMARY KEY,
            director VARCHAR(255) NOT NULL,
            poster VARCHAR(255) NOT NULL
        )
    """)
    db.execute("""
        CREATE TABLE comments (
            id INT (255) NOT NULL PRIMARY KEY,
            movie_name VARCHAR(255) NOT NULL,
            user_name VARCHAR(255) NOT NULL,
            comment VARCHAR(255) NOT NULL
        )
    """)
    db.commit()


def get_comment_counts(db, movie_name):
    return db.execute("""
        SELECT COUNT(*)
        FROM comments
        WHERE movie_id = (
            SELECT name
            FROM movies
            WHERE name = ?
        )
    """, (movie_name,)).fetchone()[0]


def add_comment_to_db(db, comment):
    db.execute("""
        INSERT INTO comments (
            id,
            movie_name,
            user_name,
            comment
        ) VALUES (
            ?, ?, ?, ?
        )
    """, (
        get_comment_counts(db, comment['movie_name']),
        comment['movie_name'],
        comment['user_name'],
        comment['comment']
    ))
    db.commit()


def get_movies(db):
    return db.execute("""
        SELECT name, director, poster
        FROM movies
    """).fetchall()


def get_comments(db, movie_name):
    return db.execute("""
        SELECT user_name, comment
        FROM comments
        WHERE movie_name = ?
    """, (movie_name,)).fetchall()
