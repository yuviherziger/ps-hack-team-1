# ps-hack-team-1

Install the Dependencies:

```shell
pip install -r requirements.txt
```

Run it (replace variable values first):

```shell
OPENAI_API_KEY="..." MONGODB_URI="..." \
  python -m uvicorn job_insights.web:app --reload
```

Query:

```shell
curl -sS \
  http://localhost:8000/answer?query=What%20are%20the%20most%20common%20skills%20for%20a%20Java%20software%20engineer
```
