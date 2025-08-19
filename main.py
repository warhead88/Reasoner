import json
from openai import OpenAI

client = OpenAI()

# Загружаем переписку
with open("data/messages.json", "r", encoding="utf-8") as f:
    messages = json.load(f)["messages"]

# Загружаем промпт
with open("prompts/analysis.txt", "r", encoding="utf-8") as f:
    base_prompt = f.read()

# Превращаем сообщения в удобный текст
chat_text = "\n".join([
    f"[{m['id']}] {m['date']} {m['from']}: {m['text']}"
    for m in messages
])

# Финальный запрос
prompt = f"{base_prompt}\n\nВот переписка:\n{chat_text}"

response = client.chat.completions.create(
    model="gpt-5",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=8000  # можешь поставить больше при длинной переписке
)

# Сохраняем результат
report = response.choices[0].message.content

with open("output/report.md", "w", encoding="utf-8") as f:
    f.write(report)

print("Готово! Отчёт в output/report.md")
