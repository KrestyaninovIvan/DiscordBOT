# переманная time время в секундах
from datetime import datetime as dt
from datetime import timedelta as td
from dateutil.relativedelta import relativedelta



class SecondsConvert:
    __TODAY = dt.utcnow()

    def __init__(self, period='0'):
        self.__period = int(period)
        self.data = None
        self.period_out()
        self.__new_today()

    def period_out(self):
        self.data = (self.__TODAY - td(days=self.__period)).date()

    def __new_today(self):
        self.__TODAY = dt.utcnow()

    @property
    def to_day(self):
        return self.__TODAY

    @property
    def day(self):
        return self.__TODAY.day

    @property
    def month(self):
        return self.__TODAY.month

    @property
    def year(self):
        return self.__TODAY.year

    def date(self, datetime):
        return datetime.date()

    @property
    def months_minus(self):
        months = self.__TODAY - relativedelta(months=1)
        return months.date()

    @property
    def months_plus(self):
        months = self.__TODAY + relativedelta(months=1)
        return months.date()

    def time_to_second(self, time_start):
        game_time = self.__TODAY - time_start
        return game_time.seconds

    def __del__(self):
        print('SecondsConvert удален')


class DataOut:
    __SECOND_DAY = 86400
    __SECOND_HOUR = 3600
    __SECOND_MINUTE = 60

    def __init__(self, time=0):
        self.__time = time

    def time_update(self, time):
        self.__time = time

    def output_days(self, inscription=False):
        days = self.__time // self.__SECOND_DAY
        if inscription:
            if days == 1:
                return f'День: {days}'
            elif days % 10 in [2, 3, 4]:
                return f'Дня: {days}'
            else:
                return f'Дней: {days}'
        else:
            return days

    def output_hours(self, inscription=False):
        hours = self.__time % self.__SECOND_DAY // self.__SECOND_HOUR
        if inscription:
            if hours == 1:
                return f'Час: {hours}'
            elif hours % 10 in [2, 3, 4]:
                return f'Часа: {hours}'
            else:
                return f'Часов: {hours}'
        else:
            return hours

    def output_minutes(self, inscription=False):
        minutes = self.__time % self.__SECOND_DAY
        minutes = minutes % self.__SECOND_HOUR
        minutes = minutes // self.__SECOND_MINUTE
        if inscription:
            if minutes == 1:
                return f'Минуту: {minutes}'
            elif minutes % 10 in [2, 3, 4]:
                return f'Минуты: {minutes}'
            else:
                return f'Минут: {minutes}'
        else:
            return minutes

    def __del__(self):
        print('DataOut удален')

