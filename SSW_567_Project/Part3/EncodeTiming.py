import json
import time
import pandas as pd
from MRTD import Luhn_Algo
from EncodingRecord import Encodingdatas 
import matplotlib.pyplot as plt

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
    Timing_data = "Timesheet.xlsx"  
    Results = "ResultsFinal.png"  
    TimerforExecution(input_file, Timing_data)
    plot_execution_times(Timing_data,Results)