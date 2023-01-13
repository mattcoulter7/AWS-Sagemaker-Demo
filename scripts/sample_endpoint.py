from flask import Blueprint,jsonify

sample_endpoint_bp = Blueprint('sample_endpoint', __name__)

@sample_endpoint_bp.route('/',methods=["GET"])
def test():
    return jsonify({})