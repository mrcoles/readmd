#
# readmd
#
# magical code to parse your markdown and make it more readable from the commandline
# this *should* be lossless, i.e., the generated file should produce the same HTML as the original
#
# potentially useful for reading someone's README.md file in the terminal -- or formatting your own.
#

import re
import sys

try: import cStringIO as StringIO
except: import StringIO

MIN_WIDTH = 10
NUM_SPACES = 4
SPACES = ' ' * NUM_SPACES

# SPECIAL STATE TYPES
TYPE_HR = 1
TYPE_UL = 2
TYPE_OL = 3
TYPE_BLOCK = 4
TYPE_CODE = 5

# REGEX's for SPECIAL STATE TYPES
_atx_header = re.compile('^(#+)\s*')
_setext_header = re.compile('^(=+|-+)\s*$')
_hr = re.compile('^(([*\-_])\s*){3,}$')
_ul_indent = re.compile('^ {0,3}([*+\-*])\s\s*')
_ol_indent = re.compile('^ {0,3}\d+\.\s\s*')
_blockquote = re.compile('^>\s*')
_code = re.compile('^ {4,}[^ ]')

_indented = re.compile('^ {4,}')
_end_space = re.compile(' +$')

SPECIAL_TYPES = (
    (TYPE_HR, _hr), # must be before UL (or make the UL regex smarter)
    (TYPE_UL, _ul_indent),
    (TYPE_OL, _ol_indent),
    (TYPE_BLOCK, _blockquote),
    (TYPE_CODE, _code),
    )

def _increment_ol_state(state, prev_state=None):
    if prev_state is None: prev_state = state

    number = prev_state.get('number', 0) + 1
    prefix_first = '%s. ' % number
    while len(prefix_first) < 4: prefix_first += ' '
    state.update({
            'number': number,
            'prefix_first': prefix_first,
            })


## The goods.

def readmd(f, width=None, out=None):
    '''
    Make a markdown file more readable for humans.

    f - filelike object that supports .next() and StopIteration
    width - (optional) width to use, otherwise uses terminal width
    out - (optional) a file-like object to write output, otherwise output is returned
    '''
    if not width:
        dims = _getTerminalSize()
        width, height = dims or (80, 24)

    out_was_none = out is None

    if out_was_none:
        out = StringIO.StringIO()

    _groupify(f, width, out)

    if out_was_none:
        return out.getvalue()


def _groupify(f, width, out, indent=''):
    '''
    groups lines into different elements and renders them to out
    '''
    group = []                         # to group sections into different elements
    has_break = BooleanClass(False)    # to record line breaks
    forced_break = BooleanClass(False) # to handle headers auto-rendering

    # special for doing recursive rendering and doing `prefix_first` properly...
    first_render = BooleanClass(True)

    prev_state = {}
    state = {}

    # helper function to pass the right arguments into _render_group
    def _do_render_group(line_after=True):
        is_first_render = first_render
        _render_group(
            group,
            width,
            indent,
            is_first_render,
            prefix_first=state.get('prefix_first', ''),
            prefix_rest=state.get('prefix_rest', ''),
            line_after=line_after,
            is_pre=state.get('type') == TYPE_CODE,
            out=out,
            )

        is_first_render and first_render.set_false()
        has_break.set_false()
        forced_break.set_false()
        while len(group): group.pop()

    # main loop that goes through the file and parses it
    while True:
        try:
            line = f.next()
        except StopIteration, e:
            if group: _do_render_group(line_after=False)
            break
        else:
            line = line.strip('\n\r').expandtabs(NUM_SPACES) # lawl - that's a function! replace('\t', SPACES)

            # deal with empty line
            if not line.strip():
                if not forced_break and group:
                    has_break.set_true()

            # deal with setext header - make sure group exists, to prevent hrs from getting matched
            elif not has_break and _setext_header.match(line) and group:
                m = _setext_header.match(line)
                underline = m.groups()[0][0]
                above_line = group.pop() if group else ''

                if len(group) > 1:
                    group.pop()
                    _do_render_group()

                prev_state, state = state, {} # clear state
                group.append(above_line)
                _do_render_group(line_after=False)

                group.append(underline * len(above_line))
                _do_render_group()
                forced_break.set_true()

            # deal with atx header
            elif _atx_header.match(line):
                m = _atx_header.match(line)
                hashes = m.groups()[0].strip(' ')

                if group:
                    _do_render_group()

                prev_state, state = state, {} # clear state
                group.append('%s %s' % (hashes, line.strip('#').strip(' ')))
                _do_render_group()
                forced_break.set_true()

            # deal with non-empty line
            else:

                # clean up forced_break if we get to some content!
                forced_break.set_false()

                # check for continuations of special types
                was_continued = False
                state_type = state.get('type')

                if state_type in (TYPE_UL, TYPE_OL, TYPE_BLOCK, TYPE_CODE):

                    # any non-empty non-code line following code will break immediately
                    if TYPE_CODE == state_type:
                        if not _code.search(line):
                            _do_render_group()

                    # continuing an ol with a ul or vice versa will convert to prior type
                    elif state_type in (TYPE_UL, TYPE_OL):
                        ul_m = _ul_indent.search(line)
                        if ul_m or _ol_indent.search(line):
                            #TODO - maybe remember if first had break or not and do rest consistently?
                            _do_render_group(line_after=has_break)

                            line = (_ul_indent if ul_m else _ol_indent).sub('', line)
                            if TYPE_OL == state.get('type'): _increment_ol_state(state)
                            was_continued = True

                        elif _indented.search(line):

                            if has_break:
                                group.append('\n')
                                has_break.set_false()

                            line = _indented.sub('', line) # remove indent for proper parsing

                            if not line: has_break.set_true()
                            was_continued = True


                    # see if we can drop the blockquote symbol from the start of a
                    # continuation of a blockquoted region
                    elif TYPE_BLOCK == state_type:
                        if _blockquote.search(line):
                            if has_break:
                                group.append('\n')
                                has_break.set_false()
                            line = _blockquote.sub('', line)
                            if not line: has_break.set_true()
                            was_continued = True


                # non-empty line after a break - group it!
                if not was_continued and has_break:
                    if group: _do_render_group()

                group.append(line)


                # first non-empty line of a new group - identify it!
                if not was_continued and len(group) == 1:
                    match = None
                    for special_type, regex in SPECIAL_TYPES:
                        match = regex.search(line)
                        if match:
                            break

                    if match:
                        prev_state, state = state, {'type': special_type}

                        if TYPE_UL == special_type:
                            group[-1] = _ul_indent.sub('', group[-1])
                            bullet = match.groups()[0]
                            state.update({
                                    'prefix_first': '%s   ' % bullet,
                                    'prefix_rest': SPACES,
                                    })

                        elif TYPE_OL == special_type:
                            group[-1] = _ol_indent.sub('', group[-1])
                            _increment_ol_state(state, prev_state)
                            state['prefix_rest'] = SPACES

                        elif TYPE_BLOCK == special_type:
                            group[-1] = _blockquote.sub('', group[-1])
                            state.update({
                                    'prefix_first': '> ',
                                    'prefix_rest': '> ',
                                    })

                        elif TYPE_HR == special_type:
                            # this doesn't extend the line for now...
                            state['character'] = match.groups()[0]
                            has_break.set_true()

                        elif TYPE_CODE == special_type:
                            state.update({
                                    'prefix_first': SPACES,
                                    'prefix_rest': SPACES,
                                    })

                    else:
                        prev_state, state = state, {}



def _render_group(group, width, indent, is_first_render, prefix_first, prefix_rest, line_after, is_pre, out):
    '''
    Do the rendering of several lines that have been grouped together by
    a particular type of element, and recursively render sub-elements
    '''
    sections = []
    cur_section = ''
    relative_width = width if width == -1 else max(MIN_WIDTH, width - len(indent) - max(len(prefix_first), len(prefix_rest)))
    first_indent = '' if is_first_render else indent

    if is_pre:
        for i, line in enumerate(group):
            out.write('%s%s\n' % (first_indent if i == 0 else indent, line))

    else:

        # recursive call to allow rendering of special types within special types
        if prefix_first and prefix_rest:
            out.write(first_indent + (prefix_first[:-1] if prefix_first.endswith(' ') else prefix_first) + ' ')
            _groupify(iter(group), width, out, indent=indent + prefix_rest)

        # render that!
        else:
            num_lines = len(group)
            for i, line in enumerate(group):
                cur_section += ('' if i == 0 else ' ') + line.strip()

                if line.endswith('  ') or line == '\n' or i + 1 == num_lines:
                    sections.append(cur_section + ('  ' if line.endswith('  ') else ''))
                    cur_section = ''

                if line == '\n':
                    sections.append('') # add a whole other line for special case with line breaks

            num_sections = len(sections)
            for i, section in enumerate(sections):
                fitted_text = _fit_text(section, relative_width, with_break=(i + 1 < num_sections))
                for j, line in enumerate(fitted_text):
                    out.write('%s%s%s\n' % (first_indent if 0 == i == j else indent,
                                               prefix_first if 0 == i == j else prefix_rest,
                                               line))

    if line_after:
        out.write(_end_space.sub('', indent) + '\n')


def _fit_text(section, width, with_break=False):
    '''fit text to a given width'''
    # returns an array of this section of text to fit the given width
    words = [x for x in section.split(' ') if x]

    if with_break and words:
        words[-1] += '  '

    result = []
    cur = ''

    for i, word in enumerate(words):
        if cur and width != -1 and (len(cur) + len(word) + 1 > width):
            result.append(cur)
            cur = word
        else:
            cur += ('' if i == 0 else ' ') + word

    result.append(cur)

    return result


class BooleanClass(object):
    '''a mutable class that represents a boolean value'''
    def __init__(self, condition): self.condition = condition
    def is_true(self): return bool(self.condition)
    def set_true(self): self.condition = True
    def set_false(self): self.condition = False
    def __bool__(self): return self.is_true()
    __nonzero__ = __bool__
    def __unicode__(self): return unicode(str(self))
    def __str__(self): return str(bool(self.condition))
    def __repr__(self): return 'BooleanClass(%s)' % unicode(self)


def _getTerminalSize():
    '''
    get the width of the terminal window, taken verbatim from:
    http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
    '''
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return None
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (env['LINES'], env['COLUMNS'])
        except:
            cr = (25, 80)
    return int(cr[1]), int(cr[0])
