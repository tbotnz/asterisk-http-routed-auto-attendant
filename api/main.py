from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()


@app.get("/call/{phone_number}")
def call(phone_number: str):
    # Response format: redirect_extension,caller_id
    print(f"Incoming call from: {phone_number}")
    if phone_number == "4431631":
        print("Redirecting call to 777")
        return PlainTextResponse("777,+15551234567")
    return PlainTextResponse("888,+15559999999")
