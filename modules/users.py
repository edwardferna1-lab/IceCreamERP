import sqlite3
import hashlib

DB = "database/northpos.db"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def create_user(username, password, role):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    try:
        cursor.execute("""
        INSERT INTO users
        (username, password, role)
        VALUES (?, ?, ?)
        """, (username, hashed_password, role))

        conn.commit()
        print("User created successfully.")

    except sqlite3.IntegrityError:
        print("Error: Username already exists.")

    finally:
        conn.close()


def login(username, password):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    cursor.execute("""
    SELECT id, username, role
    FROM users
    WHERE username = ? AND password = ?
    """, (username, hashed_password))

    user = cursor.fetchone()
    conn.close()

    if user:
        print("Access granted.")
        print(user)
        return user
    else:
        print("Access denied.")
        return None


def list_users():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, username, role
    FROM users
    """)

    users = cursor.fetchall()

    for user in users:
        print(user)

    conn.close()


if __name__ == "__main__":
    print("NORTHPOS - USERS MODULE")
    print("-----------------------")

    create_user("edward", "admin123", "ADMIN")
    login("edward", "admin123")
    list_users()