# check if day number today = monthend date
from datetime import datetime
import calendar

curr_year = int(datetime.now().strftime('%Y'))
curr_month = int(datetime.now().strftime('%m'))
calendar.monthrange(curr_year, curr_month)
print int(int(datetime.now().strftime('%d')) == calendar.monthrange(curr_year, curr_month)[1])
#print int(True)
