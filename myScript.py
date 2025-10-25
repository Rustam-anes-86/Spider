import os, json, requests
from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
MODEL= os.getenv("OPENAI_MODEL", "gpt-4o-mini")
API_KEY=os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY не задан в окружении")

CHAT_URL=f"{BASE_URL}/chat/completions"

SYSTEM_PROMPT= (
    "Ты -дружелюбный репетитор по информатике для школьниковю "
    "Объясняй просто и коротко. Если вопрос неоднозначен - уточни 1 вещь"
    "Дай решение/объяснение в 2-4 шагах и итоговый ответ"
    "Добавляй 1 мини-совет по теме в конце (1 строка)"
)

def ask_llm(question:str)->str:
    payload= {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
            ],
        "temperature":0.2,
    }

    try:
        resp=requests.post(
            CHAT_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"

            },
            data=json.dumps(payload),
            timeout=60

        )
        resp.raise_for_status()
        obj=json.loads(resp.text)
        return obj["choices"] [0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        return f"Ошибка запроса:{e}"
    
def main():
    print("Бот-репетитор запущен. Спроси что угодно по информатике (или/exit):")
    while True:
        try:
            q=input("\nТы").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nПока!"); break
        if not q:
            continue
        if q.lower() in ("/exit", "exit", "quit"):
            print("Пока!"); break
        print (f"Бот: {ask_llm(q)}")

if __name__ =="__main__":
    main()