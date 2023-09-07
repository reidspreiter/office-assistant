from unit_numbers import UnitNumbers


def key_list():
    """
    A wrapper function for a series of UnitNumbers's
    methods that lookup specific unit keycodes.
    """
    unit_numbers = UnitNumbers.UnitNumbers()
    unit_numbers.populate(purpose = "units to get keys for")
    unit_numbers.get_key_codes()
    unit_numbers.print_key_codes()