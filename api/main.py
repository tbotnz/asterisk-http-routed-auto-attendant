from fastapi import FastAPI

app = FastAPI()


@app.get("/call/{phone_number}")
def call(phone_number: str):
    print(f"Incoming call from: {phone_number}")
    return {"status": "ok", "phone_number": phone_number}
