import unittest
import hypothesis
import hypothesis.strategies as st
import tests.utils
import teryte.calendar as cal


class TestDatestrings(unittest.TestCase):

    _format_specs = [
        "", "eraless", "epoch", "era", "c", "canonical",
    ]

    @hypothesis.given(date=..., format_spec=st.sampled_from(_format_specs))
    def test_to_and_from_datestring(self, date: cal.Date, format_spec: str) -> None:
        self.assertEqual(cal.Date.fromdatestring(format(date, format_spec)), date)


if __name__ == "__main__":
    unittest.main()
