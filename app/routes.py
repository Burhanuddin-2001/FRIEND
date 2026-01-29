from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services import UserService, AIService
from app.services import UserService, AIService, EmailService # <--- Import EmailService

# Define the Blueprint
bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name")

        try:
            UserService.sign_up(email, password, name)
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("main.login"))
        except Exception as e:
            flash(f"Error: {str(e)}", "error")

    return render_template("register.html")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            # Authenticate with Supabase
            auth_response = UserService.sign_in(email, password)
            
            # Store user info in Flask Session (Encrypted Cookie)
            session["user_id"] = auth_response.user.id
            session["email"] = auth_response.user.email
            
            flash("Welcome back!", "success")
            return redirect(url_for("main.dashboard"))
        except Exception as e:
            flash("Login failed. Check your credentials.", "error")

    return render_template("login.html")

@bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("main.login"))

    profile = UserService.get_profile(session["user_id"])
    
    generated_message = None
    
    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "generate":
            # Generate AI Message
            name = profile.get("name") if profile else "Friend"
            generated_message = AIService.generate_message(name)
            
            # Store in session so we can send it in the next step if we want
            session["last_message"] = generated_message
            
        elif action == "send_test":
            # Send the last generated message to the logged-in user
            message_body = session.get("last_message")
            if message_body:
                # Wrap it in simple HTML
                html_content = f"<p>{message_body}</p><br><p><small>Sent by Friend.</small></p>"
                
                success = EmailService.send_email(
                    to_email=profile["email"],
                    subject="Just thinking of you",
                    body_html=html_content,
                    user_id=session["user_id"]
                )
                
                if success:
                    flash("Email sent! Check your inbox.", "success")
                else:
                    flash("Failed to send email.", "error")
            else:
                flash("Generate a message first!", "warning")
                
            generated_message = message_body

    return render_template("dashboard.html", user=profile, message=generated_message)

@bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))