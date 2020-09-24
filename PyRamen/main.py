"""
Analyze how well your business did on a per-product basis (as you have several choices of ramen) in order to better understand which products are doing well, which are doing poorly, and, ultimately, which products may need to be removed or changed.

1/ Read the Data
-Read in menu_data.csv and set its contents to a separate list object. 
    Initialize an empty menu list object to hold the contents of menu_data.csv.
    Use a with statement and open the menu_data.csv by using its file path.
    Use the reader function from the csv library to begin reading menu_data.csv.
    Use the next function to skip the header (first row of the CSV).
    Loop over the rest of the rows and append every row to the menu list object (the outcome will be a list of lists).
-Set up the same process to read in sales_data.csv. 
    -However, instead append every row of the sales data to a new sales list object.

2/ Manipulate the Data
    -Initialize an empty report dictionary to hold the future aggregated per-product results. 
    The report dictionary will eventually contain the following metrics:
        01-count: the total quantity for each ramen type
        02-revenue: the total revenue for each ramen type
        03-cogs: the total cost of goods sold for each ramen type
        04-profit: the total profit for each ramen type
    -Then, loop through every row in the sales list object.
        For each row of the sales data, set the following columns of the sales data to their own variables:
            Quantity
            Menu_Item
        Perform a quick check if the sales_item is already included in the report. 
        If not, initialize the key-value pairs for the particular sales_item in the report. 
        Then, set the sales_item as a new key to the report dictionary and the values as a nested dictionary containing the following:
                {
                "01-count": 0,
                "02-revenue": 0,
                "03-cogs": 0,
                "04-profit": 0,
                }
    -Create a nested loop by looping through every record in menu.
    For each row of the menu data, set the following columns of the menu data to their own variables:
                Item, Price, Cost
    If the sales_item in sales is equal to the item in menu, capture the quantity from the sales data and the price and cost from the menu data to calculate the profit for each item.
    Cumulatively add the values to the corresponding metrics in the report like so:
    Else print the message "{sales_item} does not equal {item}! NO MATCH!".

3/ Write out the contents of the report dictionary to a text file. 

"""

# Import libraries
import csv
from pathlib import Path

# Set file paths for menu_data.csv and sales_data.csv
menu_filepath = Path('../resources/menu_data.csv')
sales_filepath = Path('../resources/sales_data.csv')

# Initialize list objects to hold our menu and sales data
menu_list = []
sales_list = []


# functions 
# read menu csv file into a menu list 
def f_read_menu(filepath):
    with open(filepath, "r") as csvfile:
        my_csvreader = csv.reader(csvfile)
        next(my_csvreader)  

        # Pass reader object to list() to get a list of lists
        menu_list = list(my_csvreader)
        
    return menu_list

# as it is a large file, get number of rows in sales for a sanity check  (to compare # rows and items in the list)
def f_nr_rec_sales(filepath):
    with open(filepath, "r") as csvfile:           
        my_csvreader = csv.reader(csvfile)
        next(my_csvreader)  

        nr_rec_sales = len(list(my_csvreader))    

    return nr_rec_sales 

# read sales into a list by using append method 
def f_read_sales(filepath):
    with open(filepath, "r") as csvfile:
        my_csvreader = csv.reader(csvfile)
        next(my_csvreader)  

        # append row to menu1_list Pass reader object to list() to get a list of lists
        for row in my_csvreader:
            sales_list.append(row)

    return sales_list

# export report dic into a text file 
def f_export_text_file (filepath, results):
    with open(filepath, "w") as file:
        for result in results:
            str_record = f"{result} {results[result]} \n"
            file.write(str_record)

    return 



# 1- Read Data

# Read in the menu data into the menu list (# read csv file as a list of lists)
menu_list = f_read_menu(menu_filepath)


# Read in the sales data (in sales_data.csv) into the sales list (#append)
# number of rows 
nr_rec_sales = f_nr_rec_sales(sales_filepath)

# sales into a list 
sales_list = f_read_sales(sales_filepath)


# Sanity check --> verify nr of rows is consistent cvs vs list 
print(f"nr rows in csv {nr_rec_sales}, nr of items in list {sales_list[-1][0]}")
if nr_rec_sales != int(sales_list[-1][0]):
    print ("error !! # of sales in csv and list are not consistant")


# 2 - Process  Data

# Initialize dict object to hold our key-value pairs of items and metrics
dic_report = {}

# Initialize a row counter variable
row_count = 0

# Loop over every row in the sales list object
for sales in sales_list:
    row_count += 1

    # Initialize sales data variables
    sales_menu_item = sales[4]
    sales_qty = int(sales[3])

    # If the item value not in the report, add it as a new entry with initialized metrics
    # Naming convention allows the keys to be ordered in logical fashion, count, revenue, cost, profit
    key_to_lookup = sales_menu_item
    if key_to_lookup not in dic_report:
        print ("Key does not exist")
        dic_report[key_to_lookup] = {
                                    "01-count": 0,
                                    "02-revenue": 0,
                                    "03-cogs": 0,
                                    "04-profit": 0,
                                    }
        print(key_to_lookup, dic_report[key_to_lookup])

    # For every row in our sales data, loop over the menu records to determine a match
    for menu in menu_list:

        # Item,Category,Description,Price,Cost
        # Initialize menu data variables
        menu_item = menu[0]
        menu_price = float(menu[3])
        menu_cost = float(menu[4])
        menu_profit = menu_price - menu_cost 

         # Calculate profit of each item in the menu data
        if menu_item == sales_menu_item:

            # update report (dictionary with new sales)
            dic_report[sales_menu_item]["01-count"] += sales_qty
            dic_report[sales_menu_item]["02-revenue"] += menu_price * sales_qty
            dic_report[sales_menu_item]["03-cogs"] += menu_cost * sales_qty
            dic_report[sales_menu_item]["04-profit"] += menu_profit * sales_qty
        else:
            print(f"{sales_menu_item} does not equal {menu_item}! NO MATCH!")


# print number of sales year-to-date 
print(f"number of sales year-to-date is {row_count}")


# 3 - Report Data 
# Export a text file with the results

#Write out the contents of the report dictionary to a text file. 
# The report should output each ramen type as the keys and 01-count, 02-revenue, 03-cogs, and 04-profit metrics 
filepath_text = Path("../resources/results_ramen.txt")
f_export_text_file (filepath_text, dic_report)


