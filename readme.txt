Title: Script for data processing

User should mention the exact source path in the "src" variable, initial and the final date (format: YYYY, M/MM, D/DD).
M - single digit (0 - 9), MM - double digit (10 - 12). Similarly for the date.

The productID's for which instrumentID is not defined in the "prod_info.csv file" would be stored in a file "logfile.txt"

One has to make sure that the file name must have a date in the format "YYYY.MM.DD", "." (dot) is very important.
Otherwise, that file will not be processed and skipped with error "Some error in the try block for the file No. # has occured"

When script runs succesfully, one target file "targetfile.csv" will be generated with the header columns
(['Instrument_ID', 'Expiration_Date', 'loc_time_stamp', 'days_to_maturity', 'price', 'volume', 'Underlying_price') followed by the data.