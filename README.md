Readable Markdown in the Terminal
=================================

### Usage

python readmd.py [-w size] [file ...]

Pass in a markdown file or multiple markdown files to be converted into pretty-printed markdown and sent to STDOUT. The output will be able to generate the same HTML output as the original markdown file, but it gains the ability of being more readable as plain-text.

If no files are given, `README.md` is used as the default.

The width option (-w size) can be used to specify how many characters wide a line can be (-1 for infinitely wide). If the option is excluded, the output will default to fit the width of the current terminal.

### Use Cases

This script can be used to:

* Easily read any markdown file in your terminal
* Pretty-print your github README.md file for other peoples' pleasure

### Features

* Pretty-prints markdown that will generate the same markup as the original markdown
* Handles all special elements in markdown (headers, lists, block quote, code blocks, horizontal rules)
* Formats sub-elements, e.g., a list within a blockquote
* Converts numbers in ordered lists to properly ascend from one
* Idempotent

### Examples

Read a README.md file from a github project in your terminal:

    python readmd.py

Convert your own readme into a pretty-printed one width of 80 characters:

    python readmd.py -w 80 README.md > README.md.new
    mv README.md{.new,}

---


### TODO

- add tests
- make infinite width mode syntax look less weird?
- add a simple way to configure stylistic preferences (or even add support for new elements)?
