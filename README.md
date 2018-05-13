# edc-reportable

[![Build Status](https://travis-ci.org/clinicedc/edc-reportable.svg?branch=develop)](https://travis-ci.org/clinicedc/edc-reportable) [![Coverage Status](https://coveralls.io/repos/github/clinicedc/edc-reportable/badge.svg?branch=develop)](https://coveralls.io/github/clinicedc/edc-reportable?branch=develop)

Reportable clinic events, reference ranges, grading


    from dateutil.relativedelta import relativedelta
    from edc_base.utils import get_utcnow
    from edc_constants.constants import MALE, FEMALE
    from edc_reportable import ValueReferenceGroup, NormalReference, GradeReference
    from edc_reportable import site_reportables
    from edc_reportable.tests.reportables import normal_data, grading_data
    
Create a group for each test:

    neutrophils = ValueReferenceGroup(name='neutrophils')

A normal reference is declared like this:

    ref = NormalReference(
        name='neutrophils',
        lower=2.5,
        upper=7.5,
        units='10e9/L',
        age_lower=18,
        age_upper=99,
        age_units='years',
        gender=[MALE, FEMALE])
    
    ref
    >>> NormalReference(neutrophils, 2.5<x<7.5 10e9/L MF, 18<AGE<99 years)   

And add to a group like this:
    
    neutrophils.add_normal(ref)
 
Add as many normal references in a group as you like, just ensure the `lower` and `upper` boundaries don't overlap.

> __Note:__ If the lower and upper values of a normal reference overlap 
> with another normal reference in the same group, a `BoundaryOverlap`
> exception will be raised when the value is evaluated.
> Catch this in your tests.
 
A grading reference is declared like this:

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
    
    >>> g3
    GradeReference(neutrophils, 0.4<=x<=0.59 in 10e9/L GRADE 3, MF, 18<AGE<99 in years) GRADE 3)

And added to the group like this:

    neutrophils.add_grading(g3)

Declare and add a `GradeReference` for each reportable grade of the test. 

> __Note:__ If the lower and upper values of a grade reference overlap 
> with another grade reference in the same group, a `BoundaryOverlap`
> exception will be raised when the value is evaluated.
> Catch this in your tests.


### Registering with `site_reportables`

Once you have declared all your references, register them

    site_reportables.register(
        name='my_project',
        normal_data=normal_data,
        grading_data=grading_data)

> __Important:__ Writing out references is prone to error. It is better to declare a
> dictionary of normal references and grading references. Use the `parse` function
> so that you can use a phrase like `13.5<=x<=17.5` instead of a listing attributes. 
> There are examples of complete `normal_data` and `grading_data` in the tests.
> See`edc_reportable.tests.reportables`. 

You can export your declared references to CSV for further inspection

    >>> site_reportables.to_csv(name='my_project', path='~/')
    
    ('/Users/erikvw/my_project_normal_ranges.csv',
    '/Users/erikvw/my_project_grading.csv')    

### Using your reportables

In your code, get the references by collection name:
    
    my_project_reportables = site_reportables.get('my_project')

    neutrophil = my_project_reportables.get('neutrophil')

    report_datetime = get_utcnow()
    dob = (report_datetime - relativedelta(years=25)).date() 
    
### Check a normal value

If a value is normal, `get_normal` returns the `NormalReference` instance that matched with the value. 

    # evaluate a normal value
    normal = neutrophil.get_normal(
        value=3.5, units='10^9/L',
        gender=MALE, dob=dob, report_datetime=report_datetime)

    # returns a normal object with information about the range selected
    >>> normal.description
    '2.5<=3.5<=7.5 10^9/L MF, 18<=AGE years'

### Check an abnormal value

If a value is abnormal, `get_normal` returns `None`.

    # evaluate an abnormal value
    opts = dict(
        units='10^9/L',
        gender=MALE, dob=dob,
        report_datetime=report_datetime)
    normal = neutrophil.get_normal(value=0.3, **opts)

    # returns None
    >>> if not normal:
            print('abnormal')
    'abnormal'
 
 To show which ranges the value was evaluated against

    # use same options for units, gender, dob, report_datetime
    >>> neutrophil.get_normal_description(**opts)
    ['2.5<=x<=7.5 10^9/L MF, 18<=AGE years']
    
### Check if a value is "reportable"

    grade = neutrophil.get_grade(
        value=0.43, units='10^9/L',
        gender=MALE, dob=dob, report_datetime=report_datetime)

    >>> grade.grade
    3
    
    >>> grade.description
    '0.4<=0.43<=0.59 10^9/L GRADE 3'

    grade = neutrophil.get_grade(
        value=0.3, units='10^9/L',
        gender=MALE, dob=dob, report_datetime=report_datetime)

    >>> grade.grade
    4

    >>> grade.description
    '0.3<0.4 10^9/L GRADE 4'
    
If the value is not evaluated against any reportable ranges, a `NotEvaluated` exception is raised

    # call with the wrong units
    
    >>> grade = neutrophil.get_grade(
            value=0.3, units='mmol/L',
            gender=MALE, dob=dob, report_datetime=report_datetime)

    NotEvaluated: neutrophil value not graded. No reference range found ...

