from flask_wtf import FlaskForm


class CustomForm(FlaskForm):
    def __init__(self):
        super(CustomForm, self).__init__()

    def get_errors(self):
        errors = ''
        for v in self.errors.values():
            for m in v:
                errors += m
            errors += ','
        return errors

    def get_first_error(self):
        return self.get_errors().split(',')[0]
