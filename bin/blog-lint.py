#!/usr/bin/env python3
import sys

if not sys.version.startswith('3'):
    print('This script requires Python 3.')
    sys.exit()

import argparse

parser = argparse.ArgumentParser(description='Lint blog posts.')
parser.add_argument('input_file', help='blog post file to read')

args = parser.parse_args()

import os
if not os.path.isfile(args.input_file):
    print(f'No such file: {args.input_file}')
    sys.exit()

import re

highlight_languages = [
    "ruby",
    "apache",
    "plaintext",
    "scss",
    "javascript",
    "perl",
    "cpp",
    "nginx",
    "xml",
    "markdown",
    "python",
    "ini",
    "diff",
    "http",
    "sql",
    "bash",
    "json",
    "java",
    "cs",
    "vim",
    "makefile",
    "objectivec",
    "shell",
    "php",
    "haskell",
    "coffeescript",
    "r",
    "css",
]

# Make a "Line" class that keeps track of its own line number

class Warning:
    def __init__(self, line, message):
        self.line = line
        self.message = message

    def __str__(self):
        return args.input_file + ':' + str(self.line.number) + ': \t' + self.message
        #return str(self.line.number) + ':\t' + self.line.line + '\n\t' + self.message

class Line:
    def __init__(self, line, number):
        self.line = line
        self.number = number

class Block:
    def __init__(self, lines):
        if type(lines) is str:
            self.lines = []
            for index, line in enumerate(lines.split('\n')):
                self.lines.append(Line(line, len(self.lines)))
        else:
            self.lines = lines

    def __str__(self):
        out = ""
        for index, line in enumerate(self.lines):
            out += str(line.number) + ":\t" + line.line + '\n'
        return out

    def num_lines(self):
        return len(self.lines)

    def split(self, regex, *args):
        res = []
        return (Block(self.lines[:index], self.start), Block(self.lines[index:], self.start + index))

    @staticmethod
    def merge(*args):
        lines = []
        for b in args:
            lines.extend(b.lines)
        out = Block(lines)
        out.lines = sorted(out.lines, key=lambda l: l.number)
        return out
        
    def find_line_index(self, regex, no=1):
        i = 0
        for index, line in enumerate(self.lines):
            if re.match(regex, line.line):
                i += 1
                if i == no:
                    return index
        raise Error('No matching line found')

def extract_code_blocks(block):
    matching_indices = []

    for index, line in enumerate(block.lines):
        if re.match(r'```', line.line):
            matching_indices.append(index)

    if len(matching_indices) % 2 != 0:
        raise Error('Found an odd number of matches!')

    # Start from end so we don't have to worry about indices changing
    matching_indices = sorted(matching_indices, reverse=True)
    out = []

    for b, a in zip(*[iter(matching_indices)]*2):
        out.append(Block(block.lines[a:b+1]))
        del block.lines[a:b+1]
    
    return out

#with open(args.input_file) as infile:
errors = []
warnings = []
infile = open(args.input_file)
data = infile.read()

post = Block(data)

body_index = post.find_line_index(r'^---$', 2) + 1

header = Block(post.lines[:body_index])
body = Block(post.lines[body_index:])

code_blocks = extract_code_blocks(body)

for b in code_blocks:
    # Check that code blocks are only being used on their own
    if re.match(r'^[^`]+```', b.lines[0].line):
        errors.append(Warning(b.lines[0], 'Code blocks should be used only as their own paragraphs'))
        continue

    # Check that a language is specified (or "plaintext")
    lang = re.sub(r'^```', '', b.lines[0].line).rstrip()
    if lang not in highlight_languages:
        errors.append(Warning(b.lines[0], "Code blocks should specify a valid language or 'plaintext'. Example: ```python"))

    has_tabs = False
    largest_indent = None

    # Check indentation level and whether tabs are used
    for l in b.lines:
        has_tabs = has_tabs or bool(re.match(r'.*\t.*', l.line))
        indent = len(l.line) - len(l.line.lstrip(' '))
        if largest_indent is None or indent > largest_indent:
            largest_indent = indent
    if largest_indent and largest_indent > 0:
        errors.append(Warning(b.lines[0], 'Code blocks should be flush with left margin'))
    if has_tabs:
        warnings.append(Warning(b.lines[0], 'Code blocks should not contain tabs, use spaces instead'))

def check_spelling(line, c):
    has_typo = False
    without_code = re.sub(r'`[^`]*`', '', line.line)
    for match in re.findall(c['regex'], without_code, flags=c['flags']):
        if match != c['ideal']:
            has_typo = True
    if has_typo:
        errors.append(Warning(line, c['message']))

spelling_checks = [
    {
        'regex': r'javascript',
        'ideal': 'JavaScript',
        'flags': re.IGNORECASE,
        'message': 'JavaScript spelled wrong'
    },
    {
        'regex': r'node\.?js',
        'ideal': 'Node.js',
        'flags': re.IGNORECASE,
        'message': 'Node.js spelled wrong'
    },
    {
        'regex': r"'",
        'ideal': '’',
        'flags': 0,
        'message': "Use typographer's quotes"
    }
]

for line in body.lines:
    for c in spelling_checks:
        check_spelling(line, c)

#merged = Block.merge(body, code)


if len(errors) > 0:
    errors = sorted(errors, key=lambda e: e.line.number)
    print('Errors:') 
for error in errors:
    print(error)

print('')

if len(warnings) > 0:
    warnings = sorted(warnings, key=lambda w: w.line.number)
    print('Warnings:') 
for warning in warnings:
    print(warning)
