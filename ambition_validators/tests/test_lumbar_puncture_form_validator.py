from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_constants.constants import YES, NO, NOT_DONE

from ..form_validators import LumbarPunctureCsfFormValidator


class TestLumbarPunctureFormValidator(TestCase):

    def test_pressure(self):

        cleaned_data = {
            'opening_pressure': 10,
            'closing_pressure': 9}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got {e}')

        cleaned_data = {
            'opening_pressure': 10,
            'closing_pressure': 11}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('closing_pressure', form_validator._errors)
        self.assertIn('Cannot be greater', str(
            form_validator._errors.get('closing_pressure')))

    def test_other_csf_culture_required(self):
        cleaned_data = {'csf_culture': YES,
                        'other_csf_culture': None}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('other_csf_culture', form_validator._errors)
        self.assertIn('is required', str(
            form_validator._errors.get('other_csf_culture')))

    def test_other_csf_culture_not_required(self):
        cleaned_data = {'csf_culture': NO,
                        'other_csf_culture': 'blah'}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('other_csf_culture', form_validator._errors)
        self.assertIn('not required', str(
            form_validator._errors.get('other_csf_culture')))

    def test_csf_culture_not_perfomed(self):
        cleaned_data = {'csf_culture': NOT_DONE,
                        'other_csf_culture': 'culture'}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('other_csf_culture', form_validator._errors)
        self.assertIn('not required', str(
            form_validator._errors.get('other_csf_culture')))

    def test_csf_wbc_cell_count_less_than_three(self):
        cleaned_data = {'csf_wbc_cell_count': 2}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('csf_wbc_cell_count', form_validator._errors)
        self.assertIn('a record of "0" is expected',
                      str(form_validator._errors.get('csf_wbc_cell_count')))

    def test_india_ink_csf_arg_not_done_invalid(self):
        """Assert that either csf_cr_ag or india_ink is done.
        """
        cleaned_data = {'csf_cr_ag': NOT_DONE,
                        'india_ink': NOT_DONE}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('csf_cr_ag', form_validator._errors)
        self.assertIn('india_ink', form_validator._errors)

    def test_differential_lymphocyte_count_required(self):
        cleaned_data = {
            'csf_wbc_cell_count': 0,
            'differential_neutrophil_count': 0,
            'differential_neutrophil_unit': '%'}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('differential_lymphocyte_count', form_validator._errors)
        self.assertIn('is required', str(
            form_validator._errors.get('differential_lymphocyte_count')))

    def test_neutrophil_count_required(self):
        cleaned_data = {
            'csf_wbc_cell_count': 0,
            'differential_lymphocyte_count': 50,
            'differential_lymphocyte_unit': '%'}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('differential_neutrophil_count', form_validator._errors)
        self.assertIn('is required', str(
            form_validator._errors.get('differential_neutrophil_count')))

    def test_csf_cr_ag_no_csf_cr_ag_lfa_not_required(self):
        cleaned_data = {'csf_cr_ag': NOT_DONE,
                        'csf_cr_ag_lfa': YES}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('csf_cr_ag_lfa', form_validator._errors)
        self.assertIn('not required', str(
            form_validator._errors.get('csf_cr_ag_lfa')))

    def test_differential_neutrophil_count_percent_limit_passed(self):
        cleaned_data = {
            'csf_wbc_cell_count': 4,
            'differential_lymphocyte_count': 50,
            'differential_lymphocyte_unit': '%',
            'differential_neutrophil_count': 125.6,
            'differential_neutrophil_unit': '%'}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('differential_neutrophil_count', form_validator._errors)
        self.assertIn(
            'Cannot be greater than 100%',
            str(form_validator._errors.get('differential_neutrophil_count')))

    def test_differential_lymphocyte_count_percent_limit_passed(self):
        cleaned_data = {
            'csf_wbc_cell_count': 4,
            'differential_lymphocyte_count': 125.6,
            'differential_lymphocyte_unit': '%'}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('differential_lymphocyte_count', form_validator._errors)
        self.assertIn(
            'Cannot be greater than 100%',
            str(form_validator._errors.get('differential_lymphocyte_count')))
