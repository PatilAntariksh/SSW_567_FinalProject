import re
def character_conversion(character):
    if character == '<':
        return 0
    if '0' <= character <= '9': #checking for digits, no converstion required
        return int(character)
    if 'A' <= character <= 'Z': #checking for charachters through,converting in asked format
        return ord(character) - 55
    print(f"Invalid MRZ character: {character}")
    return None  #for invalid characters
def luhn_algo(data_g):
    weights = [7,3,1,7,3,1]   #ICAO pattern of weights specifically for passports MRZ.
    checksum = 0
    for i, char in enumerate(data_g):
        value = character_conversion(char)
        checksum += value * weights[i % 3]
    return checksum % 10
def validate_MRZ(line1, line2):
    pattern = r"^[A-Z0-9<]{44}$"
    if not re.match(pattern, line1):
        print ("Error: Line 1 format is invalid. Human intervention required.")
    if not re.match(pattern, line2):
        print ("Error: Line 2 format is invalid. Human intervention required.")
    return "Valid MRZ format"
def defining_errors(line1,line2,data_g):
    if len(line1) != 44 or len(line2) != 44:
        print("Error: Each MRZ line should be exactly 44 characters long.")
        return
    name_section = line1[5:].split("<<")
    last_name = name_section[0].replace("<", " ")
    first_name = name_section[1].replace("<", " ") if len(name_section) > 1 else ""
    p_number = line2[0:9]          #From Line2
    passport_check_digit = int(line2[9])
    b_date = line2[13:19]
    b_date_check_digit = int(line2[19])
    e_date = line2[21:27]
    e_date_check_digit = int(line2[27])
    personal_number = line2[28:37]
    personal_number_check_digit = int(line2[43])
#    Defining Errors
    p_error=p_number!=data_g.get("p_number") or luhn_algo(p_number)!=passport_check_digit
    b_error=b_date!=data_g.get("b_date") or luhn_algo(b_date)!=b_date_check_digit
    e_date_error=e_date!=data_g.get("e_date") or luhn_algo(e_date)!=e_date_check_digit
    pers_number_err=personal_number!=data_g.get("personal_number") or luhn_algo(personal_number)!=personal_number_check_digit
    name_error=last_name!=data_g.get("last_name") or first_name!=data_g.get("first_name")
    # Classify errors based on the type and number of mismatches
    if p_error and b_error and e_date_error and pers_number_err and name_error:
        print("Danger: None of the fields match.")
    if name_error:
        print("Moderate: Spelling differences in Name.")
    if p_error:
        print ("Low: Passport number or its check digit does not match.")
    if b_error:
        return "Low: Birth date or its check digit does not match."
    if e_date_error:
        return "Low: Expiration date or its check digit does not match."
    if pers_number_err:
        return "Low: Personal number or its check digit does not match."
    return "All fields match and check digits are valid."