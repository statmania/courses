#!/usr/bin/env python3
"""One-off importer: turns blog posts (smroot/blograw/posts/c-*.qmd) into course lessons.

Course-owned (not part of the kit). Re-running overwrites modules/<m>/<lesson>.qmd bodies,
so only re-run it before hand-editing lessons.
"""
import re
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
BLOG = (ROOT / "../../smroot/blograw").resolve()
POSTS = BLOG / "posts"

# module slug -> (title, description, [(post, lesson slug, kind, objectives)])
MODULES = {
    "start": ("Getting Started", "Write, compile and run your first C programs.", [
        ("c-hello-world-explained", "hello-world", "read", [
            "Explain every line of the classic Hello, World! program",
            "Compare C's structure with Python and R"]),
        ("c-test-code-quickly", "test-code-quickly", "read", [
            "Build and run a C file with one gcc command",
            "Choose a fast way to try small snippets"]),
    ]),
    "data": ("Variables and Data Types", "Declare variables and choose the right numeric type.", [
        ("c-declare-multiple-variables-in-one-line", "declare-variables", "read", [
            "Declare and initialise several variables in one statement",
            "Avoid the pointer-asterisk and partial-initialisation traps"]),
        ("c-double-vs-float", "float-vs-double", "read", [
            "Compare float and double in size, precision and range",
            "Use the right literals and format specifiers"]),
    ]),
    "operators": ("Operators and Input", "Increment operators and reading input safely.", [
        ("c-pre-vs-post-increment", "increment", "read", [
            "Tell ++i from i++ and say what each expression returns",
            "Know when the difference matters"]),
        ("c-validate-user-input", "validate-input", "code", [
            "Check scanf's return value",
            "Validate whole-number input with fgets and strtol"]),
    ]),
    "conditions": ("Making Decisions", "Branch with if, the ternary operator and switch.", [
        ("c-nested-if-explained-with-examples", "nested-if", "read", [
            "Predict when an inner if runs",
            "Trace a nested decision with a flowchart"]),
        ("c-shortcut-if-else-ternary", "ternary", "read", [
            "Write an if-else as one expression with ?:",
            "Use other if shortcuts safely"]),
        ("c-switch", "switch", "read", [
            "Write a switch with break and default",
            "Use fall-through deliberately",
            "Choose between switch and if / else if"]),
    ]),
    "loops": ("Loops", "Repeat work with while, do-while and for, then practise.", [
        ("c-do-while", "do-while", "read", [
            "Explain why a do-while body runs at least once",
            "Choose between while and do-while"]),
        ("c-break-statement-in-while-loop", "break", "read", [
            "Separate a loop's planned exit from break",
            "Apply break to search, sentinel, retry and menu loops"]),
        ("c-print-comma-separated-list", "print-lists", "code", [
            "Print a list with no trailing comma",
            "Use newlines to print rows of numbers"]),
        ("c-while-loop-practice-problems", "while-practice", "lab", [
            "Solve five while-loop problems",
            "Check your work against hints and solutions"]),
        ("c-5-for-loop-practice-problems-with-answers", "for-practice", "lab", [
            "Solve five for-loop problems",
            "Check your work against hints and solutions"]),
        ("c-nested-for-loop-practice-problems", "nested-for-practice", "lab", [
            "Draw patterns with nested for loops",
            "Explain how the outer and inner loops interact"]),
    ]),
    "data-structures": ("Arrays and Structs", "Store many values, and group related ones.", [
        ("c-save-loop-in-array", "arrays-from-loops", "code", [
            "Fill a fixed-size array from a loop",
            "Grow an array with malloc and realloc"]),
        ("c-struct", "structs", "read", [
            "Group different types into one struct",
            "Use arrays of structs, typedef and ->",
            "Compare structs with Python dicts and R lists"]),
    ]),
    "random": ("Random Numbers", "Generate and analyse random values.", [
        ("c-srand-time-null", "srand", "read", [
            "Explain why rand() repeats without a seed",
            "Seed the generator once with srand(time(NULL))"]),
        ("c-die-throw", "die-throw", "code", [
            "Simulate tossing a die until a 6 appears",
            "Store the history in an array and tally frequencies"]),
    ]),
}


def split(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    return yaml.safe_load(m.group(1)), m.group(2)


def relink(body, mslug, where):
    """Point links to other posts at their lesson pages; unlink posts not in the course."""
    def fix(m):
        text, post = m.group(1), m.group(2)
        if post in where:
            m2, l2 = where[post]
            target = f"{l2}.qmd" if m2 == mslug else f"../{m2}/{l2}.qmd"
            return f"[{text}]({target})"
        return text
    return re.sub(r"\[([^\]]+)\]\(([\w-]+)\.(?:qmd|html)\)", fix, body)


def main():
    where = {p: (m, l) for m, (_, _, ls) in MODULES.items() for p, l, _, _ in ls}
    used = set()
    nav = []
    for mslug, (mtitle, mdesc, lessons) in MODULES.items():
        mdir = ROOT / "modules" / mslug
        mdir.mkdir(parents=True, exist_ok=True)
        (mdir / "index.qmd").write_text(
            f'---\ntitle: "{mtitle}"\ndescription: "{mdesc}"\n---\n\n'
            f"{{{{< include ../../_generated/{mslug}.md >}}}}\n", encoding="utf-8")
        items = []
        for post, lslug, kind, objectives in lessons:
            meta, body = split((POSTS / f"{post}.qmd").read_text(encoding="utf-8"))
            for img in re.findall(r"\.\./img/([\w.-]+)", body):
                shutil.copy(BLOG / "img" / img, ROOT / "media" / img)
                used.add(img)
            body = body.replace("](../img/", "](../../media/")
            body = relink(body, mslug, where)
            words = len(re.sub(r"```.*?```", "", body, flags=re.S).split())
            code = len(re.findall(r"^```", body, re.M)) // 2
            minutes = max(5, round((words / 180 + code * 0.5) / 5) * 5)
            fm = {
                "title": meta["title"],
                "description": meta["description"],
                "minutes": minutes,
                "kind": kind,
                "objectives": objectives,
            }
            out = "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=1000) + "---\n" + body
            (mdir / f"{lslug}.qmd").write_text(out, encoding="utf-8")
            items.append(f"modules/{mslug}/{lslug}.qmd")
            for link in re.findall(r"\]\((?!https?:|#|\.\./\.\./media)([^)]+)\)", body):
                print(f"check link in {lslug}: {link}", file=sys.stderr)
        nav.append((mslug, mtitle, items))
    print("\n".join(
        f'      - section: "{t}"\n        href: modules/{s}/index.qmd\n        contents:\n'
        + "\n".join(f"          - {i}" for i in items) for s, t, items in nav))


main()
