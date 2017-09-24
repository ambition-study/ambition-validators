from django.core.exceptions import ValidationError
from django.db import models
from django.test import TestCase
from edc_base.model_mixins import BaseUuidModel
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO
from edc_constants.constants import NO, OTHER, YES

from .. import PreviousOpportunisticInfectionFormValidator


class PatientHistory(BaseUuidModel):

    previous_oi = models.CharField(
        verbose_name='Previous opportunistic infection other than TB?',
        max_length=5,
        choices=YES_NO)


class TestPreviousOpportunisticInfection(TestCase):

    def setUp(self):
        self.patient_history = PatientHistory()

    def test_previous_non_tb_oi(self):
        """ Assert previous_non_tb_oi invalid if previous_oi is NO in parent
         form.
         """
        self.patient_history.previous_oi = NO

        cleaned_data = {'patient_history': self.patient_history,
                        'previous_non_tb_oi': 'Kaposi_sarcoma',
                        }
        form = PreviousOpportunisticInfectionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('previous_non_tb_oi', form._errors)

    def test_previous_non_tb_oi_no_date_invalid(self):
        """Assert previous_non_tb_oi_date invalid if previous_non_tb_oi is None.
        """
        self.patient_history.previous_oi = YES

        cleaned_data = {'patient_history': self.patient_history,
                        'previous_non_tb_oi': 'Kaposi_sarcoma',
                        'previous_non_tb_oi_date': None
                        }
        form = PreviousOpportunisticInfectionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('previous_non_tb_oi_date', form._errors)

    def test_previous_non_tb_oi_other_no_other_invalid(self):
        """Assert previous_non_tb_oi_other is invalid if previous_non_tb_oi is
        not None.
        """
        self.patient_history.previous_oi = YES

        cleaned_data = {'patient_history': self.patient_history,
                        'previous_non_tb_oi': OTHER,
                        'previous_non_tb_oi_other': None
                        }
        form = PreviousOpportunisticInfectionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('previous_non_tb_oi_other', form._errors)