"""
------------------------
Matthias Guetebier
Matr.-Nr.: 108016243375
------------------------

Modul zur Annotation weiterer Informationen.
Nur fuer Preprocessing gedacht, nicht zur Anwendung des Klassifizierers notwendig.

Benoetigt eine funktionierende Installation von 'Stanza' von der Stanford NLP Group.
Anleitung zur Installation unter: https://stanfordnlp.github.io/stanza/installation_usage.html
"""


# Modul 'stanza' importieren
# und Inhalte fuer 'english' downloaden
import stanza
stanza.download('en')


def extract_text(data_dict: dict):
    """
    Text aus Datensatz als Liste von Saetzen als Token extrahieren.

    :param data_dict (dict): Datensatz als Dictionary.
    :return tokenized_text (list): Liste mit Saetzen, Saetze als Listen von Token
    """

    # Liste fuer Token
    tokenized_text = list()

    # jeden Satz als Liste von Token extrahieren
    for doc in data_dict:
        for sent in data_dict[doc]:
            toks_temp = list()

            for tok in data_dict[doc][sent]:
                tok_annotation = data_dict[doc][sent][tok]
                # Saetz als Liste von Token
                toks_temp.append(tok_annotation[0])

            # Satz an Liste von Saetzen anhaengen
            tokenized_text.append(toks_temp)

    return tokenized_text


def annotate(text: list, tokenized: bool=True):
    """
    Eingabetext mit linguistischen Eigenschaften annotieren.
    Eigenschaften: UPOS, XPOS, Lemma, Dependency Relations, Grammatical Features
    Optionale Tokenisierung. Wenn tokenized=False, Eingabetext nur als String moeglich.

    :param text (str/list): Liste mit Listen von Strings (Saetze als Liste von Tokens)
                            Wenn noch nicht tokenisiert, Eingabe als String.
    :param tokenized (bool): Eingabtext bereits tokenisiert?, Default=True
    :return: doc_local: Document Object (stanza), enthaelt alle Annotationen.
    """

    if tokenized == True:
        # Annotationspipeline von Stanza
        nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,depparse', tokenize_pretokenized=True)
        doc_local = nlp(text)
    else:
        # Annotationspipeline
        nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,depparse')
        doc_local = nlp(text)

    return doc_local


def convert_annotations(data_dict, stanza_doc):
    """
    Annotationen von Stanza zur weiteren Verwendung in Dictionary von Datensatz eintragen.

    :param data_dict (dict): Datensatz als Dictionary
    :param stanza_doc (Document Objekct (stanza)): Stanza-Objekt mit Annotationen
    :return data_dict (dict): Datensatz als Dictionary, mit eingetragenen Annotationen
    """

    # Liste von annotierten Saetzen
    sentences_list = stanza_doc.sentences
    sentences_index = -1

    # Annotationen tokenweise in
    # Dictionary des Datensatzes eintragen
    for doc in data_dict:
        for sent in data_dict[doc]:
            sentences_index += 1
            current_sentence_toks = sentences_list[sentences_index].words

            # tokenweise Eintraege
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
                # HEAD
                # Head-id = 0 --> ROOT
                data_dict[doc][sent][tok][5] = current_tok.head
                # DEPREL
                data_dict[doc][sent][tok][6] = current_tok.deprel

    return data_dict


def annotation_pipeline(data_dict: dict):
    """
    Pipeline zur Annotatione eines Datensatzes.

    :param data_dict (dict): Datensatz als Dictionary zur Annotatione
    :return data_dict (dict): Datensatz als Dictionary mit eingetragenen Annotationen
    """

    text_local = extract_text(data_dict)
    stanza_doc_local = annotate(text_local)
    data_annotated = convert_annotations(data_dict, stanza_doc_local)

    return data_annotated


####################
#### boilerplate ###
####################

if __name__ == "__main__":
    print("""Diese Datei enthaelt Funktionen fuer die Annotation von Datensaetzen
    mit Stanza. Die Funktionen dienen lediglich dem Preprocessing
    und sind nicht fuer die komfortbale Verwendung durch einen User ausgelegt.""")

    # Das zur Annotation benoetigte 'data_dict'
    # wird durch process_data(read_file(filename)) zurueckgegeben

    # Mit 'write_annotated_data' koennen die annotierten Daten
    # in eine Datei in das Unterverzeichnis 'data_annotated' geschrieben werden

    # Die Funktionen können aus 'functions_basic' importiert werden
