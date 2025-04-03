from flask import Blueprint, jsonify, request
from data.models import Jobs, db, Api_Keys


jobs_bp = Blueprint('users', __name__,
                    url_prefix="/api/jobs")


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


@jobs_bp.route("/add", methods=["POST"])
def add_job():
    api_l = request.args.get("apikey")
    job_title = request.args.get("job_title")
    team_lead_id = int(request.args.get("team_lead_id"))
    work_size = int(request.args.get("work_size"))
    collaborators = request.args.get("collaborators")
    finish = bool(request.args.get("finish"))
    email = request.args.get("email")
    rer = Api_Keys.query.filter_by(email_address=email).first()
    if not rer.check_password(api_l):
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
        rer = Api_Keys.query.filter_by(email_address=email).first()
        if not rer.check_password(api_l):
            return jsonify({"error": "Invalid API key"}), 403
        job = Jobs.query.get(job_id)
        if not job:
            return jsonify({"error": "Job not found"}), 404
        db.session.delete(job)
        db.session.commit()
        return jsonify({"message": "Job deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Error deleting job"}), 500
    