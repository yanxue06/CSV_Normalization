import csv 
import os.path
import datetime as dt
import multiprocessing as mp
import time
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

def write_csv(file_output_path, updated_content): 
    if updated_content:
        fieldnames = updated_content[0].keys()
        with open(file_output_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_content)
    print("files have been processed and saved")

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

def process_file(file_input_path, file_output_path, user_changes):
    try:
        with open(file_input_path, 'r') as file:
            rows_content = list(csv.DictReader(file))
            if user_changes == "normalize_dates":
                rows_content = normalize_dates(rows_content)
            if user_changes == "normalize_phones":
                rows_content = normalize_phones(rows_content)
            write_csv(file_output_path, rows_content)     
    except FileNotFoundError:
        print(f"Error: file not found - {file_input_path}")

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

    user_continue = input("Would you like to make changes (y/n)? ").strip().lower()
    while user_continue.strip().lower() not in ["y", "n"]:
        user_continue=input("must enter y/n. try again")

    user_changes = []
    if user_continue == "y":
        while True:
            change = input("Enter the changes you would like to apply (normalize_dates/normalize_phones). Type 'done' when finished: ").strip().lower()
            if change == "done":
                break
            elif change in ["normalize_dates", "normalize_phones"]:
                user_changes.append(change)
            else:
                print("Must enter a valid function (normalize_dates/normalize_phones).")

    if user_continue == "y" and user_changes:
        user_save_changes = input(f"Would you like to save your changes into {output_dir} (y/n)? ").strip().lower()
        while user_save_changes not in ["y", "n"]:
            user_save_changes = input("Must enter (y/n): ").strip().lower()
        processes = []
        if user_save_changes=="y":
            start_time = time.time()
            for file_input_path, file_output_path in zip(file_input_paths, file_output_paths):
                process = mp.Process(target=process_file, args=(file_input_path, file_output_path, user_changes))
                processes.append(process)
                process.start()
            
            for process in processes:
                process.join()
            
            end_time = time.time()
            print(f"Processing time: {end_time - start_time} seconds")
        else:
            print("Changes not saved.")