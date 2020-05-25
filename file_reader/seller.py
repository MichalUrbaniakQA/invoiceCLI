class SellerInvoice:
    def __init__(self, path_seller):
        self.path = path_seller

    def read_file_seller(self):
        seller = {}
        with open(self.path) as file:
            for line in file:
                key = line.split(':')
                val = line.split(':')
                seller[str(key[0])] = val[1]

        file.close()
        return seller
