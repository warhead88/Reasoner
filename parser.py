import json
from pathlib import Path

def parse_telegram_export(input_path: str, output_path: str):
    # Загружаем исходные данные
    with open(input_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    parsed_messages = []

    for msg in raw_data.get("messages", []):
        if msg.get("type") != "message":
            continue  # пропускаем сервисные события (удаление, редактирование и т.п.)

        # Вытаскиваем текст: иногда Telegram кладёт его в массив
        text = msg.get("text", "")
        if isinstance(text, list):
            # Если текст — массив с кусками (смайлики, ссылки и т.д.)
            text = "".join([part["text"] if isinstance(part, dict) else str(part) for part in text])

        parsed_messages.append({
            "id": msg.get("id"),
            "date": msg.get("date"),
            "from": msg.get("from", "Unknown"),
            "text": text.strip()
        })

    parsed_data = {"messages": parsed_messages}

    # Создаём директорию для выхода
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # Сохраняем результат
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(parsed_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Готово! Сохранено {len(parsed_messages)} сообщений в {output_path}")

if __name__ == "__main__":
    parse_telegram_export(
        "data/unparsed/data.json",
        "data/parsed/parsed_data.json"
    )

