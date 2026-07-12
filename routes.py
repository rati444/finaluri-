from functools import wraps

from flask import Blueprint, render_template, redirect, url_for, flash, session, request

from ext import db
from models import User, Resource
from forms import RegisterForm, LoginForm, ResourceForm
from choices import SUBJECTS, SEMESTERS

main = Blueprint("main", __name__)


def login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("გთხოვთ, ჯერ შეხვიდეთ სისტემაში.", "error")
            return redirect(url_for("main.login"))
        return view_func(*args, **kwargs)
    return wrapped


def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return User.query.get(user_id)


@main.context_processor
def inject_user():
    # ყველა template-ში ავტომატურად ხელმისაწვდომი იქნება "user"
    return {"user": current_user()}


@main.get("/")
def index():
    query = request.args.get("q", "").strip()
    subject = request.args.get("subject", "").strip()
    semester = request.args.get("semester", "").strip()

    resources_query = Resource.query
    if subject and subject != "all":
        resources_query = resources_query.filter(Resource.subject == subject)
    if semester and semester != "all":
        resources_query = resources_query.filter(Resource.semester == semester)
    if query:
        resources_query = resources_query.filter(Resource.title.ilike(f"%{query}%"))

    resources = resources_query.order_by(Resource.created_at.desc()).all()
    return render_template(
        "index.html",
        resources=resources,
        subjects=SUBJECTS,
        semesters=SEMESTERS,
        query=query,
        selected_subject=subject,
        selected_semester=semester,
    )


@main.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("main.index"))

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        if User.query.filter_by(email=email).first():
            flash("ეს ელფოსტა უკვე რეგისტრირებულია.", "error")
            return render_template("register.html", form=form)

        user = User(full_name=form.full_name.data.strip(), email=email, role="student")
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        flash("რეგისტრაცია წარმატებით დასრულდა!", "success")
        return redirect(url_for("main.index"))

    return render_template("register.html", form=form)


@main.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        user = User.query.filter_by(email=email).first()

        # ერთი და იგივე შეცდომას ვწერ ორივე შემთხვევაში (email არასწორია ან პაროლი)
        # რომ არავინ მიხვდეს ზუსტად რომელი email-ია დარეგისტრირებული
        if not user or not user.check_password(form.password.data):
            flash("ელფოსტა ან პაროლი არასწორია.", "error")
            return render_template("login.html", form=form)

        session["user_id"] = user.id
        flash(f"კეთილი იყოს შენი დაბრუნება, {user.full_name}!", "success")
        return redirect(url_for("main.index"))

    return render_template("login.html", form=form)


@main.get("/logout")
def logout():
    session.pop("user_id", None)
    flash("წარმატებით გამოხვედი სისტემიდან.", "success")
    return redirect(url_for("main.index"))


@main.route("/resources/add", methods=["GET", "POST"])
@login_required
def add_resource():
    form = ResourceForm()
    if form.validate_on_submit():
        resource = Resource(
            title=form.title.data.strip(),
            subject=form.subject.data,
            semester=form.semester.data,
            resource_type=form.resource_type.data,
            uploader_id=session["user_id"],
        )
        db.session.add(resource)
        db.session.commit()
        flash("მასალა წარმატებით დაემატა!", "success")
        return redirect(url_for("main.index"))

    return render_template("add_resource.html", form=form)


@main.post("/resources/<int:resource_id>/delete")
@login_required
def delete_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    user = current_user()

    # წაშლა შეუძლია მხოლოდ იმას ვინც დაამატა, ან ადმინს
    if user.role != "admin" and resource.uploader_id != user.id:
        flash("წაშლის უფლება არ გაქვს.", "error")
        return redirect(url_for("main.index"))

    db.session.delete(resource)
    db.session.commit()
    flash("მასალა წაიშალა.", "success")
    return redirect(url_for("main.index"))
