import re
import json
import time
import pandas as pd
import matplotlib.pyplot as plt

input_file = "C:\\Users\\Kavita Patil\\Desktop\\SEM 3 Stevens\\SSW567\\Testing\\SSW_567_Project\\MRTDAPP"
def character_conversion(character):
    if character == '<':
        return 0
    if '0' <= character <= '9':  # checking for digits, returning as is as o converison required
        return int(character)
    if 'A' <= character <= 'Z':  # checking for charachters through A to Z, and converting to the value format asked.
        return ord(character) - 55
    print(f"Invalid MRZ character: {character}")
    return None  #for invalid characters

def Luhn_Algo(data):
    total = 0
    reverse_data = data[::-1]  #Reversing whole string
    for i, char in enumerate(reverse_data):
        value = character_conversion(char)
        if value is None:
            print(f"Invalid character in data: {char}")
            return None
        if i % 2 == 0: #Since LUHN follows (2,1,2,1,..)
            value *= 2
            while value > 9:
                value -= 9     
        total += value
    return total % 10 #mod 10 of final ans is the checksum

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
    sex = line2[20]
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

def Results(input_file, output_file):
    with open(input_file, 'r') as input_f:
        data = json.load(input_f)['records_decoded']
    encoded = [Encodingdatas(record) for record in data]
    with open(output_file, 'w') as output_f:
        json.dump({"records_encoded": encoded}, output_f)

def TimerforExecution(input_file, Timing_data):
    with open(input_file, 'r') as input:
        datas = json.load(input)['records_decoded']
    results = []
    batchSize = [100, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    for n in batchSize:
        subset = datas[:n]
        Timer1 = time.perf_counter()                            #For Time calculation of execution without test cases
        for data in subset:
            Encodingdatas(data)
        time_without_tests = time.perf_counter()-Timer1

        Timer2 = time.perf_counter()                            #For Time calculation of execution with test cases
        for data in subset:
            encoded_line = Encodingdatas(data)
        assert len(encoded_line.split(';')[0]) ==44, "Line1 is not 44 characters"
        assert len(encoded_line.split(';')[1]) ==44, "Line2 is not 44 characters"
        assert encoded_line.split(';')[1][9] ==str(Luhn_Algo(data['line2']['passport_number'])), "Error in Passport checksum"
        assert encoded_line.split(';')[1][19]== str(Luhn_Algo(data['line2']['birth_date'])), "Error in Birth date checksum"
        assert encoded_line.split(';')[1][27]== str(Luhn_Algo(data['line2']['expiration_date'])), "Error in Expiration date checksum"
        assert encoded_line.split(';')[1][43] ==str(Luhn_Algo(data['line2']['personal_number'])), "Erorr in Personal number checksum"
        assert encoded_line.split(';')[0][2:5] == data['line1']['issuing_country'], "Error in name of the Issuing country"
        assert encoded_line.split(';')[1][13:19] == data['line2']['birth_date'], "Birth date error in Line2"
        assert data['line2']['sex'] in ['M', 'F'], "Gender should be either 'M' or 'F'"
        time_with_tests = time.perf_counter() - Timer2
        results.append((n, time_without_tests, time_with_tests))
        print(f"for {n} records: Time wihout Tets = {time_without_tests:} seconds, Time With Tests = {time_with_tests:} seconds")

        df = pd.DataFrame(results, columns=["No of lines", "Time for No tests", "Time including testing"])
        df.to_excel(Timing_data, index=False)

def plot_execution_times(Timing_data, Results):
    df = pd.read_excel(Timing_data)
    plt.plot(df['No of lines'], df['Time for No tests'], label='Without Tests', marker='.', color='red')
    plt.plot(df['No of lines'], df['Time including testing'], label='With Tests', marker='.', color='green')

    batchSize = [0, 100, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    plt.xticks(batchSize)
    
    plt.xlabel('Batch Size')
    plt.ylabel('Time for execution')
    plt.title('Results Graph')
    plt.legend()
    plt.savefig(Results)
    plt.show()

if __name__ == "__main__":
    input_file = "records_decoded.json"
    output_file = "encoded_records.json"
    Results(input_file,output_file)
    Timing_data = "Timing.xlsx"  
    Results = "ResultsGraph.png"  
    TimerforExecution(input_file, Timing_data)
    plot_execution_times(Timing_data,Results)