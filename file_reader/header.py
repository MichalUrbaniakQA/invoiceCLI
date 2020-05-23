import calendar
import time
from datetime import datetime


class Header:
    def __init__(self, path_header):
        self.path = path_header

    def read_file_header(self):
        header = {}
        with open(self.path) as file:
            for line in file:
                key = line.split(':')
                val = line.split(':')

                if val[1].__contains__("last_day_of_month"):
                    last_day_of_month = calendar.monthrange(datetime.now().year, datetime.now().month)[1]
                    val[1] = str(time.strftime("%Y-%m")) + "-" + str(last_day_of_month)

                header[str(key[0])] = val[1]

        file.close()
        return header
