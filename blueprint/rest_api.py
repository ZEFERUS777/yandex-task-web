from flask import Blueprint, jsonify
from data.models import Jobs

jobs_bp = Blueprint('users', __name__,
                    url_prefix="/api/jobs")


@jobs_bp.route("/")
def get_jobs():
    jobs = Jobs.query.all()
    return jsonify([job.to_dict() for job in jobs])


@jobs_bp.route("/<int:job_id>")
def get_job(job_id):
    job = Jobs.query.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(job.to_dict())



