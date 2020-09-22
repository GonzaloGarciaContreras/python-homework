"""
Python script for analyzing the financial records of your company. 
Data entry --> budget_data.csv. 
    This dataset is composed of two columns, Date and Profit/Losses. 

Task is to create a Python script that analyzes the records 

1/ To calculate each of the following:

-The total number of months included in the dataset.
-The net total amount of Profit/Losses over the entire period.
-The average of the changes in Profit/Losses over the entire period.
-The greatest increase in profits (date and amount) over the entire period.
-The greatest decrease in losses (date and amount) over the entire period.

Financial Analysis
----------------------------
Total Months: 86
Total: $38382578
Average  Change: $-2315.12
Greatest Increase in Profits: Feb-2012 ($1926159)
Greatest Decrease in Profits: Sep-2013 ($-2196167)


2/ Print the analysis to the terminal and export a text file with the results.

"""
# Import
from pathlib import Path
import csv


#### Functions 

# The total number of months included in the dataset 
def f_nr_months(filepath):
    with open(filepath, "r") as csvfile:            # with statement auto. takes care of closing the file once it leaves the with block
        my_csvreader = csv.reader(csvfile)
        
        next(my_csvreader)                          #remove the column headers in cvs
        nr_months = len(list(my_csvreader))         #not including headers 
        str_nr_months = f"Total Months: {nr_months}"

    return str_nr_months


# The net total amount of Profit/Losses over the entire period.
def f_t_profit_losses(filepath):
    with open(filepath, "r") as csvfile:
        my_csvreader = csv.reader(csvfile)

        next(my_csvreader)  
        t_profit_losses = 0

        for row in my_csvreader:
            t_profit_losses += float (row[1])  

        str_t_profit_losses = f"Total Profit/Losses: {t_profit_losses}"

    return str_t_profit_losses


# The average of the changes in Profit/Losses over the entire period.
def f_avg_change(filepath):
    with open(filepath, "r") as csvfile:           
        my_csvreader = csv.reader(csvfile)
        next(my_csvreader)    

        nr_months = len(list(my_csvreader))         

    with open(filepath, "r") as csvfile:
        my_csvreader = csv.reader(csvfile)
        next(my_csvreader)  

        pl_prev_line = 0 
        compute = False 
        total_pl_gap = 0
        
        for row in my_csvreader:
            if compute == True: 
                pl_gap_line = float(row[1]) - pl_prev_line 
                total_pl_gap += pl_gap_line  
                pl_prev_line = float(row[1])
            else:
                pl_prev_line = float(row[1])
                total_pl_gap = 0
                compute = True 

        avg_change = round((total_pl_gap / (nr_months - 1)),2)
        str_avg_change = f"Average Change: {avg_change}"

    return str_avg_change


# The greatest increase in profits (date and amount) over the entire period
def f_greatest_increase(filepath):
    with open(filepath, "r") as csvfile:
        my_csvreader = csv.reader(csvfile)
        next(my_csvreader)  

        pl_prev_line = 0 
        first_period = True 
        greatest_increase_period = ""
        greatest_increase_pnl = 0
        
        for row in my_csvreader:
            if first_period == False: 
                pl_gap_line = round((float(row[1]) - pl_prev_line), 2) 
                if pl_gap_line > greatest_increase_pnl:
                    greatest_increase_period = row[0]
                    greatest_increase_pnl = pl_gap_line
                pl_prev_line = float(row[1])
            else:
                pl_prev_line = float(row[1])
                first_period = False

        str_greatest_increase = f"Greatest Increase in Profits: {greatest_increase_period} ${greatest_increase_pnl}"

    return str_greatest_increase


# The greatest decrease in losses (date and amount) over the entire period.
def f_greatest_decrease(filepath):
    with open(filepath, "r") as csvfile:
        my_csvreader = csv.reader(csvfile)
        next(my_csvreader)  

        pl_prev_line = 0 
        first_period = True 
        greatest_decrease_period = ""
        greatest_decrease_pnl = 0
        
        for row in my_csvreader:
            if first_period == False: 
                pl_gap_line = round((float(row[1]) - pl_prev_line), 2) 
                if pl_gap_line < greatest_decrease_pnl:
                    greatest_decrease_period = row[0]
                    greatest_decrease_pnl = pl_gap_line
                pl_prev_line = float(row[1])
            else:
                pl_prev_line = float(row[1])
                first_period = False

        str_greatest_decrease = f"Greatest Decrease in Profits: {greatest_decrease_period} ${greatest_decrease_pnl}"

    return str_greatest_decrease


# Export a text file with the results
def f_export_text_file (filepath, list_of_results):
    with open(filepath, "w") as file:
        for result in list_of_results:
            file.write(result + "\n")

    return 



#### Main

# Variables / Input Data
filepath = Path("../resources/budget_data.csv")
filepath_text = Path("../resources/results.txt")
list_of_functions = [f_nr_months, f_t_profit_losses, f_avg_change, f_greatest_increase, f_greatest_decrease]
list_of_results = []


# Calculate KPIs
for function in list_of_functions:
    result_func = function(filepath)
    print(result_func)
    list_of_results.append(result_func)

# Export KPIs to text file
f_export_text_file (filepath_text, list_of_results)




