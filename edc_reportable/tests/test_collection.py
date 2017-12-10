from datetime import datetime
from dateutil.relativedelta import relativedelta
from edc_base.utils import get_utcnow
from edc_constants.constants import MALE, FEMALE
from pytz import utc
from unittest import TestCase

from ..grade_reference import GradeReference
from ..normal_reference import NormalReference
from ..reference_collection import ReferenceCollection, AlreadyRegistered
from ..value_reference_group import ValueReferenceGroup


class TestCollection(TestCase):

    def test_collection(self):
        dob = get_utcnow() - relativedelta(years=25)
        report_datetime = utc.localize(datetime(2017, 12, 7))
        reference = ReferenceCollection()

        self.assertTrue(repr(reference))

        neutrophils = ValueReferenceGroup(name='neutrophils')
        ln = NormalReference(
            name='neutrophils',
            lower=2.5,
            upper=7.5,
            units='10e9/L',
            age_lower=18,
            age_upper=99,
            age_units='years',
            gender=[MALE, FEMALE])

        g3 = GradeReference(
            name='neutrophils',
            grade=3,
            lower=0.4,
            lower_inclusive=True,
            upper=0.59,
            upper_inclusive=True,
            units='10e9/L',
            age_lower=18,
            age_upper=99,
            age_units='years',
            gender=[MALE, FEMALE])

        g4 = GradeReference(
            name='neutrophils',
            grade=4,
            lower=0,
            upper=0.4,
            units='10e9/L',
            age_lower=18,
            age_upper=99,
            age_units='years',
            gender=[MALE, FEMALE])

        neutrophils.add_normal(ln)
        neutrophils.add_grading(g3)
        neutrophils.add_grading(g4)

        reference.register(neutrophils)
        self.assertRaises(
            AlreadyRegistered,
            reference.register, neutrophils)
        self.assertTrue(reference.get(
            'neutrophils').get_normal(
                value=3.5, units='10e9/L',
                gender=MALE, dob=dob, report_datetime=report_datetime))

        neutrophils = reference.get('neutrophils')
        self.assertTrue(
            neutrophils.get_normal(
                value=3.5, units='10e9/L',
                gender=MALE, dob=dob, report_datetime=report_datetime))
        grade = neutrophils.get_grade(
            value=3.5, units='10e9/L',
            gender=MALE, dob=dob, report_datetime=report_datetime)
        self.assertIsNone(grade)

        grade = neutrophils.get_grade(
            value=.43, units='10e9/L',
            gender=MALE, dob=dob, report_datetime=report_datetime)
        self.assertEqual(grade.grade, 3)

        grade = neutrophils.get_grade(
            value=.3, units='10e9/L',
            gender=MALE, dob=dob, report_datetime=report_datetime)
        self.assertEqual(grade.grade, 4)
