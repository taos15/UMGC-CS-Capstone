"""Persistence outcomes translated to HTTP at the feature boundary."""
class RecordMissing(Exception):
    pass


class StaleVersion(Exception):
    pass


class DuplicateKey(Exception):
    pass
