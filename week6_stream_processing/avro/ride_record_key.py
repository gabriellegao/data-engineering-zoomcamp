from typing import Dict


class RideRecordKey:
    def __init__(self, vendor_id):
        self.vendor_id = vendor_id

    @classmethod
    def from_dict(cls, d: Dict):
        # Return format: RideRecordKey(vendor_id=123)
        return cls(vendor_id=d['vendor_id'])

    def __repr__(self):
        # Printed output format: RideRecordKey:{'vendor_id':123}
        # Real output format: RideRecordKey(vendor_id=123)
        return f'{self.__class__.__name__}: {self.__dict__}'


def dict_to_ride_record_key(obj, ctx):
    if obj is None:
        return None
    # data flow: from_dict -> __init__ -> __repr__
    return RideRecordKey.from_dict(obj)


def ride_record_key_to_dict(ride_record_key: RideRecordKey, ctx):
    # Input is an instance: RideRecord(vendor_=123,...), flowing into __init__
    # Output format: {dict}
    return ride_record_key.__dict__