from app.database.db_connection import dimension_collection
from app.utils.msg_tools import ResponseTools as response
from flask import Blueprint

dimensions = Blueprint('dimensions', __name__, url_prefix='/dimensions')


@dimensions.route('/getDimensions', methods=['GET'])
def get_dimensions():
    all_dimensions = list(dimension_collection.find({}, {"_id": 0}))
    return response.response_success(objects=all_dimensions)
