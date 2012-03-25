#!/usr/bin/env python
# -*- coding: utf-8 -*-
#date: 16.01.12
import sys
import re
import time
from contextlib import contextmanager


def unformat_mtext(s, exclude_list=('P', 'S')):
    """Returns string with removed format information

    :param s: string with multitext
    :param exclude_list: don't touch tags from this list. Default ('P', 'S') for
                         newline and fractions

    ::

        >>> text = ur'{\\fGOST type A|b0|i0|c204|p34;TEST\\fGOST type A|b0|i0|c0|p34;123}'
        >>> unformat_mtext(text)
        u'TEST123'

    """
    s = re.sub(r'\{?\\[^%s][^;]+;' % ''.join(exclude_list), '', s)
    s = re.sub(r'\}', '', s)
    return s


def mtext_to_string(s):
    """
    Returns string with removed format innformation as :func:`unformat_mtext` and
    `\\P` (paragraphs) replaced with newlines

    ::

        >>> text = ur'{\\fGOST type A|b0|i0|c204|p34;TEST\\fGOST type A|b0|i0|c0|p34;123}\\Ptest321'
        >>> mtext_to_string(text)
        u'TEST123\\ntest321'

    """

    return unformat_mtext(s).replace(u'\\P', u'\n')


def string_to_mtext(s):
    """Returns string in Autocad multitext format

    Replaces newllines `\\\\n` with `\\\\P`, etc.
    """
    return s.replace('\\', '\\\\').replace(u'\n', u'\P')


def text_width(text_item):
    """Returns width of Autocad `Text` or `MultiText` object
    """
    bbox_min, bbox_max = text_item.GetBoundingbox()
    return bbox_max[0] - bbox_min[0]


@contextmanager
def timing(message=u'Elapsed'):
    """ Context manager for timing execution

    Usage::

        with timing('some operation'):
            do_some_actions()

    Will print::

        some operation: 1.000 s

    """
    begin = time.time()
    try:
        yield begin
    finally:
        elapsed = (time.time() - begin)
        print u'%s: %.3f s' % (message, elapsed)


def dynamic_print(text):
    """Prints text dynamically in one line

    Used for printing something like animations, or progress
    """
    sys.stdout.write('\r%s' % text)
    sys.stdout.flush()
