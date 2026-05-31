from werkzeug.security import check_password_hash, generate_password_hash
import db

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    
    if not result:
        return None

    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    
    if check_password_hash(password_hash, password):
        return user_id
        
    return None

def get_user_profile(user_id):
    sql = "SELECT id, username, status FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def update_status(user_id, status):
    sql = "UPDATE users SET status = ? WHERE id = ?"
    db.execute(sql, [status, user_id])

def get_user_stats(user_id):
    sql1 = "SELECT COUNT(*) as count FROM events WHERE user_id = ?"
    events_count = db.query(sql1, [user_id])[0]["count"]
    
    sql2 = "SELECT COUNT(*) as count FROM rsvps WHERE user_id = ?"
    rsvps_count = db.query(sql2, [user_id])[0]["count"]
    
    return {"events_count": events_count, "rsvps_count": rsvps_count}

def get_user_events(user_id):
    sql = "SELECT id, title, event_date FROM events WHERE user_id = ? ORDER BY event_date ASC"
    return db.query(sql, [user_id])

def get_user_dates(user_id):
    sql = "SELECT id, date_text, status FROM user_dates WHERE user_id = ? ORDER BY date_text ASC"
    return db.query(sql, [user_id])

def add_user_date(user_id, date_text, status):
    sql = "INSERT INTO user_dates (user_id, date_text, status) VALUES (?, ?, ?)"
    db.execute(sql, [user_id, date_text, status])

def delete_user_date(date_id, user_id):
    sql = "DELETE FROM user_dates WHERE id = ? AND user_id = ?"
    db.execute(sql, [date_id, user_id])