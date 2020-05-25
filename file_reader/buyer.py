class BuyerInvoice:
    def __init__(self, path_buyer):
        self.path = path_buyer

    def read_file_buyer(self):
        buyer = {}
        with open(self.path) as file:
            for line in file:
                key = line.split(':')
                val = line.split(':')
                buyer[str(key[0])] = val[1]

        file.close()
        return buyer
