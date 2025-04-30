from flask import Blueprint, jsonify, request
from data.models import Jobs, db, Api_Keys, User
from secrets import token_urlsafe

jobs_bp = Blueprint('users', __name__,
                    url_prefix="/api/jobs")
api_bp = Blueprint('api', __name__,
                   url_prefix="/api/api_key")

def check_api_key(api_key: str, email: str):
    rer = Api_Keys.query.filter_by(email_address=email).first()
    if rer and rer.check_password(api_key):
        return True
    return False


@jobs_bp.route("/", methods=["GET"])
def get_jobs():
    jobs = Jobs.query.all()
    return jsonify([job.to_dict() for job in jobs])


@jobs_bp.route("/<int:job_id>", methods=["GET"])
def get_job(job_id):
    job = Jobs.query.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(job.to_dict())


@jobs_bp.route("/add", methods=["POST", "GET"])
def add_job():
    print("TES1")
    api_l = request.args.get("apikey")
    job_title = request.args.get("job_title")
    team_lead_id = int(request.args.get("team_lead_id"))
    work_size = int(request.args.get("work_size"))
    collaborators = request.args.get("collaborators")
    finish = bool(request.args.get("finish"))
    email = request.args.get("email")
    aper = Api_Keys().query.filter_by(email_address=email).first()
    if not aper.check_password(api_l):
        return jsonify({"error": "Invalid API key"}), 403
    if not all([job_title, team_lead_id, work_size, collaborators, finish]):
        return jsonify({"error": "Invalid input"}), 400
    # Создание записи
    new_job = Jobs(
        job_title=job_title,
        team_lead_id=team_lead_id,
        work_size=work_size,
        collaborators=collaborators,
        finish=finish
    )
    db.session.add(new_job)
    db.session.commit()
    return jsonify({"message": "Job added successfully"}), 200


@jobs_bp.route("/delete", methods=["DELETE"])
def delete_job():
    api_l = request.args.get("apikey")
    job_id = int(request.args.get("job_id"))
    email = request.args.get("email")
    try:
        aper = Api_Keys().query.filter_by(email_address=email).first()
        if not aper.check_password(api_l):
            return jsonify({"error": "Invalid API key"}), 403
        job = Jobs.query.get(job_id)
        if not job:
            return jsonify({"error": "Job not found"}), 404
        db.session.delete(job)
        db.session.commit()
        return jsonify({"message": "Job deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Error deleting job"}), 500


@jobs_bp.route("/update", methods=["PUT"])
def update_job():
    api_l = request.args.get("apikey")
    job_id = int(request.args.get("job_id"))
    job_title = request.args.get("job_title")
    team_lead_id = int(request.args.get("team_lead_id"))
    work_size = int(request.args.get("work_size"))
    collaborators = request.args.get("collaborators")
    finish = bool(request.args.get("finish"))

    email = request.args.get("email")
    API = Api_Keys().query.filter_by(email_address=email).first()

    if not API.check_password(api_l):
        return jsonify({"error": "Invalid API key"}), 403

    if not job_id:
        return jsonify({"error": "Invalid job id"}), 400

    try:
        job = Jobs.query.get(job_id)

        job.Job_Title = job_title if job_title else job.Job_Title
        job.Team_lead_id = team_lead_id if team_lead_id else job.Team_lead_id
        job.Work_Size = work_size if work_size else job.Work_Size
        job.Collaborators = collaborators if collaborators else job.Collaborators
        job.Finish = finish if finish else job.Finish
    except Exception as e:
        return jsonify({"error": "Error updating job"}), 500
    return jsonify({"message": "Job updated successfully"}), 200


@api_bp.route("/reg_api", methods=["POST"])
def reg_api():
    print("TEST")
    try:
        print("TEST0")
        email = request.args.get("email")
        api = Api_Keys.query.filter_by(email_address=email).first()
        user = User.query.filter_by(email=email).first()
        if api:
            return jsonify({"error": "User already exists"}), 401
        if not user:
            return jsonify({"error": "User does not exist"}), 400
        api_l = Api_Keys(email_address=email)
        password = token_urlsafe(16)
        api_l.set_password(password)
        db.session.add(api_l)
        db.session.commit()
        user.api_k = password
        db.session.add(user)
        db.session.commit()
        return jsonify({"apikey": password}), 200
    except Exception as e:
        return jsonify({"error": "Error registering user"}), 500