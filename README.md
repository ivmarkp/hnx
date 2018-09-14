# Hnx

Backend code that serves a RESTful API written in Python using Flask for [Hnfy](https://github.com/ivmarkp/hnfy).

### API Description

#### `GET /user/recommendations`

Fetches stories of interest for a particular HN user.

#### Parameters

* `id`: HN username of the user.
* `type`: Story type. Supported types are `top`, `new`, `show` & `ask`.

#### Response

A JSON object with a key `stories` whose value is an array of retrieved stories.

#### Example

`GET /user/recommendations?id=wewake&type=top`

```
{
  "stories": [
  {
    "author": "ladybro",
    "comments": 24,
    "points": 118,
    "time": "2018-09-11T13:05:23.000Z",
    "title": "Show HN: Mindstamp – Make Any Video Interactive in Seconds",
    "topics": [
    "Software"
    ],
    "url": "https://mindstamp.io"
  },
  {
    "author": "ristem",
    "comments": 73,
    "points": 91,
    "time": "2018-09-13T09:19:37.000Z",
    "title": "Guidelines for writing readable code",
    "topics": [
    "Programming"
    ],
    "url": "https://alemil.com/guidelines-for-writing-readable-code"
  }
]
```

### How are the recommendations generated?

Check out the "How?" section in the README of [Hnfy](https://github.com/ivmarkp/hnfy).