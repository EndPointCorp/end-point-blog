#!/usr/bin/env python3

import sys

if sys.version_info[0] < 3 or (sys.version_info[0] == 3 and sys.version_info[1] < 6):
    print('This program requires Python 3.6 or newer.')
    sys.exit(1)


from urllib3.exceptions import InsecureRequestWarning
import subprocess
import warnings as warnings_module
import argparse
import requests
import json
import os
import re

import yaml

####################
# Global variables #
####################

tried_links = {}

####################
# Script arguments #
####################


parser = argparse.ArgumentParser(description='Lint blog posts.')
parser.add_argument('input_file', help='blog post file to read')
parser.add_argument('-k', dest='forKeepers', action='store_true', help='show verbose output for keepers of the blog')
parser.add_argument('-o', dest='offline', action='store_true', help='offline: don\'t check links')

args = parser.parse_args()

if not os.path.isfile(args.input_file):
    print(f'No such file: {args.input_file}')
    sys.exit(2)


##################################################
# Context manager for changing working directory #
##################################################


class cd:
    """Context manager for changing the current working directory, from https://stackoverflow.com/a/13197763"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


############################################
# Load list of languages supported by hljs #
############################################


bin_dir = os.path.dirname(os.path.realpath(__file__))

# Run `node update-hljs-list.js` to update

highlight_languages = []
with cd(bin_dir):
    highlight_languages += json.load(open('supported_languages.json', 'r'))


######################################
# Classes for error/warning messages #
######################################


class Warning:
    def __init__(self, line, message, forKeepers=False):
        self.line = line
        self.message = message
        self.forKeepers = forKeepers

    def __str__(self):
        if type(self.line) == Line:
            return args.input_file + ':' + str(self.line.number + 1) + ': \t' + self.message
        else:
            return self.line + ': \t\t' + self.message

    def __hash__(self):
        return hash((self.line, self.message))

    def __lt__(self, other):
        if type(self.line) != Line:
            return True
        else:
            if type(other.line) == Line:
                return self.line.number < other.line.number
            else:
                return False

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
        raise Exception('No matching line found')


##############################################
# Helper function to separate code and prose #
##############################################


def extract_code_blocks(block):
    matching_indices = []

    for index, line in enumerate(block.lines):
        if re.match(r' *```', line.line):
            matching_indices.append(index)

    if len(matching_indices) % 2 != 0:
        raise Exception('Found an odd number of matches!')

    # Start from end so we don't have to worry about indices changing
    matching_indices = sorted(matching_indices, reverse=True)
    out = []

    for b, a in zip(*[iter(matching_indices)]*2):
        out.append(Block(block.lines[a:b+1]))
        del block.lines[a:b+1]

    return out


##########################
# Initialize error lists #
##########################


errors = set()
warnings = set()


#####################
# Check image sizes #
#####################


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
                    errors.add(Warning(entry.path, 'File is too big (> 300 kB): ' + entry.name, True))
                elif file_size > (1024 * 200):
                    warnings.add(Warning(entry.path, 'File is pretty big (> 200 kB): ' + entry.name, True))
except:
    pass


#################################
# Open post file and split body #
#################################


infile = open(args.input_file)
data = infile.read()

post = Block(data)

body_index = post.find_line_index(r'^---$', 2) + 1

frontmatter = Block(post.lines[:body_index])
body = Block(post.lines[body_index:])

frontmatter_string = ''

for line in frontmatter.lines:
    if line.line != '---':
        frontmatter_string += line.line
        frontmatter_string += '\n'

frontmatter_yaml = yaml.safe_load(frontmatter_string)


#####################
# Check frontmatter #
#####################


try:
    bin_dir = os.path.dirname(os.path.realpath(__file__))
    all_tags = []
    result = None
    with cd(bin_dir):
        result = subprocess.run('./show-blog-tags -s | grep -v \'^ *1 \' | sed \'s/ *[[:digit:]]* //\'', shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    all_tags = result.stdout.decode('utf-8').split('\n')

    tags = frontmatter_yaml.get('tags', [])

    if tags is None or len(tags) < 1:
        errors.add(Warning(frontmatter.lines[0], 'No tags specified'))
    else:
        tag_line = frontmatter.lines[0]

        for line in frontmatter.lines:
            if line.line.startswith('tags:'):
                tag_line = line

        if len(tags) == 0:
            errors.add(Warning(tag_line, 'No tags specified'))
        for tag in tags:
            if tag not in all_tags:
                warnings.add(Warning(tag_line, 'No other occurences of tag "' + tag + '" in blog'))
except:
    print('There was an error checking tags')

try:
    response = None

    try:
        response = requests.get('https://www.endpointdev.com/blog/authors/index.json', headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
            })
    except Exception as error:
        print(error)

    all_authors = json.loads(response.text)

    author_line = None
    for line in frontmatter.lines:
        if line.line.startswith('author: '):
            author_line = line

    author_name = author_line.line[8:].strip().strip('"').strip("'")

    if not author_name in all_authors:
        warnings.add(Warning(author_line, "Unrecognized author; please double check spelling if this isn't their first post"))
except Exception as err:
    print('There was an error getting the list of blog post authors: ', err)

try:
    image_line = None
    for line in frontmatter.lines:
        if line.line.startswith('  image_url: '):
            image_line = line

    if image_line is None:
        errors.add(Warning(frontmatter.lines[0], 'No featured image specified'))
except Exception as err:
    print('There was an error checking for a featured image: ', err)


###############
# Code blocks #
###############


code_blocks = extract_code_blocks(body)

for b in code_blocks:
    # Check that code blocks are only being used on their own
    if re.match(r'^[^` ]+```', b.lines[0].line):
        errors.add(Warning(b.lines[0], 'Code blocks should be used only as their own paragraphs'))
        continue

    # Check that a language is specified
    lang = re.sub(r'^ *```', '', b.lines[0].line).rstrip()
    if lang not in highlight_languages:
        errors.add(Warning(b.lines[0], "Code blocks should specify a valid language or 'plain'. Example: ```python"))

    has_tabs = False
    smallest_indent = None
    left_margin = len(b.lines[0].line) - len(b.lines[0].line.lstrip(' '))

    # Check indentation level and whether tabs are used
    for l in b.lines:
        has_tabs = has_tabs or bool(l.line.find('\t') >= 0)

        indent = len(l.line) - len(l.line.lstrip(' ')) - left_margin

        if (smallest_indent is None or indent < smallest_indent) and not l.line.lstrip(' ').startswith('```'):
            smallest_indent = indent
    if smallest_indent and smallest_indent != 0:
        errors.add(Warning(b.lines[0], 'Code blocks should be flush with left margin'))
    if has_tabs:
        warnings.add(Warning(b.lines[0], 'Code blocks should not contain tabs; use spaces instead'))


###################
# Spelling checks #
###################


def check_spellings(line):
    before_checks = [
        {
            'regex': r'\s+$',
            'ideal': '',
            'message': "Remove whitespace at end of line",
            'forKeepers': True,
        },
    ]

    after_checks = [
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
            'regex': r'[^\s]/[^\u200b]',
            'ideal': '',
            'message': "Add zero-width breaking space after / between words",
            'forKeepers': True,
            'skip': r''
        },
        {
            'regex': r'\d-\d',
            'ideal': '',
            'message': "Use en dashes for ranges",
            'forKeepers': True,
        },
        {
            'regex': r'--',
            'ideal': '',
            'message': "Use em dashes in prose",
            'forKeepers': True,
        },
        {
            'regex': r'^##?[^#]',
            'ideal': '',
            'message': "No headings larger than ###"
        },
        {
            'regex': r'^######+',
            'ideal': '',
            'message': "No headings smaller than #####"
        },
        {
            'regex': r'(__[^_ ]*__|\*\*[^* ]*\*\*)',
            'ideal': '',
            'message': "Consider using italics instead of single bolded words",
            'forKeepers': True,
        },
        {
            'regex': r'&(?!amp|gt|lt)[^;]*;',
            'ideal': '',
            'message': 'Use HTML entities only for <>&',
            'forKeepers': True,
        }
    ]

    for c in before_checks:
        has_typo = False
        for match in re.findall(c['regex'], line.line, flags=c['flags'] if 'flags' in c else 0):
            if match != c['ideal']:
                has_typo = True
        if has_typo:
            errors.add(Warning(line, c['message'], c['forKeepers'] if 'forKeepers' in c else False))


    without_code = re.sub(r'`[^`]+`', '', line.line)
    without_html = re.sub(r'<.*?>', '', without_code)
    without_links = re.sub(r'\[([^\]]*)\]\([^\)]*\)', r'\1', without_html)

    if re.match(r'^\s*$', without_links):
        # Nothing of interest on this line
        return
    for c in after_checks:
        has_typo = False
        if len(without_html) == 0 and len(line.line) > 0:
            warnings.add(Warning(line, 'Code blocks on their own lines should use ```'))
        for match in re.findall(c['regex'], without_links, flags=c['flags'] if 'flags' in c else 0):
            if match != c['ideal']:
                has_typo = True
        if has_typo:
            errors.add(Warning(line, c['message'], c['forKeepers'] if 'forKeepers' in c else False))


###############
# Link checks #
###############



def check_links(line):
    link_checks = [
        {
            'regex': r'^https://www\.endpointdev\.com',
            'ideal': '',
            'message': 'Links to End Point Dev website should be relative links',
            'forKeepers': True
        },
        # This next one might be unnecessary since fetching it will reveal issues
        {
            'regex': r'^https://[^.]*\.endpointdev\.com',
            'ideal': ['https://www.endpointdev.com'],
            'message': 'No subdomains for endpointdev.com should be used',
        }
    ]

    without_code = re.sub(r'`[^`]+`', '', line.line)
    links = re.findall(r'\[[^\]]*\]\((.*?(?<!\\))\)', without_code)
    links += (re.findall(r'href="([^"]*)"', without_code))

    for link in links:

        url_base = 'https://www.endpointdev.com'
        check_certs = True
        match = re.search(r'\/camp([0-9]{1,2})\/', os.getcwd())
        if match:
            url_base = f'https://www.{match.group(1)}.camp.endpoint.com:91{int(match.group(1)):02d}'
            check_certs = False

        # Remove '\' markdown escape characters
        to_try = link.replace('\\', '')

        if link.startswith('#') or link.startswith('mailto:'):
            continue
        if link.startswith('/'):
            to_try = url_base + link
        if to_try in tried_links:
            warnings.add(Warning(line, f'Duplicate link {to_try}'))
            continue

        print('Trying ', to_try, '...', end=' ', flush=True)

        try:
            if not check_certs:
                requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

            response = requests.get(to_try, allow_redirects=False, verify=check_certs, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
                })

            if not check_certs:
                warnings_module.resetwarnings()

            tried_links[to_try] = response.status_code

            end_sequence = '\n' if args.forKeepers else '\x1b[1K\r'

            if response.status_code == 200:
                print('200 OK', end=end_sequence)
                pass
            elif response.status_code >= 300 and response.status_code < 400:
                print(response.status_code, end=end_sequence)
                warnings.add(Warning(line, f'Link {to_try} resulted in HTTP {response.status_code}, location {response.headers["Location"]}', True))
            else:
                print(response.status_code, end=end_sequence)
                errors.add(Warning(line, f'Link {to_try} resulted in HTTP {response.status_code}', True))
        except Exception as error:
            errors.add(Warning(line, f"Link {to_try} couldn't be reached: {str(error)}", True))

        for c in link_checks:
            has_issue = False
            for match in re.findall(c['regex'], link, flags=c['flags'] if 'flags' in c else 0):
                if (
                    (type(c['ideal']) is str and match != c['ideal']) or
                    (type(c['ideal']) is list and match not in c['ideal'])
                    ):
                    has_issue = True
            if has_issue:
                errors.add(Warning(line, c['message'], c['forKeepers'] if 'forKeepers' in c else False))


##########################################################
# Run the checks and print resulting errors and warnings #
##########################################################


for line in body.lines:
    if not args.offline:
      check_links(line)
    check_spellings(line)

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
        if not warning.forKeepers:
            print(warning)
            continue

        if args.forKeepers:
            print(warning)

infile.close()
