import random
import string
import typing as tp

from fastapi import FastAPI, Header, Request, Response, status
from pydantic import BaseModel

app = FastAPI()


class Info(BaseModel):
    name: str
    age: int


USERS: dict[str, tp.Any] = {}
tracks_count: list[int] = []


@app.post('/api/v1/registration/register_user', status_code=status.HTTP_201_CREATED)
async def registration(data: Info) -> dict[str, str]:
    token = None
    for t_id, user in USERS.items():
        if user["name"] == data.name and user["age"] == data.age:
            token = t_id
            break
    if token is None:
        letters = string.ascii_lowercase
        token = ''.join(random.choice(letters) for i in range(40))
        while token in USERS:
            token = ''.join(random.choice(letters) for i in range(40))
        USERS[token] = {"name": data.name, "age": data.age, "tracks": {}}
    return {"token": token}


@app.post('/api/v1/tracks/add_track', status_code=status.HTTP_201_CREATED)
async def add_track(request: Request, response: Response) -> dict[str, tp.Any]:
    token = request.headers.get("x-token")
    if token is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"detail": "Missing token"}
    if token not in USERS:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"detail": "Incorrect token"}

    data = await request.json()

    if "artist" not in data or "name" not in data:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {"detail": "Not all params"}
    tracks_count.append(len(tracks_count))
    track_id = len(tracks_count)

    USERS[token]["tracks"][track_id] = {
        'name': data.get('name'),
        'artist': data.get('artist'),
        'year': data.get('year'),
        'genres': data.get('genres', [])
    }

    return {"track_id": track_id}


@app.get('/api/v1/tracks/search', status_code=status.HTTP_200_OK)
async def search_get(response: Response, name: tp.Any = None, artist: tp.Any = None,
                     x_token: tp.Any = Header(default=None)) -> dict[str, tp.Any]:
    if x_token is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"detail": "Missing token"}
    if x_token not in USERS:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"detail": "Incorrect token"}

    if artist is None and name is None:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {"detail": "You should specify at least one search argument"}

    result = []

    for track_id, track in USERS[x_token]["tracks"].items():
        res = 0
        if name is None:
            res += 1
        elif name is not None and name == track["name"]:
            res += 1

        if artist is None:
            res += 1
        elif artist is not None and artist == track["artist"]:
            res += 1

        if res == 2:
            result.append(track_id)

    return {"track_ids": result}


@app.delete('/api/v1/tracks/{track_id}', status_code=status.HTTP_200_OK)
async def delete_track(track_id: int, response: Response, x_token: tp.Any = Header(default=None)) -> dict[str, tp.Any]:
    if x_token is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"detail": "Missing token"}
    if x_token not in USERS:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"detail": "Incorrect token"}

    if track_id not in USERS[x_token]["tracks"]:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": "Invalid track_id"}

    del USERS[x_token]["tracks"][track_id]
    return {"status": "track removed"}


@app.get('/api/v1/tracks/all', status_code=status.HTTP_200_OK)
async def get_all_tracks(response: Response, x_token: tp.Any = Header(default=None)) -> tp.Any:
    if x_token is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"detail": "Missing token"}
    if x_token not in USERS:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"detail": "Incorrect token"}

    return [{"name": track["name"], "artist": track["artist"],
             "year": track["year"], "genres": track["genres"]}
            for track in USERS[x_token]["tracks"].values()]


@app.get('/api/v1/tracks/{track_id}', status_code=status.HTTP_200_OK)
async def get_track(track_id: int, response: Response, x_token: tp.Any = Header(default=None)) -> dict[str, tp.Any]:
    if x_token is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"detail": "Missing token"}
    if x_token not in USERS:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"detail": "Incorrect token"}

    if track_id not in USERS[x_token]["tracks"]:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": "Invalid track_id"}

    return {"name": USERS[x_token]["tracks"][track_id]["name"], "artist": USERS[x_token]["tracks"][track_id]["artist"]}
