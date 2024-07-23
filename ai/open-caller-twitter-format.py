from openai import OpenAI
client = OpenAI()


#print(completion.choices[0].message)

def call_openai(link):
  completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      # {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
      {"role": "user",
       "content": "Here is a link to an article : " + link + ". Summarize this article in a tweet. the response should like this format {\"text\": \"tweet goes here\"}"}
    ]
  )

  return completion.choices[0].message.content


link = "https://www.vox.com/future-perfect/361749/universal-basic-income-sam-altman-open-ai-study"

tweet = call_openai(link)

print(tweet)