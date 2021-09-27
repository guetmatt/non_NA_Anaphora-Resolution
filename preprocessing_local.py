"""
MATTHIAS GUETEBIER
Matr.-Nr.: 108016243375

Modul zur Annotation weiterer Informationen.
Benoetigt eine funktionierende Installation von 'Stanza' von der Stanford NLP Group.
Anleitung zur Installation unter: https://stanfordnlp.github.io/stanza/installation_usage.html
"""


# Modul 'stanza' importieren
import stanza
stanza.download('en')


def extract_text(data_dict):
    """

    :param data_dict:
    :return:
    """

    tokenized_text = list()

    for doc in data_dict:
        for sent in data_dict[doc]:
            toks_temp = list()

            for tok in data_dict[doc][sent]:
                tok_annotation = data_dict[doc][sent][tok]
                toks_temp.append(tok_annotation[0])

            tokenized_text.append(toks_temp)

    return tokenized_text





def annotate(text, tokenized=True):
    """
    Annotiere einen Eingabetext mit linguistischen Eigenschaften.
    Features: UPOS, XPOS, Lemma, Dependency Relations, Grammatical Features

    Optionale Tokenisierung. Wenn tokenized=False, Eingabetext nur als String moeglich.

    :param text (str/list): Liste mit Listen von Strings (Saetze als Liste von Tokens)
                            Wenn noch nicht tokenisiert, Eingabe als String.
    :param tokenized (bool): Eingabtext bereits tokenisiert oder nicht
    :return: doc_local: Document Object (stanza), enthaelt alle Annotationen.
    """

    # import stanza
    # stanza.download('en')

    if tokenized == True:
        nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,depparse', tokenize_pretokenized=True)
        doc_local = nlp(text)
    else:
        nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,depparse')
        doc_local = nlp(text)

    return doc_local



def convert_annotations(data_dict, stanza_doc):
    """

    :param data_dict:
    :param stanza_doc:
    :return:
    """

    sentences_list = stanza_doc.sentences
    sentences_index = -1

    for doc in data_dict:
        for sent in data_dict[doc]:
            sentences_index += 1
            current_sentence_toks = sentences_list[sentences_index].words

            tok_index = -1

            for tok in data_dict[doc][sent]:

                tok_annotation = data_dict[doc][sent][tok]
                tok_index += 1
                current_tok = current_sentence_toks[tok_index]

                # Lemma eintragen
                data_dict[doc][sent][tok][1] = current_tok.lemma
                # UPOS
                data_dict[doc][sent][tok][2] = current_tok.upos
                # XPOS
                data_dict[doc][sent][tok][3] = current_tok.xpos
                # FEATS
                data_dict[doc][sent][tok][4] = current_tok.feats

                # !!!!  ACHTUNG !!!!
                # HEAD bezieht sich auf satzinterne ID, in Datensaetzen ist ID allerdings Dokumentintern und SatzUEBERGREIFEND!
                # Head-id korrespondiert quasi mit dem satzinternen Index+1 des Tokens (?)
                # Head-id = 0 --> ROOT
                # HEAD
                data_dict[doc][sent][tok][5] = current_tok.head
                # DEPREL
                data_dict[doc][sent][tok][6] = current_tok.deprel




            # for tok_index, tok_list in enumerate(data_dict[doc][sent]["token"]):
            #     current_tok = current_sentence_toks[tok_index]
            #
            #     # Lemma eintragen
            #     data_dict[doc][sent]["token"][tok_index][2] = current_tok.lemma
            #     # UPOS
            #     data_dict[doc][sent]["token"][tok_index][3] = current_tok.upos
            #     # XPOS
            #     data_dict[doc][sent]["token"][tok_index][4] = current_tok.xpos
            #     # FEATS
            #     data_dict[doc][sent]["token"][tok_index][5] = current_tok.feats
            #
            #     # !!!!  ACHTUNG !!!!
            #     # HEAD bezieht sich auf satzinterne ID, in Datensaetzen ist ID allerdings Dokumentintern und SatzUEBERGREIFEND!
            #     # Head-id korrespondiert quasi mit dem satzinternen Index+1 des Tokens (?)
            #     # Head-id = 0 --> ROOT
            #     # HEAD
            #     data_dict[doc][sent]["token"][tok_index][6] = current_tok.head
            #     # DEPREL
            #     data_dict[doc][sent]["token"][tok_index][7] = current_tok.deprel

    return data_dict




def annotation_pipeline(data_dict):

    text_local = extract_text(data_dict)
    stanza_doc_local = annotate(text_local)
    data_annotated = convert_annotations(data_dict, stanza_doc_local)

    return data_annotated



# doc = annotate([["I", "ate", "an", "apple", "."], ["Um", "and", "I", "guess", "we", "should", "all", "get", "acquainted"]])
#
# print(doc.sentences[0].words)