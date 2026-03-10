#!/usr/bin/env python3
"""lorem - Generate placeholder text.

One file. Zero deps. Fills space.

Usage:
  lorem.py                        → 1 paragraph
  lorem.py 3                      → 3 paragraphs
  lorem.py words 50               → 50 words
  lorem.py sentences 10           → 10 sentences
  lorem.py chars 280              → exactly 280 characters
  lorem.py list 5                 → bullet list
  lorem.py html 3                 → HTML paragraphs
"""

import argparse
import random
import sys

WORDS = """lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod
tempor incididunt ut labore et dolore magna aliqua ut enim ad minim veniam quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat duis
aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat
nulla pariatur excepteur sint occaecat cupidatat non proident sunt in culpa qui
officia deserunt mollit anim id est laborum amet adipisicing consequuntur blanditiis
praesentium voluptatum deleniti atque corrupti quos dolores quas molestias excepturi
sint occaecati cupiditate provident similique accusantium nemo enim ipsam voluptatem
quia voluptas aspernatur aut odit fugit harum quidem rerum facilis expedita distinctio
nam libero tempore cum soluta nobis eligendi optio cumque nihil impedit quo minus
quod maxime placeat facere possimus omnis assumenda repudiandae temporibus autem
quibusdam officiis debitis necessitatibus saepe eveniet voluptates repudiandae
recusandae itaque earum hic tenetur sapiente delectus reiciendis maiores alias
perferendis doloribus asperiores repellat""".split()


def gen_sentence(min_words: int = 6, max_words: int = 15) -> str:
    n = random.randint(min_words, max_words)
    words = [random.choice(WORDS) for _ in range(n)]
    words[0] = words[0].capitalize()
    return ' '.join(words) + '.'


def gen_paragraph(min_sentences: int = 3, max_sentences: int = 7) -> str:
    n = random.randint(min_sentences, max_sentences)
    return ' '.join(gen_sentence() for _ in range(n))


def gen_words(count: int) -> str:
    words = [random.choice(WORDS) for _ in range(count)]
    words[0] = words[0].capitalize()
    # Add periods roughly every 10-15 words
    result = []
    since_period = 0
    for i, w in enumerate(words):
        result.append(w)
        since_period += 1
        if since_period >= random.randint(8, 14) and i < count - 1:
            result[-1] = result[-1] + '.'
            since_period = 0
            if i + 1 < count:
                words[i + 1] = words[i + 1].capitalize()
    if not result[-1].endswith('.'):
        result[-1] += '.'
    return ' '.join(result)


def gen_chars(count: int) -> str:
    text = ''
    while len(text) < count:
        text += gen_paragraph() + ' '
    return text[:count].rstrip() + '.'


def main():
    argv = sys.argv[1:]

    if not argv:
        print(gen_paragraph())
        return 0

    # Simple number = paragraphs
    if len(argv) == 1 and argv[0].isdigit():
        for i in range(int(argv[0])):
            if i > 0:
                print()
            print(gen_paragraph())
        return 0

    cmd = argv[0]
    count = int(argv[1]) if len(argv) > 1 else 5

    if cmd == 'words':
        print(gen_words(count))
    elif cmd == 'sentences':
        for _ in range(count):
            print(gen_sentence())
    elif cmd == 'chars':
        print(gen_chars(count))
    elif cmd == 'list':
        for _ in range(count):
            print(f"- {gen_sentence()}")
    elif cmd == 'html':
        for _ in range(count):
            print(f"<p>{gen_paragraph()}</p>")
            print()
    elif cmd == 'markdown' or cmd == 'md':
        for i in range(count):
            if i > 0:
                print()
            print(gen_paragraph())
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        print("Commands: words, sentences, chars, list, html, md", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
