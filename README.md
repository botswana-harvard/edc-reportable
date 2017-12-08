# edc-reportable

[![Build Status](https://travis-ci.org/botswana-harvard/edc-reportable.svg?branch=develop)](https://travis-ci.org/botswana-harvard/edc-reportable) [![Coverage Status](https://coveralls.io/repos/github/botswana-harvard/edc-reportable/badge.svg?branch=develop)](https://coveralls.io/github/botswana-harvard/edc-reportable?branch=develop)

Reportable clinic events, reference ranges, grading


### Normal ranges

    neutrophils = ValueReferenceGroup(name='neutrophils)
    ref = ValueReference(
        name='neutrophils',
        lower=2.5,
        upper=7.5,
        units='10e9/L',
        age_lower=18,
        age_upper=99,
        age_units='years',
        gender=[MALE, FEMALE])
    neutrophils.add_normal(ref)
    
### Check if a value is normal

    neutrophils.in_bounds(
        value=3.5, units='10e9/L',
        gender=MALE, dob=dob, report_datetime=report_datetime)
    >>> True  # normal

### Grading

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
        lower=None,
        upper=0.4,
        units='10e9/L',
        age_lower=18,
        age_upper=99,
        age_units='years',
        gender=[MALE, FEMALE])

    neutrophils.add_grading(g3)
    neutrophils.add_grading(g4)

### Check if a value is "reportable"

    neutrophils.in_bounds_for_grade(
        value=0.43, units='10e9/L',
        gender=MALE, dob=dob, report_datetime=report_datetime)
    neutrophils.grade
    >>> 3

    neutrophils.in_bounds_for_grade(
        value=0.3, units='10e9/L',
        gender=MALE, dob=dob, report_datetime=report_datetime)
    neutrophils.grade
    >>> 4

### Add `neutrophils` to the site collection
 
     reference = ReferenceCollection()
     reference.register(neutrophils)

### Add all
     
     reference.register(platelets)
     reference.register(creatinine)
     reference.register(sodium)
     ...
     ...
 
### Get `neutrophils` from the site collection
 
     neutrophils = reference.get('neutrophils')
 