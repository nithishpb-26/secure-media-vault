
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    send_file
)

from werkzeug.utils import secure_filename

from database.users import (
    create_users_table,
    verify_user,
    change_password
)

from modules.encryption import (
    encrypt_file,
    decrypt_file,
    validate_password
)

from modules.hash_utils import calculate_sha256

from database.database import (
    create_database,
    create_security_logs_table,
    save_history,
    get_history,
    get_statistics,
    save_security_log,
    get_security_logs
)

import os
import uuid

from dotenv import load_dotenv


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# FLASK APPLICATION
# =========================================================

app = Flask(__name__)

# Secret key used for Flask sessions
app.secret_key = os.getenv("FLASK_SECRET_KEY")


# =========================================================
# CONFIGURATION
# =========================================================

UPLOAD_FOLDER = "uploads"
ENCRYPTED_FOLDER = "encrypted"
DECRYPTED_FOLDER = "decrypted"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Maximum upload size: 500 MB
app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024


# =========================================================
# CREATE REQUIRED FOLDERS
# =========================================================

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)

os.makedirs(DECRYPTED_FOLDER, exist_ok=True)


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

create_database()

create_users_table()

create_security_logs_table()


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    # If already logged in, go to dashboard
    if session.get("logged_in"):

        return redirect(
            url_for("home")
        )

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        # -------------------------------------------------
        # VERIFY USER
        # -------------------------------------------------

        if verify_user(
            username,
            password
        ):

            session["logged_in"] = True

            session["username"] = username

            # Record successful login
            save_security_log(
                username,
                "LOGIN_SUCCESS",
                "SUCCESS",
                request.remote_addr
            )

            return redirect(
                url_for("home")
            )

        # -------------------------------------------------
        # RECORD FAILED LOGIN
        # -------------------------------------------------

        save_security_log(
            username if username else "UNKNOWN",
            "LOGIN_FAILED",
            "FAILED",
            request.remote_addr
        )

        return render_template(
            "login.html",
            error="Invalid username or password."
        )

    return render_template(
        "login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    # Get username BEFORE clearing session
    username = session.get("username")

    # Record logout event
    if username:

        save_security_log(
            username,
            "LOGOUT",
            "SUCCESS",
            request.remote_addr
        )

    # Clear session
    session.clear()

    return redirect(
        url_for("login")
    )


# =========================================================
# CHANGE PASSWORD
# =========================================================

@app.route("/change-password", methods=["GET", "POST"])
def change_password_page():

    if not session.get("logged_in"):

        return redirect(
            url_for("login")
        )

    if request.method == "POST":

        current_password = request.form.get(
            "current_password",
            ""
        )

        new_password = request.form.get(
            "new_password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        username = session.get("username")

        # -------------------------------------------------
        # VERIFY CURRENT PASSWORD
        # -------------------------------------------------

        if not verify_user(
            username,
            current_password
        ):

            return render_template(
                "change_password.html",
                error="Current password is incorrect."
            )

        # -------------------------------------------------
        # CHECK NEW PASSWORD
        # -------------------------------------------------

        valid, message = validate_password(
            new_password
        )

        if not valid:

            return render_template(
                "change_password.html",
                error=message
            )

        # -------------------------------------------------
        # CONFIRM NEW PASSWORD
        # -------------------------------------------------

        if new_password != confirm_password:

            return render_template(
                "change_password.html",
                error="New passwords do not match."
            )

        # -------------------------------------------------
        # PREVENT SAME PASSWORD
        # -------------------------------------------------

        if verify_user(
            username,
            new_password
        ):

            return render_template(
                "change_password.html",
                error="New password must be different from your current password."
            )

        # -------------------------------------------------
        # UPDATE PASSWORD
        # -------------------------------------------------

        updated = change_password(
            username,
            new_password
        )

        if updated:

            # Record password change
            save_security_log(
                username,
                "PASSWORD_CHANGED",
                "SUCCESS",
                request.remote_addr
            )

            return render_template(
                "change_password.html",
                success="Password changed successfully."
            )

        return render_template(
            "change_password.html",
            error="Unable to change password."
        )

    return render_template(
        "change_password.html"
    )


# =========================================================
# LOGIN PROTECTION
# =========================================================

def login_required():

    return session.get("logged_in") is True


# =========================================================
# ALLOWED FILE TYPES
# =========================================================

ALLOWED_FILES = {

    "jpg",
    "jpeg",
    "png",
    "gif",
    "bmp",

    "mp4",
    "avi",
    "mov",
    "mkv",
    "webm"

}


def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(
            ".",
            1
        )[1].lower() in ALLOWED_FILES
    )


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    if not login_required():

        return redirect(
            url_for("login")
        )

    return render_template(
        "index.html"
    )


# =========================================================
# HISTORY PAGE
# =========================================================

@app.route("/history")
def history():

    if not login_required():

        return redirect(
            url_for("login")
        )

    records = get_history()

    statistics = get_statistics()

    return render_template(

        "history.html",

        records=records,

        statistics=statistics

    )


@app.route("/security-dashboard")
def security_dashboard():

    if not login_required():

        return redirect(
            url_for("login")
        )

    statistics = get_statistics()
    logs = get_security_logs()

    return render_template(
        "security_dashboard.html",
        statistics=statistics,
        logs=logs[:10]
    )


# =========================================================
# SECURITY AUDIT LOGS
# =========================================================

@app.route("/security-logs")
def security_logs():

    if not login_required():

        return redirect(
            url_for("login")
        )

    logs = get_security_logs()

    total_events = len(logs)

    successful_events = sum(
        1 for log in logs
        if log[3] == "SUCCESS"
    )

    failed_events = sum(
        1 for log in logs
        if log[3] == "FAILED"
    )

    authentication_events = sum(
        1 for log in logs
        if "LOGIN" in log[2]
    )

    return render_template(
        "security_logs.html",
        logs=logs,
        total_events=total_events,
        successful_events=successful_events,
        failed_events=failed_events,
        authentication_events=authentication_events
    )

# =========================================================
# ENCRYPT FILE
# =========================================================

@app.route(
    "/encrypt",
    methods=["POST"]
)
def encrypt():

    if not login_required():

        return redirect(
            url_for("login")
        )

    uploaded_file = request.files.get(
        "file"
    )

    password = request.form.get(
        "password"
    )

    # -------------------------------------------------------
    # CHECK FILE
    # -------------------------------------------------------

    if not uploaded_file:

        return "No file selected."

    # -------------------------------------------------------
    # CHECK PASSWORD
    # -------------------------------------------------------

    valid, message = validate_password(
        password
    )

    if not valid:

        return message

    # -------------------------------------------------------
    # CHECK FILE TYPE
    # -------------------------------------------------------

    if not allowed_file(
        uploaded_file.filename
    ):

        return "Unsupported file type."

    # -------------------------------------------------------
    # SECURE FILENAME
    # -------------------------------------------------------

    original_name = secure_filename(
        uploaded_file.filename
    )

    if not original_name:

        return "Invalid filename."

    # -------------------------------------------------------
    # CHECK FILENAME LENGTH
    # -------------------------------------------------------

    if len(original_name) > 150:

        return "Filename is too long."

    # -------------------------------------------------------
    # GENERATE UNIQUE ID
    # -------------------------------------------------------

    unique_id = uuid.uuid4().hex

    # -------------------------------------------------------
    # TEMPORARY INPUT PATH
    # -------------------------------------------------------

    input_path = os.path.join(

        UPLOAD_FOLDER,

        unique_id + "_" + original_name

    )

    # -------------------------------------------------------
    # ENCRYPTED FILE NAME
    # -------------------------------------------------------

    encrypted_name = (
        original_name + ".enc"
    )

    # -------------------------------------------------------
    # ENCRYPTED FILE PATH
    # -------------------------------------------------------

    encrypted_path = os.path.join(

        ENCRYPTED_FOLDER,

        unique_id + "_" + encrypted_name

    )

    # -------------------------------------------------------
    # SAVE UPLOADED FILE
    # -------------------------------------------------------

    uploaded_file.save(
        input_path
    )

    # -------------------------------------------------------
    # GET FILE SIZE
    # -------------------------------------------------------

    try:

        file_size = os.path.getsize(
            input_path
        )

    except OSError:

        file_size = 0

    # -------------------------------------------------------
    # CALCULATE SHA-256
    # -------------------------------------------------------

    try:

        sha256_hash = calculate_sha256(
            input_path
        )

    except Exception:

        sha256_hash = None

    # -------------------------------------------------------
    # ENCRYPT
    # -------------------------------------------------------

    try:

        encrypt_file(

            input_path,

            encrypted_path,

            password

        )

        # ---------------------------------------------------
        # SAVE SUCCESS HISTORY
        # ---------------------------------------------------

        save_history(

            original_name,

            "ENCRYPT",

            "SUCCESS",

            file_size,

            sha256_hash

        )

        # ---------------------------------------------------
        # SAVE SECURITY LOG
        # ---------------------------------------------------

        save_security_log(

            session.get("username"),

            "ENCRYPT_SUCCESS",

            "SUCCESS",

            request.remote_addr

        )

    except Exception as error:

        # ---------------------------------------------------
        # SAVE FAILED HISTORY
        # ---------------------------------------------------

        save_history(

            original_name,

            "ENCRYPT",

            "FAILED",

            file_size,

            sha256_hash

        )

        # ---------------------------------------------------
        # SAVE FAILED SECURITY LOG
        # ---------------------------------------------------

        save_security_log(

            session.get("username"),

            "ENCRYPT_FAILED",

            "FAILED",

            request.remote_addr

        )

        return (
            f"Encryption failed: {error}"
        )

    finally:

        # ---------------------------------------------------
        # DELETE PLAINTEXT FILE
        # ---------------------------------------------------

        if os.path.exists(
            input_path
        ):

            os.remove(
                input_path
            )

    # -------------------------------------------------------
    # SEND ENCRYPTED FILE
    # -------------------------------------------------------

    return send_file(

        encrypted_path,

        as_attachment=True,

        download_name=encrypted_name

    )


# =========================================================
# DECRYPT FILE
# =========================================================

@app.route(
    "/decrypt",
    methods=["POST"]
)
def decrypt():

    if not login_required():

        return redirect(
            url_for("login")
        )

    uploaded_file = request.files.get(
        "file"
    )

    password = request.form.get(
        "password"
    )

    # -------------------------------------------------------
    # CHECK FILE
    # -------------------------------------------------------

    if not uploaded_file:

        return "No encrypted file selected."

    # -------------------------------------------------------
    # CHECK PASSWORD
    # -------------------------------------------------------

    if not password:

        return "Password is required."

    # -------------------------------------------------------
    # SECURE FILENAME
    # -------------------------------------------------------

    filename = secure_filename(
        uploaded_file.filename
    )

    if not filename:

        return "Invalid filename."

    # -------------------------------------------------------
    # CHECK .ENC EXTENSION
    # -------------------------------------------------------

    if not filename.lower().endswith(
        ".enc"
    ):

        return (
            "Please upload a .enc "
            "encrypted file."
        )

    # -------------------------------------------------------
    # CHECK FILENAME LENGTH
    # -------------------------------------------------------

    if len(filename) > 155:

        return "Filename is too long."

    # -------------------------------------------------------
    # GENERATE UNIQUE ID
    # -------------------------------------------------------

    unique_id = uuid.uuid4().hex

    # -------------------------------------------------------
    # TEMPORARY ENCRYPTED FILE
    # -------------------------------------------------------

    input_path = os.path.join(

        UPLOAD_FOLDER,

        unique_id + "_" + filename

    )

    # -------------------------------------------------------
    # ORIGINAL FILENAME
    # -------------------------------------------------------

    encrypted_original_name = (
        filename[:-4]
    )

    # -------------------------------------------------------
    # DECRYPTED FILE PATH
    # -------------------------------------------------------

    decrypted_path = os.path.join(

        DECRYPTED_FOLDER,

        unique_id + "_" +
        encrypted_original_name

    )

    # -------------------------------------------------------
    # SAVE ENCRYPTED FILE
    # -------------------------------------------------------

    uploaded_file.save(
        input_path
    )

    # -------------------------------------------------------
    # GET FILE SIZE
    # -------------------------------------------------------

    try:

        file_size = os.path.getsize(
            input_path
        )

    except OSError:

        file_size = 0

    # -------------------------------------------------------
    # CALCULATE SHA-256
    # -------------------------------------------------------

    try:

        sha256_hash = calculate_sha256(
            input_path
        )

    except Exception:

        sha256_hash = None

    # -------------------------------------------------------
    # DECRYPT
    # -------------------------------------------------------

    try:

        decrypt_file(

            input_path,

            decrypted_path,

            password

        )

        # ---------------------------------------------------
        # SAVE SUCCESS HISTORY
        # ---------------------------------------------------

        save_history(

            encrypted_original_name,

            "DECRYPT",

            "SUCCESS",

            file_size,

            sha256_hash

        )

        # ---------------------------------------------------
        # SAVE SECURITY LOG
        # ---------------------------------------------------

        save_security_log(

            session.get("username"),

            "DECRYPT_SUCCESS",

            "SUCCESS",

            request.remote_addr

        )

    except ValueError as error:

        # ---------------------------------------------------
        # SAVE FAILED HISTORY
        # ---------------------------------------------------

        save_history(

            encrypted_original_name,

            "DECRYPT",

            "FAILED",

            file_size,

            sha256_hash

        )

        # ---------------------------------------------------
        # SAVE FAILED SECURITY LOG
        # ---------------------------------------------------

        save_security_log(

            session.get("username"),

            "DECRYPT_FAILED",

            "FAILED",

            request.remote_addr

        )

        # Delete temporary encrypted file

        if os.path.exists(
            input_path
        ):

            os.remove(
                input_path
            )

        return str(error)

    except Exception as error:

        # ---------------------------------------------------
        # SAVE FAILED HISTORY
        # ---------------------------------------------------

        save_history(

            encrypted_original_name,

            "DECRYPT",

            "FAILED",

            file_size,

            sha256_hash

        )

        # ---------------------------------------------------
        # SAVE FAILED SECURITY LOG
        # ---------------------------------------------------

        save_security_log(

            session.get("username"),

            "DECRYPT_FAILED",

            "FAILED",

            request.remote_addr

        )

        # Delete temporary encrypted file

        if os.path.exists(
            input_path
        ):

            os.remove(
                input_path
            )

        return (
            f"Decryption failed: {error}"
        )

    # -------------------------------------------------------
    # DELETE TEMPORARY FILE
    # -------------------------------------------------------

    if os.path.exists(
        input_path
    ):

        os.remove(
            input_path
        )

    # -------------------------------------------------------
    # SEND DECRYPTED FILE
    # -------------------------------------------------------

    return send_file(

        decrypted_path,

        as_attachment=True,

        download_name=encrypted_original_name

    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(

        debug=True,

        host="127.0.0.1",

        port=5000

    )

