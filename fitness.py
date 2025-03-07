
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
JAAN_CHAD_DIN = "31-Day Day"
TURR_GYA_DIN = "30-Day Day"
EVEN_DIN = "Even Day"
ODD_DIN = "Odd Day"
PRIME_DIN = "Prime Day"
WAKHRA_DIN = "Leap Day"
AAM_DIN = "Regular Day"

def is_prime(n):
    if n == 2:
        return True
    if n % 2 == 0:
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
    def __init__(self):
        return None

    def get_category(self, date):
        categories = []
        day = date[0], month = date[1], year = date[2]

        # year categories
        if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:    # leap year
            categories.append(WAKHRA_SAAL)
        if year % 2 == 0:
            categories.append(AAM_SAAL)
        if year % 2 == 1:
            categories.append(EVEN_SAAL)
        if is_prime(year):
            categories.append(PRIME_SAAL)
        
        # month categories
        if month in {1, 3, 5, 6, 7, 8, 10, 12}:
            categories.append(WADDA_MAHINA, JAAN_CHAD_DIN)
        if month in {4, 6, 9, 11}:
            categories.append(NIKKA_MAHINA, TURR_GYA_DIN)
        if month % 2 == 0:
            categories.append(EVEN_MAHINA)
        if month % 2 == 1:
            categories.append(ODD_MAHINA)
        if is_prime(month):
            categories.append(PRIME_MONTH)
        if is_leapyear(year):
            if month == 2:
                categories.append(WAKHRA_MAHINA)
            else:
                categories.append(AAM_MAHINA)

        # day categories
        if day % 2 == 0:
            categories.append(EVEN_DIN)
        if day % 2 == 1:
            categories.append(ODD_DIN)
        if is_prime(day):
            categories.append(PRIME_DIN)
        if month == 2 and is_leapyear(year):
            if day == 29:
                categories.append(WAKHRA_DIN)
            else:
                categories.append(AAM_DIN)

        return categories

    def get_fitness(self, dates):
        categories = self.categorize_dates(dates)