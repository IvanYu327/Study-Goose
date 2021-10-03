from dotenv import load_dotenv
from os import getenv
import json
load_dotenv() 
WOLFRAM_KEY = getenv("WOLFRAM")

import wolframalpha

app_id = WOLFRAM_KEY
wolframClient = wolframalpha.Client(app_id)


async def wolfram(question):
    print(question)
    try:
        res = wolframClient.query(question)
        answer = next(res.results).text
        return answer
    except:
        return "Monthly usage of wolfram API has been exceeded.\nPlease wait until next month before using this command again."