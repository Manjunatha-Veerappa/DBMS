from dateutil.easter import *
from datetime import timedelta
import csv

class EasterDateCalculation:
    def easterDatCalc(self, year):
        good_friday_date = easter(year) - timedelta(2)        # easter(year) gives the easter sunday date - 2 days = good Friday
        easter_monday_date = easter(year) + timedelta(1)      # easter(year) + 1 day = Easter Monday
        print("good_friday_date: ", good_friday_date)
        print("easter_monday_date: ", easter_monday_date)


instance = EasterDateCalculation()
instance.easterDatCalc(2017)