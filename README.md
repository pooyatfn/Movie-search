# Movie-search

## About the project
this is a Movie search system that users can search their intedetes Movie, Series, Actor & ..., and system shows the result searched from cache(multi level) and if it does not cached gets it from external API.

![Screenshot 2024-06-07 224339](https://github.com/pooyatfn/Movie-search/assets/98226980/a53b7f7b-d68b-4eb5-9efd-f72896c5e5c3)

### Services:
  #### Backend:
  fastAPI app that provides an endpoint for seaching.
  #### redis:
  this service plays as first cache lavel. if intended keword does not match with any entry, it send the request to next cache level and when the results came, it caches the result for next searchs.
  #### elastic search:
  the searching entry where you can enter your data sources.
  #### kibana:
  GUI for interacting with elastic search

  ![Screenshot 2024-06-07 224858](https://github.com/pooyatfn/Movie-search/assets/98226980/7a92cf73-9a55-4228-9784-12c022c51cb3)
  
  #### external api:
  the api that used when redis and elastic do not have any matches for entered keyword.
  #### docker, compose and kubernetes:
  this project can build with docker compose and run on kubernetes cluster easily.
