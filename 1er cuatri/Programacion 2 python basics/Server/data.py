import json

FILE = "currencies.json"

def _deserialize():
    with open(FILE, "r") as f:
        text = f.read()
        return json.loads(text)

def getCurrencies():
    curreciesData = _deserialize()
    return list(curreciesData.keys())

def getCurrency(currency):
    getCurrencies = _deserialize()
    try:
        return getCurrencies[currency]
    except KeyError:
        return None

def test():
    print(getCurrencies())

if __name__ == "__main__":
    test()