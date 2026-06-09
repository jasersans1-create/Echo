# Memo: Mistakes and Lessons

- Keep the first version small: voice engine + launch core before adding GUI.
- Use local offline speech libraries only. Avoid cloud APIs and paid services.
- Make command mapping explicit and easy to extend.
- Ensure the assistant does not execute unsafe actions without confirmation.
- If voice recognition fails, return a friendly message instead of crashing.
- Prefer standard Python libraries and clear comments.
