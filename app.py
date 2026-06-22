import sqlite3
import secrets
import time
from datetime import date, datetime
from flask import Flask, render_template, request, redirect, flash, session, abort, g
import config
import events
import users

app = Flask(__name__)
app.secret_key = config.secret_key

# ---------- Helper functions ----------

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

def require_owner(event):
    if not event or event["user_id"] != session["user_id"]:
        abort(403)

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    if hasattr(g, "start_time"):
        elapsed_time = round(time.time() - g.start_time, 2)
        print("elapsed time:", elapsed_time, "s")
    return response


# ---------- Error handlers ----------

@app.errorhandler(403)
def forbidden_error(error):
    return render_template("error.html", title="403 - Forbidden", message="You do not have permission to access this page."), 403

@app.errorhandler(404)
def not_found_error(error):
    return render_template("error.html", title="404 - Not Found", message="The page you are looking for does not exist."), 404


# ---------- Home and authentication routes ----------

@app.route("/")
def index():
    keyword = request.args.get("keyword", "")
    category_id = request.args.get("category_id", "")
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")

    if keyword or category_id or start_date or end_date:
        all_events = events.search_events(keyword, category_id, start_date, end_date)
    else:
        all_events = events.get_events()

    all_categories = events.get_categories()

    return render_template("index.html",
                           events=all_events,
                           categories=all_categories,
                           keyword=keyword,
                           selected_category=category_id,
                           start_date=start_date,
                           end_date=end_date)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create_account", methods=["POST"])
def create_account():
    username = request.form["username"].strip()
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    errors = []

    if not username:
        errors.append("Username cannot be empty or contain only spaces")
    elif len(username) < 3 or len(username) > 20:
        errors.append("Username length range is 3-20 characters without spaces")

    if not password1:
        errors.append("Password cannot be empty")
    
    if password1 != password2:
        errors.append("Passwords do not match")

    if errors:
        for error in errors:
            flash(error, "error")
        return render_template("register.html", username=username)

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("Username is already taken", "error")
        return render_template("register.html", username=username)

    flash("Account created successfully! Please log in if you are eager to Party!", "success")
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"].strip()
    password = request.form["password"]

    user_id = users.check_login(username, password)

    if user_id:
        session["user_id"] = user_id
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")

    flash("Wrong username or password", "error")
    return render_template("login.html", username=username)

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
        if "csrf_token" in session:
            del session["csrf_token"]
    return redirect("/")


# ---------- Event routes ----------

@app.route("/event/new")
def new_event():
    require_login()
    categories = events.get_categories()
    return render_template("new_event.html", categories=categories)

@app.route("/create_event", methods=["POST"])
def create_event():
    require_login()
    check_csrf()

    title = request.form["title"].strip()
    description = request.form["description"].strip()
    event_date = request.form["event_date"]
    end_date = request.form["end_date"]

    category_ids = list(set(request.form.getlist("categories")))
    today = date.today().isoformat()
    int_category_ids = [int(cid) for cid in category_ids if cid.isdigit()]

    errors = []

    if not end_date:
        end_date = event_date

    if not title:
        errors.append("Title cannot be empty or contain only spaces")
    if not description:
        errors.append("Description cannot be empty or contain only spaces")

    if len(title) > 50:
        errors.append("Title max length is 50 characters")
    if len(description) > 1000:
        errors.append("Description max length is 1000 characters")

    if not event_date:
        errors.append("Event start date cannot be empty")
    elif event_date < today:
        errors.append("Event start date cannot be in the past")

    if event_date and end_date and event_date > end_date:
        errors.append("Event end date cannot be before start date")
  
    if errors:
        for error in errors:
            flash(error, "error")
        categories = events.get_categories()
        return render_template(
            "new_event.html",
            categories=categories,
            title=title,
            description=description,
            event_date=event_date,
            end_date=end_date,
            event_category_ids=int_category_ids
        )

    events.create_event(session["user_id"], title, description, event_date, end_date, category_ids)

    return redirect("/")

@app.route("/event/<int:event_id>")
def show_event(event_id):
    event = events.get_event(event_id)
    if not event:
        abort(404)

    categories = events.get_event_categories(event_id)
    rsvps = events.get_rsvps(event_id)

    user_rsvp = None
    if "user_id" in session:
        user_rsvp = events.get_user_rsvp(event_id, session["user_id"])

    return render_template("event.html", event=event, categories=categories, rsvps=rsvps, user_rsvp=user_rsvp)

@app.route("/event/<int:event_id>/edit")
def edit_event(event_id):
    require_login()
    event = events.get_event(event_id)
    require_owner(event)

    categories = events.get_categories()
    event_cats = events.get_event_categories(event_id)
    event_category_ids = [cat["id"] for cat in event_cats]

    return render_template(
        "edit_event.html",
        event=event,
        categories=categories,
        event_category_ids=event_category_ids
    )

@app.route("/event/<int:event_id>/update", methods=["POST"])
def update_event(event_id):
    require_login()
    check_csrf()
    event = events.get_event(event_id)
    require_owner(event)

    title = request.form["title"].strip()
    description = request.form["description"].strip()
    event_date = request.form["event_date"]
    end_date = request.form["end_date"]

    category_ids = list(set(request.form.getlist("categories")))
    today = date.today().isoformat()
    int_category_ids = [int(cid) for cid in category_ids if cid.isdigit()]
    
    errors = []

    if not end_date:
        end_date = event_date

    if not title:
        errors.append("Title cannot be empty or contain only spaces")
    if not description:
        errors.append("Description cannot be empty or contain only spaces")

    if len(title) > 50:
        errors.append("Title max length is 50 characters")
    if len(description) > 1000:
        errors.append("Description max length is 1000 characters")

    if not event_date:
        errors.append("Event start date cannot be empty")
    elif event_date < today:
        errors.append("Event start date cannot be in the past")

    if event_date and end_date and event_date > end_date:
        errors.append("Event end date cannot be before start date")
  
    if errors:
        for error in errors:
            flash(error, "error")
        categories = events.get_categories()
        updating_event = {
            "id": event_id,
            "title": title,
            "description": description,
            "event_date": event_date,
            "end_date": end_date
        }
        return render_template(
            "edit_event.html",
            event=updating_event,
            categories=categories,
            event_category_ids=int_category_ids
        )

    events.update_event(event_id, title, description, event_date, end_date, category_ids)
    return redirect("/event/" + str(event_id))

@app.route("/event/<int:event_id>/delete", methods=["POST"])
def delete_event(event_id):
    require_login()
    check_csrf()
    event = events.get_event(event_id)
    require_owner(event)

    events.delete_event(event_id)
    return redirect("/")


# ---------- User and profile routes ----------

@app.route("/user/<int:user_id>")
def user_profile(user_id):
    user = users.get_user_profile(user_id)
    if not user:
        abort(404)

    stats = users.get_user_stats(user_id)
    user_events = users.get_user_events(user_id)
    user_dates = users.get_user_dates(user_id)

    return render_template(
        "profile.html",
        user=user,
        stats=stats,
        user_events=user_events,
        user_dates=user_dates
    )

@app.route("/profile/update_status", methods=["POST"])
def profile_status():
    require_login()
    check_csrf()

    status = request.form["status"].strip()

    if not status:
        flash("Status cannot be empty or contain only spaces", "error")
        return redirect("/user/" + str(session["user_id"]))

    if len(status) < 2 or len(status) > 250:
        flash("Status length range is 2-250 characters without spaces", "error")
        return redirect("/user/" + str(session["user_id"]))

    users.update_status(session["user_id"], status)

    return redirect("/user/" + str(session["user_id"]))

@app.route("/profile/delete_status", methods=["POST"])
def profile_delete_status():
    require_login()
    check_csrf()

    users.update_status(session["user_id"], None)
    return redirect("/user/" + str(session["user_id"]))

@app.route("/profile/add_date", methods=["POST"])
def profile_add_date():
    require_login()
    check_csrf()

    start_date_string = request.form["start_date_string"]
    end_date_string = request.form["end_date_string"]
    date_status = request.form["date_status"]
    errors = []

    if not start_date_string:
        errors.append("Start date cannot be empty")

    if start_date_string:
        try:
            start_date = datetime.strptime(start_date_string, "%Y-%m-%d").date()
        except ValueError:
            errors.append("Invalid start date format. Please use YYYY-MM-DD")

    if end_date_string:
        try:
            end_date = datetime.strptime(end_date_string, "%Y-%m-%d").date()
        except ValueError:
            errors.append("Invalid end date format. Please use YYYY-MM-DD")
        if start_date and end_date and end_date < start_date:
            errors.append("End date cannot be before start date")

    if errors:
        for error in errors:
            flash(error, "error")
        return redirect("/user/" + str(session["user_id"]))

    end_date_string = end_date_string if end_date_string else start_date_string

    if users.overlapping_date_status(session["user_id"], start_date_string, end_date_string):
        flash("The new date range overlaps with an existing one. Please adjust the dates.", "error")
        return redirect("/user/" + str(session["user_id"]))

    users.add_user_availability(session["user_id"], start_date_string, end_date_string, date_status)
    return redirect("/user/" + str(session["user_id"]))

@app.route("/profile/delete_date/<int:date_id>", methods=["POST"])
def profile_delete_date(date_id):
    require_login()
    check_csrf()

    users.delete_user_date(date_id, session["user_id"])
    return redirect("/user/" + str(session["user_id"]))


# ---------- RSVP routes ----------

@app.route("/rsvp", methods=["POST"])
def rsvp():
    require_login()
    check_csrf()

    event_id = request.form["event_id"]
    rsvp_status = request.form["rsvp_status"]

    events.add_rsvp(event_id, session["user_id"], rsvp_status)

    flash("Your RSVP status has been updated successfully!", "success")
    return redirect("/event/" + str(event_id))
