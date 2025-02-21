import pandas as pd
import tkinter as tk
from tkinter import messagebox, filedialog
import datetime as dt
import re
import os
import multiprocessing as mp

# Function to normalize date formats
def normalize_date(date):
    formats = ["%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d"]
    for fmt in formats:
        try:
            date_obj = dt.datetime.strptime(date, fmt)
            return date_obj.strftime("%Y/%m/%d")
        except ValueError:
            continue
    return date

# Function to normalize phone number formats
def normalize_phone(phone):
    pattern = re.compile(r"^\+?1?[\s.-]?(\d{3})[\s.-]?(\d{3})[\s.-]?(\d{4})$")
    match = pattern.match(phone)
    if match:
        return "({}) {}-{}".format(match.group(1), match.group(2), match.group(3))
    return phone

# Function to normalize a CSV file
def normalize_file(file_path, output_path, date_column, phone_column, normalize_dates, normalize_phones):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    try: 
        if normalize_dates:
            if date_column in df.columns: 
                df[date_column] = df[date_column].apply(normalize_date)
    except KeyError:
        messagebox.showerror("Error", "The column {} does not exist in the DataFrame.".format(date_column))
    try: 
        if normalize_phones:
            if phone_column in df.columns: 
                df[phone_column] = df[phone_column].apply(normalize_phone)
    except KeyError: 
        messagebox.showerror("Error", "The column {} does not exist in the DataFrame.".format(phone_column))
    

    
    # Save the normalized DataFrame to the output directory
    df.to_csv(output_path, index=False)
    print(f"File {output_path} has been processed and saved")

class NormalizerApp: 
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Normalizer")
        self.create_widgets()

    def create_widgets(self):
        # Create GUI components
        self.label = tk.Label(self.root, text="Select input and output directories")
        self.label.pack(pady=10)
        self.input_button = tk.Button(self.root, text="Select Input Folder", command=self.select_input_folder)
        self.input_button.pack(pady=5)
        self.output_button = tk.Button(self.root, text="Select Output Folder", command=self.select_output_folder)
        self.output_button.pack(pady=5)

        self.normalize_dates_var = tk.BooleanVar()
        self.normalize_phones_var = tk.BooleanVar()
        self.check_phones = tk.Checkbutton(self.root, text="Normalize Phones", variable=self.normalize_phones_var)
        self.check_phones.pack(pady=(5,1))

        self.labelC = tk.Label(self.root, text="Enter your phone column name", font=("arial", 11))
        self.labelC.pack()
        self.phone_entry=tk.Entry(self.root, font=("arial", 11))
        self.phone_entry.pack(pady=(0, 5)) 

        self.check_dates = tk.Checkbutton(self.root, text="Normalize Dates", variable=self.normalize_dates_var)
        self.check_dates.pack(pady=(0,1))

        self.labelD = tk.Label(self.root, text="Enter your date column name", font=("arial", 11))
        self.labelD.pack() 
        self.date_entry=tk.Entry(self.root, font=("arial", 11))
        self.date_entry.pack() 

        self.process_button = tk.Button(self.root, text="Process Files", command=self.process_files )
        self.process_button.pack(pady=20)

        
    def select_input_folder(self):
        self.input_dir = filedialog.askdirectory()
        messagebox.showinfo("Selected Folder", f"Input Folder: {self.input_dir}")

    def select_output_folder(self):
        self.output_dir = filedialog.askdirectory()
        messagebox.showinfo("Selected Folder", f"Output Folder: {self.output_dir}")

    def process_files(self):
        # Get the list of CSV files in the input directory
        try: 
            files = [os.path.join(self.input_dir, f) for f in os.listdir(self.input_dir) if f.endswith(".csv")]
            if not files: 
                raise FileNotFoundError("no csv files in your input folder ")

            processes = []
            date_entry=self.date_entry.get() 
            phone_entry=self.phone_entry.get() 
            for file in files:
                output_path = os.path.join(self.output_dir, os.path.basename(file))
                # Create a new process for each file
                process = mp.Process(target=normalize_file, args=(file, output_path, date_entry, phone_entry, self.normalize_dates_var.get(), self.normalize_phones_var.get()))
                processes.append(process)
                process.start()

            # Wait for all processes to complete
            for process in processes:
                process.join()

            messagebox.showinfo("Process Complete", "All files have been normalized")
        except Exception as e: 
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = NormalizerApp(root)
    root.mainloop()