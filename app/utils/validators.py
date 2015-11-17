from cerberus import Validator


class MyValidator(Validator):
    def __init__(self, *args, **kwargs):
        if 'additional_context' in kwargs:
            self.additional_context = kwargs['additional_context']
        super(MyValidator, self).__init__(*args, **kwargs)

    def _validate_type_objectid(self, field, value):
        if not re.match('[a-f0-9]{24}', value):
            self._error(field, ERROR_BAD_TYPE.format('ObjectId'))