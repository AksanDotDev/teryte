import hypothesis.strategies as st
import teryte.calendar as cal


@st.composite
def date_strat(draw):
    year = draw(st.integers())
    month = draw(st.integers(min_value=1, max_value=15))
    day = draw(st.integers(min_value=1, max_value=cal.Month(month).days))
    return cal.Date(year, month, day)


st.register_type_strategy(cal.Date, date_strat())
