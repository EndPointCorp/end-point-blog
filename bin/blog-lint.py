#!/usr/bin/env python3

import sys

if sys.version_info[0] < 3 or (sys.version_info[0] == 3 and sys.version_info[1] < 6):
    print('This program requires Python 3.6 or newer.')
    sys.exit(1)

import argparse
import os
import re
import subprocess

parser = argparse.ArgumentParser(description='Lint blog posts.')
parser.add_argument('input_file', help='blog post file to read')
parser.add_argument('-o', dest='outfile', help='Make changes and write new version to given file')
parser.add_argument('-f', dest='force', action='store_true', help='force writing output file')

args = parser.parse_args()

if not os.path.isfile(args.input_file):
    print(f'No such file: {args.input_file}')
    sys.exit(2)

if args.outfile and not args.force and os.path.isfile(args.output_file):
    print(f'File exists: {args.output_file}')
    print("Use '-f' flag to overwrite")
    sys.exit(3)

highlight_languages = [
    "apache",
    "bash",
    "coffeescript",
    "cpp",
    "cs",
    "css",
    "diff",
    "haskell",
    "html",
    "http",
    "ini",
    "java",
    "javascript",
    "js",
    "json",
    "makefile",
    "markdown",
    "nginx",
    "no-highlight",
    "nohighlight",
    "objectivec",
    "perl",
    "php",
    "plain",
    "plaintext",
    "python",
    "r",
    "ruby",
    "scss",
    "shell",
    "sql",
    "text",
    "vim",
    "xml",
]

# Make a "Line" class that keeps track of its own line number

class Warning:
    def __init__(self, line, message):
        self.line = line
        self.message = message

    def __str__(self):
        if type(self.line) == Line:
            return args.input_file + ':' + str(self.line.number + 1) + ': \t' + self.message
        else:
            return self.line + ': \t\t' + self.message
    
    def __hash__(self):
        return hash((self.line, self.message))

    def __lt__(self, other):
        if type(self.line) == Line:
            if type(other.line) == Line:
                return True
            else:
                return True
        else:
            if type(other.line) == Line:
                return False
            else:
                return self.line.number < other.line.number

    def __eq__(self, other):
        return self.line == other.line and self.message == other.message

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

class cd:
    """Context manager for changing the current working directory, from https://stackoverflow.com/a/13197763"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

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

errors = set()
warnings = set()

# Check image sizes

file_path = args.input_file
path_parts = file_path.split('/')
dir_name = ''
if len(path_parts) == 1:
    # We must be in same directory as .html.md file
    dir_name = file_path[:-8]
else:
    dir_name = path_parts[-1][:-8]
    dir_name = path_parts[:-1] + [dir_name]

try:
    with os.scandir(dir_name) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                file_size = os.path.getsize(entry.path)
                if file_size > (1024 * 300):
                    errors.add(Warning(entry.path, 'File is too big (> 300 kB): ' + entry.name))
                elif file_size > (1024 * 200):
                    warnings.add(Warning(entry.path, 'File is pretty big (> 200 kB): ' + entry.name))
except:
    pass


infile = open(args.input_file)
data = infile.read()

post = Block(data)

body_index = post.find_line_index(r'^---$', 2) + 1

header = Block(post.lines[:body_index])
body = Block(post.lines[body_index:])

# Header

try:
    bin_dir = os.path.dirname(os.path.realpath(__file__))
    all_tags = []
    result = None
    with cd(bin_dir):
        result = subprocess.run('./show-blog-tags -s', shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    all_tags = result.stdout.decode('utf-8').split('\n')

    tag_line = None
    for line in header.lines:
        if line.line.startswith('tags: '):
            tag_line = line

    if tag_line is None:
        errors.add(Warning(header.lines[0], 'No tags specified'))
    else:
        tags = tag_line.line[5:].strip().split(',')
        tags = list(map(lambda t: t.strip(), tags))
        tags = list(filter(lambda t: t != '', tags))

        if len(tags) == 0:
            errors.add(Warning(tag_line, 'No tags specified'))
        for tag in tags:
            if tag not in all_tags:
                warnings.add(Warning(tag_line, 'No other occurences of tag "' + tag + '" in blog'))
except:
    print('There was an error checking tags')

# Body

code_blocks = extract_code_blocks(body)

for b in code_blocks:
    # Check that code blocks are only being used on their own
    if re.match(r'^[^`]+```', b.lines[0].line):
        errors.add(Warning(b.lines[0], 'Code blocks should be used only as their own paragraphs'))
        continue

    # Check that a language is specified
    lang = re.sub(r'^```', '', b.lines[0].line).rstrip()
    if lang not in highlight_languages:
        errors.add(Warning(b.lines[0], "Code blocks should specify a valid language or 'plaintext'. Example: ```python"))

    has_tabs = False
    smallest_indent = None

    # Check indentation level and whether tabs are used
    for l in b.lines:
        has_tabs = has_tabs or bool(re.match(r'.*\t.*', l.line))
        indent = len(l.line) - len(l.line.lstrip(' '))
        if (smallest_indent is None or indent < smallest_indent) and not l.line.startswith('```'):
            smallest_indent = indent
    if smallest_indent and smallest_indent > 0:
        errors.add(Warning(b.lines[0], 'Code blocks should be flush with left margin'))
    if has_tabs:
        warnings.add(Warning(b.lines[0], 'Code blocks should not contain tabs; use spaces instead'))

def check_spelling(line, checks):
    without_code = re.sub(r'`[^`]*`', '', line.line)
    without_html = re.sub(r'<.*?>', '', without_code)
    for c in checks:
        has_typo = False
        if len(without_html) == 0 and len(line.line) > 0:
            warnings.add(Warning(line, 'Code blocks on their own lines should use ```'))
        for match in re.findall(c['regex'], without_html, flags=c['flags']):
            if match != c['ideal']:
                has_typo = True
        if has_typo:
            errors.add(Warning(line, c['message']))

spelling_checks = [
    {
        'regex': r'javascript',
        'ideal': 'JavaScript',
        'flags': re.IGNORECASE,
        'message': 'JavaScript spelled wrong',
    },
    {
        'regex': r'node\.?js',
        'ideal': 'Node.js',
        'flags': re.IGNORECASE,
        'message': 'Node.js spelled wrong',
    },
    {
        'regex': r"'",
        'ideal': '’',
        'flags': 0,
        'message': "Use typographers’ apostrophe",
    },
    {
        'regex': r'\"',
        'ideal': '”',
        'flags': 0,
        'message': "Use typographers’ quotes",
    },
    {
        'regex': r'[^\s]/[^\s]',
        'ideal': '',
        'flags': 0,
        'message': "Add zero-width breaking space after / between words"
    },
    {
        'regex': r'\s+$',
        'ideal': '',
        'flags': 0,
        'message': "Remove whitespace before end of line"
    },
    {
        'regex': r'\d-\d',
        'ideal': '',
        'flags': 0,
        'message': "Use en dashes for ranges"
    },
    {
        'regex': r'--',
        'ideal': '',
        'flags': 0,
        'message': "Use em dashes in prose"
    },
    {
        'regex': r'^##?[^#]',
        'ideal': '',
        'flags': 0,
        'message': "No headings larger than ###"
    },
    {
        'regex': r'^######+',
        'ideal': '',
        'flags': 0,
        'message': "No headings smaller than #####"
    },
    {
        'regex': r'(__[^_ ]*__|\*\*[^* ]*\*\*)',
        'ideal': '',
        'flags': 0,
        'message': "Consider using italics instead of single bolded words"
    },
]

for line in body.lines:
    check_spelling(line, spelling_checks)

if len(errors) > 0:
    errors = sorted(errors)
    print('Errors:') 
    for error in errors:
        print(error)
    print('')

if len(warnings) > 0:
    warnings = sorted(warnings)
    print('Warnings:') 
    for warning in warnings:
        print(warning)
