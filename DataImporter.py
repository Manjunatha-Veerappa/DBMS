from datetime import datetime
from datetime import date, timedelta
import os
import re
import csv
import zipfile
import shutil

class Importer:
    row=[]

    def __init__(self, begin_date, end_date):
        self.begin_date = begin_date
        self.end_date = end_date

    # Expiration date calculation for Index futures
    def index(self, dat):
        while dat.weekday() != 4:
            dat = dat + timedelta(days=1)
        date = self.trading_holidays(dat)
        return date

    # Expiration date calculation for Money Market futures (EURIBOR)
    def euribor(self, dat):
        while (dat.weekday() != 2):
            dat = dat + timedelta(days=1)
        dat = dat - timedelta(days=2)
        date = self.trading_holidays(dat)
        return date

    # Expiration date calculation for Money Market futures (Eonia and EUR secured category)
    def eoniaAndEurSecured(self, month, year):
        o_eonia = open('EoniaAndEurSecuredExp_Dates.csv', 'r')
        reader = csv.reader(o_eonia)
        for roww in reader:
            if(roww[0] == month and roww[1] == year):
                break
        dat_obj = datetime.datetime.strptime(roww[2], "%Y.%m.%d")
        o_eonia.close()
        return dat_obj

    # Expiration date calculation for FixedIncome futures
    def fixedIncome(self, dat):
        while dat.weekday() >= 5:
            dat = dat + timedelta(days=1)
        date = self.trading_holidays(dat)
        return date

    # Expiration date calculation for Single stock futures
    def singleStock(self, dat):
        while dat.weekday() != 4:
            dat = dat + timedelta(days=1)
        date = self.trading_holidays(dat)
        return date

    # Expiration date calculation for Forex futures
    def forex(self, dat):
        while dat.weekday() != 2:
            dat = dat + timedelta(days=1)
        date = self.trading_holidays(dat)
        return date

    # Expiration date calculation for Index Dividends futures
    def indexDividend(self, dat):
        while dat.weekday() != 4:
            dat = dat + timedelta(days=1)
        date = self.trading_holidays(dat)
        return date

    # Expiration date calculation for Single Stock Dividends futures
    def singleStockDividend(self, dat):
        while dat.weekday() != 4:
            dat = dat + timedelta(days=1)
        date = self.trading_holidays(dat)
        return date

    # Expiration date calculation for Volatility futures (VSTOXX)
    def volatilityVSTOXX(self, dat):
        while dat.weekday() != 4:
            dat = dat + timedelta(days=1)
        dat = dat - timedelta(days=30)
        while dat.weekday() >= 5:
            dat = dat - timedelta(days=30)
        date = self.trading_holidays(dat)
        return date

    # Expiration date calculation for Volatility futures (Variance)
    def volatilityVariance(self, c, d):
        while dat.weekday() != 4:
            dat = dat + timedelta(days=1)
        date = self.trading_holidays(dat)
        return date

    # Trading holidays
    def trading_holidays(self, dat):
        dat_str = dat.strftime("%Y-%m-%d")                              # convert the date object into a data string   
        o_trad_holidays = open('trading_holidays.csv', 'r')             # open the trading holidays file in a read mode
        reader = csv.reader(o_trad_holidays)
        for row in reader:
            if (dat_str == row[0]):                                     # Checks if the date matches with the date in the csv file
                break
        import datetime
        dat_obj = datetime.datetime.strptime(dat_str, "%Y-%m-%d").date()      # convert the date string into an object  
        datetime_obj = datetime.datetime.combine(dat_obj, datetime.time())    # convert date object into a datetime object
        datetime_obj = datetime_obj - timedelta(int(row[1]))                  # To allot the preceding working trading date
        return datetime_obj

    #Arranging the data in the particular order and delete the unwanted rows
    def sorter(self):
        row[2] = row[18]
        row[4] = row[13]
        row[5] = row[14]
        del row[6:20]

#Main starts from here
src = "E:\Importer"                                    # Main source Path
dst_data = 'E:\Files'                                  # A path to store the data folder unzipped from the zip file.
dst_csv_files = "E:\csv_files"                         # A path to store all the csv files unzipped from the zip files present in the data folder

init_date = date(2016, 1, 10)                          # To be chosen by the user (year, month, day)
finl_date = date(2017, 2, 2)                           # To be chosen by the user (year, month, day)

o_targetfile = open('targetfile.csv', 'w', newline="")                    # one target file per month
writer = csv.writer(o_targetfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
writer.writerow(['Instrument_ID', 'Expiration_Date', 'loc_time_stamp', 'days_to_maturity', 'price', 'volume', 'Underlying_price']) # 1st row of the target fiel

o_txtfile = open("logfile.txt",'w')                      # logfile to store the productID's where instrumentID is not defined in the prod_info.csv file

o_unknown_cat = open("unknownCategoryFile.txt",'w')      # unknownCategoryFile to store the instrument ID if the category is not defined in the above class

object = Importer(init_date, finl_date)

# To unzip the main zipped file (also the sub zipped files residing in the main zipped file).
for root, dirs, files in os.walk(src):
    print("Unzipping all the files one by one present in the source path........... \n")
    for file1 in files:
        print ("Unzipping the main zipped file:", file1)
        zip = zipfile.ZipFile(src + "\\" + file1)
        zip.extractall(dst_data)
        for root, dirs, files in os.walk(dst_data):
            for file2 in files:
                source2 = os.path.join(root, file2)
                print("Unzipping the sub zipped file:", source2)
                zip = zipfile.ZipFile(source2)
                zip.extractall(dst_csv_files)
print("\n")

for root, dirs, files in os.walk(dst_csv_files):
    print ("Data processing has been started............ \n")
    for file in files:
        source = os.path.join(root,file)
        print (source)
        numbers = re.findall(r'\d+', source)                           # Search for the 8 digits in the filename and store it in the numbers list
        num_string = numbers[0]                                        # Parse the string from the numbers list
        date_str = (num_string[0:4] + "." + num_string[4:6] + "." + num_string[6:8]) # Arrange the string to the format yyyy.mm.dd
        try:
            print(date_str)
            import datetime
            date_obj = datetime.datetime.strptime(date_str, "%Y.%m.%d").date()      # convert the date string into an object
 
            if (date_obj):
                if(date_obj >= object.begin_date and date_obj <= object.end_date):  # compare the extracted date with the specified data range
                    o_file = open(source, 'r')
                    reader = csv.reader(o_file, delimiter=';')
                    for row in reader:
                        if (row[1] == "F"):                                         # Filter out futures by call_put_flag == "F"
                            row[18] = row[18] + ":" + row[19]                       # To get the loctimestamp (mm/dd/yyyy hh:mm:ss:mmm)
                            import datetime

                            loc_time_stamp = datetime.datetime.strptime(row[18], "%m/%d/%Y %H:%M:%S:%f").strftime("%Y.%m.%d")  # convert date into a format yyyy.mm.dd
                            loc_time_stamp_obj = datetime.datetime.strptime(loc_time_stamp, "%Y.%m.%d")  # date string to date object conversion

                            approx_expiration_date = row[3] + "." + row[2] + ".15"
                            import datetime
                            approx_expiration_date_object = datetime.datetime.strptime(approx_expiration_date, "%Y.%m.%d")

                            o_prodspec = open('product_info.csv', 'r')
                            reader1 = csv.reader(o_prodspec)
                            for row1 in reader1:
                                if (row[0] == row1[0]):                     # To find the instrumentID for the corresponding productID
                                    row[0] = row1[1]
                                    break
                            if (len(row[0]) < 5):                          # Checks if the length of the id is < 5 or not, if yes, No instrument ID for that
                                o_txtfile.write(row[0] + "\n")               # productID. Hence save that productID in a logfile for the future reference
                            else:
                                # writing the required data(I_ID, Exp_date, timestamp, Days_to_maturity, price, volume) by deleting the unwanted rows for the Index futures
                                if (row1[3] == "index"):
                                    row[1] = object.index(approx_expiration_date_object)       # Call the Index function to get the expiration date
                                    row[3] = row[1] - loc_time_stamp_obj            # Expiration date - loc_time_stamp = Number of days remaining for the expiration
                                    object.sorter()
                                    writer.writerow(row)

                                # writing the required data(I_ID, Exp_date, timestamp, Days_to_maturity, price, volume) by deleting the unwanted rows for the Money Market futures
                                elif (row1[3] == "money market"):
                                    if (row[0] == "DE0007201535"):                   # Checks for the EONIA futures category
                                        row[1] = object.eoniaAndEurSecured(row[2], row[3])  # Call the Eonia function to get the expiration date
                                        row[3] = row[1] - loc_time_stamp_obj         # Expiration date - loc_time_stamp = Number of days remaining for the expiration
                                        object.sorter()
                                        writer.writerow(row)

                                    elif (row[0] == "DE000A1YD7E8"):                 # Checks for the EUR secured funding futures category
                                        row[1] = object.eoniaAndEurSecured(row[2, row[3]])  # Call the EurSecured function to get the expiration date
                                        row[3] = row[1] - loc_time_stamp_obj         # Expiration date - loc_time_stamp = Number of days remaining for the expiration
                                        object.sorter()
                                        writer.writerow(row)
                                    else:
                                        row[1] = object.euribor(approx_expiration_date_object)   # Call the Euribor function to get the expiration date
                                        row[3] = row[1] - loc_time_stamp_obj         # Expiration date - loc_time_stamp = Number of days remaining for the expiration
                                        object.sorter()
                                        writer.writerow(row)

                                # writing the required data(I_ID, Exp_date, timestamp, Days_to_maturity, price, volume) by deleting the unwanted rows for the Single Stock futures
                                elif (row1[3] == "single stock"):
                                    row[1] = object.singleStock(approx_expiration_date_object)  # Call the SingleStock function to get the expiration date
                                    row[3] = row[1] - loc_time_stamp_obj             # Expiration date - loc_time_stamp = Number of days remaining for the expiration
                                    object.sorter()
                                    writer.writerow(row)

                                # writing the required data(I_ID, Exp_date, timestamp, Days_to_maturity, price, volume) by deleting the unwanted rows for the Fixed Income futures
                                elif (row1[3] == "fixed income"):
                                    approx_exp_date_fix_income = row[3] + "." + row[2] + ".10"
                                    approx_exp_date_fix_income_obj = datetime.datetime.strptime(approx_exp_date_fix_income, "%Y.%m.%d")
                                    row[1] = object.fixedIncome(approx_exp_date_fix_income_obj)  # Call the FixedIncome function to get the expiration date
                                    row[3] = row[1] - loc_time_stamp_obj             # Expiration date - loc_time_stamp = Number of days remaining for the expiration
                                    object.sorter()
                                    writer.writerow(row)

                                # writing the required data(I_ID, Exp_date, timestamp, Days_to_maturity, price, volume) by deleting the unwanted rows for the Forex futures
                                elif (row1[3] == "forex"):
                                    row[1] = object.forex(approx_expiration_date_object)       # Call the Forex to get the expiration date
                                    row[3] = row[1] - loc_time_stamp_obj            # Expiration date - loc_time_stamp = Number of days remaining for the expiration
                                    object.sorter()
                                    writer.writerow(row)

                                # writing the required data(I_ID, Exp_date, timestamp, Days_to_maturity, price, volume) by deleting the unwanted rows for the Index Dividends futures
                                elif (row1[3] == "dividends index"):
                                    approx_exp_date_div_index = row[3] + ".12" + ".15"
                                    approx_exp_date_div_index_obj = datetime.datetime.strptime(approx_exp_date_div_index, "%Y.%m.%d")
                                    row[1] = object.indexDividend(approx_exp_date_div_index_obj)  # Call the IndexDividend function to get the expiration date
                                    row[3] = row[1] - loc_time_stamp_obj            # Expiration date - loc_time_stamp = Number of days remaining for the expiration
                                    object.sorter()
                                    writer.writerow(row)

                                # writing the required data(I_ID, Exp_date, timestamp, Days_to_maturity, price, volume) by deleting the unwanted rows for the Single Stock Dividends futures
                                elif (row1[3] == "dividends single stock"):
                                    approx_exp_date_div_index = row[3] + ".12" + ".15"
                                    approx_exp_date_div_index_obj = datetime.datetime.strptime(approx_exp_date_div_index, "%Y.%m.%d")
                                    row[1] = object.singleStockDividend(approx_exp_date_div_index_obj)  # Call the SingleStockDividend function to get the expiration date
                                    row[3] = row[1] - loc_time_stamp_obj            # Expiration date - loc_time_stamp = Number of days remaining for the expiration
                                    object.sorter()
                                    writer.writerow(row)

                                # writing the required data(I_ID, Exp_date, timestamp, Days_to_maturity, price, volume) by deleting the unwanted rows for the Volatility futures
                                elif (row1[3] == "volatility"):
                                    row[1] = object.volatilityVSTOXX(approx_expiration_date_object)  # Call the VolatilityVSTOXX function to get the expiration date
                                    row[3] = row[1] - loc_time_stamp_obj                  # Expiration date - loc_time_stamp = Number of days remaining for the expiration
                                    object.sorter()
                                    writer.writerow(row)

                                else:
				    o_unknown_cat.write(row[0] + "\n")                     # Store the instrument ID for the future reference
                                    print("There are some different categories which have not been included")

                    o_prodspec.close()
                    o_file.close()
                    print("Processing of the file",source,"has been sucessfully completed")
                else:
                    print("File",source,"is not in the user mentioned data range")
        except ():
            print("Some error in the try block for the file", source,"has occured")
            pass

shutil.rmtree(dst_csv_files)                 # To completely remove the csv_files directory

