from flask import Blueprint
from app.utils.msg_tools import ResponseTools
from app.utils.validators import MyValidator

utils = Blueprint('utils', __name__, url_prefix='/utils')