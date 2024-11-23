import json
from MRTD import character_conversion, Luhn_Algo

input = "C:\\Users\\Kavita Patil\\Desktop\\SEM 3 Stevens\\SSW567\\Testing\\SSW_567_Project\\records_decoded.json"
output = "C:\\Users\\Kavita Patil\\Desktop\\SEM 3 Stevens\\SSW567\\Testing\\SSW_567_Project\\records_encoded.json"

def Results(input, output):
    with open(input, 'r') as input:
        data = json.load(input)['records_decoded']
    encoded = [Encodingdatas(data) for data in data]
    with open(output, 'w') as output:
        json.dump(encoded, output)

def Encodingdatas(data):
    issuing_country = data['line1']['issuing_country']
    last_name = data['line1']['last_name'].upper().replace(" ", "<")
    given_name = data['line1']['given_name'].upper().replace(" ", "<")
    line1 = (f"P<{issuing_country}{last_name}<{given_name}")  
    line1 += "<" * (44 - len(line1))
    


    passport_number = data['line2']['passport_number']
    passport_check_digit = Luhn_Algo(passport_number)
    country_code = data['line2']['country_code']
    birth_date = data['line2']['birth_date']
    birth_date_check_digit = Luhn_Algo(birth_date)
    sex = data['line2']['sex']
    expiration_date = data['line2']['expiration_date']
    expiration_date_check_digit = Luhn_Algo(expiration_date)
    personal_number = data['line2']['personal_number']
    personal_number_check_digit = Luhn_Algo(personal_number)
    line2 = (f"{passport_number}{passport_check_digit}{country_code}"f"{birth_date}{birth_date_check_digit}{sex}"f"{expiration_date}{expiration_date_check_digit}{personal_number}")
    line2 += "<" * (43 - len(line2))
    line2 += str(personal_number_check_digit)
    return f"{line1};{line2}"

if __name__ == "__main__":
    Results(input, output)
    print("Encoded file is saved in Software Testing Final project folder")