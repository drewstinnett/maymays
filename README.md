[![codecov](https://codecov.io/gh/drewstinnett/maymays/branch/master/graph/badge.svg)](https://codecov.io/gh/drewstinnett/maymays)

# MayMays

Fun project to try and make it easy to meme

## Features

* GraphQL API at `/graphql`

* Geneate simple AdHoc Mems by going to `/adhoc_mems/<meme_slug>/<top_text>/<bottom_text>`

* Automatically pull in top meme templates from [imgflip](https://api.imgflip.com/get_memes)

## Installation

Currently requires >= python3

Install requirements with

```
pip3 install -r requirements.txt
```

## Running Locally

The following command will bring the meme server up on localhost:8000

```
$ python3 ./manage.py runserver
```
