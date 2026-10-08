from flask import Blueprint, render_template

lab_bp = Blueprint('lab', __name__)

@lab_bp.route('/')
def index():
    return render_template('lab/index.html')