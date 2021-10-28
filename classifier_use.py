"""
------------------------
Matthias Guetebier
Matr.-Nr.: 108016243375
------------------------


Datei mit User-Funktionen des Klassifizierers.
Funktionen enthalten Training und Anwendung von Modellen/Klassifizierern,
Evaluation der Ergebnisse und Statistiken ueber Datensaetze und Modelle/Klassifizierer.
"""



#############################
### MODULE UND FUNKTIONEN ###
#############################

from functions_basic import *




################
### TRAINING ###
################


def train_model(*trainFilename: str, class_weight: bool=True, with_stats: bool=False,
                ante_scope: int=3, form: bool=True, sent_dist: bool=True,
                tok_dist: bool=True, anaph_pron: bool=True, len_ante: bool=True,
                lexical_overlap: bool=True, part_of_shell_noun: bool=True,
                ante_inf_verb: bool=True):
    """
    Ein neues Modell/Klassifizierer trainieren.

    :param trainFilename (list/str): Pfad des Trainingsdatensatzes, ausgehend von Unterverzeichnis 'data_annotated', auch mehrere Pfade moeglich
    :param class_weight (bool/dict): Gewichtung der Klassen {0, 1} in Trainingsdatensatz. Default=True
            - True: Gewichtung wird automatisch auf Basis der Daten ermitteln
            - False: Gewichtung gleichmaessig {0: 0.5, 1: 0.5}
            - Dict: Form {0: float, 1: float} mit float + float = 1
    :param with_stats (bool): Ausgabe von Statistiken ueber Trainingsdaten auf Konsole ja/nein, Default=False
    :param ante_scope (int): Skopus der Antezedenzien bei True Negatives. Default=3
    :param form (bool): Feature einbeziehen. Default=True
    :param sent_dist (bool): Feature einbeziehen. Default=True
    :param tok_dist (bool): Feature einbeziehen. Default=True
    :param anaph_pron (bool): Feature einbeziehen. Default=True
    :param len_ante (bool): Feature einbeziehen. Default=True
    :param lexical_overlap (bool): Feature einbeziehen. Default=True
    :param part_of_shell_noun (bool): Feature einbeziehen. Default=True
    :param ante_inf_verb (bool): Feature einbeziehen. Default=True
    :return model (sklearn.classifier): trainierter Sklearn LogisticRegression-Klassifizierer
    """

    # FeatureVektor
    featVecOverall = list()
    # Klassenvektor, Index parallel zu FeatureVektor
    depVarOverall = list()
    # FeatureDictionary
    featDictsOverall = list()

    # ueber einzulesende Datensaetze iterieren
    for trainFile in trainFilename:
        # Daten einlesen, TP-Instanzen extrahieren
        dataDict = read_annotated_data(trainFile)
        corefDict = cleanup_coref_dict(dataDict, extract_dd_elements(dataDict))

        # Features extrahieren
        featDict = get_features_traindata(dataDict, corefDict, with_tn_in=True, ante_scope_in=ante_scope,
                                          form_in=form, sent_dist_in=sent_dist, tok_dist_in=tok_dist,
                                          anaph_pron_in=anaph_pron, len_ante_in=len_ante, lexical_overlap_in=lexical_overlap,
                                          part_of_shell_noun_in=part_of_shell_noun,
                                          ante_inf_verb_in=ante_inf_verb)
        # Features vektorisieren
        featDict, featIndexMap = vectorize_features(featDict)

        # Trainingsvektoren mit Features und Klasse
        featVec, depVar = get_training_vector(featDict, featIndexMap)
        featVecOverall.extend(featVec)
        depVarOverall.extend(depVar)

        # Ausgabe von Statistiken erwuenscht
        # --> alle Daten sammeln
        if with_stats:
            featDictsOverall.append(featDict)

    # Model trainieren, je nach 'class_weight'
    # Eingabeparameter 'class_weight'
    # - automatisch ermitteln (True)
    if class_weight == True:
        classWeight = get_class_weight(depVarOverall)
        model = fit_model_lr((featVecOverall, depVarOverall), class_weight_in=classWeight)
    # - Verteilung gleichmaessig (False)
    elif class_weight == False:
        model = fit_model_lr((featVecOverall, depVarOverall))
    # - andere Angabe (dict)
    else:
        model = fit_model_lr((featVecOverall, depVarOverall), class_weight_in=class_weight)

    # Metadaten als Attribut des Modells
    model.feat_index_map = featIndexMap
    model.train_data_used = [trainFile for trainFile in trainFilename]

    # Ausgabe von Statistiken auf Konsole
    if with_stats:
        get_stats_from_traindata(featDictsOverall)

    return model


def export_model(filename: str, model):
    """
    Trainiertes Modell/Klassifizierer in Datei exportieren.
    Datei wird mit 'pickle' in Unterverzeichnis 'models' geschrieben.
    Schreibt zuasetzlich Textdatei mit Metadaten zu Modell (='filename_metadata.txt')

    :param filename (str): Name der Datei. Erhaelt Endung '.pkl'. Schreibt in Unterverzeichnis 'models'.
    :param model (sklearn.classifier): Trainiertes Modell.
    :return None: -- Schreiben einer externen Datei.
    """

    # Datei schreiben
    write_model_file(filename, model)
    return None


def load_model(filename: str):
    """
    Trainiertes Modell/Klassifizierer aus Datei laden.

    :param filename (str): Pfad der einzulesenden Datei.
    :return model: Trainiertes Modell/Klassifizierer.
    """

    # Datei lesen und Modell zurueckgeben
    model = load_model_file(filename)
    return model




###################
### ANWENDUNG ###
###################


def classify(testfile: str, model, console_output: bool=False, ante_scope: int=3,
             form: bool=True, sent_dist: bool=True, tok_dist: bool=True,
             anaph_pron: bool=True, len_ante: bool=True,
             lexical_overlap: bool=True, part_of_shell_noun: bool=True,
             ante_inf_verb: bool=True):
    """
    Daten aus Testdatensatz klassifizieren.
    Verwendete Features muessen den Features des Modells entsprechen.
    Eintrag der Klasse als 'is_instance'=0/1 in FeatureDictionary.

    :param testfile (str): Pfad des Testdatensatzes.
    :param model (sklearn.classifier): trainierter Klassifizierer
    :param console_output (bool): Ausgabe der als positiv klassifizierten Instanzen auf Konsole, Default=False
    :param ante_scope (int):
    :param form (bool): Feature einbeziehen. Default=True
    :param sent_dist (bool): Feature einbeziehen. Default=True
    :param tok_dist (bool): Feature einbeziehen. Default=True
    :param anaph_pron (bool): Feature einbeziehen. Default=True
    :param len_ante (bool): Feature einbeziehen. Default=True
    :param lexical_overlap (bool): Feature einbeziehen. Default=True
    :param part_of_shell_noun (bool): Feature einbeziehen. Default=True
    :param ante_inf_verb (bool): Feature einbeziehen. Default=True
    :return featDict_pred (dict): Dictionary mit Features der Testdaten
    """

    # Testdatensatz einlesen
    data = read_annotated_data(testfile)
    # Testkandidaten extrahieren
    candidates = get_candidates(data, ante_scope_in=ante_scope)

    # Features extrahieren und vektorisieren
    featDict_pred = get_features_testdata(data, candidates, form_in=form, sent_dist_in=sent_dist,
                                          tok_dist_in=tok_dist, anaph_pron_in=anaph_pron,
                                          len_ante_in=len_ante, lexical_overlap_in=lexical_overlap,
                                          part_of_shell_noun_in=part_of_shell_noun,
                                          ante_inf_verb_in=ante_inf_verb)
    featDict_pred, featIndexMap = vectorize_features(featDict_pred)

    # Testkandidaten klassifizieren
    featDict_pred = classify_all(model, featDict_pred)

    # Konsolenausgabe der positiven Klassifizierungen
    if console_output:
        write_pred_console(featDict_pred, data)

    return featDict_pred


def classify_with_file(testfile: str, outfilename: str, model, console_output: bool=False,
                       with_overview: bool=True, ante_scope: int=3, form: bool=True,
                       sent_dist: bool=True, tok_dist: bool=True, anaph_pron: bool=True,
                       len_ante: bool=True, lexical_overlap: bool=True,
                       part_of_shell_noun: bool=True, ante_inf_verb: bool=True):
    """
    Daten aus Testdatensatz klassifizieren und Klassifizierung in externe Datei schreiben.
    Schreibt in Unterverzeichjnis 'solution'.
    Verwendete Features muessen den Features des Modells entsprechen.
    Eintrag der Klasse als 'is_instance'=0/1 in FeatureDictionary.

    :param testfile (str): Pfad des Testdatensatzes.
    :param outfilename (str): Name/Pfad der zu schreibenden Datei (nach Schema der SharedTask), Ausgangspunkt Unterverzeichnis 'solution'
    :param model (sklearn.classifier): trainierter Klassifizierer
    :param console_output (bool): Ausgabe der als positiv klassifizierten Instanzen auf Konsole, Default=False
    :param with_overview (bool): Datei mit Ubersicht zu positiv klassifizierten Instanzen schreiben, Default=True
    :param ante_scope (int): Skopus der Antezedens-Kandidaten, Default=3
    :param form (bool): Feature einbeziehen. Default=True
    :param sent_dist (bool): Feature einbeziehen. Default=True
    :param tok_dist (bool): Feature einbeziehen. Default=True
    :param anaph_pron (bool): Feature einbeziehen. Default=True
    :param len_ante (bool): Feature einbeziehen. Default=True
    :param lexical_overlap (bool): Feature einbeziehen. Default=True
    :param part_of_shell_noun (bool): Feature einbeziehen. Default=True
    :param ante_inf_verb (bool): Feature einbeziehen. Default=True
    :return featDict_pred (dict): Dictionary mit Features der Testdaten
    """

    # Testdatensatz einlesen
    data = read_annotated_data(testfile)
    # Testkandidaten extrahieren
    candidates = get_candidates(data, ante_scope_in=ante_scope)

    # Features extrahieren und vektorisieren
    featDict_pred = get_features_testdata(data, candidates, form_in=form, sent_dist_in=sent_dist,
                                          tok_dist_in=tok_dist,  anaph_pron_in=anaph_pron,
                                          len_ante_in=len_ante, lexical_overlap_in=lexical_overlap,
                                          part_of_shell_noun_in=part_of_shell_noun,
                                          ante_inf_verb_in=ante_inf_verb)
    #featDict_pred, featIndexMap = vectorize_features(([featDict_pred]))
    featDict_pred, featIndexMap = vectorize_features(featDict_pred)
    #featDict_pred_new = featDict_pred[0]
    # Testkandidaten klassifizieren
    featDict_pred = classify_all(model, featDict_pred)

    # Ergebnisse in Datei schreiben
    write_pred_file(outfilename, featDict_pred, data)

    # Konsolenausgabe
    if console_output:
        write_pred_console(featDict_pred, data)

    # Ubersichtsdatei schreiben
    if with_overview:
        write_pred_file_overview(outfilename, featDict_pred, data)

    return featDict_pred


def sim_cross_val():
    """
    Einen Durchlauf der CrossValidation simulieren.
    Trainiert fuenf Modelle mit jeweils vier Datensaetzen aus
    'data_annotated/development' und wendet diese jeweils
    auf einen Datensatz aus 'data_annotated/test' an.
    Fuer jede Anwendung werden ausfuehrliche Evaluationen
    auf der Konsole ausgegeben.
    Die Modelle werden in das Verzeichnis 'models' exportiert.

    :return None: Ausgabe auf Konsole
    """

    # Datensaetze
    datasets = ["AMI_dev.txt", "light_dev.txt", "Persuasion_dev.txt",
                "RST_DTreeBank_dev.txt", "Switchboard_3_dev.txt" ]
    # Zaehler fuer Testdatensatz und Dateinamen
    id_testdata = 4
    counter = 1

    # 5 Iterationen
    for data in datasets:
        # testdatensatz
        test = datasets[id_testdata][:-8] + "_test.txt"
        # trainingsdatensaetze
        train = datasets[0:id_testdata] + datasets[id_testdata+1:]

        # modell trainieren mit Daten aus 'development'
        model = train_model("development/"+train[0], "development/"+train[1], "development/"+train[2], "development/"+train[3])
        export_model("simCrossVal_model" + str(counter), model)

        # Modell anwenden und Evaluation ausgeben
        print(f"--- MODELL {str(counter)} ---")
        print(f"--- TESTDATEN: {'./test/'+test} ---")
        evaluate_predictions("test/"+test, model)

        counter += 1
        id_testdata -= 1




##################
### EVALUATION ###
##################


def evaluate_predictions(testfile: str, model, console_output: bool=False, ante_scope: int=3,
                         form: bool=True, sent_dist: bool=True, tok_dist: bool=True,
                         anaph_pron: bool=True, len_ante: bool=True, lexical_overlap: bool=True,
                         part_of_shell_noun: bool=True, ante_inf_verb: bool=True):
    """
    Testdaten mit Goldannotation klassifizieren und Ergebnisse evaluieren.

    :param testfile (str): Pfad des Testdatensatzes.
    :param model (sklearn.classifier): trainierter Klassifizierer
    :param console_output (bool): Ausgabe der als positiv klassifizierten Instanzen auf Konsole, Default=False
    :param ante_scope (int): Skopus der Antezedens-Kandidaten, Default=3
    :param form (bool): Feature einbeziehen. Default=True
    :param sent_dist (bool): Feature einbeziehen. Default=True
    :param tok_dist (bool): Feature einbeziehen. Default=True
    :param anaph_pron (bool): Feature einbeziehen. Default=True
    :param len_ante (bool): Feature einbeziehen. Default=True
    :param lexical_overlap (bool): Feature einbeziehen. Default=True
    :param part_of_shell_noun (bool): Feature einbeziehen. Default=True
    :param ante_inf_verb (bool): Feature einbeziehen. Default=True
    :return None: -- Ausgabe auf Konsole
    """
    # Testdaten und Golddaten einlesen
    dataGold = read_annotated_data(testfile)
    corefGold = cleanup_coref_dict(dataGold, extract_dd_elements(dataGold))

    # Testdaten klassifizieren
    featDict_pred = classify(testfile, model, console_output=console_output,
                             ante_scope=ante_scope, form=form, sent_dist=sent_dist,
                             tok_dist=tok_dist, anaph_pron=anaph_pron, len_ante=len_ante,
                             lexical_overlap=lexical_overlap, part_of_shell_noun=part_of_shell_noun,
                             ante_inf_verb=ante_inf_verb)

    # Evaluation auf Konsole ausgeben
    evalDict = prec_recall_f1(featDict_pred, corefGold)
    print()
    # Evaluation nach Formen ('it', 'this', 'that')
    # auf Konsole ausgeben
    evalDict_withForms = eval_with_forms(featDict_pred, corefGold)

    return None


def statistics_data(datafile: str):
    """
    Statistische Kennzahlen fuer einen Datensatz auf Konsole ausgeben.

    :param datafile: Pfad der einzulesenden Datei
    :return statsDict (dict): Dictionary mit Kennzahlen -- Ausgabe auf Konsole
    """

    # Datensatz einlesen
    data = read_annotated_data(datafile)

    # Statistiken extrahieren
    # und auf Konsole ausgeben
    statsDict = get_stats_from_data(data)

    return statsDict


def statistics_model(model):
    """
    Statistische Kennzahlen zu trainiertem Modell/Klassifizierer auf Konsole ausgeben.

    :param model (sklearn.classifier): trainiertes Modell/Klassifizierer
    :return stats_dict (dict): Dictionary mit statistischen Kennzahlen.
    """

    # Kennzahlen extrahieren
    # und auf Konsole ausgeben
    stats_dict = get_stats_from_model(model)

    return stats_dict


def statistics_traindata(*trainFilename: str, with_tn: bool=True, ante_scope: int=3,
                         form: bool=True, sent_dist: bool=True, tok_dist: bool=True,
                         anaph_pron: bool=True, len_ante: bool=True,
                         lexical_overlap: bool=True, part_of_shell_noun: bool=True,
                         ante_inf_verb: bool=True):
    """
    Statistische Kennzahlen fuer generierte Trainingsdaten auf Konsole ausgeben.
    Rueckgabe eines Dictionaries mit den Kennzahlen.

    :param trainFilename (str/list): Pfad des Trainingsdatensatzes, auch mehrere Pfade moeglich
    :param with_tn (bool): Einbezug von True Negatives, notwendig fuer Anwendung. Default=True
    :param ante_scope (int): Skopus der Antezedenzien bei True Negatives. Default=4
    :param form (bool): Feature einbeziehen. Default=True
    :param sent_dist (bool): Feature einbeziehen. Default=True
    :param tok_dist (bool): Feature einbeziehen. Default=True
    :param anaph_pron (bool): Feature einbeziehen. Default=True
    :param len_ante (bool): Feature einbeziehen. Default=True
    :param lexical_overlap (bool): Feature einbeziehen. Default=True
    :param part_of_shell_noun (bool): Feature einbeziehen. Default=True
    :param ante_inf_verb (bool): Feature einbeziehen. Default=True
    :return stats_dict (dict): Dictionary mit statistischen Kennzahlen
    """
    # FeatureDictionary
    featDictsOverall = list()

    # ueber einzulesende Datensaetze iterieren
    for trainFile in trainFilename:
        # Daten einlesen, TP-Instanzen extrahieren
        dataDict = read_annotated_data(trainFile)
        corefDict = cleanup_coref_dict(dataDict, extract_dd_elements(dataDict))

        # Features extrahieren
        featDict = get_features_traindata(dataDict, corefDict, with_tn_in=with_tn, ante_scope_in=ante_scope,
                                          form_in=form, sent_dist_in=sent_dist, tok_dist_in=tok_dist,
                                          anaph_pron_in=anaph_pron, len_ante_in=len_ante, lexical_overlap_in=lexical_overlap,
                                          part_of_shell_noun_in=part_of_shell_noun, ante_inf_verb_in=ante_inf_verb)
        # Features aller Datensaetze sammeln
        featDictsOverall.append(featDict)

    # Dictionary mit Kennzahlen anlegen
    # und Kennzahlen auf Konsole ausgeben
    stats_dict = get_stats_from_traindata(featDictsOverall)

    return stats_dict


def write_tp_instances(*trainFilename: str):
    """
    Konsolenausgabe der TP-Instanzen in Datensaetzen.

    :param trainFilename (str/list): Pfad des Trainingsdatensatzes, auch mehrere Pfade moeglich
    :return None: -- Konsolenausgabe
    """

    # ueber einzulesende Datensaetze iterieren
    for trainFile in trainFilename:
        # Daten einlesen, TP-Instanzen extrahieren
        dataDict = read_annotated_data(trainFile)
        corefDict = cleanup_coref_dict(dataDict, extract_dd_elements(dataDict))

        # TP-Instanzen auf Konsole ausgeben
        show_tp_instances(dataDict, corefDict)

    return None




def run_script():
    """ Verfuegbare Funktionen in gewuenschter Art und Reihenfolge ausfuehren. """

    sim_cross_val()


###################
### boilerplate ###
###################

if __name__ == "__main__":
    print("""Diese Datei enthaelt Funktionen fuer das Training, die Anwendung und die Evaluation
    eines LogisticRegression-Klassifizierers fuer Anaphern mit nicht-nominalem Antezedens.""")

    run_script()