import json

import redis
import requests
import uvicorn
from elasticsearch import Elasticsearch
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from configs import API_URL, ELASTICSEARCH_URL, ELASTICSEARCH_PASSWORD, ELASTICSEARCH_USER, \
    REDIS_HOST, REDIS_PASSWORD, REDIS_PORT

app = FastAPI()

redis_client = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT), password=REDIS_PASSWORD)

es = Elasticsearch(ELASTICSEARCH_URL, http_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD), verify_certs=False)

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def search_form(request: Request):
    return templates.TemplateResponse("search_form.html", {"request": request})


@app.get("/search/", response_class=HTMLResponse)
async def search_movie(request: Request, movie_name: str):
    search_result = redis_client.get(movie_name)
    if search_result:
        movies_result = [item for item in json.loads(search_result)]
        return templates.TemplateResponse("movie_details.html", {"request": request, "movies_result": movies_result})

    es_response = es.search(index='movies', body={"query": {"match": {"Series_Title": movie_name}}})
    if es_response['hits']['total']['value'] > 0:
        search_result = es_response['hits']['hits']
        movies_result = [item['_source'] for item in search_result]
        redis_client.set(movie_name, json.dumps(movies_result))
        return templates.TemplateResponse("movie_details.html", {"request": request, "movies_result": movies_result})

    querystring = {"query": movie_name}
    headers = {
        "X-RapidAPI-Key": "cd43af9cfdmsh6c224a18db2e7d9p182ab9jsneb1b946a7f1b",
        "X-RapidAPI-Host": "imdb146.p.rapidapi.com"
    }
    api_response = requests.get(API_URL, headers=headers, params=querystring,
                                proxies={"https": "socks5://proxy.my.sahab.ir:8123",
                                         "http": "socks5://proxy.my.sahab.ir:8123"})
    if api_response.status_code == 200:
        search_result = api_response.json()['titleResults']['results']
        if len(search_result) == 0:
            return templates.TemplateResponse("no_movies.html", {"request": request})
        movies_result = [{'Poster_Link': item['titlePosterImageModel']['url'], 'Series_Title': item['titleNameText'],
                          'Released_Year': item['titleReleaseText'], 'Stars': item['topCredits']} for item in
                         search_result]
        return templates.TemplateResponse("movie_details.html", {"request": request, "movies_result": movies_result})

    return templates.TemplateResponse("no_movies.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
