Title: Script for data processing

User should mention the exact source path in the "src" variable, initial and the final date (format: YYYY, M/MM, D/DD).
M - single digit (0 - 9), MM - double digit (10 - 12). Similarly for the date.

Regarding unzipping a file, code extract the main zip file to the defined "X" location (folder named "Data" would be saved) and then again extracts the sub zip files present in "X" location (zip files present in the "Data" folder) and stores it in defined "Y" location (all the csv files would be saved).

For data processing, location of "Y" must be the source path. Once data processing has been done, "Y" directory would be automatically deleted.

The productID's for which instrumentID is not defined in the "prod_info.csv file" would be stored in a file "logfile.txt"

The instrumentID for the unknown category would be stored in a file "unknownCategoryFile.txt"

When script runs succesfully, one target file "targetfile.csv" will be generated with the header columns
(['Instrument_ID', 'Expiration_Date', 'loc_time_stamp', 'days_to_maturity', 'price', 'volume', 'Underlying_price') followed by the data.
