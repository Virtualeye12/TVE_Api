import re,codecs
import unidecode


LATIN_1_CHARS = (
            ('\xe2\x80\x99', "'"),
            ('\xc3\xa9', 'e'),
            ('\xe2\x80\x90', '-'),
            ('\xe2\x80\x91', '-'),
            ('\xe2\x80\x92', '-'),
            ('\xe2\x80\x93', '-'),
            ('\xe2\x80\x94', '-'),
            ('\xe2\x80\x94', '-'),
            ('\xe2\x80\x98', "'"),
            ('\xe2\x80\x9b', "'"),
            ('\xe2\x80\x9c', '"'),
            ('\xe2\x80\x9c', '"'),
            ('\xe2\x80\x9d', '"'),
            ('\xe2\x80\x9e', '"'),
            ('\xe2\x80\x9f', '"'),
            ('\xe2\x80\xa6', '...'),
            ('\xe2\x80\xb2', "'"),
            ('\xe2\x80\xb3', "'"),
            ('\xe2\x80\xb4', "'"),
            ('\xe2\x80\xb5', "'"),
            ('\xe2\x80\xb6', "'"),
            ('\xe2\x80\xb7', "'"),
            ('\xe2\x81\xba', "+"),
            ('\xe2\x81\xbb', "-"),
            ('\xe2\x81\xbc', "="),
            ('\xe2\x81\xbd', "("),
            ('\xe2\x81\xbe', ")")
        )

def clean_latin1(data):
    try:
        data = data.encode('utf-8').decode('iso-8859-1')
        for _hex, _char in LATIN_1_CHARS:
            data = data.replace(_hex, _char)
        data = re.sub("`","\'",data)
        return data#.encode('utf8')
    except:
        return data

def remove_nested_parens(input_str):
    result = ''
    paren_level = 0
    for ch in input_str:
        if ch == '{':
            paren_level += 1
        elif (ch == '}') and paren_level:
            paren_level -= 1
        elif not paren_level:
            result += ch
    return result


def tokenize_light(x):
    return x.split(' ')


def clean_hard(document):
    document = clean_latin1(document)
    document = remove_nested_parens(document)
    document = re.sub(r"<!--?.*?-->", "", document)
    document = document.replace('\\N', "")
    document = document.replace('\n', " ")
    document = codecs.decode(document, 'unicode_escape')
    document = re.sub(r'^https?:\/\/.*[\r\n]*', '', document)
    document = re.sub(r"\S*@\S*\.\S*|\www\.\S*\.\S*", "", document)
    document = re.sub(r'[^\x00-\x7f]', '', document)
    document = re.sub(r'\.\.+', '. ', document)
    document = re.sub(r"\s+\d+\s+", " ", document)
    document = re.sub(r"\s+[^A-Za-z]*\s+", " ", " " + document + " ")
    document = re.sub(r' +', ' ', document)
    document = re.sub(r"http\S+", "", document)
    document = re.sub(r"\'","\'\'",document)
    document = " ".join([ word for word in document.split(" ") if len(word) < 30 ])
    document = unidecode.unidecode(u'{}'.format(document))
    return document.strip()
