from edc_form_validators import FormValidator
from edc_constants.constants import YES, OTHER


class FollowUpFormValidator(FormValidator):

    def clean(self):

        self.validate_other_specify(
            field='fluconazole_dose',
            other_specify_field='fluconazole_dose_other',
            other_stored_value=OTHER)

        self.required_if(
            YES,
            field='rifampicin_started',
            field_required='rifampicin_start_date')
