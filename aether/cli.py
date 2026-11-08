"""
AETHER — Professional CLI with full AI Auditor
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.markdown import Markdown
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

from aether.core import Aether

console = Console() if HAS_RICH else None


def main() -> None:
    parser = argparse.ArgumentParser(description="AETHER — Fundamental Engineering + Professional AI Auditor")
    parser.add_argument("input", nargs="?", help="Файл или - для stdin")
    parser.add_argument("--json", action="store_true", help="JSON вывод")
    parser.add_argument("--audit", action="store_true", help="Полный ИИ-аудит")
    parser.add_argument("--report", metavar="FILE", help="Сохранить Markdown-отчёт")
    args = parser.parse_args()

    if args.input in (None, "-"):
        content = sys.stdin.read()
        filename = "stdin"
    else:
        path = Path(args.input)
        if not path.exists():
            print(f"Файл не найден: {args.input}", file=sys.stderr)
            sys.exit(1)
        content = path.read_text(encoding="utf-8", errors="replace")
        filename = path.name

    engine = Aether()

    if args.audit:
        report = engine.audit_ai(content, filename)
        if args.report:
            md = engine.generate_report_md(report)
            Path(args.report).write_text(md, encoding="utf-8")
            print(f"Отчёт сохранён: {args.report}")

        if args.json or not HAS_RICH:
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return

        console.print(Panel(
            f"[bold]AETHER AI Auditor[/bold]\n{report['summary']}\nOverall: [bold]{report['overall']}/100[/bold]",
            title=filename
        ))
        table = Table(title="Scores")
        table.add_column("Criterion", style="cyan")
        table.add_column("Score", justify="right")
        for k, v in report["scores"].items():
            color = "green" if v >= 80 else "yellow" if v >= 60 else "red"
            table.add_row(k, f"[{color}]{v}[/{color}]")
        console.print(table)
        console.print(f"Tokens (est.): {report['estimated_tokens']}  |  Chars: {report['length_chars']}")

        if report["issues"]:
            console.print(Panel("\n".join(f"• {i}" for i in report["issues"]), title="Issues", border_style="yellow"))
        if report["recommendations"]:
            console.print(Panel("\n".join(f"• {r}" for r in report["recommendations"]), title="Recommendations", border_style="green"))
        if report["risks"]:
            console.print(Panel("\n".join(f"• {r}" for r in report["risks"]), title="Risks", border_style="red"))
        if report.get("improved_template"):
            console.print(Panel(report["improved_template"], title="Suggested Structure", border_style="blue"))
        return

    # Normal mode
    root = engine.process(content, filename)
    if args.json:
        print(json.dumps(root.to_dict(), ensure_ascii=False, indent=2))
    else:
        meta = root.meta
        print(json.dumps({
            "domain": meta.get("domain"),
            "particles": meta.get("particle_count"),
            "depth": meta.get("depth"),
            "engineering": meta.get("engineering"),
        }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
