import conllu
import os
import re
from collections import OrderedDict


class ConlluDoc:
    def __init__(self, conllu_doc_id, conllu_doc_filename, conllu_doc_source):
        self.doc_id = conllu_doc_id
        self.filename = conllu_doc_filename
        self.source = conllu_doc_source

    def __str__(self):
        return f"conllu document : doc_id = {self.doc_id}, filename = {self.filename}, source = {self.source}"

    def __repr__(self):
        return (
            f"{type(self).__name__}"
            f'(doc_id="{self.doc_id}", '
            f'filename="{self.filename}", '
            f"source={self.source})"
        )


class ConlluSent:
    def __init__(self, conllu_sent_doc_id, conllu_sent_sent_id, conllu_sent_sent_text):
        self.doc_id = conllu_sent_doc_id
        self.sent_id = conllu_sent_sent_id
        self.text = conllu_sent_sent_text

    def __str__(self):
        return f"conllu sentence : doc_id = {self.doc_id}, sent_id = {self.sent_id}, text = {self.text}"

    def __repr__(self):
        return (
            f"{type(self).__name__}"
            f'(doc_id="{self.doc_id}", '
            f'sent_id="{self.sent_id}", '
            f"text={self.text})"
        )


class TokenFields:
    def __init__(self, token_form, token_lemma, token_upos, token_xpos, token_feats: dict, token_head, token_deprel, token_deps, token_misc):
        self.FORM = token_form  # 2
        self.LEMMA = token_lemma  # 3
        self.UPOS = token_upos  # 4
        self.XPOS = token_xpos  # 5
        self.FEATS = token_feats  # 6
        self.HEAD = token_head  # 7
        self.DEPREL = token_deprel  # 8
        self.DEPS = token_deps  # 9
        self.MISC = token_misc  # 10

    def __str__(self):
        return str({
            "FORM": self.FORM,
            "LEMMA": self.LEMMA,
            "UPOS": self.UPOS,
            "XPOS": self.XPOS,
            "FEATS": self.FEATS,
            "HEAD": self.HEAD,
            "DEPREL": self.DEPREL,
            "DEPS": self.DEPS,
            "MISC": self.MISC
        })

    def __repr__(self):
        return (
            f"{type(self).__name__}"
            f'(FORM="{self.FORM}", '
            f'LEMMA="{self.LEMMA}", '
            f'UPOS="{self.UPOS}", '
            f'XPOS="{self.XPOS}", '
            f'FEATS="{self.FEATS}", '
            f'HEAD="{self.HEAD}", '
            f'DEPREL="{self.DEPREL}", '
            f'DEPS="{self.DEPS}", '
            f"MISC={self.MISC})"
        )


class ConlluToken:
    def __init__(self, conllu_token_token_id, conllu_token_sent_id, conllu_token_fields: TokenFields):
        self.token_id = conllu_token_token_id
        self.sent_id = conllu_token_sent_id
        self.fields = conllu_token_fields

    def __str__(self):
        return f"conllu token : token_id = {self.token_id}, sent_id = {self.sent_id}, fields = {self.fields}"

    def __repr__(self):
        return (
            f"{type(self).__name__}"
            f'(token_id="{self.token_id}", '
            f'sent_id="{self.sent_id}", '
            f"fields={self.fields})"
        )


def fix_conllu_text_lines_with_regex(conllu_text):
    """
    Use regex to clean up strange # text lines format errors
    """
    fixed_text = re.sub(r'(# text.*?)(?=\n1\t|\Z)', lambda x: x.group(1).replace('\n', ' '), conllu_text, flags=re.DOTALL)  # Replace newlines in # text line before 1\t part
    fixed_text = fixed_text.replace('\xa0', ' ')  # Replace NBSP with regular space
    fixed_text = re.sub(r' +', ' ', fixed_text)  # Replace multiple spaces with a single space
    fixed_text = re.sub(r' \r?\n', '\n', fixed_text)  # Remove trailing spaces before newlines
    return fixed_text


def fix_conllu(conllu_filepath):
    """
    Try: Open conllu file -> Fix format errors -> Save conllu file
    """
    try:
        with open(conllu_filepath, 'r', encoding='UTF8') as f:
            conllu_text = f.read()

        fixed_conllu_text = fix_conllu_text_lines_with_regex(conllu_text)

        with open(conllu_filepath, 'w', encoding='UTF8') as f:
            f.write(fixed_conllu_text)
    except:
        print(f"Error fixing file: {conllu_filepath}")


for path, directories, files in os.walk('Texts'):
    for file in files:
        filepath = os.path.join(path, file)
        fix_conllu(filepath)


for path, directories, files in os.walk('Texts'):
    doc_id = 1
    for file in files:
        with open(os.path.join(path, file), 'r', encoding='UTF8') as conllu_file:
            conllu_doc = ConlluDoc(doc_id, file, conllu_doc_source='random.com')
            print(conllu_doc)
            sentence_id = 1
            for token_list in conllu.parse_incr(conllu_file):
                conllu_sentence = ConlluSent(doc_id, sentence_id, token_list.metadata['text'])
                print(conllu_sentence)
                token_id = 1
                for token in token_list:
                    token_fields = TokenFields(token_form=token['form'], token_lemma=token['lemma'],
                                               token_upos=token['upos'], token_xpos=token['xpos'],
                                               token_feats=token['feats'], token_head=token['head'],
                                               token_deprel=token['deprel'], token_deps=token['deps'],
                                               token_misc=token['misc'])
                    conllu_token = ConlluToken(token_id, sentence_id, token_fields)
                    print(conllu_token)
                    token_id += 1
                sentence_id += 1
        doc_id += 1
print('done')
