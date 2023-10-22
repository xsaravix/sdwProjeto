import requests
import json
import pandas as pd
import time

urlreq = 'https://653520b1c620ba9358ec2f15.mockapi.io/clients'

def get_user():
  response = requests.get(urlreq)
  return response.json() if response.status_code == 200 else None

users = get_user()
print(json.dumps(users, indent=2))

!pip install openai

openai_api_key = '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'

import openai

openai.api_key = openai_api_key

def generate_ai_news(user):
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {
          "role": "system",
          "content": "Você é um especialista em odontologia."
      },
      {
          "role": "user",
          "content": f"Crie uma mensagem para {user['name']} sobre a importância do cuidado com a saúde bucal. Se {user['plano_odonto']} for Sim diga para aproveitar seu plano odontológico. (máximo de 150 caracteres)"
      }
    ]
  )
  return completion.choices[0].message.content.strip('\"')

for user in users:
  news = generate_ai_news(user)
  print(news)
  user['news'].update({'news': news})
  time.sleep(20)

def update_user(user):
  response = requests.put(f"{urlreq}/users/{user['id']}", json=user)
  return True if response.status_code == 200 else False

for user in users:
  success = update_user(user)
  print(f"User {user['name']} updated? {success}!")