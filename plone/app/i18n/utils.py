import re

def make_token(domain, value):
    return '%s:%s' % (domain, value)

def split_token(token):
    return token.split(':')

def normalize_language_token(l):
    return l.lower().replace('_', '-')
    
def match(msg, query):
    """
    Case-insensitive fuzzy string matching. The use-cases are primarily
    variable interpolation and matching text appearing inside tags.

    The methods returns the accuracy of the match.

    Let's try a few simple matches.
    
    >>> match('Match me', 'match')
    1.0

    >>> match('Match me', 'me')
    1.0

    >>> match('Match me', 'match me')
    1.0

    Out-of-order words count as mismatches. The weight of a mismatch is
    proportional to the word length.

    >>> match('Match me', 'me match')
    0.375
 
    Words need not appear next to each other as long as the
    order is correct:

    >>> match('abc def ghi jkl mno prq stu vxy', 'def mno')
    1.0
    
    Non-matched words count negatively:

    >>> match('abc def ghi jkl mno prq stu vxy', 'zzz def mno')   # doctest: +ELLIPSIS
    0.72...
    
    >>> match('${count} item(s) renamed.', '23 item(s) renamed.') # doctest: +ELLIPSIS
    0.89...

    >>> match('Ignore <span class=\"discreet\">tags</span>', 'Ignore tags')
    1.0
    
    """

    # the empty query always matches
    if not query:
        return 1

    # fuzzy matching word by word
    words = filter(None, re.split(r"[\s,+=\-/\*!]", query.lower()))
    msg = msg.lower()
    
    i = 0
    non_matched = ''
    for word in words:
        try:
            i = msg.index(word, i)
        except ValueError:
            non_matched += word
        
    return 1-float(len(non_matched))/len(query)
