import conf

class DataHelper:
    def __init__(self):
        self.file = conf.file

    def getOne(self, dni, user):
        with open(self.file, "r", encoding="utf-8") as f:
            for line in f:
                splitted = line.strip().split(",")
                if splitted[0] == dni:
                    return splitted[1].strip().lower()
        return False