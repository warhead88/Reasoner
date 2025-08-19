import json
from openai import OpenAI
from pathlib import Path

client = OpenAI()

# Загружаем переписку (уже обработанную parser.py)
with open("data/parsed/parsed_data.json", "r", encoding="utf-8") as f:
    messages = json.load(f)["messages"]

# Загружаем промпт
with open("prompts/analysis.txt", "r", encoding="utf-8") as f:
    base_prompt = f.read()

# Превращаем сообщения в удобный для чтения текст
chat_text = "\n".join([
    f"[{m['id']}] {m['date']} {m['from']}: {m['text']}"
    for m in messages if m["text"]  # пропускаем пустые
])

# Формируем финальный промпт
prompt = f"{base_prompt}\n\nВот переписка:\n{chat_text}"

# Отправляем в OpenAI
response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=8000  # можно поднять лимит при длинной переписке
)

report = response.choices[0].message.content

# Сохраняем отчёт
Path("output").mkdir(parents=True, exist_ok=True)
with open("output/report.md", "w", encoding="utf-8") as f:
    f.write(report)

print("📄 Готово! Отчёт в output/report.md")

