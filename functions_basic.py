"""
------------------------
Matthias Guetebier
Matr.-Nr.: 108016243375
------------------------


Grundlegende Funktionen fuer den Umgang mit Daten und Strukturen.
Backend, nicht zur Verwendung von Nutzern geeignet.
"""




##################################
### EXTERNE MODULE IMPORTIEREN ###
##################################

### PATHLIB ###
from pathlib import Path

### SCIKIT-LEARN ###
# DictVectorizer zur Vektorisierung von Feature-Dictionaries
# enthaelt 'OneHot-Encoding' fuer kategorische Features
from sklearn.feature_extraction import DictVectorizer
# Sklearn-Implementationen von Logistischer Regression fuer Klassifizierung
from sklearn.linear_model import LogisticRegression, SGDClassifier

### PICKLE ###
# Modelle / KLassifizierer exportieren & importieren
import pickle


### GLOBALE VARIABLEN ###

# Liste von Shell Nouns
shell_nouns = ['ability', 'absurdity', 'acceptance', 'accident', 'account', 'accusation',
               'achievement', 'acknowledgement', 'act', 'action', 'adage', 'admission', 'advantage',
               'advice', 'affirmation', 'age', 'agenda', 'agreement', 'aim', 'allegation', 'allegory',
               'alternative', 'amazement', 'ambition', 'amendment', 'analogy', 'analysis', 'anger',
               'announcement', 'annoyance', 'anomaly', 'answer', 'anticipation', 'anxiety', 'aphorism',
               'appeal', 'application', 'appointment', 'appreciation', 'apprehension', 'approach',
               'area', 'argument', 'arrangement', 'art', 'aspect', 'assertion', 'assessment', 'asset',
               'assignment', 'assumption', 'assurance', 'astonishment', 'attempt', 'attitude',
               'attraction', 'attribute', 'audacity', 'authority', 'awareness', 'axiom', 'bargain',
               'basis', 'beauty', 'belief', 'benefit', 'bet', 'betting', 'bid', 'bitterness', 'blessing',
               'blow', 'boast', 'bonus', 'breakthrough', 'brief', 'burden', 'business', 'calculation',
               'call', 'campaign', 'capability', 'capacity', 'case', 'catastrophe', 'catch', 'catchphrase',
               'cause', 'caveat', 'certainty', 'challenge', 'chance', 'change', 'characteristic', 'charge',
               'charm', 'cheek', 'choice', 'claim', 'cliche', 'clout', 'clue', 'coincidence', 'comfort',
               'command', 'comment', 'commission', 'commitment', 'compensation', 'complaint', 'complication',
               'compliment', 'compromise', 'compulsion', 'concept', 'conception', 'concern', 'concession',
               'conclusion', 'condition', 'confession', 'confidence', 'confirmation', 'conjecture',
               'connection', 'consensus', 'consequence', 'consideration', 'consolation', 'conspiracy',
               'constraint', 'contention', 'context', 'contract', 'contradiction', 'contrast', 'contribution',
               'conundrum', 'convention', 'conviction', 'corollary', 'counterclaim', 'countermeasure', 'coup',
               'courage', 'courtesy', 'credo', 'crime', 'criterion', 'criticism', 'critique', 'crusade', 'crux',
               'cure', 'curiosity', 'curse', 'custom', 'danger', 'deal', 'debacle', 'decency', 'deception',
               'decision', 'declaration', 'decree', 'deduction', 'defence', 'definition', 'delight', 'delusion',
               'demand', 'demonstration', 'denial', 'description', 'desire', 'destiny', 'determination', 'diagnosis',
               'dictum', 'difference', 'difficulty', 'dilemma', 'directive', 'disadvantage', 'disappointment',
               'disaster', 'disclosure', 'discovery', 'discrepancy', 'disgrace', 'disgust', 'disinclination', 'disposition',
               'disquiet', 'distinction', 'distortion', 'doctrine', 'dogma', 'doubt', 'downside', 'drama', 'drawback',
               'dread', 'dream', 'drive', 'duty', 'eagerness', 'edict', 'effect', 'effort', 'effrontery', 'endeavour',
               'energy', 'enigma', 'enterprise', 'equation', 'era', 'error', 'essence', 'estimate', 'ethos', 'event',
               'evidence', 'example', 'exception', 'excuse', 'expectation', 'experience', 'explanation', 'extent',
               'facility', 'fact', 'factor', 'failure', 'faith', 'fallacy', 'fantasy', 'farce', 'fate', 'fault', 'fear',
               'feature', 'feeling', 'fiction', 'fight', 'finding', 'flaw', 'flexibility', 'folly', 'forecast', 'foresight',
               'formula', 'foundation', 'franchise', 'freedom', 'frustration', 'function', 'fury', 'gall', 'gambit', 'gamble',
               'generalization', 'goal', 'gossip', 'grace', 'gratitude', 'grief', 'grievance', 'gripe', 'ground', 'grudge',
               'grumble', 'guarantee', 'guess', 'guilt', 'gumption', 'habit', 'handicap', 'happiness', 'heart', 'hint', 'hope',
               'hunch', 'hurdle', 'hypothesis', 'idea', 'ideal', 'illusion', 'image', 'impact', 'imperative', 'impetus',
               'implication', 'importance', 'impression', 'improvement', 'impulse', 'inability', 'incapacity', 'incentive',
               'inclination', 'inconsistency', 'indication', 'indicator', 'indignation', 'inducement', 'inevitability', 'inference',
               'information', 'initiative', 'injunction', 'inkling', 'innovation', 'insight', 'insistence', 'inspiration', 'instinct',
               'instruction', 'intelligence', 'intent', 'intention', 'interest', 'interpretation', 'intimation', 'intuition',
               'invitation', 'irony', 'irritation', 'issue', 'job', 'joke', 'joy', 'judgement', 'justification', 'keenness',
               'key', 'knack', 'knowledge', 'lament', 'law', 'leeway', 'legacy', 'legend', 'lesson', 'licence', 'lie', 'likelihood',
               'limitation', 'line', 'link', 'logic', 'longing', 'luck', 'mandate', 'manifestation', 'manoeuvre', 'marvel', 'maxim',
               'measure', 'merit', 'message', 'metaphor', 'method', 'miracle', 'misapprehension', 'miscalculation', 'misconception',
               'misfortune', 'misjudgment', 'misperception', 'mission', 'mistake', 'moment', 'motion', 'motivation', 'motive', 'motto',
               'move', 'mystery', 'myth', 'necessity', 'need', 'nerve', 'news', 'nightmare', 'nonsense', 'norm', 'notice',
               'notification', 'notion', 'nous', 'novelty', 'nuisance', 'oath', 'object', 'objection', 'objective', 'obligation',
               'observation', 'obsession', 'obstacle', 'occasion', 'oddity', 'offence', 'offer', 'opinion', 'opportunity', 'option',
               'order', 'orthodoxy', 'outcome', 'pact', 'pain', 'paradox', 'paranoia', 'part', 'passion', 'payoff', 'peculiarity',
               'perception', 'period', 'permission', 'permit', 'perspective', 'persuasion', 'petition', 'phenomenon', 'philosophy',
               'pity', 'place', 'plan', 'plea', 'pleasure', 'pledge', 'plot', 'ploy', 'point', 'policy', 'position', 'possibility',
               'potential', 'power', 'practice', 'praise', 'precaution', 'precept', 'preconception', 'precondition', 'predicament',
               'prediction', 'preface', 'preference', 'prejudice', 'premise', 'premonition', 'preoccupation', 'presentiment', 'pressure',
               'presumption', 'presupposition', 'pretence', 'pretext', 'pride', 'principle', 'priority', 'privilege', 'prize',
               'probability', 'problem', 'procedure', 'proclamation', 'prognosis', 'programme', 'project', 'projection', 'promise',
               'pronouncement', 'proof', 'propensity', 'prophecy', 'proposal', 'proposition', 'prospect', 'protest', 'proverb',
               'provision', 'proviso', 'provocation', 'punishment', 'purpose', 'puzzle', 'qualification', 'query', 'quest',
               'question', 'quibble', 'race', 'rage', 'rationale', 'reaction', 'readiness', 'reading', 'realisation',
               'reality', 'reason', 'reasoning', 'reassurance', 'recipe', 'reckoning', 'recognition', 'recollection',
               'recommendation', 'refinement', 'reflection', 'refusal', 'region', 'regret', 'relief', 'reluctance',
               'remark', 'remedy', 'reminder', 'reply', 'report', 'reposte (ri~)', 'request', 'requirement',
               'resentment', 'reservation', 'resistance', 'resolution', 'resolve', 'response', 'responsibility',
               'restriction', 'result', 'retort', 'revelation', 'revolution', 'reward', 'right', 'risk', 'ritual',
               'role', 'room', 'routine', 'rule', 'ruling', 'rumour', 'ruse', 'rush', 'sadness', 'satisfaction',
               'scandal', 'scenario', 'scheme', 'scope', 'secret', 'sensation', 'sentiment', 'sequel', 'shame',
               'shock', 'sign', 'signal', 'significance', 'similarity', 'sin', 'site', 'situation', 'skill', 'slogan',
               'snag', 'solace', 'solution', 'sorrow', 'space', 'speciality', 'speculation', 'spot', 'stage', 'stamina',
               'stance', 'stand', 'standpoint', 'statement', 'step', 'stereotype', 'stipulation', 'story', 'strategy',
               'strength', 'struggle', 'subject', 'subtext', 'success', 'suggestion', 'superstition', 'supposition',
               'surmise', 'surprise', 'suspicion', 'symbol', 'symptom', 'tactic', 'tale', 'talent', 'talk', 'target',
               'task', 'teaching', 'technique', 'temerity', 'temptation', 'tendency', 'tenet', 'terror', 'test', 'testimony',
               'theme', 'theory', 'thesis', 'thing', 'thinking', 'thought', 'threat', 'thrill', 'time', 'tip', 'topic',
               'tradition', 'tragedy', 'travesty', 'trend', 'trick', 'triumph', 'trouble', 'truism', 'truth', 'twist',
               'uncertainty', 'understanding', 'undertaking', 'unknown', 'unwillingness', 'upshot', 'urge', 'venture',
               'verdict', 'version', 'view', 'viewpoint', 'virtue', 'vision', 'vocation', 'vow', 'warning', 'way', 'weakness',
               'whinge', 'whisper', 'willingness', 'willpower', 'wisdom', 'wish', 'wit', 'wonder', 'worry', 'yearning', 'zeal']




#######################
### VORVERARBEITUNG ###
#######################
### ACHTUNG ###
### In diesem Abschnitt werden Kenntnisse
### ueber das verwendete Annotationsschema vorausgesetzt


def read_file(filename: str) -> list:
    """
    Datensatz zeilenweise einlesen, vorangehenden und abschliessenden Whitespace entfernen.
    Rueckgabe von Liste mit Zeilen.

    :param filename (str): _kompletter_ Pfad der einzulesenden Daten
    :return: lines (list): Liste mit eingelesenen Zeilen
    """

    # Dateipfad systemuebergreifend konvertieren
    filename = Path(filename)

    # Datensatz oeffnen und zeilenweise einlesen
    with open(filename, mode="r", encoding="UTF-8") as infile:
        lines = infile.readlines()

    # vorangehenden und abschliessenden Whitespace entfernen
    for index, line in enumerate(lines):
        lines[index] = line.strip()

    return lines


def process_data(lines: list) -> dict:
    """
    Daten bereinigen und in geeignete Struktur fuer Weiterverarbeitung bringen.

    :param lines (list): Liste mit eingelesenen Zeilen
    :return: data_dict (dict): Dictionary mit eingebetteten Dictionaries (3 Ebenen)
        - Ebene 1: Keys fuer Dokumente innerhalb eines Datensatzes, string ("doc_id1/2/.../n")
        - Ebene 2: Keys fuer Saetze innerhalb eines Dokumentes, integer (1, 2, ...)
        - Ebene 3: Keys fuer Token im Satz, integer (1, 2, ...)
        - Struktur von data_dict: {"doc_id": {sent_id : {tok_id : Liste mit Annotationen }}}
        - Struktur der Liste hinter Key "tok_id": data_dict["doc_id"][sent_id][tok_id]
            [   [0] FORM (str)
                [1] LEMMA (str)
                [2] UPOS (str)
                [3] XPOS (str)
                [4] FEATS (str)
                [5] HEAD (str)
                [6] DEPREL (str)
                [7] DEPS (str)
                [8] MISC (str)
                [9] IDENTITY (list)
                [10] BRIDGING (list)
                [11] DISCOURSE_DEIXIS (list) -> [EntityID, MarkableID, Min, etc]
                [12] REFERENCE (list)
                [13] NOM_SEM (str)
            ]
    """

    # Liste fuer Zwischenschritt der Bereinigung
    lines_temp = list()
    # Dictionary fuer bereinigte Daten
    data_dict = dict()

    # erste Zeile aus eingelesener Datei entfernen
    # (--> Beschreibung der Spalten)
    lines.pop(0)

    # ueber Zeilen iterieren
    for index, line in enumerate(lines):
        # leere Zeilen ignorieren
        if line == "":
            pass

        # weitere Zeilen an Whitespace splitten
        else:
            lines_temp.append(line.split())


    # Zaehler fuer Dokumente und Saetze innerhalb eines Datensatzes
    counter_docs = 0
    counter_sents = 0

    # ueber nicht-leere Zeilen iterieren
    for index, line in enumerate(lines_temp):
        # Zeilen beginnend mit '#'
        # -> enthalten Metainformation
        if line[0] == "#":

            # "newdoc"-Zeile
            # -> neues Dokument in einem Datensatz
            if line[1].strip() == "newdoc":
                # Zaehler Dokumente hochsetzen
                counter_docs += 1
                # Zaehler Saetze pro Dokument zuruecksetzen
                counter_sents = 0

                # doc_id zwischenspeichern
                current_doc_id = "doc_id" + str(counter_docs)
                # doc_id = neuer Key, Value dict
                data_dict[current_doc_id] = dict()

            # "sent_id"-Zeile
            # -> neuer Satz in Dokument
            elif line[1].strip() == "sent_id":

                # Zaehler Saetze hochsetzen
                # Zaehler als Key, Value dict
                counter_sents += 1
                data_dict[current_doc_id][counter_sents] = dict()

            # andere "#"-Zeilen ignorieren
            else:
                pass

        # Zeilen, die nicht mit "#" beginnen
        # -> Token mit Annotationen
        else:
            # "_"-Element anhaengen, falls Annotation in Spalte "NOM_SEM" fehlt
            # betrifft alle Token, bei denen Spalte "IDENTITY" nicht annotiert wurde
            if len(line) == 14:
                line.append("_")

            # aktuelle tok_id zwischenspeichern
            # tok_id als Key, Value Liste mit Annotationen
            current_tok_id = int(line[0])
            data_dict[current_doc_id][counter_sents][current_tok_id] = line[1:]

    return data_dict


def write_annotated_data(filename: str, data_annotated: dict) -> None:
    """
    Die annotierten Datensaetzen in neue Textdateien schreiben,
    um die Annotationen von Stanza permanent sichern zu koennen.
    Datei wird in Unterverzeichnis 'data_annotataed' geschrieben.

    :param filename (str): Name der zu schreibenden Datei (nicht kompletter Pfad)
                - z.B. filename = 'development/AMI_annotated.txt'
    :param data_annotated (dict): Datensatz als Dictionary
    :return: None, schreibt Datei mit Annotationen
    """

    # systemuebergreifender Pfad
    path_to_write = Path(Path.cwd(), "data_annotated", filename)

    # zu schreibende Datei oeffnen/anlegen
    with open(path_to_write, mode="w", encoding="UTF-8") as outfile:
        for doc in data_annotated:
            # aktuelle DokumentID als "#"-Zeile
            outfile.write("#\t" + doc +"\n")

            for sent in data_annotated[doc]:
                # aktuelle SatzID als "#"-Zeile
                outfile.write("#\t" + str(sent) + "\n")

                # Token + Annotationen zeilenweise schreiben
                # Token + Annotationen durch Tabs getrennt
                for tok_id in data_annotated[doc][sent]:
                    outfile.write(str(tok_id) + "\t")
                    for element in data_annotated[doc][sent][tok_id]:
                        outfile.write(str(element) + "\t")
                    outfile.write("\n")

    return None


def convert_DDannotations_to_dict(data_dict: dict) -> dict:
    """
    Hilfsfunkion.
    Annotationen zu DiscourseDeixis in eingelesenen Datensaetzen zu Dictionaries umwandeln (voher Listen).
    Bsp.:
        - Input: data_dict[doc][sent][tok][11] = ["EntityID=id", "MarkableID=id", ...]
        - Output: data_dict[doc][sent][tok][11] = {"EntityID": id, "MarkableID":id, "Min":(int, int), etc.}

    :param data_dict (dict): Datensatz als Dictionary mit DD-Infos als Listen
    :return data_dict (dict): Datensatz als Dictionary mit DD-Infos als Dictionaries
    """

    # uber Token iterieren
    for doc in data_dict:
        for sent in data_dict[doc]:
            for tok in data_dict[doc][sent]:

                # Annotationen zwischenspeichern
                # tok_annotation[11] = Spalte zu DiscourseDeixis
                tok_annotation = data_dict[doc][sent][tok]


                # Token Instanz von DiscourseDeixis
                if tok_annotation[11].startswith("("):

                    # Klammern aus Annotationen entfernen, Normierung
                    if tok_annotation[11].endswith(")"):
                        data_dict[doc][sent][tok][11] = tok_annotation[11][1:-1]
                    else:
                        data_dict[doc][sent][tok][11] = tok_annotation[11][1:]

                    # Zwischenstrukuren
                    # fuer vorhandene DD-Infos
                    current_keys = list()
                    current_vals = list()

                    # DD-Infos in Keys/Values aufteilen
                    # einzelne Infos getrennt durch "|"
                    # z.B. "EntityID=DD-Id1" --> {"EntityID":Id1}
                    for entry in tok_annotation[11].split("|"):
                        border_index = entry.index("=")
                        current_keys.append(entry[0:border_index])
                        current_vals.append(entry[border_index + 1:])
                    # Keys/Values als Dictionary
                    tok_as_dict = dict(zip(current_keys, current_vals))

                    # "Min" = minimale Spanne der Instanz
                    # -> zu Tupel umwandeln (IndexAnfang, IndexEnde)
                    tok_as_dict["Min"] = tuple([int(index) for index in tok_as_dict["Min"].split(",")])
                    data_dict[doc][sent][tok][11] = tok_as_dict

    return data_dict


def read_annotated_data(filename: str) -> dict:
    """
    Textdateien mit annotierten Datensaetzen einlesen.

    :param filename (str): Pfad der einzulesenden Datei, ausgehend von Unterverzeichnis 'data_annotated'
    :return data_dict (dict): Datensatz als Dictionary (Struktur: siehe 'process_data()')
    """

    # Pfad systemuebergreifend
    #filename = Path(filename)
    filename = Path(Path.cwd(), "data_annotated", filename)

    # Datei zeilenweise einlesen
    with open(filename, mode="r", encoding="UTF-8") as infile:
        lines = infile.readlines()
    for index, line in enumerate(lines):
        lines[index] = line.split()

    # Dictionary anlegen
    data_dict = dict()

    # ueber Zeilen iterieren
    for line in lines:
        # Zeile mit DokumentID
        if line[0].strip().startswith("#") and line[1].strip().startswith("doc"):
            # DokumentID als Key, Value dict
            current_doc = line[1]
            data_dict[current_doc] = {}

        # "#"-Zeile mit SatzID
        elif line[0].strip().startswith("#"):
            # SatzID als Key, Value dict
            current_sent = int(line[1])
            data_dict[current_doc][current_sent] = {}

        # Zeile mit Token
        else:
            # TokID als Key, Value Liste mit Annotationen
            data_dict[current_doc][current_sent][int(line[0])] = []
            for entry in line[1:]:
                data_dict[current_doc][current_sent][int(line[0])].append(entry)
    # DD-Infos zu Dictionaries umwandeln
    data_dict = convert_DDannotations_to_dict(data_dict)

    return data_dict


def extract_dd_elements(data: dict) -> dict:
    """
    Instanzen von Discourse Deixis aus Datensatz extrahieren.
    Zusammengehoerige Instanzen gruppieren.

    :param data (dict): Datensatz als Dictionary
    :return: coref_dict(dict): Dictionary mit Gruppen von koreferierenden DD-Instanzen
            - Struktur coref_dict = {doc_id: {entity_id: {"elements": ( Min=(int, int), sent=(int) } } }
    """

    # Dictionary fuer Koreferenzmengen
    coref_dict = dict()

    # ueber Token iterieren
    for doc in data:
        # DokumentID als Key, Value dict
        coref_dict[doc] = dict()

        for sent in data[doc]:
            for tok in data[doc][sent]:

                # Annotationen zu Token zwischenspeichern
                tok_annotation = data[doc][sent][tok]

                # Instanz von DD
                if type(tok_annotation[11]) == dict:

                    # EntityID zwischenspeichern
                    # zur Gruppierung koreferierender Instanzen
                    current_entID = tok_annotation[11]["EntityID"]

                    # Antezedenzien bestehend aus mehreren Saetzen
                    if "ElementOf" in tok_annotation[11].keys():
                        current_entID = tok_annotation[11]["ElementOf"]

                    # EntityID als Key, Value dict
                    # coref_dict[doc][current_entID]["elements"] = tuple
                    #   --> ( Min, SentID ) --> ( (Int, Int), String )
                    coref_dict[doc][current_entID] = coref_dict[doc].get(current_entID, dict())
                    coref_dict[doc][current_entID]["elements"] = coref_dict[doc][current_entID].get("elements", list())
                    coref_dict[doc][current_entID]["elements"].append((tok_annotation[11]["Min"], sent))

    return coref_dict


def cleanup_coref_dict(data: dict, coref: dict) -> dict:
    """
    Nicht relevante Faelle aus Dictionary mit Koreferenzmengen rausfiltern.
    Nicht relevante Faelle:
        - anaphorischer Ausdruck != "it", "this", "that"
        - Antezedens besteht aus mehr als einem Satz

    :param data (dict): Datensatz als Dictionary
    :param coref (dict): Dictionary mit Koreferenzmengen aus Datensatz
    :return coref_clean (dict): Dictionary mit relevanten Koreferenzmengen
    """

    # Liste relevanter anaphorischer Ausdruecke
    relevant_forms = ["this", "that", "it"]
    # Dictionary fuer relevante DD-Instanzen
    coref_clean = dict()

    # ueber Koreferenzmengen iterieren
    for doc in coref:
        for dd_ent in coref[doc]:

            # Menge enthaelt genau zwei Elemente
            # --> [0] = Antezedens, [1] = Anapher
            if len(coref[doc][dd_ent]["elements"]) == 2:

                # sent_id der Anapher fuer leichteren lookup
                sent_id = coref[doc][dd_ent]["elements"][1][1]

                # Anapher besteht aus genau einem Token
                if coref[doc][dd_ent]["elements"][1][0][0] == coref[doc][dd_ent]["elements"][1][0][1]:
                    # zwischenspeichern fuer leichteren Lookup
                    anaph_id = coref[doc][dd_ent]["elements"][1][0][0]
                    anaph_form = data[doc][sent_id][anaph_id][0].lower()

                    # Anaphorischer Ausdruck = "it/this/that"
                    # -> Koreferenzmenge zur relevanten Mengen
                    if anaph_form in relevant_forms:
                        coref_clean[doc] = coref_clean.get(doc, {})
                        coref_clean[doc][dd_ent] = coref[doc][dd_ent]

    return coref_clean


def get_true_dd_elements(coref: dict) -> list:
    """
    Hilfsfunktion.
    Liste mit IDs von Elementen von Koreferenzmengen erstellen.
    Erleichtert abgleich mit Golddaten.

    :param coref (dict): Dictionary mit relevanten Koreferenzmengen
    :return true_dd_ent (list): Liste mit IDs zu Koreferenzmengen
        - Struktur = [ (ante_sent_id, anaph_tok_ik, doc_id), (...), ...]
    """

    # Liste initiieren
    true_dd_ent = list()

    # ueber Koreferenzmengen iterieren
    for doc in coref:
        for dd_id in coref[doc]:
            # Tuple mit IDs an Liste haengen
            # SatzID Antezedens, TokID Anapher, DokumentID
            ante_sent_id = coref[doc][dd_id]["elements"][0][1]
            anaph_tok_id = coref[doc][dd_id]["elements"][1][0][0]
            true_dd_ent.append(tuple([ante_sent_id, anaph_tok_id, doc]))

    return true_dd_ent


def get_candidates(data: dict, ante_scope_in: int=4) -> dict:
    """
    Aus Testdatensaetzen Kandidatenpaare fuer Koreferenzen extrahieren.
    Schema: "it/this/that" + vorangehender Satz in festgelegtem Skopus.
    Paare: SatzID Antezedens, TokID Anapher

    :param data (dict): Datensatz als Dictionary
    :param ante_scope (int): Skopus der Antezedens-Kandidaten, Default=4
    :return candidates (dict): Dictionary mit Anaphern (tok_id) und moeglichen Antezedenzien ( [sent_id1, sent_id2, ...] ).
        - Struktur = {doc_id: {tok_id: [sent_id1, sent_id2, ...] }}
    """

    # relevante Formen/Anaphern
    relevant_forms = ["it", "this", "that"]
    # Dictionary fuer Kandidaten initiieren
    candidates = dict()

    # ueber Token iterieren
    for doc in data:
        candidates[doc] = {}

        for sent in data[doc]:
            for tok in data[doc][sent]:
                # Token = "it/this/that"
                if data[doc][sent][tok][0].strip().lower() in relevant_forms:
                    # Eintrag Liste von Ante-Kandidaten
                    # inklusive aktuellem Satz
                    candidates[doc][tok] = []

                    # Skopus fuer Kandidaten-Saetze
                    ante_scope = ante_scope_in
                    # IndexError vermeiden, falls Skopus zu gross
                    if sent < ante_scope:
                        ante_scope = ante_scope - (ante_scope - sent)
                    for prev_sent in range(ante_scope):
                        candidates[doc][tok].append(sent - prev_sent)

    return candidates


def get_features_testdata(data: dict, candidates: dict, form_in: bool=True,
                          sent_dist_in: bool=True, tok_dist_in: bool=True,
                          anaph_pron_in: bool=True, len_ante_in: bool=True,
                          lexical_overlap_in: bool=True, part_of_shell_noun_in: bool=True,
                          ante_inf_verb_in: bool=True) -> dict:
    """
    Features zur Klassifizierung fuer jedes Kandidatenpaar extrahieren
    und in Dictionary eintragen.

    :param data (dict): Datensatz als Dictionary
    :param candidates (dict): Kandidatenpaare als Dictionary
    :param form_in (bool): Feature einbeziehen. Default=True
    :param sent_dist_in (bool): Feature einbeziehen. Default=True
    :param tok_dist_in (bool): Feature einbeziehen. Default=True
    :param anaph_pron_in (bool): Feature einbeziehen. Default=True
    :param len_ante_in (bool): Feature einbeziehen. Default=True
    :param lexical_overlap_in (bool): Feature einbeziehen. Default=True
    :param part_of_shell_noun_in (bool): Feature einbeziehen. Default=True
    :param ante_inf_verb_in (bool): Feature einbeziehen. Default=True
    :return: feature_dict (dict): Dictionary mit IDs und Features zu Kandidatenpaaren
        - Struktur= {KandidatID: {"identifier": {"anaph_sent_id":val, "ante_sent_id":val, "anaph_tok_id":val, "ante_tok_id":val, "doc":val},
                                 {"features": {"form":val, "sent_dist":val, "tok_dist":val} }
    """

    # Dictionary fuer Features
    feature_dict = dict()
    # ID fuer Ante-Anaph-Paare
    ent_id = 0

    # ueber Kandidatenpaare iterieren
    for doc in candidates:
        for anaph_tok_id in candidates[doc]:
            for ante_sent_id in candidates[doc][anaph_tok_id]:
                ent_id += 1

                # zwischenspeichern fuer leichteren Lookup
                anaph_sent_id = candidates[doc][anaph_tok_id][0]
                ante_tok_id = min(data[doc][ante_sent_id].keys())

                # IDs zu Kandidatenpaar eintragen
                feature_dict[ent_id] = {"identifier":{}, "features":{}}
                feature_dict[ent_id]["identifier"]["anaph_sent_id"] = anaph_sent_id
                feature_dict[ent_id]["identifier"]["ante_sent_id"] = ante_sent_id
                feature_dict[ent_id]["identifier"]["anaph_tok_id"] = anaph_tok_id
                feature_dict[ent_id]["identifier"]["ante_tok_id"] = ante_tok_id
                feature_dict[ent_id]["identifier"]["doc"] = doc

                # Featurewerte eintragen
                if form_in:
                    feature_dict[ent_id]["features"]["form"] = data[doc][anaph_sent_id][anaph_tok_id][0].strip().lower()
                if sent_dist_in:
                    feature_dict[ent_id]["features"]["sent_dist"] = anaph_sent_id - ante_sent_id
                if tok_dist_in:
                    #feature_dict[ent_id]["features"]["tok_dist"] = anaph_tok_id - ante_tok_id
                    feature_dict[ent_id]["features"]["tok_dist"] = anaph_tok_id - max(data[doc][ante_sent_id].keys())

                if anaph_pron_in:
                    if data[doc][anaph_sent_id][anaph_tok_id][2] == "PRON":
                        feature_dict[ent_id]["features"]["anaph_pron"] = 1
                    else:
                        feature_dict[ent_id]["features"]["anaph_pron"] = 0
                if len_ante_in:
                    feature_dict[ent_id]["features"]["len_ante"] = len(data[doc][ante_sent_id].keys())
                if lexical_overlap_in:
                    feature_dict[ent_id]["features"]["lexical_overlap"] = get_lexical_overlap(data, doc, ante_sent_id, anaph_sent_id)
                if part_of_shell_noun_in:
                    # EVTL LISTE MIT SHELL NOUNS HARDCODEN??
                    #shell_nouns = read_shell_nouns("data_annotated/other/appendix_habil_schmid.csv")
                    global shell_nouns
                    feature_dict[ent_id]["features"]["part_of_shell_noun"] = get_shell_noun_part(shell_nouns, data, doc, anaph_sent_id, anaph_tok_id)

                if ante_inf_verb_in:
                    feature_dict[ent_id]["features"]["ante_inf_verb"] = get_has_inf_verb(data, doc, ante_sent_id)

    return feature_dict


def get_features_traindata(data: dict, coref: dict, with_tn_in: bool=True, ante_scope_in: int=3,
                           form_in: bool=True, sent_dist_in: bool=True, tok_dist_in: bool=True, anaph_pron_in: bool=True,
                           len_ante_in: bool=True, lexical_overlap_in: bool=True, part_of_shell_noun_in: bool=True,
                           ante_inf_verb_in: bool=True) -> dict:
    """
    Features zur Klassifizierung fuer Trainingspaare extrahieren und
    in ein Dictionary eintragen.

    :param data (dict): Datensatz als Dictionary
    :param coref (dict): Dictionary mit Koreferenzmengen aus Datensatz
    :param with_tn_in (bool): True Negatives in Trainingsdaten einbeziehen ja/nein, Default=True
    :param ante_scope_in (int): Skopus der Antezedens-Kandidaten fuer TN
    :param form_in (bool): Feature einbeziehen. Default=True
    :param sent_dist_in (bool): Feature einbeziehen. Default=True
    :param tok_dist_in (bool): Feature einbeziehen. Default=True
    :param anaph_pron_in (bool): Feature einbeziehen. Default=True
    :param len_ante_in (bool): Feature einbeziehen. Default=True
    :param lexical_overlap_in (bool): Feature einbeziehen. Default=True
    :param part_of_shell_noun_in (bool): Feature einbeziehen. Default=True
    :param ante_inf_verb (bool): Feature einbeziehen. Default=True
    :return: feature_dict (dict): Dictionary mit IDs und Features zu Trainingspaaren
        - Struktur= {KandidatID: {"identifier": {"anaph_sent_id":val, "ante_sent_id":val, "anaph_tok_id":val, "ante_tok_id":val, "doc":val, "tp_anaph":val},
                                 {"features": {"form":val, "sent_dist":val, "tok_dist":val} }
    """

    # Dictionary fuer Features
    feature_dict = dict()
    # ID fuer Ante-Anaph-Paare
    ent_id = 0

    # ueber Trainingspaare iterieren
    for doc in coref:
        for dd_ent in coref[doc]:
            ent_id += 1

            # zwischenspeichern fuer leichteren lookup
            anaph_sent_id = coref[doc][dd_ent]["elements"][1][1]
            ante_sent_id = coref[doc][dd_ent]["elements"][0][1]
            anaph_tok_id = coref[doc][dd_ent]["elements"][1][0][0]
            ante_tok_id = coref[doc][dd_ent]["elements"][0][0][0]

            # IDs zu Trainingspaar eintragen
            feature_dict[ent_id] = {"identifier":{}, "features":{}}
            feature_dict[ent_id]["identifier"]["anaph_sent_id"] = anaph_sent_id
            feature_dict[ent_id]["identifier"]["ante_sent_id"] = ante_sent_id
            feature_dict[ent_id]["identifier"]["anaph_tok_id"] = anaph_tok_id
            feature_dict[ent_id]["identifier"]["ante_tok_id"] = ante_tok_id
            feature_dict[ent_id]["identifier"]["doc"] = doc
            # Eintrag, ob TN-Instanz mit
            # TN-Anaph oder TP-Anaph
            if ante_sent_id:
                feature_dict[ent_id]["identifier"]["tp_anaph"] = 1

            # Featurewerte eintragen
            feature_dict[ent_id]["features"]["is_instance"] = 1
            if form_in:
                feature_dict[ent_id]["features"]["form"] = data[doc][anaph_sent_id][anaph_tok_id][0].lower()
            if sent_dist_in:
                feature_dict[ent_id]["features"]["sent_dist"] = anaph_sent_id - ante_sent_id
            if tok_dist_in:
                # tok_dist basierend auf _letztem_ token in Antezedens
                # -> daher 'ante_tok_id' nicht anwendbar
                #feature_dict[ent_id]["features"]["tok_dist"] = anaph_tok_id - ante_tok_id
                feature_dict[ent_id]["features"]["tok_dist"] = anaph_tok_id - max(data[doc][ante_sent_id].keys())
            if anaph_pron_in:
                if data[doc][anaph_sent_id][anaph_tok_id][2] == "PRON":
                    feature_dict[ent_id]["features"]["anaph_pron"] = 1
                else:
                    feature_dict[ent_id]["features"]["anaph_pron"] = 0
            if len_ante_in:
                feature_dict[ent_id]["features"]["len_ante"] = len(data[doc][ante_sent_id].keys())
            if lexical_overlap_in:
                feature_dict[ent_id]["features"]["lexical_overlap"] = get_lexical_overlap(data, doc, ante_sent_id, anaph_sent_id)
            if part_of_shell_noun_in:
                # EVTL LISTE MIT SHELL NOUNS HARDCODEN??
                #shell_nouns = read_shell_nouns("data_annotated/other/appendix_habil_schmid.csv")
                global shell_nouns
                feature_dict[ent_id]["features"]["part_of_shell_noun"] = get_shell_noun_part(shell_nouns, data, doc, anaph_sent_id, anaph_tok_id)

            if ante_inf_verb_in:
                feature_dict[ent_id]["features"]["ante_inf_verb"] = get_has_inf_verb(data, doc, ante_sent_id)

    # wenn erwuenscht
    # Eintraege fuer TN anlegen
    if with_tn_in:
        feature_dict = get_true_negatives(data, coref, feature_dict, ante_scope_in, form_in=form_in, sent_dist_in=sent_dist_in, tok_dist_in=tok_dist_in,
                                          anaph_pron_in=anaph_pron_in, len_ante_in=len_ante_in, lexical_overlap_in=lexical_overlap_in,
                                          part_of_shell_noun_in=part_of_shell_noun_in, ante_inf_verb_in=ante_inf_verb_in)

    return feature_dict


def get_true_negatives(data: dict, coref: dict, feat_dict: dict, ante_scope_in: bool, form_in: bool,
                       sent_dist_in: bool, tok_dist_in: bool, anaph_pron_in: bool, len_ante_in: bool,
                       lexical_overlap_in: bool, part_of_shell_noun_in: bool, ante_inf_verb_in: bool):
    """
    Hilfsfunktion.
    Eintraege fuer TN in Dictionary mit Trainingsdaten anlegen.
    Parameter werden aus Funktion 'get_features_traindata()' uebergeben.

    :param data (dict): Datensatz als Dictionary
    :param coref (dict): Dictionary mit Koreferenzmengen aus Datensatz
    :param feat_dict (dict): Dictionary mit Trainingsdaten (siehe 'get_features_traindata()')
    :param ante_scope_in (int): Skopus der Antezedens-Kandidaten fuer TN
    :param form_in (bool): Feature einbeziehen. Default=True
    :param sent_dist_in (bool): Feature einbeziehen. Default=True
    :param tok_dist_in (bool): Feature einbeziehen. Default=True
    :param anaph_pron_in (bool): Feature einbeziehen. Default=True
    :param len_ante_in (bool): Feature einbeziehen. Default=True
    :param lexical_overlap_in (bool): Feature einbeziehen. Default=True
    :param part_of_shell_noun_in (bool): Feature einbeziehen. Default=True
    :param ante_inf_verb_in (bool): Feature einbeziehen. Default=True
    :return: feat_dict (dict): Dictionary mit IDs und Features zu Trainingspaaren (siehe 'get_features_traindata()')
    """

    # lokale Variable fuer ante_scope
    # dient zur Vermeidung von Ueberschreibungen
    tn_ante_scope = ante_scope_in
    # IDs fuer Ante-Anaph-Paare an passender Stelle fortsetzen
    ent_id = max(feat_dict.keys())

    # relevante Formen fuer Anaphern
    relevant_forms = ["it", "this", "that"]
    # Liste IDs von TP-Instanzen + doc_id
    true_dd_ent = get_true_dd_elements(coref)
    # Liste IDs von TP-Anaphern + doc_id
    true_dd_anaph = [(tup[1], tup[2]) for tup in true_dd_ent]

    # ueber Token iterieren
    for doc in data:
        for sent in data[doc]:
            for tok_id in data[doc][sent]:

                # Token = "it/this/that"
                if data[doc][sent][tok_id][0].strip().lower() in relevant_forms:

                    # durch Skopus fuer Antezedens-Kandidaten rotieren
                    # Bsp.:
                    # TN1 -> Ante-Kandidat = 3 Saetze vor Anaph
                    # TN2 -> Ante-Kandidat = 2 Saetze vor Anaph, etc.
                    tn_ante_scope -= 1
                    if tn_ante_scope < 0:
                        tn_ante_scope = ante_scope_in

                    # Anaph-Satz hat weniger als tn_ante_scope vorangehende Saetze
                    # -> ueberspringen
                    if sent <= tn_ante_scope:
                        continue

                    # wenn aktueller "it/this/that"-Token ist TP-Instanz
                    # zugehoerigen AntezedensSatz extrahieren
                    # -> fuer Gegentest, um TP-Instanz nicht als TN zu verwenden
                    if tuple([tok_id, doc]) in true_dd_anaph:
                        # SatzID dazugehoeriger Antezedens
                        ante_sent_id = true_dd_ent[true_dd_anaph.index(tuple([tok_id, doc]))][0]
                    # aktueller "it/this/that"-Token ist TN-Instanz
                    else:
                        ante_sent_id = None
                    ante_sent_id_tn = sent - tn_ante_scope

                    # wenn aktuelles Paar 'Token + AnteSatz' = TP
                    # -> ueberspringen
                    if ante_sent_id_tn == ante_sent_id:
                        continue

                    # IDs fuer TN eintragen
                    ent_id += 1
                    feat_dict[ent_id] = {"identifier": {}, "features": {}}
                    feat_dict[ent_id]["identifier"]["anaph_sent_id"] = sent
                    feat_dict[ent_id]["identifier"]["ante_sent_id"] = ante_sent_id_tn
                    feat_dict[ent_id]["identifier"]["anaph_tok_id"] = tok_id
                    feat_dict[ent_id]["identifier"]["ante_tok_id"] = min(data[doc][sent - tn_ante_scope].keys())
                    feat_dict[ent_id]["identifier"]["doc"] = doc

                    # Eintrag, ob TN-Instanz mit
                    # TN-Anaph oder TP-Anaph
                    if ante_sent_id:
                        feat_dict[ent_id]["identifier"]["tp_anaph"] = 1
                    else:
                        feat_dict[ent_id]["identifier"]["tp_anaph"] = 0

                    # Featurewerte eintragen
                    feat_dict[ent_id]["features"]["is_instance"] = 0
                    if form_in:
                        feat_dict[ent_id]["features"]["form"] = data[doc][sent][tok_id][0].strip().lower()
                    if sent_dist_in:
                        feat_dict[ent_id]["features"]["sent_dist"] = sent - (ante_sent_id_tn)
                    if tok_dist_in:
                        feat_dict[ent_id]["features"]["tok_dist"] = tok_id - max(data[doc][ante_sent_id_tn].keys())

                    if anaph_pron_in:
                        if data[doc][sent][tok_id][2] == "PRON":
                            feat_dict[ent_id]["features"]["anaph_pron"] = 1
                        else:
                            feat_dict[ent_id]["features"]["anaph_pron"] = 0

                    if len_ante_in:
                        if ante_sent_id:
                            feat_dict[ent_id]["features"]["len_ante"] = len(data[doc][ante_sent_id].keys())
                        else:
                            feat_dict[ent_id]["features"]["len_ante"] = len(data[doc][ante_sent_id_tn].keys())

                    if lexical_overlap_in:
                        feat_dict[ent_id]["features"]["lexical_overlap"] = get_lexical_overlap(data, doc, ante_sent_id_tn, sent)
                    if part_of_shell_noun_in:
                        #shell_nouns = read_shell_nouns("data_annotated/other/appendix_habil_schmid.csv")
                        global shell_nouns
                        feat_dict[ent_id]["features"]["part_of_shell_noun"] = get_shell_noun_part(shell_nouns, data, doc, sent, tok_id)

                    if ante_inf_verb_in:
                        feat_dict[ent_id]["features"]["ante_inf_verb"] = get_has_inf_verb(data, doc, ante_sent_id_tn)

    return feat_dict


def get_lexical_overlap(data: dict, doc: str, ante_sent_id: int, anaph_sent_id: int) -> int:
    """
    Anteil der lexikalischen Ueberlappung eines Satzes mit anaphorischen Ausdruck
    mit einem Antezedenssatz.
    Lexikalische Uberlappung =
        Frequenz der AnaphLemma in Antesatz /
        ((Anzahl Token AnteSatz + Anzahl Token AnaphSatz) / 2)

    :param data (dict): Datensatz als Dictionary
    :param doc (str): ID aktuelles Dokument (Key in 'data')
    :param ante_sent_id (int): ID des Antezedenssatzes in 'data'
    :param anaph_sent_id (int): ID des Anaphersatzes in 'data'
    :return lexical_overlap (float): Anteil der lexikalischen Ueberlappung
    """

    # Liste von Token in
    # Antezedenssatz und Anaphersatz
    ante_token = [data[doc][ante_sent_id][tok][1].lower() for tok in data[doc][ante_sent_id]]
    anaph_token = [data[doc][anaph_sent_id][tok][1].lower() for tok in data[doc][anaph_sent_id]]

    # Zaehler fuer
    # Frequenz der Lemma des Anaphersatzes in AnteSatz
    same_lemmas = 0

    # ueber Token in Anaphersatz iterieren
    for tok in anaph_token:
        # wenn Token in AnteSatz vorkommt
        # Zaehler hochsetzen
        if tok in ante_token:
            same_lemmas += 1

    # lexikalische Uberlappung berechnen
    lexical_overlap = same_lemmas / ((len(ante_token) + len(anaph_token)) / 2)

    return lexical_overlap


def read_shell_nouns(filename: str) -> list:
    """
    Hilfsfunktion. Liste mit Shell Nouns einlesen.

    :param filename (str): Pfad der einzulesenden Datei ('data_annotated/other/appendix_habil_schmid.csv')
    :return shell_nouns (list): Liste mit Shell Nouns
    """

    # systemuebergreifender Dateipfad
    filename = Path(filename)
    # Liste fuer Shell Nouns
    shell_nouns = list()

    # Datei zeilenweise einlesen
    with open(filename, mode="r", encoding="UTF-8") as infile:
        lines = infile.readlines()

    # Zeile 1 und 2 entfernen
    lines.pop(0)
    lines.pop(0)

    # Shell Nouns an Liste anhaengen
    for index, line in enumerate(lines):
        shell_nouns.append(line.strip().split(";")[0])

    return shell_nouns


def get_shell_noun_part(shell_nouns: list, data: dict, doc: str, anaph_sent_id: int, anaph_tok_id: int) -> int:
    """
    Fuer einen anaphorischen Ausdruck (bzw. Kandidaten) feststellen,
    ob dieser Teil einer Shell Noun-Konstruktion ist (z.B. 'this fact').

    :param shell_nouns (list): Liste mit Shell Nouns
    :param data (dict): Datensatz als Dictionary
    :param doc (str): ID aktuelles Dokuement (Key fuer 'data')
    :param anaph_sent_id (int): ID des Anaphersatzes
    :param anaph_tok_id (int): ID des anaphorischen Ausdrucks
    :return is_sn_part (int): Teil einer Shell Noun-Konstruktion ja/nein (0/1)
    """

    # Rueckgabe-Parameter
    is_sn_part = 0

    # wenn in Anaphersatz noch ein
    # Token hinter dem anaphorischen Ausdruck
    # vorhanden ist
    if anaph_tok_id < max(data[doc][anaph_sent_id].keys()):
        # Lemma des Tokens nach anaphorischem Ausdruck
        following_tok = data[doc][anaph_sent_id][anaph_tok_id+1][1].lower().strip()

        # wenn Token nach anaphorischem Ausdruck ein Shell Noun
        if following_tok in shell_nouns:
            is_sn_part = 1

    return is_sn_part


def vectorize_features(feat_dict: dict) -> tuple:
    """
    Mit DictVectorizer von Sklearn Features fuer Klassifizierung vektorisieren.
    Vektoren koennen als Input fuer Klassifizierer genutzt werden.
    Enthaelt OneHot-Encoding fuer kategorische Features.
    Details: https://scikit-learn.org/dev/modules/feature_extraction.html#dict-feature-extraction

    :param feat_dict (dict): Dictionary mit Features pro Kandidat (Struktur siehe 'get_features_testdata')
    :return feat_dict, feat_index_map (tuple):
        - feat_dict (dict): Feature-Dictionary mit zusaetzlichem Key "vector" pro Kandidat (Struktur siehe 'get_features_testdata')
            - z.B. {KandidatID: {"features": ..., "identifier": ..., "vector": [0. 1. 0. ...] }}
        - feat_index_map (dict): Mapping von Features auf Index in Vektor
    """

    # DictVectorizer instanziieren
    # Features alphabetisch sortiert
    vectorizer = DictVectorizer(sort=True)

    # Liste fuer Feature-Eintraege
    vec_input = list()
    # Liste befuellen
    # -> [ {"form": val, "sent_dist":val, ...}, {"form":val, ...}, ...]
    for ent_id in feat_dict:
        vec_input.append(feat_dict[ent_id]["features"])

    # Features vektorisieren
    vectorized = vectorizer.fit_transform(vec_input).toarray()
    # Mapping extrahieren
    feat_index_map = vectorizer.vocabulary_

    # (ent_id - 1) = Index zugehoeriger FeatVektor in Liste mit Vektoren
    for ent_id in feat_dict:
        feat_dict[ent_id]["vector"] = vectorized[ent_id-1]

    return feat_dict, feat_index_map


def get_training_vector(features: dict, feat_index_map: dict) -> tuple:
    """
    Aus Trainingspaaren (Ante, Anaph) die Trainingsdaten/Vektoren mit
    Feature-Vektoren und abhaengigen Variablen fuer Klassifizierer erstellen.
    Abhaengige Variable = Instanz von DD ja/nein

    :param feaetures (dict): Dictionary mit Features zu Trainingsdaten.
    :param feat_index_map (dict): Mapping von Features auf Index in Vektoren in 'features'.
    :return: feature_vec, dependent_var (tuple): FeatureVektoren und dazugehoerige abhaengige Variable, Index parallel
        - feature_vec (list): Liste mit Vektoren von FeatureWerten
        - dependent_var (list): Liste mit Werten der abhaengigen Variable
    """

    # Listen fuer Vektoren initiieren
    feature_vec = list()
    dependent_var = list()

    # Index abhaengiger Variable in 'features[dd_id]["vector"]'
    index_depVar = feat_index_map["is_instance"]

    # ueber Trainingspaare iterieren
    for ent_id in features:
        # Wert abhaengiger Variable eintragen
        dependent_var.append(features[ent_id]["vector"][index_depVar])

        # Vektor FeatureWerte eintragen
        feature_vec_temp = list()
        feature_vec_temp.extend(features[ent_id]["vector"][0:index_depVar])
        feature_vec_temp.extend(features[ent_id]["vector"][index_depVar+1:])
        feature_vec.append(feature_vec_temp)

    return feature_vec, dependent_var


def get_class_weight(dependent_var: list) -> dict:
    """
    Balance der Klassen in Trainingsdaten berechnen.
    Dient als Hyperparameter dem Finetuning bei Training eines Klassifizierers mit unbalancierten Trainingsdaten.
    Klassen = {0, 1} = {nicht-DD-Instanz, DD-Instanz}

    :param dependent_var (list): Liste mit Werten fuer Klassen zu Trainingspaaren
    :return class_weight (dict): Dictionary mit Gewichtung der Klassen, {0: gewicht, 1: gewicht}
    """

    # Anzahl TP und TN zaehlen
    counter_tp = dependent_var.count(1)
    counter_tn = dependent_var.count(0)
    # Anteil von TP/TN an Gesamtmenge ermitteln
    weight_tn = len(dependent_var) / (2 * counter_tn)
    weight_tp = len(dependent_var) / (2 * counter_tp)
    class_weight = {0: weight_tn, 1: weight_tp}

    #weight_tn = counter_tn / (counter_tp + counter_tn)
    #weight_tp = counter_tp / (counter_tp + counter_tn)
    #weight_tn = counter_tn / (counter_tp + counter_tn) * 3/4
    #weight_tp = 1 - weight_tn

    # Anteile invers eintragen
    #class_weight = {0:weight_tp, 1:weight_tn}

    return class_weight




###############################
### KLASSIFIZIERER TRAINING ###
###############################


def fit_model_lr(*data: tuple, class_weight_in: dict=None):
    """
    Modell fuer LogisticRegression trainieren.

    :param data (tuple): Trainingsdaten, Output von "get_feature_vec_training"
        - (feature_vec, dependent_var)
        - feature_vec = Liste mit Feature-Vektoren
        - dependent_var = Liste mit Werten der abhaengigen Variable (0,1)
        - Werte fuer eine Einheit an gleicher Indexposition
    :param class_weight (dict): Dictionary mit Gewichtung fuer Klassen, Default=None
    :param warm_start (bool): vorhandenes Modell weitertrainieren ja/nein, Default=False
    :return lr_classifier (sklearn.LogisticRegression): LogisticRegression-Klassifizierer, trainiertes Modell
    """

    # Listen mit Trainingsdaten
    # Input fuer Modell
    x_train = list()
    y_train = list()

    # Listen mit TrainingsWerten befuellen
    for element in data:
        x_train += element[0]
        y_train += element[1]

    # Klassifizierer instanziieren und trainieren
    lr_classifier = LogisticRegression(class_weight=class_weight_in, max_iter=1000)
    lr_classifier.fit(x_train, y_train)

    return lr_classifier




################################
### KLASSIFIZIERER ANWENDUNG ###
################################


def classify_all(classifier, feat_dict: dict) -> dict:
    """
    Testdaten klassifizieren.

    :param classifier (sklearn.LogisticRegressionModel): trainierter Klassifizierer
    :param feat_dict (dict): Dictionary mit FeatureWerten und IDs fuer Testdaten
    :return feat_dict (dict): Dictionary mit eingetragenen Ergebnissen
            - Ergebnisse unter feat_dict[ent_id]["features"]["is_instance"]
    """

    # ueber Testdaten iterieren
    # jedes Testdatum klassifizieren
    # Ergebnis in Dictionary eintragen
    for ent_id in feat_dict:
        pred = classifier.predict(feat_dict[ent_id]["vector"].reshape(1, -1))
        feat_dict[ent_id]["features"]["is_instance"] = pred[0]

        # gibt Wahrscheinlichkeiten aus
        #print(classifier.predict_proba(feat_dict[ent_id]["vector"].reshape(1, -1)))

    return feat_dict


def write_pred_file(filename: str, feat_dict_pred: dict, data: dict) -> None:
    """
    Datei mit Ergebnissen zu Testdaten schreiben.
    Formatierung nach Vorgabe der SharedTask.
    Schreibt in Unterverzeichnis 'solution'.

    :param filename (str): Name/Pfad der zu schreibenden Datei, Ausgangspunkt Unterverzeichnis 'solution'
                - z.B. filename = 'AMI/AMI_classified.txt'
    :param feat_dict_pred (dict): Featuredictionary mit klassifizierten Testdaten
    :param data (dict): Testdatensatz als Dictionary
    :return None: Schreiben einer externen Datei
    """

    # Dictionary kopieren
    # vermeidet inplace-Veraenderung
    import copy
    data_copy = data.copy()

    # DD-Elemente aus Ergebnissen in Datensatz eintragen
    # IDs anlegen
    counter_dd_id = 0
    counter_markable_id = 0
    doc_id = str()

    # vorige DD-Eintraege entfernen (Gold)
    for doc in data_copy:
        for sent in data_copy[doc]:
            for tok in data_copy[doc][sent]:
                if type(data_copy[doc][sent][tok][11]) == dict:
                    data_copy[doc][sent][tok][11] = "_"

    # ueber Testdaten iterieren
    for ent_id in feat_dict_pred:
        # wenn Ergebnis = DD-Instanz
        # Eintrag in Datensatz
        # -> eigene Loesung
        if feat_dict_pred[ent_id]["features"]["is_instance"] == 1:

            # ID-Zaehler fuer jedes Dokument innerhalb einer Datei zuruecksetzen
            if doc_id != feat_dict_pred[ent_id]["identifier"]["doc"]:
                counter_dd_id = 0
                counter_markable_id = 0

            # zwischenspeichern fuer leichteren lookup
            doc_id = feat_dict_pred[ent_id]["identifier"]["doc"]
            ante_sent_id = feat_dict_pred[ent_id]["identifier"]["ante_sent_id"]
            ante_tok_id_start = feat_dict_pred[ent_id]["identifier"]["ante_tok_id"]
            ante_tok_id_end = max([tok_id for tok_id in data[doc_id][ante_sent_id]])
            anaph_tok_id = feat_dict_pred[ent_id]["identifier"]["anaph_tok_id"]
            anaph_sent_id = feat_dict_pred[ent_id]["identifier"]["anaph_sent_id"]

            # Strings erstellen
            # Anapher Beispiel: "(EntityID=41-DD|MarkableID=dd_markable_82|Min=2886,2886|SemType=do)"
            # Antezedens Beispiel:
            #   - erster Tok aus Satz: "(EntityID=41-DD|MarkableID=dd_markable_81|Min=2877,2885|SemType=dn"
            #   - letzer Tok aus Satz: ")"
            counter_dd_id += 1
            counter_markable_id += 1
            ante_string_start = f"(EntityID={counter_dd_id}-DD|MarkableID=dd_markable_{counter_markable_id}|Min={ante_tok_id_start},{ante_tok_id_end}|SemType=dn"
            ante_string_end = ")"
            counter_markable_id += 1
            anaph_string = f"(EntityID={counter_dd_id}-DD|MarkableID=dd_markable_{counter_markable_id}|Min={anaph_tok_id},{anaph_tok_id}|SemType=do)"

            # Anaphern die mit weiteren Anaphern koreferent sind integrieren
            if data[doc_id][anaph_sent_id][anaph_tok_id][11] != "_" and data[doc_id][anaph_sent_id][anaph_tok_id][11] != ")":
                id_entry = data[doc_id][anaph_sent_id][anaph_tok_id][11].split("|")[0]
                prev_id = id_entry[id_entry.index("=")+1:]
                anaph_string = f"(EntityID={prev_id},{counter_dd_id}-DD|MarkableID=dd_markable_{counter_markable_id}|Min={anaph_tok_id},{anaph_tok_id}|SemType=do)"

            # Strings nach SharedTask-Format
            # in Dictionary zu Datensatz eintragen
            data_copy[doc_id][ante_sent_id][ante_tok_id_start][11] = ante_string_start
            data_copy[doc_id][ante_sent_id][ante_tok_id_end][11] = ante_string_end
            data_copy[doc_id][anaph_sent_id][anaph_tok_id][11] = anaph_string

    # Pfad systemuebergreifend
    path_to_write = Path(Path.cwd(), "solution", filename)
    # Datei schreiben nach Format der SharedTask
    with open(path_to_write, mode="w", encoding="UTF-8") as outfile:
        for doc in data_copy:
            outfile.write("#\t" + doc + "\n")
            for sent in data_copy[doc]:
                outfile.write("#\t" + str(sent) + "\n")
                for tok in data_copy[doc][sent]:
                    outfile.write(str(tok) + "\t")
                    for element in data_copy[doc][sent][tok]:
                        outfile.write(str(element) + "\t")
                    outfile.write("\n")
                outfile.write("\n\n")

    return None


def write_pred_file_overview(filename: str, feat_dict: dict, data: dict) -> None:
    """
    Uebersicht zu klassifizierten Testdaten in Datei schreiben.
    Uebersicht enthaelt (Antezedens, Anapher)-Paare die als
    DD-Instanzen klassifiziert wurden.
    Datei wird in Unterverzeichnis 'solution_overview' geschrieben.

    :param filename (str): Name/Pfad der zu schreibenden Datei
                - z.B. filename = 'AMI_classified.txt'
    :param feat_dict (dict): Featuredictionary mit klassifizierten Testdaten
    :param data (dict): kompletter Testdatensatz als Dictionary
    :return None: Schreiben einer externen Datei
    """

    # zaehler fuer DD-Instanzen
    counter = 0

    # Pfad systemuebergreifend
    path_to_write = Path(Path.cwd(), "solution_overview", filename)
    # Datei anlegen
    with open(path_to_write, mode="w", encoding="UTF-8") as outfile:
        # Ueberschrift mit Spalteninfos
        outfile.write("# COLUMNS: FORM\tLEMMA\tUPOS\tXPOS\tFEATS\tHEAD\n\n")

        # ueber Testdaten iterieren
        for ent_id in feat_dict:
            # Ergebnis = DD-Instanz
            if feat_dict[ent_id]["features"]["is_instance"] == 1:

                # IDs fuer lookup
                counter += 1
                doc_id = feat_dict[ent_id]["identifier"]["doc"]
                ante_sent_id = feat_dict[ent_id]["identifier"]["ante_sent_id"]
                anaph_sent_id = feat_dict[ent_id]["identifier"]["anaph_sent_id"]

                # Unterueberschriften zu DD-Instanzen
                outfile.write(f"# KOREFERENZPAAR {counter}:\n")
                outfile.write("\t# ANTEZEDENS:\n")
                # Token in Antezedens-Satz mit Annotationen zeilenweise schreiben
                for tok in data[doc_id][ante_sent_id]:
                    out_string = "\t".join(data[doc_id][ante_sent_id][tok][0:6])
                    outfile.write("\t" + out_string + "\n")
                outfile.write("\n")

                # Satz der Anapher-Token enthaelt zeilenweise schreiben
                outfile.write("\t# ANAPHER:\n")
                for tok in data[doc_id][anaph_sent_id]:
                    out_string = "\t".join(data[doc_id][anaph_sent_id][tok][0:6])
                    outfile.write("\t" + out_string + "\n")
                outfile.write("\n\n")

    return None


def write_pred_console(feat_dict: dict, data: dict) -> None:
    """
    Die als TP klassifizierten Testdaten auf der Konsole ausgeben.

    :param feat_dict (dict): Featuredictionary mit klassifizierten Testdaten
    :param data (dict): kompletter Testdatensatz als Dictionary
    :return None: Konsolenausgbae der als TP klassifizierten Kandidaten
    """

    # ueber DD-Kandidaten iterieren
    for ent_id in feat_dict:
        # Kandidat laut Modell = TP
        if feat_dict[ent_id]["features"]["is_instance"] == 1:

            # IDs fuer lookup
            doc_id = feat_dict[ent_id]["identifier"]["doc"]
            ante_sent_id = feat_dict[ent_id]["identifier"]["ante_sent_id"]
            anaph_sent_id = feat_dict[ent_id]["identifier"]["anaph_sent_id"]
            anaph_tok_id = feat_dict[ent_id]["identifier"]["anaph_tok_id"]

            # zwischenspeichern fuer leserlichen code
            ante_sent = [data[doc_id][ante_sent_id][tok][0] for tok in data[doc_id][ante_sent_id]]
            anaph_sent = [data[doc_id][anaph_sent_id][tok][0] if tok != anaph_tok_id else '*'+data[doc_id][anaph_sent_id][tok][0]+'*' for tok in data[doc_id][anaph_sent_id]]

            print(f"ID\t{ent_id}")
            print(f"ANTE\t{' '.join(ante_sent)}")
            print(f"ANAPH\t{' '.join(anaph_sent)}")
            print()

    return None




def write_model_file(filename: str, classifier) -> None:
    """
    Trainierten Klassifizierer in Datei schreiben.
    Weitere Datei mit Metadaten zu Klassifizierer schreiben, Name=filename+"_metadata.txt".
    Dateien werden in Unterverzeichnis 'models' geschrieben.

    :param filename (str): Name der Datei, erhaelt Endung '.pkl'
            - z.B. filename='example_model'
    :param classifier: trainierter Klassifizierer
    :return None: externe Datei wird geschrieben
    """

    # Warnhinweis mit User-Abfrage
    print("----------------------------------")
    print("ACHTUNG:")
    print("Bei Ausfuehrung dieser Funktion wird der Befehl 'pickle.dump()' ausgefuehrt, wodurch ein serialisiertes Objekt exportiert wird. Dadurch kann Python-Code, welcher in diesem Objekt enthalten ist, ausgefuehrt werden. Die Funktion sollte nur auf vertrauenswuerdige Objekte angewendet werden.")
    print()
    print("Moechten Sie die Funktion weiterhin ausfuehren, geben Sie eine '1' ein.")
    print("Moechten Sie die Funktion nicht ausfuehren, geben Sie ein beliebiges anderes Zeichen ein.")
    user_in = input()

    # Pfad systemuebergreifend
    path_to_write = Path(Path.cwd(), "models", filename+".pkl")
    path_to_write_metadata = Path(Path.cwd(), "models", filename+"_metadata.txt")

    # User Bestaetigung der Ausfuehrung
    # -> Datei wird geschrieben
    if user_in == "1":
        print("Die Funktion wird ausgefuehrt.")
        print()
        # modus 'wb' fuer binaryFile fuer pickle
        with open(path_to_write, "wb") as outfile:
            pickle.dump(classifier, outfile)

        # Datei mit Metadaten schreiben
        with open(path_to_write_metadata, mode="w", encoding="UTF-8") as outfile:
            outfile.write(f"# METADATEN ZU MODELL {filename}\n\n")

            # verwendete Trainingsdaten
            outfile.write("# VERWENDETE TRAININGSDATEN\n")
            for file in classifier.train_data_used:
                outfile.write(f"{file}\n")
            outfile.write("\n")

            # Klassen, Iterations, Intercept etc.
            outfile.write("# DATEN ZU TRAININGSVORGANG\n")
            outfile.write(f"classes\t{classifier.classes_}\n")
            outfile.write(f"class_weights\t{classifier.get_params()['class_weight']}\n")
            outfile.write(f"intercept/bias term\t{classifier.intercept_[0]}\n")
            outfile.write(f"n_iterations\t{classifier.n_iter_[0]}\n")
            outfile.write(f"n_features\t{classifier.n_features_in_}\n")
            outfile.write("\n")

            # verwendete Features schreiben
            outfile.write("# VERWENDETE FEATURES UND IHRE GEWICHTUNG\n")
            feat_index_map = classifier.feat_index_map
            index_dep_var = feat_index_map["is_instance"]
            for feat in feat_index_map:
                # abhaengige Variable ueberspringen
                if feat == "is_instance":
                    continue
                # Gewichtung des Features eintragen
                if feat_index_map[feat] > index_dep_var:
                    outfile.write(f"{feat}\t{classifier.coef_[0][feat_index_map[feat]-1]}\n")
                else:
                    outfile.write(f"{feat}\t{classifier.coef_[0][feat_index_map[feat]]}\n")

    else:
        print("Die Funktion wird nicht ausgefuehrt.")
        print()

    return None



def load_model_file(filename: str):
    """
    Datei mit trainiertem Klassifizierer importieren.

    :param filename: _kompletter_ Pfad der einzulesenden Datei
    :return classifier (sklearn.LogisticRegressionClassifier): trainierter Klassifizierer
    """

    # Warnhinweis mit User-Abfrage
    print("----------------------------------")
    print("ACHTUNG:")
    print("Bei Ausfuehrung dieser Funktion wird der Befehl 'pickle.load()' ausgefuehrt, wodurch ein serialisiertes Objekt geladen wird. Dadurch kann Python-Code, welcher in diesem Objekt enthalten ist, ausgefuehrt werden. Die Funktion sollte nur auf vertrauenswuerdige Dateien angewendet werden.")
    print()
    print("Moechten Sie die Funktion weiterhin ausfuehren, geben Sie eine '1' ein.")
    print("Moechten Sie die Funktion nicht ausfuehren, geben Sie ein beliebiges anderes Zeichen ein.")
    user_in = input()

    # Pfad systemuebegreifend
    filename = Path(Path.cwd(), "models", filename)

    # User-Bestaetigung
    # Datei importieren
    if user_in == "1":
        print("Die Funktion wird ausgefuehrt.")
        print()
        # modus 'rb' fuer binaryFile fuer pickle
        with open(filename, "rb") as infile:
            classifier = pickle.load(infile)
        return classifier

    else:
        print("Die Funktion wird nicht ausgefuehrt.")
        print()
        return None



################################
### EVALUATION UND STATISTIK ###
################################


def prec_recall_f1(feat_dict_pred: dict, coref: dict) -> dict:
    """
    Evaluationsmaße fuer klassifizierte Testdaten berechnen.
    Ausgabe der Ergebnisse auf Konsole.

    :param feat_dict_pred (dict): Dictionary mit klassifizierten Testdaten
    :param coref (dict): Dictionary mit Koreferenzmengen in Golddaten
    :return eval_dict (dict): Dictionary mit Evaluationsdaten + Konsolenausgabe
        - Keys: "count_tp", "count_fp", "count_tn", "count_fn",
                "total", "recall", "pecision", "accuracy", "accuracy_for_tp", "f_one"
    """

    # Zaehler fuer True Positives etc.
    count_tp = 0
    count_fp = 0
    count_tn = 0
    count_fn = 0

    # Liste mit Gold-Paaren aus (ante_sent_id, anaph_tok_id)
    true_dd_ent = get_true_dd_elements(coref)

    # ueber (Ante, Anaph)-Paare in Testdaten iterieren
    for ent_id in feat_dict_pred:
        # Ergebnis der Klassifizierung
        y_pred = feat_dict_pred[ent_id]["features"]["is_instance"]
        # IDs Antezedens-Satz, Anapher-Token
        ante_sent_id = feat_dict_pred[ent_id]["identifier"]["ante_sent_id"]
        anaph_tok_id = feat_dict_pred[ent_id]["identifier"]["anaph_tok_id"]
        doc = feat_dict_pred[ent_id]["identifier"]["doc"]

        # Ergebnis = is_instance
        if y_pred == 1:

            # Abgleich mit Golddaten
            if tuple([ante_sent_id, anaph_tok_id, doc]) in true_dd_ent:
                count_tp += 1
            else:
                count_fp += 1

        # Ergebnis = nicht-is_instance
        else:
            # Abgleich mit Golddaten
            if tuple([ante_sent_id, anaph_tok_id, doc]) in true_dd_ent:
                count_fn += 1
            else:
                count_tn += 1

    # Gesamtmenge an Testinstanzen
    count_total = count_tp + count_fp + count_fn + count_tn

    # Evaluationsdaten berechnen
    # tryExcept um Division durch Null zu vermeiden
    try:
        recall = count_tp / (count_tp + count_fn)
    except:
        recall = 0

    try:
        precision = count_tp / (count_tp + count_fp)
    except:
        precision = 0

    accuracy = (count_tp + count_tn) / (count_total)
    accuracy_for_tp = count_tp / len(true_dd_ent)

    try:
        f_one = count_tp / (count_tp + (0.5*(count_fp + count_fn)))
    except:
        f_one = 0


    # Dictionary anlegen
    eval_dict = {"tp": count_tp,
                 "fp": count_fp,
                 "tn": count_tn,
                 "fn": count_fn,
                 "total": count_total,
                 "recall": recall,
                 "precision": precision,
                 "accuracy": accuracy,
                 "accuracy_for_tp": accuracy_for_tp,
                 "f_one": f_one}

    print("----- EVALUATION OVERALL-------------")
    print("STAT\tVALUE")
    for key in eval_dict:
        print(key, round(eval_dict[key], 2), sep="\t")
    print()
    print("------------------------------------")

    return eval_dict


def eval_with_forms(feat_dict_pred: dict, coref: dict) -> dict:
    """
    Evaluationsmaße fuer klassifizierte Testdaten abhaengig von Anapher-Form berechnen.
    Ausgabe der Ergebnisse auf Konsole.

    :param feat_dict_pred (dict): Dictionary mit klassifizierten Testdaten
    :param coref (dict): Dictionary mit Koreferenzmengen in Golddaten
    :return eval_dict (dict): Dictionary mit Evaluationsdaten + Konsolenausgabe
            - Keys: "it", "this", "that"
            - Subkeys: "tp", "tn", "fp", "fn", "total", "recall", "pecision", "accuracy", "f_one"
        """

    # Dictionary anlegen
    eval_dict = {"it": {"tp":0, "tn":0, "fp":0, "fn":0},
                 "that": {"tp":0, "tn":0, "fp":0, "fn":0},
                 "this": {"tp":0, "tn":0, "fp":0, "fn":0} }

    # Liste Gold-Paare aus (ante_sent_id, anaph_tok_id)
    true_dd_ent = get_true_dd_elements(coref)

    # ueber (Ante, Anaph)-Paare in Testdaten iterieren
    for ent_id in feat_dict_pred:

        # Ergebnis der Klassifizierung
        y_pred = feat_dict_pred[ent_id]["features"]["is_instance"]
        # IDs und Anapher-Form
        ante_sent_id = feat_dict_pred[ent_id]["identifier"]["ante_sent_id"]
        anaph_tok_id = feat_dict_pred[ent_id]["identifier"]["anaph_tok_id"]
        anaph_form = feat_dict_pred[ent_id]["features"]["form"]
        doc = feat_dict_pred[ent_id]["identifier"]["doc"]

        # Ergebnis = DD-Instanz
        if y_pred == 1:
            # Abgleich mit Golddaten
            if tuple([ante_sent_id, anaph_tok_id, doc]) in true_dd_ent:
                eval_dict[anaph_form]["tp"] = eval_dict[anaph_form].get("tp", 0) + 1
            else:
                eval_dict[anaph_form]["fp"] = eval_dict[anaph_form].get("fp", 0) + 1
        # Ergebnis = keine DD-Instanz
        else:
            # Abgleich mit Golddaten
            if tuple([ante_sent_id, anaph_tok_id, doc]) in true_dd_ent:
                eval_dict[anaph_form]["fn"] = eval_dict[anaph_form].get("fn", 0) + 1
            else:
                eval_dict[anaph_form]["tn"] = eval_dict[anaph_form].get("tn", 0) + 1

    # Evaluationsmaße berechnen
    for form in eval_dict:
        eval_dict[form]["total"] = sum([eval_dict[form][key] for key in eval_dict[form]])

        # TryExcept um Division durch Null zu vermeiden
        try:
            eval_dict[form]["recall"] = eval_dict[form]["tp"] / (eval_dict[form]["tp"] + eval_dict[form]["fn"])
        except:
            eval_dict[form]["recall"] = 0

        try:
            eval_dict[form]["precision"] = eval_dict[form]["tp"] / (eval_dict[form]["tp"] + eval_dict[form]["fp"])
        except:
            eval_dict[form]["precision"] = 0

        try:
            eval_dict[form]["accuracy"] = (eval_dict[form]["tp"] + eval_dict[form]["tn"]) / eval_dict[form]["total"]
        except:
            eval_dict[form]["aacuracy"] = 0

        try:
            eval_dict[form]["f_one"] = eval_dict[form]["tp"] / (eval_dict[form]["tp"] + (0.5 * (eval_dict[form]["fp"] + eval_dict[form]["fn"])))
        except:
            eval_dict[form]["f_one"] = 0

        try:
            eval_dict[form]["acc_for_tp"] = eval_dict[form]["tp"] / (eval_dict[form]["tp"] + eval_dict[form]["fn"])
        except:
            eval_dict[form]["acc_for_tp"] = 0


    # Konsolenausgabe
    print()
    print("----- EVALUATION FOR FORMS----------")
    print("FORM\tSTAT\tVALUE")
    for form in eval_dict:
        for key in eval_dict[form]:
            print(form, key, eval_dict[form][key], sep="\t")
    print()
    print("------------------------------------")

    return eval_dict


def get_stats_from_data(data: dict) ->dict:
    """
    Deskriptive Statistiken zu Datensaetzen ermitteln.
    Fuer annotierte Golddaten gedacht.
    Mit Konsolenausgabe.

    :param data (dict): Datensatz als Dictionary
    :return stats_dict (dict): Dictionary mit statistischen Kennzahlen
            - Keys: "count_dd_ent_total", "count_dd_ent_relevant", "count_sent", "count_tok",
                    "count_it", "count_it_dd", "count_this", "count_this_dd", "count_that", "count_that_dd",
                    "avg_sent_dist", "avg_tok_dist", "avg_sent_dist_it/this/that", "avg_tok_dist_it/this/that",
                    "it/this/that_prob", "it_to_that", "this_to_that", "that_to_that"
    """

    # Liste fuer Abgleich
    relevant_forms = ["it", "this", "that"]

    stats_dict = {"overall": {},
                  "it": {},
                  "this": {},
                  "that": {} }

    # alle DD-Instanzen zaehlen
    coref_dict = extract_dd_elements(data)
    for doc in coref_dict:
        for ent in coref_dict[doc]:
            stats_dict["overall"]["dd_ent_total"] = stats_dict["overall"].get("dd_ent_total", 0) + 1


    # alle relevanten DD-Instanzen zaehlen (= Anapher "it", "this" oder "that")
    coref_dict = cleanup_coref_dict(data, coref_dict)
    for doc in coref_dict:
        for ent in coref_dict[doc]:
            stats_dict["overall"]["dd_ent_relevant"] = stats_dict["overall"].get("dd_ent_relevant", 0) + 1

    # Anzahl Saetze und Token zaehlen
    for doc in data:
        for sent in data[doc]:
            stats_dict["overall"]["count_sents"] = stats_dict["overall"].get("count_sents", 0) + 1
            for tok in data[doc][sent]:
                stats_dict["overall"]["count_toks"] = stats_dict["overall"].get("count_toks", 0) + 1

                # GEsamt-Anzahl "it"/"this"/"that" zaehlen
                curr_form = data[doc][sent][tok][0].strip().lower()
                if curr_form in relevant_forms:
                    stats_dict[curr_form]["freq_total"] = stats_dict[curr_form].get("freq_total", 0) + 1
                    #if type(data[doc][sent][tok][11]) == dict:
                        #stats_dict[curr_form]["freq_dd"] = stats_dict[curr_form].get("freq_dd", 0) + 1

    # FeatureDictionary fuer DD-Instanzen anlegen
    feat_dict = get_features_traindata(data, coref_dict, with_tn_in=False)

    # uber DD-Instanzen iterieren
    for ent_id in feat_dict:
        curr_form = feat_dict[ent_id]["features"]["form"]

        stats_dict[curr_form]["freq_dd"] = stats_dict[curr_form].get("freq_dd", 0) + 1

        # Werte allgemein aufaddieren
        stats_dict["overall"]["avg_sent_dist"] = stats_dict["overall"].get("avg_sent_dist", 0) + feat_dict[ent_id]["features"]["sent_dist"]
        stats_dict["overall"]["avg_tok_dist"] = stats_dict["overall"].get("avg_tok_dist", 0) + feat_dict[ent_id]["features"]["tok_dist"]
        stats_dict["overall"]["avg_anaph_pron"] = stats_dict["overall"].get("avg_anaph_pron", 0) + feat_dict[ent_id]["features"]["anaph_pron"]
        stats_dict["overall"]["avg_len_ante"] = stats_dict["overall"].get("avg_len_ante", 0) + feat_dict[ent_id]["features"]["len_ante"]
        stats_dict["overall"]["avg_lex_overlap"] = stats_dict["overall"].get("avg_lex_overlap", 0) + feat_dict[ent_id]["features"]["lexical_overlap"]
        stats_dict["overall"]["avg_part_of_sn"] = stats_dict["overall"].get("avg_part_of_sn", 0) + feat_dict[ent_id]["features"]["part_of_shell_noun"]
        stats_dict["overall"]["avg_ante_inf_verb"] = stats_dict["overall"].get("avg_ante_inf_verb", 0) + feat_dict[ent_id]["features"]["ante_inf_verb"]

        # Werte spezifisch nach Form der Anapher aufaddieren
        stats_dict[curr_form]["avg_sent_dist"] = stats_dict[curr_form].get("avg_sent_dist", 0) + feat_dict[ent_id]["features"]["sent_dist"]
        stats_dict[curr_form]["avg_tok_dist"] = stats_dict[curr_form].get("avg_tok_dist", 0) + feat_dict[ent_id]["features"]["tok_dist"]
        stats_dict[curr_form]["avg_anaph_pron"] = stats_dict[curr_form].get("avg_anaph_pron", 0) + feat_dict[ent_id]["features"]["anaph_pron"]
        stats_dict[curr_form]["avg_len_ante"] = stats_dict[curr_form].get("avg_len_ante", 0) + feat_dict[ent_id]["features"]["len_ante"]
        stats_dict[curr_form]["avg_lex_overlap"] = stats_dict[curr_form].get("avg_lex_overlap", 0) + feat_dict[ent_id]["features"]["lexical_overlap"]
        stats_dict[curr_form]["avg_part_of_sn"] = stats_dict[curr_form].get("avg_part_of_sn", 0) + feat_dict[ent_id]["features"]["part_of_shell_noun"]
        stats_dict[curr_form]["avg_ante_inf_verb"] = stats_dict[curr_form].get("avg_ante_inf_verb", 0) + feat_dict[ent_id]["features"]["ante_inf_verb"]


    # durchschnittliche Werte ermitteln
    stats_dict["overall"]["avg_sent_dist"] = stats_dict["overall"]["avg_sent_dist"] / stats_dict["overall"]["dd_ent_relevant"]
    stats_dict["overall"]["avg_tok_dist"] = stats_dict["overall"]["avg_tok_dist"] / stats_dict["overall"]["dd_ent_relevant"]
    stats_dict["overall"]["avg_anaph_pron"] = stats_dict["overall"]["avg_anaph_pron"] / stats_dict["overall"]["dd_ent_relevant"]
    stats_dict["overall"]["avg_len_ante"] = stats_dict["overall"]["avg_len_ante"] / stats_dict["overall"]["dd_ent_relevant"]
    stats_dict["overall"]["avg_lex_overlap"] = stats_dict["overall"]["avg_lex_overlap"] / stats_dict["overall"]["dd_ent_relevant"]
    stats_dict["overall"]["avg_part_of_sn"] = stats_dict["overall"]["avg_part_of_sn"] / stats_dict["overall"]["dd_ent_relevant"]
    stats_dict["overall"]["avg_ante_inf_verb"] = stats_dict["overall"]["avg_ante_inf_verb"] / stats_dict["overall"]["dd_ent_relevant"]

    # durchschnittliche Werte fuer Formen berechnen
    for form in relevant_forms:
        for key in stats_dict[form]:
            if key == "freq_total" or key == "freq_dd":
                pass
            else:
                stats_dict[form][key] = stats_dict[form][key] / stats_dict[form]["freq_dd"]

    # Wahrscheinlichkeiten der Vorkommen von it, this, that
    # Teil einer DD-Entitaet zu sein
    stats_dict["it"]["dd_prob"] = stats_dict["it"]["freq_dd"] / stats_dict["it"]["freq_total"]
    stats_dict["this"]["dd_prob"] = stats_dict["this"]["freq_dd"] / stats_dict["this"]["freq_total"]
    stats_dict["that"]["dd_prob"] = stats_dict["that"]["freq_dd"] / stats_dict["that"]["freq_total"]

    # Konsolenausgabe
    print()
    print("----- STATISTICS ABOUT DATASET -----")
    print("\tSTAT\t\tVALUE")
    for category in stats_dict:
        print(f"--- {category} ---")
        for stat in stats_dict[category]:
            print(stat, round(stats_dict[category][stat], 4), sep="\t")
        print()
    print("------------------------------------")

    return stats_dict


def get_stats_from_model(classifier) -> dict:
    """
    Deskriptive Statistiken zu trainierten Klassifizierern ermitteln.
    Mit Konsolenausgabe.

    :param classifier: trainierter Klassifizierer
    :return stats_dict (dict): Dictionary mit statistischen Kennzahlen.
                - Keys: "classes", "class_weights", "intercept", "n_iterations", "n_features",
                        "feature_weights[_feature_]"
    """

    stats_dict = dict()
    # Mapping 'feature' -> Index in FeatureVektor
    feat_index_map = classifier.feat_index_map
    # Index der abhaengigen Variable in FeatureVektor
    index_dep_var = feat_index_map["is_instance"]

    # Statistiken eintragen
    # mit sklearn-Methoden
    stats_dict["classes"] = classifier.classes_
    stats_dict["class_weights"] = classifier.get_params()["class_weight"]
    stats_dict["intercept"] = classifier.intercept_[0]
    stats_dict["n_iterations"] = classifier.n_iter_[0]
    stats_dict["n_features"] = classifier.n_features_in_
    stats_dict["feature_weights"] = dict()


    # ueber features iterieren
    for feat in feat_index_map:
        # abhaengige Variable ueberspringen
        if feat == "is_instance":
            continue
        # Gewichtung des Features eintragen
        if feat_index_map[feat] > index_dep_var:
            stats_dict["feature_weights"][feat] = classifier.coef_[0][feat_index_map[feat] - 1]
        else:
            stats_dict["feature_weights"][feat] = classifier.coef_[0][feat_index_map[feat]]

    # Konsolenausgabe
    print()
    print("----- STATISTICS ABOUT MODEL -------")
    print("\tSTAT\t\tVALUE")
    for key in stats_dict:
        if key == "feature_weights":
            print()
            print("\tFEAT / COEF\t\tWEIGHT")
            for feat in stats_dict[key]:
                print(f"\t{feat}\t\t{stats_dict[key][feat]}")
        else:
            print(f"\t{key}\t\t{stats_dict[key]}")
    print("------------------------------------")

    return stats_dict


def get_stats_from_traindata(feat_dicts: list) -> dict:
    """
    Statistische Kennzahlen ueber verwendete Trainingsdaten extrahieren.
    Mit Konsolenausgabe.

    :param feat_dicts (list): Liste mit Feature-Dictionaries
    :return stats_dict (dict): Dictionary mit statistischen Kennzahlen ueber Trainingsdaten
    """

    # Dictionary fuer Statistiken
    #stats_dict = dict()
    stats_dict = {"TP": {},
                  "TN": {} }


   # ueber Dictionaries iterieren
    for feat_dict in feat_dicts:
        # ueber Trainingsdaten iterieren
        for ent_id in feat_dict:
            # TP-Instanzen
            if feat_dict[ent_id]["features"]["is_instance"] == 1:
                stats_dict["TP"]["freq_total"] = stats_dict["TP"].get("freq_total", 0) + 1

                for feat in feat_dict[ent_id]["features"]:
                    if feat == "is_instance":
                        pass
                    elif feat == "form":
                        stats_dict["TP"][feat_dict[ent_id]["features"][feat]] = stats_dict["TP"].get(feat_dict[ent_id]["features"][feat], 0) + 1
                    else:
                        stats_dict["TP"]["avg_" + str(feat)] = stats_dict["TP"].get("avg_" + feat, 0) + feat_dict[ent_id]["features"][feat]

            # TN-Instanzen
            else:
                stats_dict["TN"]["freq_total"] = stats_dict["TN"].get("freq_total", 0) + 1
                # TN mit TP-Anaph
                if feat_dict[ent_id]["identifier"]["tp_anaph"] == 1:
                    stats_dict["TN"]["freq_tp_anaph"] = stats_dict["TN"].get("freq_tp_anaph", 0) + 1

                for feat in feat_dict[ent_id]["features"]:
                    if feat == "is_instance":
                        pass
                    elif feat == "form":
                        stats_dict["TN"][feat_dict[ent_id]["features"][feat]] = stats_dict["TN"].get(feat_dict[ent_id]["features"][feat], 0) + 1
                    else:
                        stats_dict["TN"]["avg_" + str(feat)] = stats_dict["TN"].get("avg_" + feat, 0) + feat_dict[ent_id]["features"][feat]

    for inst in stats_dict:
        for feat in stats_dict[inst]:
            if feat == "freq_total" or feat == "freq_tp_anaph" or feat == "it" or feat == "this" or feat == "that":
                pass
            else:
                stats_dict[inst][feat] = stats_dict[inst][feat] / stats_dict[inst]["freq_total"]


    # Konsolenausgabe
    print()
    print("----- STATS ABOUT TRAINDATA ----------")
    print("STAT\t\tVALUE")

    for inst in stats_dict:
        print(f"--- {inst} ---")
        for feat in stats_dict[inst]:
            print(feat, stats_dict[inst][feat], sep="\t")
    print("------------------------------------")

    return stats_dict


def show_tp_instances(data: dict, coref: dict) -> None:
    """
    True Positives aus Trainingsdaten auf der Konsole ausgeben.

    :param data (dict): kompletter Datensatz als Dictionary
    :param coref (dict): Dictionary mit allen relevanten Koreferenzpaaren
    :return None: -, Ausgabe auf der Konsole
    """

    # Koreferenzpaare ermitteln
    true_dd = get_true_dd_elements(coref)

    # ueber KorefPaare iterieren
    for ent in true_dd:

        # zwischenspeichern fuer leichteren Lookup
        ante_sent_id = ent[0]
        anaph_tok_id = ent[1]
        doc = ent[2]

        # Antezedens-String erstellen
        ante_sent = " ".join([data[doc][ante_sent_id][tok][0] for tok in data[doc][ante_sent_id]])
        # Anapher-Satz ermitteln
        anaph_sent_found = False
        for sent_id in data[doc]:
            if anaph_sent_found:
                break
            for tok_id in data[doc][sent_id]:
                if tok_id == anaph_tok_id:
                    anaph_sent_id = sent_id
                    anaph_sent_found = True
                    break
        # Anapher-String erstellen
        anaph_sent = " ".join([data[doc][anaph_sent_id][tok][0] if tok != anaph_tok_id else '*'+data[doc][anaph_sent_id][tok][0]+'*'for tok in data[doc][anaph_sent_id]])

        # Konsolenausgabe
        print("ANTE", ante_sent, sep="\t")
        print("ANAPH", anaph_sent, sep="\t")
        print()
        print()

    return None


def get_has_inf_verb(data: dict, doc: str, sent_id: int) -> int:
    """
    Für einen Antezedenssatz-Kandidaten ueberpruefen,
    ob dieser ein infinites Verb enthaelt.

    :param data (dict): Datensatz als Dictionary
    :param doc (str): aktuelles Dokument im Datensatz
    :param sent_id (int): aktueller Satz im Dokument
    :return has_inf_verb (bool): Satz enthaelt infinites Verb ja/nein
    """

    # Return-Variable
    has_inf_verb = 0

    # Verben im Antezdenssatz-Kandidaten extrahieren
    verbs = list()
    for tok in data[doc][sent_id]:
        if data[doc][sent_id][tok][2] == "VERB" or data[doc][sent_id][tok][2] == "AUX":
            verbs.append({"tok_id":tok, "feats":data[doc][sent_id][tok][4].split("|")})

    # fuer jedes Verb testen, ob infinit
    for verb in verbs:
        for feat in verb["feats"]:
            if feat.startswith("VerbForm"):
                sep_index = feat.index("=")
                verb_form = feat[sep_index+1:]
                if verb_form == "Inf":
                    has_inf_verb = 1

    return has_inf_verb




###################
### boilerplate ###
###################

if __name__ == "__main__":
    pass