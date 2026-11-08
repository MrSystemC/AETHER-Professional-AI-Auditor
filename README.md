# AETHER — Система фундаментальной инженерии цифрового мира

Самостоятельная система для разбора, анализа и инженерии цифровых артефактов + **ИИ-Аудитор**.

## ИИ-Аудит

```bash
python -m aether.cli examples/good_prompt.txt --audit
python -m aether.cli examples/weak_prompt.txt --audit
```

Выдаёт скоринг (ясность, структура, стоимость, надёжность), проблемы и рекомендации.

## Обычный разбор

```bash
python -m aether.cli examples/agent.json
python -m aether.cli examples/code.py
```

## Веб

```bash
python -m aether.web
```

Кнопка «ИИ-Аудит» в интерфейсе.

## Концепт

`docs/AETHER_Концепт_v1.0.md`
