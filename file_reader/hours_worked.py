class HoursWorked:
    def __init__(self, path_hours_worked):
        self.path = path_hours_worked

    def read_file_hours_worked(self):
        hours_worked = {}
        with open(self.path) as file:
            for line in file:
                key = line.split(':')
                val = line.split(':')
                hours_worked[str(key[0])] = val[1]

        file.close()
        return hours_worked
