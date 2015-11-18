from flask import jsonify


class ResponseTools:

    @staticmethod
    def response(code, msg, objects=''):
        result = {'response': {'code': code, 'msg': msg}, 'data': objects}
        return jsonify(result)

    @staticmethod
    def response_success(code = 200, msg = 'Success', objects = ''):
        return ResponseTools.response(code, msg, objects)

    @staticmethod
    def response_fail(code = 400, msg = 'Failed', objects = '', json_dump = False):
        return ResponseTools.response(code, msg, objects)

    @staticmethod
    def response_server_fail(code = 500, msg = 'Server Faliure', objects = '', json_dump = False):
        return ResponseTools.response(code, msg, objects)
