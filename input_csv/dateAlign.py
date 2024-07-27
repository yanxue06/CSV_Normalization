import csv 
import os.path
import datetime as dt
import multiprocessing 
import re 
import os

def normalize_date(date): 
    formats = ["%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d"]
    for fmt in formats: 
        try:
            date_obj=dt.datetime.strptime(date, fmt) #creating date_object with the desired format, error if not
            normalized_date_obj=dt.datetime.strftime(date_obj, "%Y/%m/%d") #converting obj back to string 
            return normalized_date_obj
        except ValueError: 
            continue 

def normalize_dates(file): 
    for row in file:
        row["date_column"] = normalize_date(row["date_column"])
    return file #my row content should be updated with my desired date normalization

def write_csv(file_output_paths, updated_files): 
    for file_output_path, updated_content in zip(file_output_paths, updated_files):
        if updated_content:
            fieldnames = updated_content[0].keys()
            with open(file_output_path, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(updated_content)

def normalize_phone(phone): 
      pattern = re.compile(r"^\+?1?[\s.-]?(\d{3})[\s.-]?(\d{3})[\s.-]?(\d{4})$") 
      match=pattern.match(phone)
      if match:
          return "({}) {}-{}".format(match.group(1), match.group(2), match.group(3))
      else: 
          return phone
      
def normalize_phones(file): #taking in a csv file with all the content stored as a dictionary 
    for row in file: 
        row["phone"]=normalize_phone(row["phone"])
    return file     

if __name__=="__main__":
    input_dir = input("Please enter the directory containing CSV files to normalize('input_csv'): ").strip().lower()
    while not os.path.isdir(input_dir):
        input_dir = input("Invalid directory. Please enter the directory containing CSV files to normalize: ").strip().lower()
    
    output_dir = input("Please enter the directory to save normalized CSV files('output_csv'): ").strip().lower()
    while not os.path.isdir(output_dir):
        output_dir = input("Invalid directory. Please enter the directory to save normalized CSV files: ").strip().lower()
    
    file_input_paths=[]
    file_output_paths=[] 

    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            file_input_path = os.path.join(input_dir, filename)
            file_output_path = os.path.join(output_dir, filename)
            file_input_paths.append(file_input_path)
            file_output_paths.append(file_output_path)

    # Load contents of all CSV files into updated_files
    updated_files = []
    for file_input_path in file_input_paths:
        try:
            with open(file_input_path, 'r') as file:
                rows_content = list(csv.DictReader(file))
                updated_files.append(rows_content)
        except FileNotFoundError:
            print(f"Error: file not found - {file_input_path}")
            
    user_continue = input("Would you like to make changes (y/n)? ").strip().lower()
    while user_continue.strip().lower() not in ["y", "n"]:
        user_continue=input("must enter y/n. try again")

    while user_continue == "y":
        user_changes = input("What type of changes would you like to apply (normalize_dates/normalize_phones)? ").strip().lower()
        while user_changes not in ["normalize_dates", "normalize_phones"]:
            user_changes = input("Must enter a valid function (normalize_dates/normalize_phones). Try again: ").strip().lower()
        
        if user_changes == "normalize_dates":
            for i in range(len(updated_files)):
                updated_files[i] = normalize_dates(updated_files[i])
        elif user_changes == "normalize_phones":
            for i in range(len(updated_files)):
                updated_files[i] = normalize_phones(updated_files[i])
        user_continue = input("Would you like to make more changes (y/n)? ").strip().lower()
        while user_continue.strip().lower() not in ["y", "n"]:
            user_continue=input("must enter y/n. try again")
            if user_changes=="n":
                print("okay, no more changes") 

    user_saveChanges=input("would you like to save your changes into {} (y/n)".format(output_dir))
    
    while user_saveChanges.strip().lower() not in ["y", "n"]: 
        user_saveChanges=("must enter (y/n)")
    
    if user_saveChanges=="y": 
        write_csv(file_output_paths, updated_files)
        print("files should be updates")
    else: 
        print("changes not saved.")