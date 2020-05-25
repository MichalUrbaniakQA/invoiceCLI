import codecs
import os
from datetime import datetime

import fire
import pdfkit

from file_reader.buyer import Buyer
from file_reader.details import Details
from file_reader.header import Header
from file_reader.hours_worked import HoursWorked
from file_reader.seller import Seller

cur_month = str(datetime.now().month)
cur_year = str(datetime.now().year)


def __remove_invoice_if_exist(invoice_template_html, invoice_pdf_name):
    if os.path.exists(invoice_template_html):
        os.remove(invoice_template_html)
    if os.path.exists(invoice_pdf_name):
        os.remove(invoice_pdf_name)


def __create_template_and_save_as_html(invoice_template_html, html_template, encoding):
    file = codecs.open(invoice_template_html, "w", encoding)
    file.write(html_template)
    file.close()


def __set_output_invoice_path():
    path = input("Enter invoice output path (press enter if default):")
    if not path:
        return os.path.expanduser("~/Desktop")
    return path


def __set_number_hours_worked(hours_worked_dict):
    number_hours = input("Enter the number of hours worked (press enter if default):")
    if not number_hours:
        return hours_worked_dict[cur_month]
    return number_hours


def create_invoice():
    invoice_template_html = 'invoice_template.html'
    invoice_pdf_name = 'invoice.pdf'
    encoding = 'utf-8'
    util_data_path = 'util/data/'

    seller = Seller(util_data_path + 'seller.txt')
    seller_dict = seller.read_file_seller()
    buyer = Buyer(util_data_path + 'buyer.txt')
    buyer_dict = buyer.read_file_buyer()
    header = Header(util_data_path + 'header.txt', cur_month, cur_year)
    header_dict = header.read_file_header()

    hours_worked = HoursWorked('util/hours_worked/hours_worked_2020.txt')
    hours_worked_dict = hours_worked.read_file_hours_worked()

    output_invoice_path = __set_output_invoice_path()
    number_hours_worked = __set_number_hours_worked(hours_worked_dict)

    details = Details(util_data_path + 'details.txt', number_hours_worked, cur_month, cur_year)
    details_dict = details.read_file_header()

    html_template = """
    <!DOCTYPE html>
    <html lang="en">
      <head>
          <meta charset="utf-8">
          <title>Invoice</title>
          <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
          <link rel="stylesheet" href="util/template/style.css"/>
      </head>
      <body>
        <div id="container_top">
            <section id="top_details">
              <section>
                  <div class="column1">
                      <div>
                          <div class="invoice_title">""" + details_dict['invoice_title'] + """</div>
                      </div>
                      <div>
                          <div class="seller_header">Sprzedawca</div>
                          <div class="seller_name">""" + seller_dict['name'] + """</div>
                          <div class="seller_nip">NIP: """ + seller_dict['nip'] + """</div>
                          <div class="seller_street">""" + seller_dict['street'] + """</div>
                          <div class="seller_city">""" + seller_dict['city'] + """</div>
                      </div>
                  </div>
                  <div class="column2">
                      <div>
                          <div class="place_of_issue">Miejsce wystawienia</div>
                          <div class="place_of_issue_city">""" + header_dict['city'] + """</div>
                          <div class="date_of_issue">Data wystawienia</div>
                          <div class="date_of_issue_details">""" + header_dict['create_date'] + """</div>
                          <div class="sell_date">Data sprzedaży</div>
                          <div class="sell_date_details">""" + header_dict['sell_date'] + """</div>
                      </div>
                      <div>
                          <div class="buyer_header">Nabywca</div>
                          <div class="buyer_name">""" + buyer_dict['name'] + """</div>
                          <div class="buyer_nip">NIP: """ + buyer_dict['nip'] + """</div>
                          <div class="buyer_street">""" + buyer_dict['street'] + """</div>
                          <div class="buyer_city">""" + buyer_dict['city'] + """</div>
                      </div>
                  </div>
            </section>
        </div>
        <div id="container_main_details">
            <section id="main_details">
                <div class="services">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Lp.</th>
                                <th>Nazwa towaru lub usługi</th>
                                <th>Jm.</th>
                                <th>Ilość</th>
                                <th>Cena netto</th>
                                <th>Wartość netto</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>""" + details_dict['lp'] + """</td>
                                <td>""" + details_dict['title'] + """</td>
                                <td>""" + details_dict['jm'] + """</td>
                                <td>""" + number_hours_worked + """</td>
                                <td>""" + details_dict['net_per_hour'] + """</td>
                                <td>""" + details_dict['net_all_price'] + """</td>
                            </tr>
                            <tr>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td class="last">VAT</td>
                                <td class="last">""" + details_dict['vat_percent'] + """</td>
                            </tr>
                            <tr>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td class="last">Kwota VAT</td>
                                <td class="last">""" + details_dict['vat_price'] + """</td>
                            </tr>
                            <tr>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td class="last">Razem brutto</td>
                                <td class="last">""" + details_dict['gross_all_price'] + """</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </section>
        </div>
        <div id="container_bottom">
            <section id="bottom_details">
                <div class="column3">
                    <div class="payment">Sposób płatności:</div>
                    <div class="account">Numer konta:</div>
                    <div class="total_price_digital">Do zapłaty:</div>
                    <div class="total_price_word">Kwota słownie:</div>
                </div>
                <div class="column4">
                    <div class="payment_details">""" + details_dict['payment'] + """</div>
                    <div class="account_details">""" + details_dict['account'] + """</div>
                    <div class="total_price_digital_details">""" + details_dict['gross_all_price'] + """ PLN</div>
                    <div class="total_price_word_details">""" + details_dict['total_price_word'] + """</div>
                </div>
            </section>
        </div>
        <div id="signature">
            <div>
                <p>Wystawił:</p>
            </div>
            <div>
                <p>Odebrał:</p>
            </div>
        </div>
      </body>
    </html>

        """

    __remove_invoice_if_exist(invoice_template_html, invoice_pdf_name)
    __create_template_and_save_as_html(invoice_template_html, html_template, encoding)
    pdfkit.from_file(invoice_template_html, output_invoice_path + '/' + invoice_pdf_name)


if __name__ == '__main__':
    fire.Fire(create_invoice())
