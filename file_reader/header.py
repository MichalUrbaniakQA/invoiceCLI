import calendar
import time
from datetime import datetime, timedelta


class HeaderInvoice:
    def __init__(self, path_header, cur_month, cur_year):
        self.path = path_header
        self.cur_month = cur_month
        self.cur_year = cur_year

    def read_file_header(self):
        header = {}
        with open(self.path) as file:
            for line in file:
                key = line.split(':')
                val = line.split(':')

                if val[1].__contains__("last_day_of_month"):
                    last_day_of_month = calendar.monthrange(int(self.cur_year), int(self.cur_month))[1]
                    val[1] = str(time.strftime("%Y-%m")) + "-" + str(last_day_of_month)

                    date_object = datetime.strptime(val[1], '%Y-%m-%d').date()
                    if date_object.isoweekday() == 6:
                        val[1] = date_object - timedelta(1)
                    if date_object.isoweekday() == 7:
                        val[1] = date_object - timedelta(2)

                header[str(key[0])] = str(val[1])

        file.close()
        return header
