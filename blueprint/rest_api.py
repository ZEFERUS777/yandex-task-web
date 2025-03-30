from flask import Blueprint, jsonify
from data.models import Jobs

jobs_bp = Blueprint('users', __name__, 
                    url_prefix="/api/jobs")



@jobs_bp.route("/")
def get_jobs():
    jobs = Jobs.query.all()
    return jsonify([job.to_dict() for job in jobs])