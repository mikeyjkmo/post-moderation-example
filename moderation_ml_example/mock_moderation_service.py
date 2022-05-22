from pydantic import BaseModel
from fastapi import FastAPI


class FragmentPayload(BaseModel):
    fragment: str


app = FastAPI()


@app.post("/sentences")
async def post_sentences(payload: FragmentPayload):
    return {
        "hasFoulLanguage": "frick" in payload.fragment.lower()
    }
