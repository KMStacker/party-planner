import os
os.environ["DATABASE_FILE"] = "test_database.db"

import sqlite3
import random
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
import config

def seed_database():
    con = sqlite3.connect(config.database_file)
    cursor = con.cursor()

    cursor.execute("DELETE FROM user_availability")
    cursor.execute("DELETE FROM rsvps")
    cursor.execute("DELETE FROM event_categories")
    cursor.execute("DELETE FROM events")
    cursor.execute("DELETE FROM users")

    user_count = 1000*100
    event_count = 1000*1000

    password_hash = generate_password_hash("1234")
    user_ids = []
    user_statuses = ["Yes to everything", "No to everything", "Up to no good", "Some fun ty!", "Naaah", None]
    
    for i in range(1, user_count + 1):
        username = f"user_{i}"
        status = random.choice(user_statuses)
        cursor.execute(
            "INSERT INTO users (username, password_hash, status) VALUES (?, ?, ?)",
            (username, password_hash, status)
        )
        user_ids.append(cursor.lastrowid)

    cursor.execute("SELECT id FROM categories")
    category_ids = [row[0] for row in cursor.fetchall()]

    base_date = datetime.now()
    titles = ["small party", "big party", "average party", "epic party", "chill party", "wild party", "fun party", "casual party", "midsummer party", "winter party"]
    descriptions = ["small fun with friends.", "big fun with friends.", "average fun with friends.", "epic fun with friends.", "chill fun with friends.", "wild fun with friends.", "fun fun with friends.", "casual fun with friends.", "midsummer fun with friends.", "winter fun with friends."]

    for i in range(1, event_count + 1):
        user_id = random.choice(user_ids)
        title = f"{random.choice(titles)} #{i}"
        description = random.choice(descriptions)
        days_offset = random.randint(0, 365)
        start_datetime = base_date + timedelta(days=days_offset)
        event_date = start_datetime.date().isoformat()
        
        duration = random.choice([0, 0, random.randint(1, 14)])
        end_datetime = start_datetime + timedelta(days=duration)
        end_date = end_datetime.date().isoformat()
        
        cursor.execute(
            "INSERT INTO events (user_id, title, description, event_date, end_date) VALUES (?, ?, ?, ?, ?)",
            (user_id, title, description, event_date, end_date)
        )
        event_id = cursor.lastrowid

        num_categories = random.randint(0, 7)
        if num_categories > 0:
            sampled_cats = random.sample(category_ids, min(num_categories, len(category_ids)))
            for cat_id in sampled_cats:
                cursor.execute(
                    "INSERT INTO event_categories (event_id, category_id) VALUES (?, ?)",
                    (event_id, cat_id)
                )

        max_rsvps = min(len(user_ids)//20, 50)
        num_rsvps = random.randint(0, max_rsvps)
        sampled_users = random.sample(user_ids, num_rsvps)
        statuses = ["In", "Maybe", "Out"]

        for r_user_id in sampled_users:
            cursor.execute(
                "INSERT INTO rsvps (event_id, user_id, rsvp_status) VALUES (?, ?, ?)",
                (event_id, r_user_id, random.choice(statuses))
            )

    for user_id in user_ids:
        s1 = (base_date + timedelta(days=1)).date().isoformat()
        e1 = (base_date + timedelta(days=1)).date().isoformat()
        cursor.execute(
            "INSERT INTO user_availability (user_id, start_date, end_date, date_status) VALUES (?, ?, ?, ?)",
            (user_id, s1, e1, "Available")
        )
        
        s2 = (base_date + timedelta(days=10)).date().isoformat()
        e2 = (base_date + timedelta(days=15)).date().isoformat()
        cursor.execute(
            "INSERT INTO user_availability (user_id, start_date, end_date, date_status) VALUES (?, ?, ?, ?)",
            (user_id, s2, e2, "Unavailable")
        )
        
        s3 = (base_date + timedelta(days=20)).date().isoformat()
        e3 = (base_date + timedelta(days=25)).date().isoformat()
        cursor.execute(
            "INSERT INTO user_availability (user_id, start_date, end_date, date_status) VALUES (?, ?, ?, ?)",
            (user_id, s3, e3, "Available")
        )

    con.commit()
    con.close()

if __name__ == "__main__":
    seed_database()