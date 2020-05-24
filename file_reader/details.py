import locale
import re
from datetime import datetime

import inflect
from translate import Translator


class Details:
    def __init__(self, path_details, number_hours_worked, cur_month, cur_year):
        self.path = path_details
        self.number_hours_worked = number_hours_worked
        self.cur_month = cur_month
        self.cur_year = cur_year

    def read_file_header(self):
        details = {}
        with open(self.path) as file:
            for line in file:
                key = line.split(':')
                val = line.split(':')

                if val[1].__contains__("{month}"):
                    locale.setlocale(locale.LC_ALL, '')
                    current_month_word = datetime.today().strftime("%B")
                    current_data = current_month_word + " " + self.cur_year

                    val[1] = re.sub(r"[{}]", "", val[1]).replace("month", current_data)

                details[str(key[0])] = val[1]

            file.close()
            self.__float_to_int(details, self.number_hours_worked)
            details['total_price_word'] = self.__gross_price_to_polish(details)

            self.__final_prices(details)
            details['invoice_title'] = details['invoice_title'] + ' ' + self.__invoice_title_create()

        return details

    def __float_to_int(self, details, number_hours_worked):
        net_all_price = int(details['net_per_hour']) * int(number_hours_worked)
        details['net_all_price'] = net_all_price

        vat_price = int(int(details['net_all_price'] * int(details['vat_percent'])) / 100)
        details['vat_price'] = vat_price

        gross_all_price = details['net_all_price'] + details['vat_price']
        details['gross_all_price'] = gross_all_price

    def __final_prices(self, details):
        details['net_all_price'] = "{0:,}".format(details['net_all_price']).replace(',', " ") + ',00'
        details['vat_price'] = "{0:,}".format(details['vat_price']).replace(',', " ") + ',00'
        details['gross_all_price'] = "{0:,}".format(details['gross_all_price']).replace(',', " ") + ',00'
        details['net_per_hour'] = details['net_per_hour'].replace('\n', "") + ',00'
        details['vat_percent'] = str(details['vat_percent']) + '%'

    def __invoice_title_create(self):
        invoice_number_2020y = {'5': '2', '6': '3', '7': '4', '8': '5', '9': '6', '10': '7', '11': '8', '12': '9'}
        invoice_number_2021y = {'1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8',
                                '9': '9', '10': '10', '11': '11', '12': '12'}

        inv_number = ''

        if self.cur_year == '2020':
            inv_number = invoice_number_2020y[self.cur_month]
        if self.cur_year == '2021':
            inv_number = invoice_number_2021y[self.cur_month]

        invoice_title = inv_number + '/' + self.cur_month + '/' + self.cur_year
        return invoice_title

    def __gross_price_to_polish(self, details):
        p = inflect.engine()
        en_words = p.number_to_words(details['gross_all_price'])

        translator = Translator("pl")
        pl_words = translator.translate(en_words) + ' 00/100 PLN'

        return pl_words
