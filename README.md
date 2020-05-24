### For the first i am not programmer so dont judge my code :) This app was create for fun

### **InvoiceCLI**
Creating an invoice from the CLI.

### **Idea**
Automatic creation of an invoice with minimal time consumption.

### **What data I need?**
Four file in /util/data/ (actual there are in .gitignore)
- buyer.txt
- seller.txt
- header.txt
- details.txt

e.g. buyer.txt:
- name:Some Namce
- nip:12345678
- street:ĄŹŻblablabla
- city:00-000 CityName
    
e.g. seller.txt:
- name:Some Namce
- nip:12345678
- street:ĄŹŻblablabla
- city:00-000 CityName

e.g. header.txt:
- city:CityName
- create_date:last_day_of_month
- sell_date:last_day_of_month
    
e.g. header.txt:
- city:CityName
- create_date:last_day_of_month
- sell_date:last_day_of_month
 
e.g. details.txt:   
- lp:1
- jm:hour.
- net_per_hour:9999
- vat_percent:23
- payment:przelew
- account:11 11 1111 1111 1111
- invoice_title:Faktura VAT
- title:Usługi IT w miesiącu {month} według z umowy z dnia dd.mm.yyyy
    
### **How it works?**
After run app
- code get data from text files
- data from text files are inject to html (I wanted to make some fun with css but after that I think it was wrong idea :D)
- app convert html to pdf
- if pdf is exist in directory, old pdf is remove (html directory output is app app main class directory, pdf directory output is Desktop)

### **What I need to do?**
After run app I got console with two input
1) "Enter invoice output path (press enter if default):
2) "Enter the number of hours worked (press enter if default):

Why?
1) path to output directory. If you press enter without any data then output directory is ```os.path.expanduser("~/Desktop")```
2) How many worked hours you want to insert into invoice. If you press enter without any data then number of hours is got from http://kalendarz.livecity.pl/czas-pracy/2021 
```
calendar_working_hour_2021y = {'1': '152', '2': '160', '3': '184', '4': '168', '5': '152', '6': '168',
                                       '7': '176', '8': '176',
                                       '9': '176', '10': '168', '11': '160', '12': '176'}
```
If current month is december, then we got 176 hours for 12.2021

### **How is invoice title?**
My personal template is:
- Faktura VAT +
- buyer +
- number of invoice +
- month of invoice +
- year of invoice

e.g. 'Faktura VAT Matrix 2/5/2020'
- 'Faktura VAT buyerName' is got from file.text
- number is number of month because this is invoice for one my client and usually I send one invoice per month
```
invoice_number_2021y = {'1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8',
                                '9': '9', '10': '10', '11': '11', '12': '12'}
```
- '/5' is got from current month ```datetime.now().month```
- '/2020' is got from current year ```datetime.now().year```

### **What I do with it?**
- I created simply file.bat which cd to app directory and run app
- I setted scheduler on my windows system which every last day of month run my file.bat



# And that is all :)
