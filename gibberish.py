from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import collections
import random
import textwrap

app = FastAPI()

# Define the input schema
class TextGenerationRequest(BaseModel):
    num_words: int
    text_data: str

@app.post("/generate_text/")
async def generate_text(request: TextGenerationRequest):
    num_words = request.num_words
    text_data = request.text_data

    # Check if inputs are valid
    if num_words <= 0:
        raise HTTPException(status_code=400, detail="Number of words must be greater than zero.")
    if not text_data:
        raise HTTPException(status_code=400, detail="Text data cannot be empty.")

    w1 = w2 = ''
    possibles = collections.defaultdict(list)

    # Process the text to build the table of possible words
    for line in text_data.splitlines():
        for word in line.split():
            possibles[w1, w2].append(word)
            w1, w2 = w2, word

    # Avoid empty possibilities lists at the end of the input
    possibles[w1, w2].append('')
    possibles[w2, ''].append('')

    # Generate random output starting from a capitalized prefix
    try:
        w1, w2 = random.choice([k for k in possibles if k[0][:1].isupper()])
    except IndexError:
        raise HTTPException(status_code=400, detail="No suitable starting word pair found in text data.")

    output = [w1, w2]
    for _ in range(num_words):
        word = random.choice(possibles[w1, w2])
        output.append(word)
        w1, w2 = w2, word

    # Return the formatted output
    generated_text = textwrap.fill(' '.join(output))
    return {"generated_text": generated_text}
