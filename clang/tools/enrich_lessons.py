#!/usr/bin/env python3
"""Adds the kit's right-rail content to every lesson: rail-links (front matter) and
.takeaways / .column-margin blocks (end of body). No cheat sheet: it overlapped the takeaways. Idempotent: re-running replaces front matter
keys and skips blocks that are already there. Course-owned."""
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CPP = "https://en.cppreference.com/w/c/"
G = "fa-book"


def L(title, path, icon=G):
    return {"title": title, "url": path if path.startswith("http") else CPP + path, "icon": icon}


# slug -> (takeaways, cheatsheet [(code, text)], links, glossary (term, definition))
D = {
    "hello-world": (
        ["Every C program starts running at `main`.", "`#include <stdio.h>` makes `printf` available.", "`return 0;` tells the system the program succeeded."],
        [("#include <stdio.h>", "Bring in input/output functions"), ("int main(void)", "Where the program starts"), ('printf("hi\\n");', "Print text; \\n is a new line"), ("return 0;", "Exit with success")],
        [L("printf reference", "io/fprintf"), L("GCC manual", "https://gcc.gnu.org/onlinedocs/gcc/Invoking-GCC.html", "fa-terminal")],
        ("Compiler", "A program that turns C source code into a program the computer can run, such as `gcc`."),
    ),
    "test-code-quickly": (
        ["`gcc file.c -o out && ./out` builds and runs in one line.", "Online compilers need no setup for tiny snippets.", "Add `-Wall -Wextra` to catch mistakes early."],
        [("gcc a.c -o a", "Compile a.c into program a"), ("./a", "Run it"), ("-Wall -Wextra", "Turn on useful warnings"), ("./a < in.txt", "Feed input from a file")],
        [L("GCC manual", "https://gcc.gnu.org/onlinedocs/gcc/Invoking-GCC.html", "fa-terminal"), L("OnlineGDB C compiler", "https://www.onlinegdb.com/online_c_compiler", "fa-globe")],
        ("Redirect", "`<` makes a program read its input from a file instead of the keyboard."),
    ),
    "declare-variables": (
        ["`int a, b, c;` declares three ints but initialises none.", "In `int *p, q;` only `p` is a pointer.", "Initialise each variable you declare."],
        [("int a, b, c;", "Three uninitialised ints"), ("int x = 5, y = 10;", "Each gets its own value"), ("int a = b = 0;", "Chained: b must exist already"), ("int *p, q;", "p is a pointer, q is an int")],
        [L("Declarations", "language/declarations"), L("Initialization", "language/initialization")],
        ("Initialisation", "Giving a variable its first value at the moment it is declared."),
    ),
    "float-vs-double": (
        ["`double` has about 15 to 16 digits of precision, `float` about 7.", "Neither stores 0.1 exactly.", "Default to `double`; literals like `3.14` are already doubles."],
        [("float", "4 bytes, about 7 digits"), ("double", "8 bytes, about 15 digits"), ("3.14f", "A float literal"), ("%f / %lf", "printf / scanf specifiers")],
        [L("Arithmetic types", "language/arithmetic_types"), L("Floating-point environment", "numeric/fenv")],
        ("Precision", "How many significant digits a type can keep before rounding changes the value."),
    ),
    "increment": (
        ["`++i` changes `i`, then returns the new value.", "`i++` returns the old value, then changes `i`.", "On its own line they do the same thing."],
        [("b = ++a;", "a becomes 6, b is 6"), ("y = x++;", "y is 5, x becomes 6"), ("i++;", "Standalone: same as ++i"), ("i += 1", "Add 1 explicitly")],
        [L("Increment and decrement", "language/operator_incdec"), L("Operator precedence", "language/operator_precedence")],
        ("Side effect", "A change to a variable made while an expression is evaluated, such as `i++`."),
    ),
    "validate-input": (
        ["`scanf` returns how many values it read; check it.", "Partial input like `12abc` slips past a plain `scanf`.", "`fgets` + `strtol` reports exactly where the number ends."],
        [("scanf(\"%d\", &n) == 1", "True if an int was read"), ("fgets(buf, n, stdin)", "Read a whole line"), ("strtol(s, &end, 10)", "Convert; end marks where it stopped"), ("*end == '\\n'", "Nothing left over: valid")],
        [L("scanf", "io/fscanf"), L("strtol", "string/byte/strtol")],
        ("Buffer", "A block of memory holding text before the program uses it, such as the line `fgets` reads."),
    ),
    "nested-if": (
        ["The inner `if` runs only when the outer condition is true.", "`&&` can replace a nest when there is no `else` between the checks.", "Use braces on every level."],
        [("if (a) { if (b) {...} }", "b is checked only when a is true"), ("if (a && b)", "Flat version of the same test"), ("else", "Pairs with the nearest if"), ("{ }", "Always add braces")],
        [L("if statement", "language/if")],
        ("Nesting", "Placing one statement inside another, such as an `if` inside an `if`."),
    ),
    "ternary": (
        ["`cond ? a : b` is an expression that picks a value.", "Use it for choosing a value, not for long branches.", "Parenthesise it inside bigger expressions."],
        [("max = a > b ? a : b;", "Larger of two values"), ("if (x) ...", "Any non-zero value is true"), ("(a > b)", "A comparison is 1 or 0"), ("printf(\"%s\", ok ? \"yes\" : \"no\")", "Choose text inline")],
        [L("Conditional operator", "language/operator_other")],
        ("Expression", "Code that produces a value, unlike a statement such as `if`."),
    ),
    "switch": (
        ["`switch` compares one integer or char against `case` labels.", "Without `break`, execution falls through to the next case.", "Always add a `default` case."],
        [("switch (x) { ... }", "Pick a case by value"), ("case 1: ... break;", "Run, then leave the switch"), ("default:", "No case matched"), ("case 'a': case 'b':", "Grouped cases")],
        [L("switch statement", "language/switch"), L("break statement", "language/break")],
        ("Fall-through", "Continuing into the next `case` because a `break` is missing."),
    ),
    "do-while": (
        ["The body of a `do-while` always runs at least once.", "The condition is tested after the body.", "Note the semicolon after `while (...)`."],
        [("do { ... } while (c);", "Run first, then test"), ("while (c) { ... }", "Test first, then run"), ("do-while", "Menus, retry prompts, PIN entry"), ("break;", "Leave the loop early")],
        [L("do-while loop", "language/do")],
        ("Sentinel", "A special input value, such as 0, that tells a loop to stop."),
    ),
    "break": (
        ["The condition is the planned exit; `break` is the special-case exit.", "`while (1)` with a `break` suits menus and retries.", "`break` leaves only the innermost loop."],
        [("break;", "Leave the loop now"), ("while (1)", "Endless loop, needs a break"), ("if (x == t) break;", "Stop on a match"), ("continue;", "Skip to the next pass")],
        [L("break statement", "language/break"), L("while loop", "language/while")],
        ("Innermost loop", "The loop closest around the `break`; outer loops keep running."),
    ),
    "print-lists": (
        ["Print the separator before every item except the first.", "A `first` flag always works, even for odd cases.", "Print `\\n` after the inner loop, not inside it."],
        [('printf("%d, ", i)', "Leaves a trailing comma"), ("if (i > 0) printf(\", \");", "Separator before items"), ("i ? \", \" : \"\"", "Ternary separator"), ('printf("\\n");', "End each row")],
        [L("printf reference", "io/fprintf")],
        ("Delimiter", "The text placed between items in a list, such as a comma and a space."),
    ),
    "while-practice": (
        ["Set up the counter before the loop and change it inside.", "A forgotten update is an infinite loop.", "`n % 10` is the last digit and `n / 10` removes it."],
        [("while (i <= 10)", "Repeat while true"), ("i++;", "Update the counter"), ("n % 10", "Last digit"), ("n /= 10;", "Drop the last digit")],
        [L("while loop", "language/while")],
        ("Loop counter", "A variable that changes each pass and eventually makes the condition false."),
    ),
    "for-practice": (
        ["`for (init; test; update)` packs the loop bookkeeping on one line.", "Pick `for` when you know how many passes you need.", "Use `long` or `unsigned long long` for large factorials."],
        [("for (i = 1; i <= n; i++)", "Count 1 to n"), ("i += 2", "Step by two"), ("product *= i;", "Accumulate a product"), ("next = a + b;", "Fibonacci step")],
        [L("for loop", "language/for")],
        ("Accumulator", "A variable that collects a running total or product through a loop."),
    ),
    "nested-for-practice": (
        ["The outer loop picks the row; the inner loop walks its columns.", "Print `\\n` after the inner loop finishes.", "Row and column numbers drive the pattern."],
        [("for (r...) for (c...)", "Rows, then columns"), ("c <= r", "Triangle: grow with the row"), ("(r + c) % 2", "Checkerboard test"), ('printf("\\n");', "After each row")],
        [L("for loop", "language/for")],
        ("Nested loop", "A loop inside another loop; the inner loop runs fully for each outer pass."),
    ),
    "arrays-from-loops": (
        ["Use the loop index to store each result: `a[i] = ...`.", "A fixed array needs its size known up front.", "`malloc` and `realloc` grow storage at run time."],
        [("int a[5];", "Five ints, indices 0 to 4"), ("a[i] = i * i;", "Store a result"), ("malloc(n * sizeof *p)", "Allocate n items"), ("realloc(p, m * sizeof *p)", "Resize; free(p) when done")],
        [L("Arrays", "language/array"), L("malloc", "memory/malloc")],
        ("Index", "A number that picks one element of an array; the first is 0."),
    ),
    "structs": (
        ["A struct groups fields of different types into one value.", "Use `.` on a struct and `->` on a pointer to one.", "`typedef` gives the struct a shorter name."],
        [("struct S { int id; };", "Declare a struct type"), ("s.id = 7;", "Access a field"), ("p->id", "Field through a pointer"), ("typedef struct {...} S;", "Name it once")],
        [L("Struct types", "language/struct")],
        ("Padding", "Unused bytes the compiler inserts between fields to keep them aligned."),
    ),
    "srand": (
        ["Without a seed, `rand()` repeats the same sequence every run.", "`srand(time(NULL))` seeds from the clock.", "Seed once, at the start of `main`, never inside a loop."],
        [("rand()", "Next pseudo-random int"), ("srand(seed);", "Set the starting point"), ("time(NULL)", "Seconds since 1970"), ("rand() % 6 + 1", "A die roll, 1 to 6")],
        [L("rand", "numeric/random/rand"), L("time", "chrono/time")],
        ("Seed", "The starting value of a pseudo-random generator; the same seed gives the same numbers."),
    ),
    "die-throw": (
        ["Store every roll in an array to analyse the run afterwards.", "A frequency array counts how often each face appeared.", "Index 1 to 6 means the array needs 7 slots."],
        [("rand() % 6 + 1", "A fair die"), ("freq[roll]++;", "Tally a face"), ("int freq[7] = {0};", "Slots 1 to 6 used"), ("while (roll != 6)", "Until a six appears")],
        [L("rand", "numeric/random/rand"), L("Arrays", "language/array")],
        ("Frequency", "How many times a value occurred in the data."),
    ),
}


def main():
    for f in sorted((ROOT / "modules").glob("*/*.qmd")):
        slug = f.stem
        if slug == "index":
            continue
        take, cheat, links, (term, definition) = D[slug]
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", f.read_text(encoding="utf-8"), re.S)
        meta, body = yaml.safe_load(m.group(1)), m.group(2)
        meta.pop("cheatsheet", None)
        meta["rail-links"] = links
        body = body.rstrip("\n") + "\n"
        if "{.takeaways}" not in body:
            body += "\n::: {.takeaways}\n" + "\n".join(f"- {t}" for t in take) + "\n:::\n"
        if "{.column-margin}" not in body:
            body += f"\n::: {{.column-margin}}\n**{term}.** {definition}\n:::\n"
        fm = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, width=1000)
        f.write_text(f"---\n{fm}---\n{body}", encoding="utf-8")
    print("enriched", len(D), "lessons")


main()
