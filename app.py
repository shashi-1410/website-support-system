from flask import Flask, render_template, request, redirect, session
import json

app = Flask(__name__)
app.secret_key = "secret123"


# ---------------------------
# Ticket Functions
# ---------------------------

def load_tickets():
    with open("tickets.json", "r") as f:
        return json.load(f)


def save_tickets(data):
    with open("tickets.json", "w") as f:
        json.dump(data, f)


# ---------------------------
# Content Functions
# ---------------------------

def load_content():
    with open("content.json", "r") as f:
        return json.load(f)


def save_content(data):
    with open("content.json", "w") as f:
        json.dump(data, f)


# ---------------------------
# Style Functions
# ---------------------------

def load_style():
    with open("style.json", "r") as f:
        return json.load(f)


def save_style(data):
    with open("style.json", "w") as f:
        json.dump(data, f)


# ---------------------------
# Log Functions
# ---------------------------

def load_logs():
    with open("logs.json", "r") as f:
        return json.load(f)


def save_logs(data):
    with open("logs.json", "w") as f:
        json.dump(data, f)


# ---------------------------
# User Functions
# ---------------------------

def load_users():
    with open("users.json", "r") as f:
        return json.load(f)


# ---------------------------
# Routes
# ---------------------------

@app.route("/")
def home():

    if "user" not in session:
        return redirect("/login")

    test_mode = request.args.get("test")

    content = load_content()
    style = load_style()

    banner = content.get("banner", "Welcome")
    button_color = style.get("button_color", "blue")

    return render_template(
        "index.html",
        banner=banner,
        button_color=button_color,
        role=session["role"],
        test_mode=test_mode
    )


# ---------------------------
# Ticket Routes
# ---------------------------

@app.route("/tickets")
def tickets():

    if "user" not in session:
        return redirect("/login")

    data = load_tickets()
    return render_template("tickets.html", tickets=data)


@app.route("/create_ticket", methods=["POST"])
def create_ticket():

    issue = request.form["issue"]

    tickets = load_tickets()

    ticket = {
        "id": len(tickets) + 1,
        "issue": issue,
        "status": "Pending"
    }

    tickets.append(ticket)
    save_tickets(tickets)

    return redirect("/tickets")


@app.route("/resolve/<int:id>")
def resolve_ticket(id):

    tickets = load_tickets()

    for ticket in tickets:
        if ticket["id"] == id:
            ticket["status"] = "Resolved"

    save_tickets(tickets)

    logs = load_logs()

    logs.append({
        "ticket_id": id,
        "action": "Ticket resolved",
        "engineer": session.get("user", "unknown")
    })

    save_logs(logs)

    return redirect("/tickets")


# ---------------------------
# Content Editor
# ---------------------------

@app.route("/editor")
def editor():

    content = load_content()
    return render_template("editor.html", content=content)


@app.route("/update_banner", methods=["POST"])
def update_banner():

    banner = request.form["banner"]

    data = load_content()
    data["banner"] = banner

    save_content(data)

    return redirect("/")


# ---------------------------
# Style Editor
# ---------------------------

@app.route("/style_editor")
def style_editor():

    style = load_style()
    return render_template("style_editor.html", style=style)


@app.route("/update_style", methods=["POST"])
def update_style():

    color = request.form["button_color"]

    style = load_style()
    style["button_color"] = color

    save_style(style)

    return redirect("/")


# ---------------------------
# Authentication
# ---------------------------

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login_user", methods=["POST"])
def login_user():

    username = request.form["username"]
    password = request.form["password"]

    users = load_users()

    for user in users:
        if user["username"] == username and user["password"] == password:

            session["user"] = username
            session["role"] = user["role"]

            return redirect("/dashboard")

    return "Invalid Login"


@app.route("/logout")
def logout():

    session.clear()
    return redirect("/login")


# ---------------------------
# Logs
# ---------------------------

@app.route("/logs")
def logs():

    data = load_logs()
    return render_template("logs.html", logs=data)


# ---------------------------
# Dashboard
# ---------------------------

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html", role=session["role"])


# ---------------------------
# Run Application
# ---------------------------

if __name__ == "__main__":
    app.run(debug=True)