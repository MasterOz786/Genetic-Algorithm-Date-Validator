
"""
    Provides a fitness function for the dates population, using association not aggregation
"""

# Year Based Categories
EVEN_SAAL = "Even Year"
ODD_SAAL = "Odd Year"
PRIME_SAAL = "Prime Year"
WAKHRA_SAAL = "Leap Year"
AAM_SAAL = "Regular Year"

# Month Based Categories
WADDA_MAHINA = "31-Day Month"
NIKKA_MAHINA = "30-Day Month"
EVEN_MAHINA = "Even Month"
ODD_MAHINA = "Odd Month"
PRIME_MONTH = "Prime Month"
WAKHRA_MAHINA = "Leap Month"
AAM_MAHINA = "Regular Month"

# Day Based Categories
JAAN_CHAD_DIN = "31 Day"
TURR_GYA_DIN = "30 Day"
EVEN_DIN = "Even Day"
ODD_DIN = "Odd Day"
PRIME_DIN = "Prime Day"
WAKHRA_DIN = "Leap Day"
AAM_DIN = "Regular Day"

# INVALID CLASSES
INVALID_LEAP_SAAL = "Invalid Leap Year"
INVALID_LEAP_MONTH = "Invalid Leap Month"
INVALID_LEAP_DAY = "Invalid Leap Day"
INVALID_BUKHEEL_SAAL = "Invalid Year (Hadood Tajawaz)"
INVALID_BUKHEEL_MONTH = "Invalid Month (Hadood Tajawaz)"
INVALID_BUKHEEL_DAY = "Invalid Day (Hadood Tajawaz)"
INVALID_SAKHI_SAAL = "Invalid Year (Negative)"
INVALID_SAKHI_MONTH = "Invalid Month (Negative)"
INVALID_SAKHI_DAY = "Invalid Day (Negative)"

def is_prime(n):
    if n == 2:
        return True
    if n < 2 or n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def is_leapyear(n):
    if n % 4 == 0 and n % 100 != 0 or n % 400 == 0:
        return True
    return False

class Fitness:
    def __init__(self, dates):
        self.categories = {
            "SAAL": {
                "EVEN": 0,
                "ODD": 0,
                "PRIME": 0,
                "WAKHRA": 0,
                "AAM": 0
            },
            "MAHINA": {
                "WADDA": 0,
                "NIKKA": 0,
                "EVEN": 0,
                "ODD": 0,
                "PRIME": 0,
                "WAKHRA": 0,
                "AAM": 0
            },
            "DIN": {
                "JAAN_CHAD": 0,
                "TURR_GYA": 0,
                "EVEN": 0,
                "ODD": 0,
                "PRIME": 0,
                "WAKHRA": 0,
                "AAM": 0
            },
            "INVALID_LEAP": {
                "SAAL": 0,
                "MONTH": 0,
                "DAY": 0
            },
            "INVALID_BUKHEEL": {
                "SAAL": 0,
                "MONTH": 0,
                "DAY": 0
            },
            "INVALID_SAKHI": {
                "SAAL": 0,
                "MONTH": 0,
                "DAY": 0
            }
        }

        self.dates = dates
        self.unique_categories = 0
        self.redundant_categories = 0
        return None

    def __get_categories(self, dates): # returns a dict of frequencies of categories
        for date in dates:
            print(date)
            day, month, year = date
            
            """ Valid Categories """
            # year categories
            if is_leapyear(year):
                self.categories["SAAL"]["WAKHRA"] += 1
            else:
                self.categories["SAAL"]["AAM"] += 1
            
            if year % 2 == 0:
                self.categories["SAAL"]["EVEN"] += 1
            else:
                self.categories["SAAL"]["ODD"] += 1
            
            if is_prime(year):
                self.categories["SAAL"]["PRIME"] += 1
            
            # Month categories
            if month in {1, 3, 5, 7, 8, 10, 12}:
                self.categories["MAHINA"]["WADDA"] += 1
            elif month in {4, 6, 9, 11}:
                self.categories["MAHINA"]["NIKKA"] += 1
            
            if month % 2 == 0:
                self.categories["MAHINA"]["EVEN"] += 1
            else:
                self.categories["MAHINA"]["ODD"] += 1
            
            if is_prime(month):
                self.categories["MAHINA"]["PRIME"] += 1
            
            if month == 2 and is_leapyear(year):
                self.categories["MAHINA"]["WAKHRA"] += 1
            else:
                self.categories["MAHINA"]["AAM"] += 1
            
            # Day categories
            if day % 2 == 0:
                self.categories["DIN"]["EVEN"] += 1
            else:
                self.categories["DIN"]["ODD"] += 1
            
            if is_prime(day):
                self.categories["DIN"]["PRIME"] += 1
            
            if month in {1, 3, 5, 7, 8, 10, 12} and day == 31:
                self.categories["DIN"]["JAAN_CHAD"] += 1
            elif month in {4, 6, 9, 11} and day == 30:
                self.categories["DIN"]["TURR_GYA"] += 1
            
            if month == 2:
                if is_leapyear(year):
                    if day == 29:
                        self.categories["DIN"]["WAKHRA"] += 1
                    elif day < 29:
                        self.categories["DIN"]["AAM"] += 1
                elif day > 28:
                    self.categories["INVALID_BUKHEEL"]["DAY"] += 1
            
            # Invalid categories
            if year <= 0:
                self.categories["INVALID_BUKHEEL"]["SAAL"] += 1
            if month <= 0:
                self.categories["INVALID_BUKHEEL"]["MONTH"] += 1
            if month > 12:
                self.categories["INVALID_BUKHEEL"]["MONTH"] += 1
            if day <= 0:
                self.categories["INVALID_BUKHEEL"]["DAY"] += 1
            elif day > 31:
                self.categories["INVALID_SAKHI"]["DAY"] += 1

        return self.categories

    def clear_categories(self):
        # set all values to 0
        self.categories = {key: {subkey: 0 for subkey in self.categories[key]} for key in self.categories}

    def compute_fitness(self, dates):
        # clear the categories frequency count
        self.clear_categories()

        # pass the list of dates to categorize them
        categories = self.__get_categories(dates)
        
        # flatten the categories
        flat_categories = {key: value for subdict in categories.values() for key, value in subdict.items() if value > 0}
        
        unique_categories_sum = len(flat_categories)
        redundant_categories_sum = sum(value - 1 for value in flat_categories.values() if value > 1)

        # compute fitness
        if unique_categories_sum + redundant_categories_sum > 0:
            fitness = unique_categories_sum / (1 + redundant_categories_sum)
        else:
            fitness = 0

        fitness = unique_categories_sum - redundant_categories_sum

        print(flat_categories)
        print(unique_categories_sum, redundant_categories_sum, fitness)
        
        return fitness
