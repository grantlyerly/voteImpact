from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Length

class check_zip():
    """
    Custom validator for checking Zip Codes.
    Checks to ensure the input both has a length of 5 and is a number
    """
    
    def __call__(self, form, field):
        data = field.data
        if (
            data is not None
            and data.isdigit()
            and len(data) == 5
        ):
            return
        
        else:
            raise ValidationError("Zip Code must be a 5 digit number.")
        
class Distinct():
    "Custom validator to ensure that ZipCodes are distinct. Simply reverse EqualTo"

    def __init__(self, fieldname, message=None):
        self.fieldname=fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError as exc:
            raise ValidationError(
                field.gettext("Invalid field name '%s'.") % self.fieldname
            ) from exc
        if field.data != other.data:
            return

        d = {
            "other_label": hasattr(other, "label")
            and other.label.text
            or self.fieldname,
            "other_name": self.fieldname,
        }
        message = self.message
        if message is None:
            message = field.gettext("Field must be distinct from %(other_name)s.")

        raise ValidationError(message % d)

class ZipCodeForm(FlaskForm):
    zip_code_1 = StringField('Zip Code 1', validators = [DataRequired(), check_zip()])
    zip_code_2 = StringField('Zip Code 2', validators = [DataRequired(), check_zip(), Distinct('zip_code_1', "Zip codes must be different.")])
    year = IntegerField('Year')
    submit = SubmitField('Submit')


class AdditionalInfoForm(FlaskForm):
    zip_code = StringField('Zip Code', validators=[DataRequired(), check_zip()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    year = IntegerField('Year')
    submit = SubmitField('Submit')