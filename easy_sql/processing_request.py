from key_words import keyword, select_syntax


def match(text, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')):
    return alphabet.isdisjoint(text.lower())


def process_the_request(raw_req):
    kw_and_args = identifying_key_words_and_arguments(raw_req)
    req = request_collection(kw_and_args)
    return req


def identifying_key_words_and_arguments(raw_req):
    word_list = raw_req.split()
    kw_and_args = {}
    last_word = ''

    for word in word_list:
        if word in keyword:
            last_word = word
            kw_and_args[last_word] = []
        elif match(word):
            kw_and_args[last_word].append(word)

    return kw_and_args


def request_collection(kw_and_args):
    req = ''
    for key in select_syntax:
        if key in kw_and_args:
            req += key + ' '.join(kw_and_args[key])

    return req
