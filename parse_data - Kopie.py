"""MATTHIAS GUETEBIER"""


##############
### MODULE ###
##############

# Stanza fuer Tagging von U/XPOS, FEAT (morphological), DEPS
import stanza



def read_file(filename):
    """Funktion, die eine Datei zeilenweise einliest.
    Input:
    1. filename (str): Name/Pfad der einzulesenden Datei
    Return:
    1. lines (list): Liste mit eingelesene Zeilen
    """
    with open(filename, mode="r", encoding="UTF-8") as infile:
        lines = infile.readlines()

    for index, line in enumerate(lines):
        lines[index] = line.strip().split()

    return lines


"""TODO:
EINZELNE DOKUMENTE INNERHALB DER TEXTDATEIEN PARSEN
WEIL DIE PROBLEME MIT DER INDIZIERUNG BEREITEN!!!!
"""


def parse_data(data_raw):
    """Funktion, die eingelesene Zeilen segmentiert.
    Input:
    1. data_raw (list): Liste mit eingelesenen Zeilen
    Return:
    1. data_parsed (list): geparste Daten
    """
    """
    Struktur der geparsten Daten:
    data_parsed = [
        [0] ID (str)
        [1] FORM (str)
        [2] LEMMA (str)
        [3] UPOS (str)
        [4] XPOS (str)
        [5] FEATS (str)
        [6] HEAD (str)
        [7] DEPREL (str)
        [8] DEPS (str)
        [9] MISC (str)
        [10] IDENTITY (list)    --> [ [EntityID, MarkableID, Min, SemType, ...], ... ]
        [11] BRIDGING (list)    --> [ [MarkableID, Rel, ...], ... ]
        [12] DISCOURSE_DEIXIS (list)    --> [ [EntityID, MarkableID, Min, SemType, ...], ... ]
        [13] REFERENCE (list)   --> [ [...], ... ]
        [14] NOM_SEM (list) --> [ [MarkableID, Entity_Type, Genericity, ...], ... ]
        ]
        
        [10] bis [14] als eingebettete Listen, um mit eingebetteten Referenzen umzugehen
    """

    data_parsed = list()

    # GEPARSTE KOPIE DER DATEN GENERIEREN
    # fuer jede Zeile...
    for index, line in enumerate(data_raw):
        # leere Zeilen entfernen
        if len(line) == 0:
            pass
        # Zeilen beginnend mit "#" behalten zur Satzerkennung
        elif line[0] == "#":
            data_parsed.append(line)

        else:
            # Spalte 15 (NOM-SEM) existiert nur fuer NP
            # --> wenn nicht vorhanden: "_" anhaengen
            if len(line) == 14:
                line.append("_")

            # EVTL REICHT ES, DAS GANZE NUR FUER SPALTE 12 ZU MACHEN
            # DA DIE ANDEREN SPALTEN uU NICHT RELEVANT SIND
            # fuer die Spalten 10-14
            for column_index in range(10,15):
                # an "(" splitten, um mit eingebetteten Referenzen umzugehen
                line[column_index] = line[column_index].split("(")
                # leere Elemente loeschen, die durch split("(") entstehen
                if line[column_index][0] == "":
                    del line[column_index][0]
                # an "|" splitten --> einzelne Merkmale als Elemente einer eingebetteten Liste
                for index2, element in enumerate(line[column_index]):
                    line[column_index][index2] = element.split("|")

            # fertig geparste Zeile anhaengen
            data_parsed.append(line)

    return data_parsed



def extract_dd_elements(data_parsed):
    """Funktion, die aus den gegebenen Daten alle Elemente extrahiert,
    die als Discourse Deixis annotiert wurden
    Input:
    1. data_parsed (list): Liste mit geparsten Datensaetzen
    Return:
    1. ...
    """

    # ERSTMAL VERSCH DOKUMENTE INNERHALB DER DATEIEN IGNORIEREN
    # MUSS ABER NOCH UNTERSCHIEDEN WERDEN, UM DIE KOREFERENZMENGEN
    # ZU UNTERSCHEIDEN !
    # ANSONSTEN EVENTUELL DIE EINZELNEN DOKUMENTE WOANDERS PARSEN
    # UND DANN HIER EINZELN REINGEBEN
    # EVTL BESSER WEIL SONST DIE DICTIONARIES DYNAMISCH ANGELEGT
    # WERDEN MUESSEN --> DAS WAERE GLAUB ICH NERVIG
    # WEISS NOCH NICHT GENAU MAL GUCKEN


    dd_classes_dict = dict()

    for index, line in enumerate(data_parsed):
        if line[0] == "#":
            pass

        # zeilen ohne dd-annotation ignorieren
        # zeilen mit dd-annotation ")" ignorieren
        # --> werden im prozess erkannt
        elif line[12] != [["_"]] and line[12] != [[")"]]:

            for index2, annotation in enumerate(line[12]):
            #for index2, annotation in enumerate(line_reversed):

                # Fall: DD-Element besteht aus einzelnem Wort
                if len(annotation) > 1 and annotation[-1].endswith(")"):

                    # nur die Zahl, zB '1-DD'
                    #dd_id_key = annotation[0][annotation[0].index("=")+1:]
                    # kompletter String, zB 'EntityID=1-DD'
                    dd_id_key = annotation[0]

                    # DD-Element (komplette Zeile) an Liste der Aequivalenzklasse anhaengen
                    dd_class = dd_classes_dict.get(dd_id_key, list())
                    #dd_class.append(annotation)
                    dd_class.append(line)
                    dd_classes_dict[dd_id_key] = dd_class

                    #print(index, line[0], line[1], line[12], sep="\t")
                    #print()


                elif len(annotation) > 1 and not annotation[-1].endswith(")"):

                    # zaehler fuer eingebettete annotationen
                    counter = len(line[12]) - index2
                    next_index = index

                    while counter != 0:

                        next_index += 1

                        if len(data_parsed[next_index]) == 15:
                            if data_parsed[next_index][12] == [[")"]]:
                                counter -= 1
                        else:
                            pass


                    # for number in range(index, next_index+1):
                    #     #print(index, data_parsed[number])
                    #     if len(data_parsed[number]) == 15:
                    #         #print(index, data_parsed[number][0], data_parsed[number][1], data_parsed[number][12], sep="\t")
                    #     else:
                    #         #print(data_parsed[number])
                    # #print()

                    # zaehler fuer eingebettete dd-annotationen




                # weitere Faelle:
                # - DD-Element besteht aus mehreren Worten
                #   --> ertes Wort erkennen
                #   --> letztes Wort erkennen
                # - eingebettete DD-Elemente erkennen --> Zeilen reversed durchgehen?
                #                                     --> glaub ich brauch nen counter






def tagging_pos_feats_deps(data_parsed):
    """
    Funktion, die bei einem tokenisierten Text UPOS, XPOS, FEATS und DEPS annotiert.
    Benoetigt das Modul 'Stanza' mit dem Standardsprachmodell fuer 'en'.

    :param data_parsed:

    :return:
    """

    # Text als String extrahieren
    words = list()

    for index, line in enumerate(data_parsed):
        if line[0] == "#":
            pass
        else:
            words.append(line[1])
    doc_string = " ".join(words)

    tagger = stanza.Pipeline(lang="en", processors="tokenize,mwt,pos,lemma,depparse")

    #!!!!!!!!!!!!!
    # LIEBER SATZWEISE TAGGEN; SONST KOMISCHE ERGEBNISSE
    #!!!!!!!!!!!!
    doc_tagged = tagger(doc_string)

    print(doc_tagged)





# Funktion, die alle weiteren Funktionen aufruft
def run_script():

    ### KORPORA EINLESEN & PARSEN ###
    # Dateien einlesen
    # Korpora: light, Switchboard, ARRAU (trains9x, gnome, rst_x, pear)
    rawlines_light = read_file(r"SharedTaskData/light_dev.CONLLUA")
    # rawlines_switch = read_file(r"SharedTaskData/Switchboard_3_dev.CONLL_LDC2021E05/Switchboard_3_dev.CONLL")
    # rawlines_trains91 = read_file(r"SharedTaskData/ARRAU2.0_UA_v3_LDC2021E05/v3/Trains_91.CONLL")
    # rawlines_trains93 = read_file(r"SharedTaskData/ARRAU2.0_UA_v3_LDC2021E05/v3/Trains_93.CONLL")
    # rawlines_gnome = read_file(r"SharedTaskData/ARRAU2.0_UA_v3_LDC2021E05/v3/Gnome_Subset2.CONLL")
    # rawlines_pear = read_file(r"SharedTaskData/ARRAU2.0_UA_v3_LDC2021E05/v3/Pear_Stories.CONLL")
    #rawlines_rst_train = read_file(r"SharedTaskData/ARRAU2.0_UA_v3_LDC2021E05/v3/RST_DTreeBank_train.CONLL")


    # Testdaten fuer Uebersichtilichkeit
    rawlines_light_test = rawlines_light[0:int(len(rawlines_light)/10)]
    # Parsen
    #light_parsed = parse_data(rawlines_light)
    # print("LIGHT DONE")
    lighttest_parsed = parse_data(rawlines_light_test)
    print("LIGHT TEST DONE PARSING")
    tagging_pos_feats_deps(lighttest_parsed)



    # switch_parsed = parse_data(rawlines_switch)
    # print("SWITCH DONE")
    # trains91_parsed = parse_data(rawlines_trains91)
    # print("TRAINS91 DONE")
    # trains93_parsed = parse_data(rawlines_trains93)
    # print("TRAINS93 DONE")
    # gnome_parsed = parse_data(rawlines_gnome)
    # print("GNOME DONE")
    # pear_parsed = parse_data(rawlines_pear)
    # print("PEAR DONE")
    #rst_train_parsed = parse_data(rawlines_rst_train)
    #print("RST_TRAIN DONE")


    # TESTAUSGABEN TEST TEST
    #extract_dd_elements(light_parsed)

    #extract_dd_elements(rst_train_parsed)

    counter = 0
    # for index, line in enumerate(light_parsed):
    #     if line[0] == "#":
    #         pass
    #     elif line[12] != [["_"]]:
    #         print(index, line[0], line[1], line[12], sep="\t")

###########################################################
# Hauptprogramm
###########################################################

if __name__ == "__main__":

    # Funktion, die alle weiteren Funktionen aufruft
    run_script()