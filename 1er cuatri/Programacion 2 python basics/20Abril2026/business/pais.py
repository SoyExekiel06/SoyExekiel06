class pais:
    def __init__(self):
        self.name = "Argentina"
        self.population = "50000000"
        self.sup = 2780000
        self.capital = "CABA"
        self.FootballTeams = [
            {
                "name" : "Boca Juniors"
            },
            {
                "name" : "River Plate"
            },
            {
                "name" : "San Lorenzo"
            }
        ]
        self.worestCountryEver = True
        self.NuevoAtributo = "AAA"

    def toDict(self):
        param_list = dir(self)
        attr_list = {}
        for attr in param_list:
            if (attr.startswith("__") and attr.endswith("__")) or callable(getattr(self, attr)):
                pass
            else:
                attr_list[attr] = getattr(self,attr)
        return attr_list

    def fromDict(self, data):
        for key in data.keys():
            setattr(self, key, data[key])

