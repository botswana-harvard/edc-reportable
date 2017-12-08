# edc-reportable

[![Build Status](https://travis-ci.org/botswana-harvard/edc-reportable.svg?branch=develop)](https://travis-ci.org/botswana-harvard/edc-reportable) [![Coverage Status](https://coveralls.io/repos/github/botswana-harvard/edc-reportable/badge.svg?branch=develop)](https://coveralls.io/github/botswana-harvard/edc-reportable?branch=develop)

Reportable clinic events, reference ranges, grading


### Normal ranges

    reference = ReferenceCollection()
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
    reference.register(neutrophils)
