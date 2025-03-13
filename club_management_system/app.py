from flask import Flask, render_template, redirect, url_for, request, flash, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, SignupForm
from models import db, User, Proposal, EventClub, Product
from flask_mail import Mail, Message
from datetime import datetime
import os
from matplotlib.figure import Figure
import io
from dotenv import load_dotenv
import os

load_dotenv()
print(f"Loaded MAIL_USERNAME: {os.getenv('MAIL_USERNAME')}")
print(f"Loaded MAIL_PASSWORD: {os.getenv('MAIL_PASSWORD')}")


app = Flask(__name__)

# Secure mail server configuration using environment variables
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'anugya2202@gmail.com'
app.config['MAIL_PASSWORD'] = 'Kartikrinky22'
app.config['MAIL_DEFAULT_SENDER'] = 'anugya2202@gmail.com'
  # Default sender from env
app.config['MAIL_DEBUG'] = True  # Enable debugging


# Initialize Flask-Mail
mail = Mail(app)
app.config.from_object("config.Config")

@app.route("/test-email")
def test_email():
    try:
        msg = Message(
            subject="Test Email",
            recipients=["pranjalup25@gmail.com"],  # Replace with your test recipient
            body="This is a test email sent from Flask-Mail."
        )
        mail.send(msg)
        return "Email sent successfully!"
    except Exception as e:
        return f"Failed to send email: {e}"


# Initialize database and Flask-Login
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    form = LoginForm()
    return render_template("login.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered. Please log in.", "danger")
            return redirect(url_for("signup"))
        if User.query.filter_by(username=form.username.data).first():
            flash("Username already taken. Please choose another.", "danger")
            return redirect(url_for("signup"))

        hashed_password = generate_password_hash(form.password.data, method="pbkdf2:sha256")
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            department=form.department.data,
            position=form.position.data,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for(f"dashboard_{new_user.position.lower()}"))
    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            if user.position == "lead":
                return redirect(url_for("dashboard_lead"))
            elif user.position == "member":
                return redirect(url_for("dashboard_member"))
            elif user.position == "board":
                return redirect(url_for("dashboard_board"))
            else:
                return redirect(url_for("home"))
        else:
            flash("Invalid username or password", "danger")
    return render_template("login.html", form=form)


@app.route("/dashboard/member")
@login_required
def dashboard_member():
    return render_template("dashboard_member.html", user=current_user)


@app.route("/dashboard/lead")
@login_required
def dashboard_lead():
    return render_template("dashboard_lead.html", user=current_user)


@app.route("/dashboard/board")
@login_required
def dashboard_board():
    if current_user.position != "board":
        flash("Access restricted to board members only.", "danger")
        return redirect(url_for("dashboard_member"))

    # Fetch all leads grouped by department
    leads = User.query.filter_by(position="lead").all()
    return render_template("dashboard_board.html", user=current_user, leads=leads)


@app.route("/view-and-contact-boards")
@login_required
def view_and_contact_boards():
    if current_user.position != "board":
        flash("Access restricted to board members only.", "danger")
        return redirect(url_for("dashboard_board"))

    # Fetch all board members
    boards = User.query.filter_by(position="board").all()
    return render_template("view_and_contact_boards.html", boards=boards)

@app.route("/view-activities")
@login_required
def view_activities():
    # Logic to fetch and display activities (you can replace this with your actual logic)
    activities = [
        {"title": "Club Meeting", "date": "2024-11-15", "description": "Monthly club meeting."},
        {"title": "Workshop", "date": "2024-11-20", "description": "Technical workshop on Python."}
    ]
    return render_template("view_activities.html", activities=activities)

@app.route("/contact-lead")
@login_required
def contact_lead():
    # Logic to fetch lead information of the current member's department
    if current_user.position != "member":
        flash("Only members can contact their leads.", "danger")
        return redirect(url_for("dashboard_member"))
    
    lead = User.query.filter_by(department=current_user.department, position="lead").first()
    if not lead:
        flash("No lead found for your department.", "danger")
        return redirect(url_for("dashboard_member"))

    return render_template("contact_lead.html", lead=lead)



@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("login"))


@app.route("/submit-proposal", methods=["GET", "POST"])
@login_required
def submit_proposal():
    if request.method == "POST":
        proposal_content = request.form.get("proposal")
        if proposal_content:
            new_proposal = Proposal(user_id=current_user.id, content=proposal_content)
            db.session.add(new_proposal)
            db.session.commit()
            flash("Proposal submitted successfully!", "success")
        else:
            flash("Proposal content cannot be empty.", "danger")
        return redirect(url_for("dashboard_member"))
    return render_template("submit_proposal.html")


@app.route("/view-proposals")
@login_required
def view_proposals():
    proposals = Proposal.query.all()
    return render_template("view_proposals.html", proposals=proposals)


@app.route("/about-club")
@login_required
def about_club():
    club_info = [
        {"image": "static/img/club_image1.jpg", "text": "Welcome to our club! We host exciting events and activities."},
        {"image": "static/img/club_image2.jpg", "text": "Our members enjoy collaboration and learning."},
        {"image": "static/img/club_image3.jpg", "text": "Join us for workshops, events, and more!"},
    ]
    return render_template("about_club.html", club_info=club_info)


@app.route("/manage-events", methods=["GET", "POST"])
@login_required
def manage_events():
    if current_user.position not in ["lead", "board"]:
        flash("Only leads or board members can access this page.", "danger")
        return redirect(url_for("dashboard_member"))

    events = EventClub.query.all()
    return render_template("manage_events.html", events=events)


@app.route("/add-event", methods=["POST"])
@login_required
def add_event():
    if current_user.position not in ["lead", "board"]:
        flash("Only leads or board members can add events.", "danger")
        return redirect(url_for("dashboard_lead"))

    title = request.form.get("title")
    description = request.form.get("description")
    event_date = request.form.get("date")

    if not title or not description or not event_date:
        flash("All fields are required.", "danger")
        return redirect(url_for("manage_events"))

    new_event = EventClub(
        title=title,
        description=description,
        event_date=datetime.strptime(event_date, "%Y-%m-%d"),
        created_by=current_user.id
    )
    db.session.add(new_event)
    db.session.commit()

    flash("Event added successfully!", "success")
    return redirect(url_for("manage_events"))


@app.route("/sales-chart")
@login_required
def sales_chart():
    # Fetch data for the pie chart
    products = Product.query.all()
    product_names = [product.name for product in products]
    sales_data = [product.sales for product in products]

    # Create pie chart
    fig = Figure()
    ax = fig.subplots()
    if sum(sales_data) > 0:
        ax.pie(sales_data, labels=product_names, autopct='%1.1f%%', startangle=90)
        ax.legend(loc="upper left")
    else:
        ax.text(0.5, 0.5, "No sales data available", horizontalalignment="center", fontsize=14)

    # Render chart as an image
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return Response(buf.getvalue(), mimetype="image/png")


@app.route("/manage-sales", methods=["GET", "POST"])
@login_required
def manage_sales():
    if current_user.position not in ["lead", "board"]:
        flash("Only leads or board members can access this page.", "danger")
        return redirect(url_for("dashboard_member"))

    products = Product.query.all()
    total_sales = sum(product.sales for product in products)

    if request.method == "POST":
        name = request.form.get("name")
        price = float(request.form.get("price"))
        sales = float(request.form.get("sales", 0))

        if not name or price <= 0:
            flash("Invalid product details.", "danger")
        else:
            new_product = Product(name=name, price=price, sales=sales)
            db.session.add(new_product)
            db.session.commit()
            flash("Product added successfully!", "success")

        return redirect(url_for("manage_sales"))

    return render_template("manage_sales.html", products=products, total_sales=total_sales)


@app.route("/update-sales", methods=["POST"])
@login_required
def update_sales():
    if current_user.position not in ["lead", "board"]:
        flash("Only leads or board members can update sales.", "danger")
        return redirect(url_for("dashboard_member"))

    product_id = request.form.get("product_id")
    quantity_sold = request.form.get("quantity_sold")

    if not product_id or not quantity_sold:
        flash("Invalid input. Product ID and Quantity Sold are required.", "danger")
        return redirect(url_for("manage_sales"))

    product = Product.query.get(product_id)
    if product:
        product.sales += float(quantity_sold) * product.price  # Update sales
        db.session.commit()
        flash(f"Updated sales for {product.name}.", "success")
    else:
        flash("Product not found.", "danger")

    return redirect(url_for("manage_sales"))


@app.route("/assign-task", methods=["GET", "POST"])
@login_required
def assign_task():
    if current_user.position not in ["lead", "board"]:
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for("dashboard_member"))

    members = User.query.filter_by(position="member").all()

    if request.method == "POST":
        recipient_email = request.form.get("recipient_email")
        task_content = request.form.get("task_content")

        if not recipient_email or not task_content:
            flash("Recipient email and task content are required.", "danger")
        else:
            try:
                msg = Message(
                    subject="Task Assignment",
                    recipients=[recipient_email],
                    body=f"Hello,\n\nYou have been assigned the following task:\n\n{task_content}\n\nBest regards,\n{current_user.username}"
                )
                mail.send(msg)
                flash("Task assigned successfully via email.", "success")
            except Exception as e:
                flash(f"Failed to send email: {e}", "danger")

        return redirect(url_for("assign_task"))

    return render_template("assign_task.html", members=members)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
