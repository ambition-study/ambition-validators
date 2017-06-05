from edc_constants.constants import YES, NO, OTHER

from ..models import PatientHistory
from .form_mixins import SubjectModelFormMixin


class PatientHistoryForm(SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()

        condition = cleaned_data.get('first_line_arvs') == (
            'AZT + 3-TC + either EFV or NVP or DTG')
        self.required_if_true(
            condition=condition, field_required='first_line_choice')

        self.m2m_required_if(response='focal_neurologic_deficit',
                             field='focal_neurologic_deficit',
                             m2m_field='neurological')

        self.required_if(
            YES,
            field='med_history',
            field_required='tb_site')

        self.required_if(
            YES,
            field='tb_treatment',
            field_required='taking_rifampicin')

        self.required_if(
            YES,
            field='taking_rifampicin',
            field_required='rifampicin_started_date')

        self.required_if(
            YES,
            field='previous_infection',
            field_required='infection_date')

        self.required_if(
            YES,
            field='previous_infection',
            field_required='previous_infection_specify')

        self.required_if(
            YES,
            field='taking_arv',
            field_required='arv_date')

        self.required_if(
            OTHER,
            field='first_line_arvs',
            field_required='first_line_arvs_other')

        self.required_if(
            OTHER,
            field='second_line_arvs',
            field_required='second_line_arvs_other')

        self.required_if(
            NO,
            field='patient_adherence',
            field_required='last_dose')

        self.required_if(
            YES,
            field='other_medications',
            field_required='specify_medications')

    class Meta:
        model = PatientHistory
        fields = '__all__'
