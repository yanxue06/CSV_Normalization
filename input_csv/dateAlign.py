import csv 
import os.path
import datetime as dt

def normalize_date(date): 
    formats = ["%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d"]
     
    for fmt in formats: 
        try:
            date_obj=dt.datetime.strptime(date, fmt)
            normalized_date_obj=dt.datetime.strftime(date_obj, "%Y/%m/%d")
            print (normalized_date_obj)
            return normalized_date_obj
        except ValueError: 
            continue 

def write_new_csv(file_input_path, file_output_path, output_dir): 
    normalized_dates=[] 
    rows_content=[]
    try: 
        with open(file_input_path, 'r') as file: 
            rows_content = list(csv.DictReader(file)) #multuple files ca prb use ultiprocessing
            fieldnames=rows_content[0].keys() 
            for row in rows_content: 
                date_str=row["date_column"]
                normalized_dates.append(normalize_date(date_str))
                print(normalized_dates)
    except FileNotFoundError:
        print("Error: file not found")
        return 
    userInput = (input("would you like to create new files with these new dates(y/n)")).strip().lower() 
    while userInput not in ("y", "n"):
        print("must enter y/n")
    if userInput=="y": 
        make_csv(file_output_path, rows_content, normalized_dates, fieldnames)
    else:
        print("no new file created")

def make_csv(file_output_path, rows_content, normalized_dates, fieldnames): 
    k=0
    for row in rows_content:
        row["date_column"]=normalized_dates[k]
        k+=1 
    with open (file_output_path, 'w', newline='') as file: 
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader() 
        writer.writerows(rows_content)

if __name__=="__main__":
    
    input_dir = input("Please enter the directory containing CSV files to normalize('input_csv'): ").strip().lower()
    while not os.path.isdir(input_dir):
        input_dir = input("Invalid directory. Please enter the directory containing CSV files to normalize: ").strip().lower()
    
    output_dir = input("Please enter the directory to save normalized CSV files('output_csv'): ").strip().lower()
    while not os.path.isdir(output_dir):
        output_dir = input("Invalid directory. Please enter the directory to save normalized CSV files: ").strip().lower()
    
    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            file_input_path = os.path.join(input_dir, filename)
            file_output_path = os.path.join(output_dir, filename)
            write_new_csv(file_input_path, file_output_path, output_dir)
