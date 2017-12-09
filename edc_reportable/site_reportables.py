import csv
import os

from .grade_reference import GradeReference
from .normal_reference import NormalReference
from .reference_collection import ReferenceCollection
from .value_reference_group import ValueReferenceGroup, GRADING, NORMAL
from edc_reportable.parsers import unparse


class Reportables:

    def __init__(self):
        self._registry = {}

    def __iter__(self):
        return iter(self._registry.items())

    def register(self, name=None, normal_data=None, grading_data=None):
        if name in self._registry:
            reference_collection = self._registry.get(name)
        else:
            reference_collection = ReferenceCollection(name=name)
        for name, datas in normal_data.items():
            grp = ValueReferenceGroup(name=name)
            for data in datas:
                val_ref = NormalReference(name=name, **data)
                grp.add_normal(val_ref)
            reference_collection.register(grp)
        for name, datas in grading_data.items():
            grp = reference_collection.get(name)
            for data in datas:
                grade_ref = GradeReference(name=name, **data)
                grp.add_grading(grade_ref)
            reference_collection.update_grp(grp)
        site_reportables._registry.update(
            {reference_collection.name: reference_collection})

    def get(self, name):
        return self._registry.get(name)

    def get_normal(self, name):
        return self._registry.get(name)[NORMAL]

    def get_grading(self, name):
        return self._registry.get(name)[GRADING]

    def read_csv(self, name=None, path=None):
        pass

    def to_csv(self, key=None, path=None):
        path = path or os.path.expanduser('~/')
        filename1 = os.path.join(path, f'{key}_normal_ranges.csv')
        filename2 = os.path.join(path, f'{key}_grading.csv')
        reference_collection = self.get(key)
        data = reference_collection.as_data()
        try:
            fieldnames = list(data.get('normal')[0].keys())
        except IndexError:
            pass
        else:
            fieldnames.insert(1, 'description')
            with open(filename1, 'w') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for dct in data.get('normal'):
                    dct.update(description=unparse(**dct))
                    writer.writerow(dct)
        try:
            fieldnames = list(data.get('grading')[0].keys())
        except IndexError:
            pass
        else:
            fieldnames.insert(1, 'description')
            with open(filename2, 'w') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for dct in data.get('grading'):
                    dct.update(description=unparse(**dct))
                    writer.writerow(dct)
        return filename1, filename2


site_reportables = Reportables()
