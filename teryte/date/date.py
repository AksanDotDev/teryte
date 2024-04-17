import enums


class Date:
    """Basic type for Teryte dates.

    Constructors:

    __new__()
    noncanonical()
    arbitrary()
    fromdatestring()
    frominignedate()
    fromordinal()

    Operators:
    __repr__, __str__
    __eq__, __le__, __lt__, __ge__, __gt__, __hash__
    __add__, __radd__, __sub__ (Only with timedelta args)

    Methods:

    todatestring()
    toinignedate()
    toordinal()
    weekday()
    inigneweekday()
    month()
    inignemonth()
    canonicaldate()
    equivalentdates()
    eraordinalday()

    """


class DateSequence:
    """Helper class for formatting sequences of dates.

    Constructors:

    __new__()
    fromiterstrs()
    fromiterdates()
    frominignestrs()
    fromiterinignedates()

    Methods:

    toliststrs()
    tolistdates()
    tolistinignestrs()
    tolistinignedates()

    """
