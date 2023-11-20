from fastapi import FastAPI
from api.pdf_parser.main import main


app = FastAPI()


@app.get("/api/trigger-main")
def trigger_main():
    print("Triggering main function")  # Add this line for debugging
    main()
    return {"message": "Main function triggered"}
