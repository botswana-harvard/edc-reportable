from datetime import datetime
from dateutil.relativedelta import relativedelta
from edc_base.utils import get_utcnow
from edc_constants.constants import MALE, FEMALE
from pytz import utc
from unittest import TestCase

from ..normal_reference import NormalReference
from ..value_reference_group import InvalidValueReference, NotEvaluated, BoundariesOverlap
from ..value_reference_group import ValueReferenceGroup, ValueReferenceAlreadyAdded


class TestValueReference(TestCase):

    def test_value_reference_group(self):
        dob = get_utcnow() - relativedelta(years=25)
        report_datetime = utc.localize(datetime(2017, 12, 7))
        grp = ValueReferenceGroup(name='labtest')
        self.assertTrue(repr(grp))

        ref = NormalReference(
            name='blahblah',
            lower=10,
            upper=None,
            units='mg/dL',
            age_lower=18,
            age_upper=99,
            age_units='years',
            gender=MALE)

        self.assertRaises(
            InvalidValueReference,
            grp.add_normal, ref)

        ref = NormalReference(
            name='labtest',
            lower=10,
            upper=None,
            units='mg/dL',
            age_lower=18,
            age_upper=99,
            age_units='years',
            gender=MALE)

        grp.add_normal(ref)

        self.assertFalse(grp.get_normal(
            value=9,
            units='mg/dL',
            gender=MALE,
            dob=dob))
        self.assertFalse(grp.get_normal(
            value=10,
            units='mg/dL',
            gender=MALE,
            dob=dob))
        self.assertTrue(grp.get_normal(
            value=11,
            units='mg/dL',
            gender=MALE,
            dob=dob))
        self.assertRaises(
            ValueReferenceAlreadyAdded,
            grp.add_normal, ref)

        # try without upper bound age
        grp = ValueReferenceGroup(name='another_labtest')
        ref = NormalReference(
            name='another_labtest',
            lower=10,
            upper=None,
            units='mg/dL',
            age_lower=18,
            age_units='years',
            gender=MALE)

        grp.add_normal(ref)

        self.assertFalse(grp.get_normal(
            value=9,
            units='mg/dL',
            gender=MALE,
            dob=dob))
        self.assertFalse(grp.get_normal(
            value=10,
            units='mg/dL',
            gender=MALE,
            dob=dob))
        self.assertTrue(grp.get_normal(
            value=11,
            units='mg/dL',
            gender=MALE,
            dob=dob))
        self.assertRaises(
            ValueReferenceAlreadyAdded,
            grp.add_normal, ref)
        self.assertEqual(
            grp.get_normal_description(
                units='mg/dL',
                gender=MALE,
                dob=dob),
            ['10.0<x mg/dL M, 18<AGE years'])

        grp = ValueReferenceGroup(name='labtest')

        ref_male = NormalReference(
            name='labtest',
            lower=10,
            upper=None,
            units='mg/dL',
            age_lower=18,
            age_upper=99,
            age_units='years',
            gender=MALE)
        ref_female1 = NormalReference(
            name='labtest',
            lower=1.7,
            upper=3.5,
            upper_inclusive=True,
            units='mg/dL',
            age_lower=18,
            age_upper=99,
            age_units='years',
            gender=FEMALE)
        ref_female2 = NormalReference(
            name='labtest',
            lower=7.3,
            upper=None,
            units='mg/dL',
            age_lower=18,
            age_upper=99,
            age_units='years',
            gender=FEMALE)

        grp.add_normal(ref_male)
        grp.add_normal(ref_female1)
        grp.add_normal(ref_female2)

        self.assertFalse(grp.get_normal(
            value=9, gender=MALE, dob=dob,
            report_datetime=report_datetime,
            units='mg/dL'))
        self.assertFalse(grp.get_normal(
            value=10, gender=MALE, dob=dob,
            report_datetime=report_datetime,
            units='mg/dL'))
        self.assertTrue(grp.get_normal(
            value=11, gender=MALE, dob=dob,
            report_datetime=report_datetime,
            units='mg/dL'))

        self.assertFalse(grp.get_normal(
            value=1, gender=FEMALE, dob=dob,
            report_datetime=report_datetime,
            units='mg/dL'))
        self.assertFalse(grp.get_normal(
            value=1.7, gender=FEMALE, dob=dob,
            report_datetime=report_datetime,
            units='mg/dL'))
        self.assertTrue(grp.get_normal(
            value=1.8, gender=FEMALE, dob=dob,
            report_datetime=report_datetime,
            units='mg/dL'))
        self.assertTrue(grp.get_normal(
            value=3.4, gender=FEMALE, dob=dob,
            report_datetime=report_datetime,
            units='mg/dL'))
        self.assertTrue(grp.get_normal(
            value=3.5, gender=FEMALE, dob=dob,
            report_datetime=report_datetime,
            units='mg/dL'))
        self.assertFalse(grp.get_normal(
            value=3.6, gender=FEMALE, dob=dob,
            report_datetime=report_datetime,
            units='mg/dL'))

        self.assertFalse(grp.get_normal(
            value=7.3, gender=FEMALE, dob=dob,
            report_datetime=report_datetime,
            units='mg/dL'))
        self.assertTrue(grp.get_normal(
            value=7.4, gender=FEMALE, dob=dob,
            report_datetime=report_datetime,
            units='mg/dL'))

        self.assertRaises(
            NotEvaluated,
            grp.get_normal,
            value=7.4, gender=FEMALE, dob=report_datetime.date(),
            report_datetime=report_datetime,
            units='mg/dL')

        self.assertRaises(
            NotEvaluated,
            grp.get_normal,
            value=7.4, gender=FEMALE, dob=report_datetime.date(),
            report_datetime=report_datetime,
            units='mmol/L')

        # for a normal value, show what it was evaluated against
        # for messaging
        self.assertFalse(grp.get_normal(
            value=7.3, gender=FEMALE, dob=dob,
            report_datetime=report_datetime,
            units='mg/dL'))
        self.assertEqual(
            grp.get_normal_description(
                gender=FEMALE, dob=dob,
                report_datetime=report_datetime,
                units='mg/dL'),
            ['1.7<x<=3.5 mg/dL F, 18<AGE<99 years',
             '7.3<x mg/dL F, 18<AGE<99 years'])

        # overlaps with ref_female3
        ref_female4 = NormalReference(
            name='labtest',
            lower=7.3,
            upper=9.3,
            units='mg/dL',
            age_lower=18,
            age_upper=99,
            age_units='years',
            gender=FEMALE)
        grp.add_normal(ref_female4)

        self.assertRaises(
            BoundariesOverlap,
            grp.get_normal,
            value=7.4, gender=FEMALE, dob=dob,
            report_datetime=report_datetime,
            units='mg/dL')
