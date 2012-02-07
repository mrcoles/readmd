Make Markdown Easier to Read as Plaintext
=========================================

For example, take this file:

    A markdown file
    ===

    1. This file is awesome
    1. It has contents
    1. Lorem ipsum dolor sit amet, vestibulum nulla nunc, enim pellentesque tempor, pretium proin in ligula, ac in. Suspendisse praesent pellentesque dis mollis maecenas, mattis vehicula. Morbi vestibulum morbi. Proin et facilisis aliquam lectus lorem, rutrum phasellus, duis semper sodales venenatis diam ad, sodales wisi wisi eget. Lobortis nonummy, blandit lectus elit egestas, id ut nullam, parturient minus lobortis.
    1. Integer ut nullam nonummy quam in, risus penatibus suspendisse, et per sodales sed libero vitae odio, pede quam, nibh sed per condimentum. Tincidunt massa dui. Nisl vitae, vulputate sit tempus. Praesent turpis interdum, eu sollicitudin odio cursus eleifend purus nam, porttitor ac pellentesque libero adipiscing rhoncus, ipsum pede urna. In torquent, volutpat nulla, ut nullam et in dolor praesent mollis, wisi adipiscing.

    > how cool?
    >
    >
    > so cool.

and convert it with this command `readmd -w=80 file.md` to:

    A markdown file
    ===============

    1.  This file is awesome
    2.  It has contents
    3.  Lorem ipsum dolor sit amet, vestibulum nulla nunc, enim pellentesque tempor,
        pretium proin in ligula, ac in. Suspendisse praesent pellentesque dis mollis
        maecenas, mattis vehicula. Morbi vestibulum morbi. Proin et facilisis
        aliquam lectus lorem, rutrum phasellus, duis semper sodales venenatis diam
        ad, sodales wisi wisi eget. Lobortis nonummy, blandit lectus elit egestas,
        id ut nullam, parturient minus lobortis.
    4.  Integer ut nullam nonummy quam in, risus penatibus suspendisse, et per
        sodales sed libero vitae odio, pede quam, nibh sed per condimentum.
        Tincidunt massa dui. Nisl vitae, vulputate sit tempus. Praesent turpis
        interdum, eu sollicitudin odio cursus eleifend purus nam, porttitor ac
        pellentesque libero adipiscing rhoncus, ipsum pede urna. In torquent,
        volutpat nulla, ut nullam et in dolor praesent mollis, wisi adipiscing.

    > how cool?
    >
    > so cool.

Furthermore, if you do not specify a width parameter, it will just default to
the width of your current screen.

### Use Cases

This script can be used to:

*   Easily read any markdown file in your terminal
*   Pretty-print your github README.md file for other peoples' pleasure

### Command-line Usage

Read a README.md file from a github project (in your current directory) in your
terminal:

    readmd | less

Convert your own readme into a pretty-printed one width of 80 characters:

    readmd -w=80 README.md README.md.new
    mv README.md{.new,}

Read something from standard in and save it as a file:

    cat some-file.md | readmd - some-pretty-file.md

### Details

*   Command-line Usage: readmd [-w=width] [input_file [output_file]]
*   Defaults to trying README.md if no file is specified
*   Defaults to width of current terminal if not width is specified
*   Specify a width of -1 to have the script bypass text wrapping
*   Pretty-prints markdown that will generate the same markup as the original
    markdown
*   Handles all special elements in markdown (headers, lists, block quote, code
    blocks, horizontal rules)
*   Formats sub-elements, e.g., a list within a blockquote
*   Converts numbers in ordered lists to properly ascend from one
*   Idempotent


### Installation

Install with `python setup.py install`

---

### TODO

-   add a simple way to configure stylistic preferences (or even add support for
    new elements)?
-   figure out if hr's should expand or not
-   figure out if sub-lists without extra line-break should be kept as sub-lists
