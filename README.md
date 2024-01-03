# ps-hack-team-1

Install the Dependencies:

```shell
pip install -r requirements.txt
```

Run it (replace variable values first):

```shell
OPENAI_API_KEY="..." MONGODB_URI="..." TOKENIZERS_PARALLELISM=true \
  python job_insights/prompt_ui.py
```

Open [http://127.0.0.1:7860/](http://127.0.0.1:7860/) in your browser.
