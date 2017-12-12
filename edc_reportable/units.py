from django.utils.safestring import mark_safe

CELLS_PER_MILLIMETER_CUBED = 'cells/mm^3'
CELLS_PER_MILLIMETER_CUBED_DISPLAY = mark_safe('cells/mm<sup>3</sup>')
COPIES_PER_MILLILITER = 'copies/mL'
GRAMS_PER_DECILITER = 'g/dL'
IU_LITER = 'IU/L'
MICROMOLES_PER_LITER = 'umol/L'
MILLIGRAMS_PER_DECILITER = 'mg/dL'
MILLIMOLES_PER_LITER = 'mmol/L'
TEN_X_3_PER_LITER = '10^3/L'
TEN_X_3_PER_LITER_DISPLAY = mark_safe('10sup>3</sup>/L')
TEN_X_9_PER_LITER = '10^9/L'
TEN_X_9_PER_LITER_DISPLAY = mark_safe('10sup>9</sup>/L')
