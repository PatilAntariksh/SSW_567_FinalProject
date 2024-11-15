import re

def character_conversion(character):
    if character == '<':
        return 0
    if '0' <= character <= '9':  # checking for digits, returning as is as o converison required
        return int(character)
    if 'A' <= character <= 'Z':  # checking for charachters through A to Z, and converting to the value format asked.
        return ord(character) - 55
    print(f"Invalid MRZ character: {character}")
    return None  #for invalid characters

def Luhn_Algo(given_data):
    weights = [7,3,1,7,3,1]   #ICAO pattern of weights specifically for passports MRZ.
    checksum = 0
    for i, char in enumerate(given_data):
        value = character_conversion(char)
        checksum += value * weights[i % 3]
    return checksum % 10

def Validating_MRZ(line1, line2):
    pattern = r"^[A-Z0-9<]{44}$"
    if not re.match(pattern, line1):
        return "Error: Line 1 format is invalid. Human intervention required."
    if not re.match(pattern, line2):
        return "Error: Line 2 format is invalid. Human intervention required."
    return "Valid MRZ format"

def Defining_Errors(line1, line2, given_data):
    if len(line1) != 44 or len(line2) != 44:
        print("Error: Each MRZ line should be exactly 44 characters long.")
        return

    document_type = line1[0]               #From Line1
    issuing_country = line1[2:5]
    name_section = line1[5:].split("<<")
    last_name = name_section[0].replace("<", " ")
    first_name = name_section[1].replace("<", " ") if len(name_section) > 1 else ""
    
    passport_number = line2[0:9]          #From Line2
    passport_check_digit = int(line2[9])
    nationality = line2[10:13]
    birth_date = line2[13:19]
    birth_date_check_digit = int(line2[19])
    gender = line2[20]
    expiration_date = line2[21:27]
    expiration_date_check_digit = int(line2[27])
    personal_number = line2[28:37]
    personal_number_check_digit = int(line2[43])



#    Defining Errors
    passport_error = passport_number != given_data.get("passport_number") or Luhn_Algo(passport_number) != passport_check_digit
    birth_date_error = birth_date != given_data.get("birth_date") or Luhn_Algo(birth_date) != birth_date_check_digit
    expiration_date_error = expiration_date != given_data.get("expiration_date") or Luhn_Algo(expiration_date) != expiration_date_check_digit
    personal_number_error = personal_number != given_data.get("personal_number") or Luhn_Algo(personal_number) != personal_number_check_digit
    name_error = last_name != given_data.get("last_name") or first_name != given_data.get("first_name")

    # Classify errors based on the type and number of mismatches
    if passport_error and birth_date_error and expiration_date_error and personal_number_error and name_error:
        return "Danger: None of the fields match."
    elif name_error:
        return "Moderate: Spelling differences in Name."
    elif passport_error:
        return "Low: Passport number or its check digit does not match."
    elif birth_date_error:
        return "Low: Birth date or its check digit does not match."
    elif expiration_date_error:
        return "Low: Expiration date or its check digit does not match."
    elif personal_number_error:
        return "Low: Personal number or its check digit does not match."
    
    else:
     return "All fields match and check digits are valid."