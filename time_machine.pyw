from datetime import datetime
from datetime import timedelta
import re


date_today = datetime.today()

class TimeMachine:
	global now_pattern
	global now_pattern_colons
	global today_pattern
	now_pattern = "%Y-%m-%d %H-%M-%S-%f"
	now_pattern_colons = "%Y-%m-%d %H:%M:%S"
	today_pattern = "%Y-%m-%d"

	def show_now_pattern(self):
		return now_pattern

	def show_today_pattern(self):
		return today_pattern

	def now(self):
		return datetime.now().strftime(now_pattern)

	def now_colons(self):
		return datetime.now().strftime(now_pattern_colons)

	def today(self):
		return datetime.now().strftime(today_pattern)

	def mondays(self):
		
		list_of_mondays = []

		for index in range(-30, 91):
			date = date_today + timedelta(days = index)

			if date.isoweekday() == 1:
				list_of_mondays.append(date.strftime("%Y-%m-%d"))
			else:
				pass
		return list_of_mondays

	def x_days_including_today(self, x_days):
		starting_date = (int(x_days) - 1) * -1 
		list_of_dates = []

		for index in range(starting_date, 1):
			date = date_today + timedelta(days = index)
			list_of_dates.append(date.strftime("%Y-%m-%d"))

		return list_of_dates

	def extract_day(self, date):
		try:
			self.date = date

			day = re.search("\d\d\d\d\-\d\d\-\d\d", self.date).group()

			return day
		except:
			pass

	def date_to_number(self, date):
		if isinstance(date, str):
			end = datetime.strptime(date, today_pattern)
		else:
			end = datetime.strftime(date, today_pattern)
			end = datetime.strptime(end, today_pattern)

		start = "2000-01-01"
		start = datetime.strptime(start, today_pattern)

		difference = end - start

		return int(difference.days)

	def date_time_to_number(self, date):
		if isinstance(date, str):
			end = datetime.strptime(date, now_pattern_colons)
		else:
			end = datetime.strftime(date, now_pattern_colons)
			end = datetime.strptime(end, now_pattern_colons)

		start = "2000-01-01 00:00:00"
		start = datetime.strptime(start, now_pattern_colons)

		difference = end - start
		day_to_seconds = int(difference.days) * 86400
		time_to_seconds = int(difference.seconds)
		difference_seconds = day_to_seconds + time_to_seconds

		return difference_seconds

