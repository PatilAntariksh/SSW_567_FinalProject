import unittest
from MRTD import character_conversion, Luhn_Algo, Validating_MRZ, Defining_Errors

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
        expected_checksum = 3 
        self.assertEqual(Luhn_Algo(data), expected_checksum)
    
    def test_luhn_algo_correct_checksum2(self):           
        data = "Z23456789"  
        expected_checksum = 1  
        self.assertEqual(Luhn_Algo(data), expected_checksum)

    def test_luhn_algo_incorrect_checksum1(self):
        data = "K898902C4"   
        expected_checksum = 2
        self.assertNotEqual(Luhn_Algo(data), "Wrong Checksum",expected_checksum)

    def test_luhn_algo_incorrect_checksum2(self):
        data = "Q23423435"   
        expected_checksum = 1
        self.assertNotEqual(Luhn_Algo(data), "Wrong Checksum",expected_checksum)
        
    def test_defining_errors_all_match(self):
        line1 = "P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<"
        line2 = "L898902C33UTO7408121F1204155ZE184226B<<<<<<6"
        given_data = {
        "passport_number": "L898902C3",  # Check digit '6'
        "birth_date": "740812",          # Check digit '2'
        "expiration_date": "120415",     # Check digit '9'
        "personal_number": "ZE184226B",  # Check digit '1'
        "last_name": "ERIKSSON",
        "first_name": "ANNA MARIA",
        "line2": line2
    }
        self.assertEqual(Defining_Errors(line1, line2, given_data), "All fields match and check digits are valid.")


    def test_defining_errors_all_match2(self):
        line1 = "P<CANJONES<<SARAH<WILLIAM<<<<<<<<<<<<<<<<<<<"
        line2 = "E987654289CAN8607157F2707155Z1234567B<<<<<<2"
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

    

    def test_defining_errors_danger(self):
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

    def test_defining_errors_moderate(self):
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
