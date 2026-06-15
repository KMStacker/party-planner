import db

def get_events():
    sql = """
    SELECT events.id, events.user_id, events.title, events.event_date, users.username
    FROM events 
    JOIN users ON events.user_id = users.id 
    ORDER BY events.event_date ASC
    """
    return db.query(sql)

def get_categories():
    sql = "SELECT id, name FROM categories ORDER BY name"
    return db.query(sql)

def create_event(user_id, title, description, event_date, category_ids):
    sql = "INSERT INTO events (user_id, title, description, event_date) VALUES (?, ?, ?, ?)"
    db.execute(sql, [user_id, title, description, event_date])

    event_id = db.last_insert_id()

    sql_cat = "INSERT INTO event_categories (event_id, category_id) VALUES (?, ?)"
    for cat_id in category_ids:
        db.execute(sql_cat, [event_id, cat_id])

    return event_id

def get_event(event_id):
    sql = """
    SELECT events.id, events.user_id, events.title, events.description, events.event_date, users.username
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
    SELECT users.username, rsvps.status
    FROM rsvps
    JOIN users ON rsvps.user_id = users.id
    WHERE rsvps.event_id = ?
    ORDER BY rsvps.created_at DESC
    """
    return db.query(sql, [event_id])

def add_rsvp(event_id, user_id, status):
    sql_check = "SELECT id FROM rsvps WHERE event_id = ? AND user_id = ?"
    existing = db.query(sql_check, [event_id, user_id])

    if existing:
        sql = "UPDATE rsvps SET status = ? WHERE event_id = ? AND user_id = ?"
        db.execute(sql, [status, event_id, user_id])
    else:
        sql = "INSERT INTO rsvps (event_id, user_id, status) VALUES (?, ?, ?)"
        db.execute(sql, [event_id, user_id, status])

def update_event(event_id, title, description, event_date, category_ids):
    sql = "UPDATE events SET title = ?, description = ?, event_date = ? WHERE id = ?"
    db.execute(sql, [title, description, event_date, event_id])

    db.execute("DELETE FROM event_categories WHERE event_id = ?", [event_id])
    sql_cat = "INSERT INTO event_categories (event_id, category_id) VALUES (?, ?)"
    for cat_id in category_ids:
        db.execute(sql_cat, [event_id, cat_id])

def delete_event(event_id):
    db.execute("DELETE FROM event_categories WHERE event_id = ?", [event_id])
    db.execute("DELETE FROM rsvps WHERE event_id = ?", [event_id])
    db.execute("DELETE FROM events WHERE id = ?", [event_id])

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
