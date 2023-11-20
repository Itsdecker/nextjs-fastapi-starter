from fastapi import FastAPI
from api.standalone.download_drive_ep import download_drive_ep
from api.standalone.pdf_csv import convert_pdfs_csv

app = FastAPI()


@app.get("/api/download_drive_ep")
def trigger_download():
    result = download_drive_ep()
    return result

# Corrected endpoint name to match the log message


@app.get("/api/convert-pdfs")
def pdf_csv():
    result = convert_pdfs_csv()
    return result
