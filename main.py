from openai import OpenAI 
from config import BASE_QUERY, TERM_DAYS, THEME, TITLE_FILTER, AUTHOR_FILTER, ABSTRACT_FILTER, INCLUDE_FILTER, EXCLUDE_FILTER

client = OpenAI()

completion = client.chat.completions.create(
    model = "gpt-4o-mini",
    store = True,
    messages=[
        {"role":"user", "content": "write haiku about you"}
    ]
)

print(completion)