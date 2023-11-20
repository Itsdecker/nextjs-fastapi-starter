# pdf_csv.py

import os
import camelot
import pandas as pd


def convert_pdfs_csv():
    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    input_folder = os.path.join(current_script_directory, "pdfs/")
    output_folder = os.path.join(current_script_directory, "output/")

    os.makedirs(output_folder, exist_ok=True)
    pdf_files = [file for file in os.listdir(
        input_folder) if file.lower().endswith(".pdf")]

    if not pdf_files:
        return "No PDFs to convert to CSV."

    all_data = []

    for pdf_file in pdf_files:
        keep_columns = ["Name", "Phone", "VIN", "RO#", "Date"]

        try:
            tables = camelot.read_pdf(os.path.join(input_folder, pdf_file), flavor="stream",
                                      table_areas=["3,587,725,198"],
                                      columns=[
                                          "103,164,176,239,312,332,366,401,445,481,725"],
                                      split_text=True, strip_text='=', pages="all")
            dfs = []

            for table in tables:
                df = table.df
                df = df.drop(0)
                df.columns = df.iloc[0]
                dfs.append(df)

            parsed_report = pd.concat(dfs, ignore_index=True)
            parsed_report = parsed_report[parsed_report[keep_columns[0]]
                                          != keep_columns[0]]
            parsed_report = parsed_report[keep_columns]

            parsed_report = parsed_report.dropna(
                how='all', subset=keep_columns)
            parsed_report = parsed_report[~parsed_report.apply(
                lambda row: all(cell.strip() == '' for cell in row), axis=1)]
            all_data.append(parsed_report)

        except Exception as e:
            print(f"Error processing file {pdf_file}: {e}")

    if not all_data:
        return "No data to process. No CSV file created."
    else:
        master_df = pd.concat(all_data, ignore_index=True)
        master_df['Date'] = pd.to_datetime(
            master_df['Date'], format='%m/%d/%y')
        master_df.sort_values(by='Date', inplace=True)
        master_df['Date'] = master_df['Date'].dt.strftime('%m/%d/%y')

        master_filename = os.path.join(output_folder, "MASTER_REPORT.csv")
        master_df.to_csv(master_filename, index=False)
        return f"Master CSV file created at {master_filename}"


if __name__ == "__main__":
    # Test the function or perform some standalone tasks
    result = convert_pdfs_csv()
    print(result)
