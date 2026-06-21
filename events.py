import db

def get_events():
    sql = """
    SELECT events.id, events.user_id, events.title, events.event_date, events.end_date, users.username
    FROM events 
    JOIN users ON events.user_id = users.id 
    ORDER BY events.event_date ASC
    """
    return db.query(sql)

def get_categories():
    sql = "SELECT id, name FROM categories ORDER BY name"
    return db.query(sql)

def create_event(user_id, title, description, event_date, end_date, category_ids):
    con = db.get_connection()
    try:
        with con:
            event_id = con.execute(
                "INSERT INTO events (user_id, title, description, event_date, end_date) VALUES (?, ?, ?, ?, ?)",
                [user_id, title, description, event_date, end_date]
            ).lastrowid

            for cat_id in category_ids:
                con.execute(
                    "INSERT INTO event_categories (event_id, category_id) VALUES (?, ?)",
                    [event_id, cat_id]
                )
        return event_id
    finally:
        con.close()

def get_event(event_id):
    sql = """
    SELECT events.id, events.user_id, events.title, events.description, events.event_date, events.end_date, users.username
    FROM events
    JOIN users ON events.user_id = users.id
    WHERE events.id = ?
    """
    result = db.query(sql, [event_id])
    return result[0] if result else None

def get_event_categories(event_id):
    sql = """SELECT categories.id, categories.name
             FROM categories
             JOIN event_categories ON categories.id = event_categories.category_id 
             WHERE event_categories.event_id = ?"""
    return db.query(sql, [event_id])

def get_rsvps(event_id):
    sql = """
    SELECT users.username, rsvps.rsvp_status
    FROM rsvps
    JOIN users ON rsvps.user_id = users.id
    WHERE rsvps.event_id = ?
    ORDER BY rsvps.created_at DESC
    """
    return db.query(sql, [event_id])

def get_user_rsvp(event_id, user_id):
    sql = "SELECT rsvp_status FROM rsvps WHERE event_id = ? AND user_id = ?"
    result = db.query(sql, [event_id, user_id])
    return result[0]["rsvp_status"] if result else None

def add_rsvp(event_id, user_id, rsvp_status):
    sql = """
    INSERT INTO rsvps (event_id, user_id, rsvp_status)
    VALUES (?, ?, ?)
    ON CONFLICT(event_id, user_id) DO UPDATE SET rsvp_status = excluded.rsvp_status
    """
    db.execute(sql, [event_id, user_id, rsvp_status])

def update_event(event_id, title, description, event_date, end_date, category_ids):
    con = db.get_connection()
    try:
        with con:
            con.execute(
                "UPDATE events SET title = ?, description = ?, event_date = ?, end_date = ? WHERE id = ?",
                [title, description, event_date, end_date, event_id]
            )
            con.execute("DELETE FROM event_categories WHERE event_id = ?", [event_id])
            for cat_id in category_ids:
                con.execute(
                    "INSERT INTO event_categories (event_id, category_id) VALUES (?, ?)",
                    [event_id, cat_id]
                )
    finally:
        con.close()

def delete_event(event_id):
    con = db.get_connection()
    try:
        with con:
            con.execute("DELETE FROM events WHERE id = ?", [event_id])
    finally:
        con.close()

def search_events(keyword, category_id, start_date, end_date):
    sql = """
    SELECT DISTINCT events.id, events.user_id, events.title, events.event_date, users.username
    FROM events
    JOIN users ON events.user_id = users.id
    LEFT JOIN event_categories ON events.id = event_categories.event_id
    WHERE 1=1
    """
    params = []

    if keyword:
        sql += " AND (events.title LIKE ? OR events.description LIKE ?)"
        params.append(f"%{keyword}%")
        params.append(f"%{keyword}%")

    if category_id:
        sql += " AND event_categories.category_id = ?"
        params.append(category_id)

    if start_date:
        sql += " AND events.event_date >= ?"
        params.append(start_date)

    if end_date:
        sql += " AND events.event_date <= ?"
        params.append(end_date)

    sql += " ORDER BY events.event_date ASC"
    return db.query(sql, params)
