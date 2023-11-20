import os
import camelot
import pandas as pd

# Get the directory of the current script
current_script_directory = os.path.dirname(os.path.abspath(__file__))

# Set up input and output folders relative to the script's location
input_folder = os.path.join(current_script_directory, "pdfs/")
output_folder = os.path.join(current_script_directory, "output/")

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# List all PDF files in the input folder
pdf_files = [file for file in os.listdir(
    input_folder) if file.lower().endswith(".pdf")]

# Check if there are any PDF files in the folder
if not pdf_files:
    print("No PDFs to convert to CSV.")
else:
    all_data = []  # List to hold data from all PDFs

    for pdf_file in pdf_files:
        keep_columns = ["Name", "Phone", "VIN", "RO#", "Date"]

        # Read tables from PDF
        try:
            tables = camelot.read_pdf(os.path.join(input_folder, pdf_file), flavor="stream",
                                      table_areas=["3,587,725,198"],
                                      columns=[
                                          "103,164,176,239,312,332,366,401,445,481,725"],
                                      split_text=True, strip_text='=', pages="all")
            dfs = []

            for table in tables:
                table.df = table.df.drop(0)
                table.df.columns = table.df.iloc[0]
                dfs.append(table.df)

            parsed_report = pd.concat(dfs, ignore_index=True)
            parsed_report = parsed_report[parsed_report[keep_columns[0]]
                                          != keep_columns[0]]
            parsed_report = parsed_report[keep_columns]

            # Clean and filter data
            parsed_report = parsed_report.dropna(
                how='all', subset=keep_columns)
            parsed_report = parsed_report[~parsed_report.apply(lambda row: all(
                cell.strip() == '' or cell == ',' for cell in row), axis=1)]
            parsed_report = parsed_report[~parsed_report.apply(lambda row: any(
                cell.strip() == '' or cell == ',' for cell in row), axis=1)]

            all_data.append(parsed_report)

        except Exception as e:
            print(f"Error processing file {pdf_file}: {e}")

    # Check if there is data to process
    if not all_data:
        print("No data to process. No CSV file created.")
    else:
        # Combine all data into a single DataFrame and sort
        master_df = pd.concat(all_data, ignore_index=True)
        master_df['Date'] = pd.to_datetime(
            master_df['Date'], format='%m/%d/%y')
        master_df.sort_values(by='Date', inplace=True)

        # Format the 'Date' column to MM/DD/YY before writing to CSV
        master_df['Date'] = master_df['Date'].dt.strftime('%m/%d/%y')

        # Export the master DataFrame to a CSV file
        master_filename = os.path.join(output_folder, "MASTER_REPORT.csv")
        master_df.to_csv(master_filename, index=False)
        print("Master CSV file creation completed.")
