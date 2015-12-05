from flask import jsonify


# class for handling API responses
class ResponseTools:

    # creates a response based on the inputs
    @staticmethod
    def response(code, msg, objects=''):
        result = {'response': {'code': code, 'msg': msg}, 'data': objects}
        return jsonify(result)

    # creates a successful response with a 200
    @staticmethod
    def response_success(code = 200, msg = 'Success', objects = ''):
        return ResponseTools.response(code, msg, objects)

    # creates a failed response with a 400
    @staticmethod
    def response_fail(code = 400, msg = 'Failed', objects = '', json_dump = False):
        return ResponseTools.response(code, msg, objects)

    # creates a server fail with a 500
    @staticmethod
    def response_server_fail(code = 500, msg = 'Server Faliure', objects = '', json_dump = False):
        return ResponseTools.response(code, msg, objects)
