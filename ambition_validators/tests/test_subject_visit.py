from django import forms
from django.test import TestCase, tag

from edc_constants.constants import YES, OTHER
from edc_base.modelform_validators import REQUIRED_ERROR
from edc_visit_tracking.constants import MISSED_VISIT, UNSCHEDULED

from ..form_validators import SubjectVisitFormValidator


@tag('visit')
class TestSubjectVisitFormValidator(TestCase):

    def test_reason_missed(self):
        options = {
            'reason': MISSED_VISIT,
            'reason_missed': None}
        form_validator = SubjectVisitFormValidator(
            cleaned_data=options)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('reason_missed',
                      form_validator._errors)
        self.assertIn(REQUIRED_ERROR, form_validator._error_codes)

    def test_reason_unscheduled(self):
        options = {
            'reason': UNSCHEDULED,
            'reason_unscheduled': None}
        form_validator = SubjectVisitFormValidator(
            cleaned_data=options)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('reason_unscheduled',
                      form_validator._errors)
        self.assertIn(REQUIRED_ERROR, form_validator._error_codes)

    def test_reason_unscheduled_other(self):
        options = {
            'reason_unscheduled': OTHER,
            'reason_unscheduled_other': None}
        form_validator = SubjectVisitFormValidator(
            cleaned_data=options)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('reason_unscheduled_other',
                      form_validator._errors)
        self.assertIn(REQUIRED_ERROR, form_validator._error_codes)

    def test_info_source_other(self):
        options = {
            'info_source': OTHER,
            'info_source_other': None}
        form_validator = SubjectVisitFormValidator(
            cleaned_data=options)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('info_source_other',
                      form_validator._errors)
        self.assertIn(REQUIRED_ERROR, form_validator._error_codes)