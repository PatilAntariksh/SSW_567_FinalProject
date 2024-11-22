import unittest
from updated_mrtd import character_conversion, Luhn_Algo, Validating_MRZ, Defining_Errors

class TestMRZFunctions(unittest.TestCase):
    
    def test_character_conversion(self):                 #Testing for correct conversion
        self.assertEqual(character_conversion('A'), 10)  
        self.assertEqual(character_conversion('Z'), 35)  
        self.assertEqual(character_conversion('5'), 5)    
        self.assertEqual(character_conversion('<'), 0)   

    def test_character_conversionI1(self):                 #Printing Invalid Input
        self.assertIsNone(character_conversion('*'), "None for invalid character")
    def test_character_conversionI2(self):                 #Printing Invalid Input
        self.assertIsNone(character_conversion('#'), "None for invalid character")
    def test_character_conversionI3(self):                 #Printing Invalid Input
        self.assertIsNone(character_conversion('/'), "None for invalid character")
        
    def test_luhn_algo_correct_checksum1(self):           
        data = "L898902C3"  
        expected_checksum = 2 
        self.assertEqual(Luhn_Algo(data), expected_checksum)
    
    def test_luhn_algo_correct_checksum2(self):           
        data = "Z23456789"  
        expected_checksum = 8  
        self.assertEqual(Luhn_Algo(data), expected_checksum)

    def test_luhn_algo_incorrect_checksum1(self):
        data = "K898902C4"   
        expected_checksum = 2
        self.assertNotEqual(Luhn_Algo(data), "Wrong Checksum",expected_checksum)

    def test_luhn_algo_incorrect_checksum2(self):
        data = "Q23423435"   
        expected_checksum = 1
        self.assertNotEqual(Luhn_Algo(data), "Wrong Checksum",expected_checksum)
        
    def test_validating_mrz_correct_format(self):
        line1 = "P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<"     #Killed Mutants
        line2 = "L898902C36UTO7408122F1204159ZE184226B<<<<<<1"
        self.assertEqual(Validating_MRZ(line1, line2), "Valid MRZ format")

    def test_validating_mrz_incorrect_format(self):
        line1 = "P<UTOERIKSSON<<ANNA<<<<<<<<<<<<<<<<<<<<<<<<"       # Killed Mutants
        line2 = "L898902C36UTO7408122F1204159ZE184226B<<<1"  
        self.assertEqual(Validating_MRZ(line1, line2), "Error: Line 1 format is invalid. Human intervention required.")
    
    def test_defining_errors_all_match(self):
        line1 = "P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<"
        line2 = "L898902C32UTO7408127F1204155ZE184226B<<<<<<5"
        given_data = {
        "passport_number": "L898902C3",  
        "birth_date": "740812",          
        "expiration_date": "120415",    
        "personal_number": "ZE184226B", 
        "last_name": "ERIKSSON",
        "first_name": "ANNA MARIA",
        "line2": line2
    }
        self.assertEqual(Defining_Errors(line1, line2, given_data), "All fields match and check digits are valid.")


    def test_defining_errors_all_match2(self):
        line1 = "P<CANJONES<<SARAH<WILLIAM<<<<<<<<<<<<<<<<<<<"
        line2 = "E987654289CAN8607158F2707154Z1234567B<<<<<<2"
        given_data = {
        "passport_number": "E98765428",
        "birth_date": "860715",
        "expiration_date": "270715",
        "personal_number": "Z1234567B",
        "last_name": "JONES",
        "first_name": "SARAH WILLIAM",
        "line2": line2
        }
        self.assertEqual(Defining_Errors(line1, line2, given_data), "All fields match and check digits are valid.")

    

    def test_defining_errors_danger1(self):
        line1 = "P<UTOERIKSSON<<JOHN<DOE<<<<<<<<<<<<<<<<<<<<<"
        line2 = "L111111111UTO1111111F1111119ZE111111A<<<<<<0"
        given_data = {
            "passport_number": "L898902C3",
            "birth_date": "740812",
            "expiration_date": "120415",
            "personal_number": "ZE184226B",
            "last_name": "ERIKSSON",
            "first_name": "ANNA MARIA",
            "line2": "L898902C36UTO7408122F1204159ZE184226B<<<<<1"
        }
        
        self.assertEqual(Defining_Errors(line1, line2, given_data), "Danger: None of the fields match.")

    def test_defining_errors_danger2(self):
        line1 = "P<UTOERIKSSON<<ANNA<<<<<<<<<<<<<<<<<<<<<<<<<"
        line2 = "L898902C36UTO7408122F1204159ZE184226B<<<<<<1"
        given_data = {
            "passport_number": "L898902C3",
            "birth_date": "740812",
            "expiration_date": "120415",
            "personal_number": "ZE184226B",
            "last_name": "ERIKSSON",
            "first_name": "ANNA MARIA", 
            "line2": line2
        }
        self.assertEqual(Defining_Errors(line1, line2, given_data), "Danger: None of the fields match.")

    def test_defining_errors_moderate(self):
        line1 = "P<CANJONES<<SARAH<WILLIAM<<<<<<<<<<<<<<<<<<<"
        line2 = "E987654289CAN8607157F2707155Z1234567B<<<<<<2"
        given_data = {
        "passport_number": "E98765428",
        "birth_date": "860715",
        "expiration_date": "270715",
        "personal_number": "Z1234567B",
        "last_name": "JONES",
        "first_name": "SARAH",
        "line2": line2
        } 
        self.assertEqual(Defining_Errors(line1, line2, given_data), "Moderate: Spelling differences in Name.")
    

    def test_defining_errors_low_severity(self):
        line1 = "P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<"
        line2 = "L898902C36UTO7408122F1204159ZE184226B<<<<<<1"
        given_data = {
            "passport_number": "L12345678",  
            "birth_date": "740812",
            "expiration_date": "120415",
            "personal_number": "ZE184226B",
            "last_name": "ERIKSSON",
            "first_name": "ANNA MARIA",
            "line2": line2
        }
        
        self.assertEqual(Defining_Errors(line1, line2, given_data), "Low: Passport number or its check digit does not match.")

    

if __name__ == '__main__':
    unittest.main()
