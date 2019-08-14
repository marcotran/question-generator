import spacy
from spacy.lang.en import English
from summa import summarizer
import re

def noun_ques(text):
    temp_sent = text
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    for chunk in doc.noun_chunks:
        if chunk.root.dep_ == 'nsubj':
            temp_sent = temp_sent.replace(chunk.text, 'Who')
            break
    return temp_sent if temp_sent != text else ''

def quote_ques(text):
    if text.startswith('"') and ('said' in text or 'asked' in text):
        quote, no_quote = text.rsplit('"', 1)
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(no_quote)
        for chunk in doc.noun_chunks:
            result = quote + '",' + no_quote.replace(chunk.text, 'who')
            break
        return result
    else:
        return ''


def verb_ques(text):
    result = ''
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    for token in doc:
        if token.dep_ == 'ROOT' and token.pos_ == 'VERB':
            rights = token.rights
            right = next(rights)
            right_tree_len = len(list(token.rights))
            if (right_tree_len == 0 or (right_tree_len == 1 and next(token.rights).dep_ == 'punct')):
                result += 'doing '
            else:
                result += token.text + ' '
            if right.dep_ == 'prep' or right.dep_ == 'prt':
                result += right.text + ' '
                if right.dep_ == 'prt':
                    result += next(rights).text + ' '
            break
        else:
            result += token.text + ' '
    return result + 'what?' if result else ''

def post_qoute_ques(text):
        regex_to_match = '(?:said|asked)\s*,\s*"'
        regex = ',\s*"'
        match = re.search(regex_to_match, text)
        if (match):
                return re.split(regex, text)[0] + ' what?'
        else:
            return ''
def clean_summarize_text(text):
    if text:
        summary = summarizer.summarize(text)
    if summary:
        cleaned = re.sub('[‘’“”]','"', summary)
        cleaned = re.sub("''",'"', cleaned)
        return cleaned.split('\n') if cleaned else ''
    return ''

# main function
def question_generator(text):
    sents = clean_summarize_text(text)
    toggle = True
    for sent in sents:
        ques = ''
        if quote_ques(sent):
            ques = quote_ques(sent)
        elif post_qoute_ques(sent):
            ques = post_qoute_ques(sent)
        elif toggle:
            ques = noun_ques(sent)
            toggle = False
        else:
            toggle = True
            ques = verb_ques(sent)
        print("sentence: ", sent)
        print("question: ", ques)
        print()