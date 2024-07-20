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

def write_new_csv(file1): 
    normalized_dates=[] 
    rows_content=[]
    try: 
        with open(file1, 'r') as file: 
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
        abs_path="/Users/yammy/Desktop/SideQuests/CSV scripting/output_csv" 
        output_filename="output.csv"
        output_filepath=os.path.join(abs_path, output_filename) 
        write_csv(output_filepath, rows_content, normalized_dates, fieldnames)
    else:
        print("no new file created")

def write_csv(output_filepath, rows_content, normalized_dates, fieldnames): 
    k=0
    for row in rows_content:
        row["date_column"]=normalized_dates[k]
        k+=1 
    with open (output_filepath, 'w', newline='') as file: 
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader() 
        writer.writerows(rows_content)

if __name__=="__main__":
    
    file1=input("please write the csv file name you would like to normalize the date for: ").strip()
    while not os.path.isfile(file1): 
        file1=(str)(input("1st input not a path. please write the csv file name you would like to normalize the date for: ")).strip() 
    
    write_new_csv(file1)
