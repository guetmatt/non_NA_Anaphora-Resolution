"""
MATTHIAS GUETEBIER
Matr.-Nr.: 108016243375

Modul mit Funktionen die Datensaetze der SharedTask einlesen.
"""


##############
### MODULE ###
##############

# Lokales Modul zur Annotation weiterer linguistischer Eigenschaften mit 'stanza'
# from preprocessing_local import annotation_pipeline

from get_features import get_tok_dist_training, get_sent_dist_training


##################
### FUNKTIONEN ###
##################

def read_file(filename):
    """
    Textdatei zeilenweise einlesen.
    Vorangehenden und abschliessenden Whitespace entfernen.

    :param filename (str): Name/Pfad der Textdatei
    :return: lines: Liste mit eingelesenen Zeilen
    """

    # Datei oeffnen und zeilenweise einlesen
    with open(filename, mode="r", encoding="UTF-8") as infile:
        lines = infile.readlines()

    # vorangehenden und abschliessenden Whitespace entfernen
    for index, line in enumerate(lines):
        lines[index] = line.strip()

    return lines




### ALTER VERSION DER FUNKTION ###
# def process_data(data_lines):
#     """
#     Daten bereinigen und in geeignete Struktur fuer Weiterverarbeitung bringen.
#
#     :param data_lines (list):
#     :return: cleanData_dict (dict): Dictionary mit zwei eingebetteten Dictionaries.
#                                     Ebene 1: Keys fuer Dokumente innerhalb eines Datensatzes ("doc_id1/2/.../n")
#                                     Ebene 2: Keys fuer Saetze innerhalb eines Dokumentes ("sent_id")
#                                     Ebene 3: Gesamter Satz, einzelne Token etc. ("text", "token")
#
#     Struktur von cleanData_dict:
#         cleanData_dict = {doc_id1/2/.../n :
#                             {sent_id :
#                                 {"text" : kompletter Satz als String,
#                                 "token" : alle Token als Listen in einer Liste} } }
#     Struktur der Liste hinter Key "token":
#         cleanData_dict["doc_id"]["sent_id"]["token"][0] (erster Token) =
#          [  [0] ID (str)
#             [1] FORM (str)
#             [2] LEMMA (str)
#             [3] UPOS (str)
#             [4] XPOS (str)
#             [5] FEATS (str)
#             [6] HEAD (str)
#             [7] DEPREL (str)
#             [8] DEPS (str)
#             [9] MISC (str)
#             [10] IDENTITY (list)    --> [EntityID, MarkableID, Min, SemType, ...]
#             [11] BRIDGING (list)    --> [MarkableID, Rel, ...]
#             [12] DISCOURSE_DEIXIS (list)    --> [EntityID, MarkableID, Min, SemType, ...]
#             [13] REFERENCE (list)   --> [...]
#             [14] NOM_SEM (list) --> [MarkableID, Entity_Type, Genericity, ...]
#         ]
#     """
#
#     # Liste fuer Zwischenschritt der Bereinigung
#     data_temp = list()
#     # Dictionary fuer bereinigte Daten
#     cleanData_dict = dict()
#
#     # erste Zeile aus Textdatei entfernen
#     # (--> Beschreibung der Spalten)
#     data_lines.pop(0)
#
#     for index, line in enumerate(data_lines):
#         # leere Zeilen ignorieren
#         if line == "":
#             pass
#
#         # Zeilen, die mit '#' beginnen
#         # Zeilen mit einzelnen Token + Annotationen
#         # --> jeweils splitten
#         else:
#             data_temp.append(line.split())
#
#
#     # Zaehler fuer verschiedene Dokumente innerhalb einer Datei
#     counter_docs = 0
#     counter_sents = 0
#
#     for index, line in enumerate(data_temp):
#         if line[0] == "#":
#             if line[1].strip() == "newdoc":
#                 counter_docs += 1
#
#                 ### FUER EIGENE SENT_IDs ###
#                 counter_sents = 0
#                 ### ###
#
#                 current_doc_id = "doc_id" + str(counter_docs)
#                 cleanData_dict[current_doc_id] = dict()
#
#             elif line[1].strip() == "sent_id":
#
#
#
#                 # ORIGINALE SENT_IDs
#                 #current_sent_id = line[3]
#                 #cleanData_dict[current_doc_id][current_sent_id] = dict()
#
#                 # EIGENE SENT_IDs ALS INTEGER
#                 counter_sents += 1
#                 cleanData_dict[current_doc_id][counter_sents] = dict()
#
#             elif line[1].strip() == "text":
#                 cleanData_dict[current_doc_id][counter_sents]["text"] = " ".join(tuple(line[3:]))
#
#             # weitere Infos:
#             # turn_id, speaker
#             # --> erstmal ignorieren
#             # weil schwierig damit umzugehen; Reihenfolge newdoc > sent_id > text ist garantiert
#             # weitere Reihenfolge aber nicht
#             else:
#                 #cleanData_dict[current_doc_id][current_sent_id][line[1].strip()] = line[3].strip()
#                 pass
#
#         else:
#             current_tokenList = cleanData_dict[current_doc_id][counter_sents].get("token", list())
#
#             # "_"-Element anhaengen, falls Annotation in Spalte "NOM_SEM" fehlt
#             # betrifft alle Token, bei denen Spalte "IDENTITY" nicht annotiert wurde
#             if len(line) == 14:
#                 line.append("_")
#
#             current_tokenList.append(line)
#             cleanData_dict[current_doc_id][counter_sents]["token"] = current_tokenList
#
#     # DD-Annotationen von Listen zu Dictionaries umwandeln
#     # Keys: 'EntityID', 'MarkableID', 'Min', 'SemType', ('ElementOf')
#     for doc in cleanData_dict:
#         for sent in cleanData_dict[doc]:
#             for tok_index, tok_list in enumerate(cleanData_dict[doc][sent]["token"]):
#                 if tok_list[12].startswith("("):
#
#                     # Klammern aus Annotationen entfernen zur Normierung
#                     if tok_list[12].endswith(")"):
#                         tok_list[12] = tok_list[12][1:-1]
#                     else:
#                         tok_list[12] = tok_list[12][1:]
#
#                     current_keys = list()
#                     current_vals = list()
#
#                     #print(tok_list[12])
#
#                     for entry in tok_list[12].split("|"):
#                         border_index = entry.index("=")
#                         current_keys.append(entry[0:border_index])
#                         current_vals.append(entry[border_index+1:])
#
#                     tok_as_dict = dict(zip(current_keys, current_vals))
#                     # "Min" = minimale Spanne der Instanz
#                     # --> zu Tupel umwandeln (IndexAnfang, IndexEnde)
#                     tok_as_dict["Min"] = tuple([int(index) for index in tok_as_dict["Min"].split(",")])
#                     cleanData_dict[doc][sent]["token"][tok_index][12] = tok_as_dict
#
#
#     return cleanData_dict

################################################
### TEST


def process_data(data_lines):
    """
    Daten bereinigen und in geeignete Struktur fuer Weiterverarbeitung bringen.

    :param data_lines (list):
    :return: cleanData_dict (dict): Dictionary mit zwei eingebetteten Dictionaries.
                                    Ebene 1: Keys fuer Dokumente innerhalb eines Datensatzes ("doc_id1/2/.../n")
                                    Ebene 2: Keys fuer Saetze innerhalb eines Dokumentes ("sent_id")
                                    Ebene 3: Gesamter Satz, einzelne Token etc. ("text", "token")

    Struktur von cleanData_dict:
        cleanData_dict = {doc_id1/2/.../n :
                            {sent_id :
                                { tok_id : Liste mit Annotationen }
    Struktur der Liste hinter Key "tok_id":
        cleanData_dict["doc_id"][sent_id][tok_id] =
         [  [0] FORM (str)
            [1] LEMMA (str)
            [2] UPOS (str)
            [3] XPOS (str)
            [4] FEATS (str)
            [5] HEAD (str)
            [6] DEPREL (str)
            [7] DEPS (str)
            [8] MISC (str)
            [9] IDENTITY (list)    --> [EntityID, MarkableID, Min, SemType, ...]
            [10] BRIDGING (list)    --> [MarkableID, Rel, ...]
            [11] DISCOURSE_DEIXIS (list)    --> [EntityID, MarkableID, Min, SemType, ...]
            [12] REFERENCE (list)   --> [...]
            [13] NOM_SEM (list) --> [MarkableID, Entity_Type, Genericity, ...]
        ]
    """

    # Liste fuer Zwischenschritt der Bereinigung
    data_temp = list()
    # Dictionary fuer bereinigte Daten
    cleanData_dict = dict()

    # erste Zeile aus Textdatei entfernen
    # (--> Beschreibung der Spalten)
    data_lines.pop(0)

    for index, line in enumerate(data_lines):
        # leere Zeilen ignorieren
        if line == "":
            pass

        # Zeilen, die mit '#' beginnen
        # Zeilen mit einzelnen Token + Annotationen
        # --> jeweils splitten
        else:
            data_temp.append(line.split())


    # Zaehler fuer verschiedene Dokumente innerhalb einer Datei
    counter_docs = 0
    counter_sents = 0

    for index, line in enumerate(data_temp):
        if line[0] == "#":
            if line[1].strip() == "newdoc":
                counter_docs += 1

                ### FUER EIGENE SENT_IDs ###
                counter_sents = 0
                ### ###

                current_doc_id = "doc_id" + str(counter_docs)
                cleanData_dict[current_doc_id] = dict()

            elif line[1].strip() == "sent_id":

                # ORIGINALE SENT_IDs
                #current_sent_id = line[3]
                #cleanData_dict[current_doc_id][current_sent_id] = dict()

                # EIGENE SENT_IDs ALS INTEGER
                counter_sents += 1
                cleanData_dict[current_doc_id][counter_sents] = dict()

            # TEXT WIRD IM NEUEN ANSATZ IGNORIERT
            # elif line[1].strip() == "text":
            #     cleanData_dict[current_doc_id][counter_sents]["text"] = " ".join(tuple(line[3:]))

            # weitere Infos:
            # turn_id, speaker
            # --> erstmal ignorieren
            # weil schwierig damit umzugehen; Reihenfolge newdoc > sent_id > text ist garantiert
            # weitere Reihenfolge aber nicht
            else:
                #cleanData_dict[current_doc_id][current_sent_id][line[1].strip()] = line[3].strip()
                pass

        else:

            # "_"-Element anhaengen, falls Annotation in Spalte "NOM_SEM" fehlt
            # betrifft alle Token, bei denen Spalte "IDENTITY" nicht annotiert wurde
            if len(line) == 14:
                line.append("_")

            # somit direkter Zugriff auf Token + Annotationen per tok_id
            # ermoeglicht nachher leichteren lookup
            current_tok_id = int(line[0])
            cleanData_dict[current_doc_id][counter_sents][current_tok_id] = line[1:]



    # DD-Annotationen von Listen zu Dictionaries umwandeln
    # Keys: 'EntityID', 'MarkableID', 'Min', 'SemType', ('ElementOf')
    for doc in cleanData_dict:
        for sent in cleanData_dict[doc]:
            for tok in cleanData_dict[doc][sent]:

                tok_annotation = cleanData_dict[doc][sent][tok]

                # tok_annotation[11] = DD-Annotationen
                if tok_annotation[11].startswith("("):

                    if tok_annotation[11].endswith(")"):
                        # Klammern aus Annotationen entfernen zur Normierung
                        cleanData_dict[doc][sent][tok][11] = tok_annotation[11][1:-1]
                    else:
                        cleanData_dict[doc][sent][tok][11] = tok_annotation[11][1:]

                    current_keys = list()
                    current_vals = list()

                    for entry in tok_annotation[11].split("|"):
                        border_index = entry.index("=")
                        current_keys.append(entry[0:border_index])
                        current_vals.append(entry[border_index + 1:])
                    tok_as_dict = dict(zip(current_keys, current_vals))

                    # "Min" = minimale Spanne der Instanz
                    # --> zu Tupel umwandeln (IndexAnfang, IndexEnde)
                    tok_as_dict["Min"] = tuple([int(index) for index in tok_as_dict["Min"].split(",")])
                    cleanData_dict[doc][sent][tok][11] = tok_as_dict


    return cleanData_dict




def extract_dd_elements(data):
    """

    :param data (dict):
    :return:
    """

    coref_dict = dict()

    for doc in data:

        # Liste fuer alle Koreferenzmengen in diesem Dokument
        #coref_dict[doc] = list()
        coref_dict[doc] = dict()

        for sent in data[doc]:

            for tok in data[doc][sent]:

                tok_annotation = data[doc][sent][tok]

                # Instanz von DD
                if type(tok_annotation[11]) == dict:

                    current_entID = tok_annotation[11]["EntityID"]

                    # GROBFASSUNG PASST ANSCHEINEND
                    # ES MUESSEN NOCH "ElementOf"-Annotationen BEHANDELT WERDEN
                    # UND DIE ZURODNUNG ZUSAMMENGHEORIGER IDs!

                    # Antezedenzien bestehend aus mehreren Saetzen
                    # fuer Details siehe Erlaeuterungen zu Annotation "ElementOf"
                    if "ElementOf" in tok_annotation[11].keys():
                        current_entID = tok_annotation[11]["ElementOf"]


                    # coref_dict[doc][current_entID]["elements"] = tuple
                    # --> ( Min, SentID ) --> ( (Int, Int), String )
                    coref_dict[doc][current_entID] = coref_dict[doc].get(current_entID, dict())
                    coref_dict[doc][current_entID]["elements"] = coref_dict[doc][current_entID].get("elements", list())
                    coref_dict[doc][current_entID]["elements"].append((tok_annotation[11]["Min"], sent))

    #print(*[(element, coref_dict["doc_id1"][element]) for element in coref_dict["doc_id1"]], sep="\n")

    return coref_dict






### ALTER VERSION DER FUNKTION ###
# def extract_dd_elements(data):
#     """
#
#     :param data (dict):
#     :return:
#     """
#
#     coref_dict = dict()
#
#     for doc in data:
#
#         # Liste fuer alle Koreferenzmengen in diesem Dokument
#         #coref_dict[doc] = list()
#         coref_dict[doc] = dict()
#
#         for sent in data[doc]:
#             for tok_list in data[doc][sent]["token"]:
#
#                 # Instanz von DD
#                 if type(tok_list[12]) == dict:
#
#                     current_entID = tok_list[12]["EntityID"]
#
#                     # GROBFASSUNG PASST ANSCHEINEND
#                     # ES MUESSEN NOCH "ElementOf"-Annotationen BEHANDELT WERDEN
#                     # UND DIE ZURODNUNG ZUSAMMENGHEORIGER IDs!
#
#                     # Antezedenzien bestehend aus mehreren Saetzen
#                     # fuer Details siehe Erlaeuterungen zu Annotation "ElementOf"
#                     if "ElementOf" in tok_list[12].keys():
#                         current_entID = tok_list[12]["ElementOf"]
#
#                     # coref_dict[doc][current_entID]["elements"] = tuple()
#                     # --> ( Min, SentID ) --> ( (Int, Int), String )
#                     coref_dict[doc][current_entID] = coref_dict[doc].get(current_entID, dict())
#                     coref_dict[doc][current_entID]["elements"] = coref_dict[doc][current_entID].get("elements", list())
#                     coref_dict[doc][current_entID]["elements"].append((tok_list[12]["Min"], sent))
#
#     #print(*[(element, coref_dict["doc_id1"][element]) for element in coref_dict["doc_id1"]], sep="\n")
#
#     return coref_dict



def cleanup_coref_dict(coref_dict, data_dict):
    """
    Nicht relevante Faelle aus Dictionary mit Koreferenzmengen rausfiltern.
    Nicht relevante Faelle:
        - Anapher != "it", "this", "that"
        ( - Antezedens besteht aus mehr als einem Satz) ??

    :param coref_dict:
    :param data_dict:
    :return:
    """

    relevant_forms = ["this", "that", "it"]
    coref_dict_clean = dict()

    for doc in coref_dict:
        for dd_ent in coref_dict[doc]:

            # DD-Entitaet enthaelt genau zwei Elemente
            # --> [0] = Antezedens und [1] = Anapher
            if len(coref_dict[doc][dd_ent]["elements"]) == 2:

                # sent_id der Anapher fuer leichteren lookup
                sent_id = coref_dict[doc][dd_ent]["elements"][1][1]

                if coref_dict[doc][dd_ent]["elements"][1][0][0] == coref_dict[doc][dd_ent]["elements"][1][0][1]:
                    anaph_id = coref_dict[doc][dd_ent]["elements"][1][0][0]
                    anaph_form = data_dict[doc][sent_id][anaph_id][0].lower()


                    if anaph_form in relevant_forms:
                        coref_dict_clean[doc] = coref_dict_clean.get(doc, {})
                        coref_dict_clean[doc][dd_ent] = coref_dict[doc][dd_ent]

    return coref_dict_clean
















# Funktion, die alle weiteren Funktionen aufruft
def run_script():

    # DEVELOPMENT DATENSAETZE EINLESEN
    AMI_dev_dict = process_data(read_file(r"C:/Users/Arbeit/Documents/RuhrUniBochum/bachelorarbeit/code/data/development/AMI_dev.conllua"))
    # light_dev_dict = process_data(read_file(r"C:/Users/Arbeit/Documents/RuhrUniBochum/bachelorarbeit/code/data/development/light_dev.CONLLUA"))
    # persuasion_dev_dict = process_data(read_file(r"C:/Users/Arbeit/Documents/RuhrUniBochum/bachelorarbeit/code/data/development/Persuasion_dev.CONLLUA"))
    # RST_DTreeBank_dev_dict = process_data(read_file(r"C:/Users/Arbeit/Documents/RuhrUniBochum/bachelorarbeit/code/data/development/RST_DTreeBank_dev.CONLL"))
    # switchboard3_dev_dict = process_data(read_file(r"C:/Users/Arbeit/Documents/RuhrUniBochum/bachelorarbeit/code/data/development/Switchboard_3_dev.CONLL"))

    # # TRAINING DATENSAETZE EINLESEN
    # gnome_subset_dict = process_data(read_file(r"C:/Users/Arbeit/Documents/RuhrUniBochum/bachelorarbeit/code/data/training/Gnome_Subset2.CONLL"))
    # pear_stories_dict = process_data(read_file(r"C:/Users/Arbeit/Documents/RuhrUniBochum/bachelorarbeit/code/data/training/Pear_Stories.CONLL"))
    # RST_DTreeBank_train_dict = process_data(read_file(r"C:/Users/Arbeit/Documents/RuhrUniBochum/bachelorarbeit/code/data/training/RST_DTreeBank_train.CONLL"))
    # trains91_dict = process_data(read_file(r"C:/Users/Arbeit/Documents/RuhrUniBochum/bachelorarbeit/code/data/training/Trains_91.CONLL"))
    # trains93_dict = process_data(read_file(r"C:/Users/Arbeit/Documents/RuhrUniBochum/bachelorarbeit/code/data/training/Trains_93.CONLL"))

    # # TESTEN DER ANNOTATIONSPIPELINE
    # AMI_annotated = annotation_pipeline(AMI_dev_dict)
    #
    # for doc in AMI_annotated:
    #     for sent in AMI_annotated[doc]:
    #         for tok in AMI_annotated[doc][sent]:
    #             print(AMI_annotated[doc][sent][tok])



    # #testlist = extract_dd_elements(AMI_annotated)
    #
    test_dict = extract_dd_elements(AMI_dev_dict)

    test_dict = get_tok_dist_training(test_dict)
    test_dict = get_sent_dist_training(test_dict)
    #
    # #print(*[(element, test_dict[doc][element]) for element in test_dict[doc] for doc in test_dict], sep="\n")
    #
    counter_two = 0
    counter_more = 0
    counter_else = 0

    sent_dist_total = 0

    for doc in test_dict:
        for element in test_dict[doc]:

            if len(test_dict[doc][element]["elements"]) == 2:
                counter_two += 1

                sent_dist_total += test_dict[doc][element]["sent_dist"]

                print(doc, element, test_dict[doc][element], sep="\t")

            elif len(test_dict[doc][element]["elements"]) > 2:
                #print(doc, element, test_dict[doc][element], sep="\t")
                counter_more += 1

            else:

                counter_else += 1

    print("ZWEI ELEMENTE:", counter_two, sep="\t")
    print("MEHR ALS ZWEI ELEMENTE:", counter_more, sep="\t")
    print("ELSE:", counter_else, sep="\t")

    print("AVG SENTDIST TWO ELEMENTS:", sent_dist_total/counter_two)

    # # TEST CLEANUP VON COREF DICT
    coref_dict_clean = cleanup_coref_dict(test_dict, AMI_dev_dict)



    for doc in coref_dict_clean:
        for dd_ent in coref_dict_clean[doc]:
            print(coref_dict_clean[doc][dd_ent])

    #print(testlist)

    # for entry in testlist:
    #     print(entry)
    #     print()

###########################################################
# Hauptprogramm
###########################################################

if __name__ == "__main__":

    # Funktion, die alle weiteren Funktionen aufruft
    run_script()