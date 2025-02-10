import sys #to stop program if an input error occurs
import regex as re #the native module is re, regex needs to be installed
from datetime import datetime #for year validation
from localization.localization import load_localization

loc = load_localization()

def validate_number(number, number_field_name):
    if number <= 0:
        print(loc["negativeNumberError"].format(field_name=number_field_name))
        sys.exit()
    return number

def validate_text(text, text_field_name):
    if text == "":
        print(loc["emptyTextError"].format(field_name=text_field_name))
        sys.exit()
    return text

def validate_sn(sn):
    validate_number(sn, loc["snField"])

    sn_str = str(sn) #the parse converts to int, so convertion back to str is needed for validation on its length
    if len(sn_str) != 13:
        print(loc["snLenghtError"])
        sys.exit()
    
    return sn
    
def validate_year(year):
    current_year = datetime.now().year
    if year < 1900 or year > current_year:
        print(loc["invalidYearError"].format(current_year=current_year))
        sys.exit()

    return year

def validate_fine(fine):
    if fine < 0 or fine >= 10:
        print(loc["invalidFineError"].format(fine=fine))
        sys.exit()
    
    return fine

def validate_available_amount(available_amount, total_amount):
    if available_amount <= 0 or available_amount > total_amount:
        print(loc["invalidAvailableAmountError"].format(available_amount=loc["availableAmountField"]))
        sys.exit()

    return available_amount

def validate_name(name, field_name):
    validate_text(name, field_name)
    
    if len(name) > 30:
        print(loc["nameLenghtError"].format(field_name=field_name))
        sys.exit()
    
    if re.search(r"\b(DROP|DELETE|INSERT|UPDATE|SELECT|ALTER|TABLE)\b", name, re.IGNORECASE):
        print(loc["InvalidNameError"].format(field_name=field_name))
        sys.exit()
    
    if re.search(r"[^\p{L}\.\-'\s]", name):
        print(loc["InvalidCharacterError"].format(field_name=field_name))
        sys.exit()
    
    return name

def validate_condition(name):  
    name = name.strip().lower()
    language_variations = loc.get("localConditionVariations")

    if name in language_variations:
        return language_variations[name]
    else:
        print(loc["conditionError"])
        sys.exit()
