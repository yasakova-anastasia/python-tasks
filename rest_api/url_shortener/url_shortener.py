import uuid

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI()


class ToShort(BaseModel):
    url: str


class Shorted(BaseModel):
    url: str
    key: str


URL = {}


@app.post('/shorten', status_code=status.HTTP_201_CREATED, response_model=Shorted)
async def short_url(to_short: ToShort) -> dict[str, str]:
    key = str(uuid.uuid3(uuid.NAMESPACE_URL, to_short.url))
    key = key[:10]
    URL[key] = to_short.url

    return {'url': to_short.url, 'key': key}


@app.get('/go/{key}', status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def redirect_to_url(key: str, response: RedirectResponse) -> None:
    if key not in URL:
        raise HTTPException(status_code=404)

    response.headers['location'] = URL[key]
