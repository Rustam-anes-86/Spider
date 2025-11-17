import os, json
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

print ("Сейчас с Вами общается ИИ - ассистент!")

client = OpenAI()

with open("faq.json", "r", encoding="utf-8") as f:
    FAQ=json.load(f)


def ask_llm(user_q:str)->str:
    faq_text="\n".join([f"Q: {item['q']}\nA: {item['a']}" for item in FAQ])

    prompt= f"""
Ты - AI-консультант банка.
У тебя есть список FAQ (вопрос-ответ).
Клиент задает вопрос: "{user_q}"

Задача: 
1. Найди наиболее похожий вопрос из FAQ.
2. Если нашел -дай готовый ответ(НЕ придумывай новый).
3. Если нет ничего похожего - ответь строго: "нет похожего"

FAQ:
{faq_text}
"""
    
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"system", "content":"Ты помощник банка."},
                  {"role":"user", "content":prompt }],
        temperature=0
    )

    return resp.choices[0].message.content.strip()

def get_answer(user_q:str)->str:
    answer=ask_llm(user_q)
    if "нет похожего" in answer.lower():
        phone="9091"
        return f"Пожалуйста, по этому вопросу свяжитесь с оператором по номеру {phone}"
    else:
        return answer

while True:
    q=input("Клиент: ")
    if q.lower() in ["exit", "выход"]:
        break
    print("AI:", get_answer(q))






