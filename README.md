# Resolution von it-, this- und that-Anaphern mit nicht-nominalem Antezedens


## Einführung

Das vorliegende Programm ist ein Klassifizierer für die Resolution von it-, this- und that-Anaphern mit nicht-nominalem Antezedens. Das Programm bietet Funktionen für Training und Anwendung eines Modells, zur Evaluation der Ergebnisse und für die Ausgabe von statistischen Kennzahlen zu Modellen und Datensätzen.


## Anwendung

Der Klassifizierer kann auf zwei Arten verwendet werden.

- mit Python (z.B. in einer Kommandozeile) die Datei `classifier_use.py` mit ihren Funktionen importieren durch den Befehl `from classifier_use import *`
- im Quellcode der Datei `classifier_use.py` die gewünschten Funktionen und Abläufe in die Funktion `run_script()` schreiben und die Datei mit Python ausführen

Es sind insgesamt drei Dateien vorhanden.

- `functions_basic.py` - Grundlegende Funktionen für das Handling von Daten und Strukturen. Nicht für die Verwendung durch einen User ausgelegt.
- `stanza_preprocessing.py` - Funktionen für die Vorverarbeitung der Datensätze durch Annotationsschritte mit Stanza. Nicht für die Verwendung durch einen User ausgelegt.
- `classifier_use.py` - Enthält die Funktionen des Klassifizierers, die für die Verwendung des Users ausgelegt sind. Durch diese Datei werden die nachfolgend erläuterten Funktionen verfügbar.

### Hinweis
- in der hier vorliegenden Version des Programms fehlen die Verzeichnisse `data` und `data_annotated`, die für das Einlesen von Test- und Trainingsdatensätzen notwendig sind. Die Datensätze können aus datenschutzrechtlichen Gründen nicht öffentlich zur Verfügung gestellt werden.


## Funktionen von `classifier_use.py`

### Hinweise zu Dateinamen
- Trainings- und Testdatensätze werden immer im Unterverzeichnis `./data_annotated/` gesucht.
- Namen von Dateien, die geschrieben werden sollen, müssen mit Dateiendungen angegeben werden. Ausnahme: Funktion `export_model()`, hier bekommt der Dateiname die Endung `.pkl`.
- Namen von Dateien, die eingelesen werden sollen, müssen mit ihrem Pfad, ausgehend von `./data_annotated/` bzw `./models/` (bei `load_model()`) angegeben werden.


### Training

#### -- Funktion `train_model`
- Trainiert einen Klassifizierer mit angegebenen Trainingsdaten und angegebenen Features. Als `'trainFilename` angegebene Dateien werden in Unterverzeichnis `./data_annotated/` gesucht.
- Parameter: `*trainFilename, class_weight, with_stats, ante_scope, form, sent_dist, tok_dist, anaph_pron, len_ante, lexical_overlap, part_of_shell_noun, ante_inf_verb`
- Return: `model`
- Beispielanwendung: `model = train_model('training/Trains_91.txt', 'development/Persuasion_dev.txt')`

	- `*trainFilename (string)` - Pfad eines Trainingsdatensatzes der eingelesen werden soll, ausgehend von Unterverzeichnis `./data_annotated/`. Mehrfachnennung moeglich, z.B. `statistics_traindata('training/Pear_stories.txt', 'training/Gnome_Subset2.txt')`
	- `class_weight (bool/dict)` - Optional. Default=True. Gewichtung der Klassen im Trainingsdatensatz.
		- `True`: Gewichtung wird automatisch aus Daten ermittelt
		- `False`: gleichmäßige Gewichtung, Klasse 0: 0.5, Klasse 1: 0.5
		- `dict`: manuelle Gewichtung mit Dictionary der Form `{0: float, 1: float}`
	- `with_stats (bool)` - Optional. Default=False. Ausgabe von Statistiken über die Trainingsdaten auf der Konsole.
	- `ante_scope (int)` - Optional. Default=3. Skopus der vorangehenden Sätze, die als Antezedenzien für True Negatives verwendet werden sollen. Anzahl der True Negatives wird nicht verändert, nur der Skopus durch den bei Erstellung der TN-Instanzen rotiert wird.
	- `form (bool)` - Optional. Default=True. Einbezug des Features beim Training. Form des anaphorischen Ausdrucks (it, this oder that).
	- `sent_dist (bool)` - Optional. Default=True. Einbezug des Features beim Training. Distanz zwischen Satz des anaphorischen Ausdrucks und Antezedenssatz.
	- `tok_dist (bool)` - Optional. Default=True. Einbezug des Features beim Training. Distanz zwischen anaphorischem Ausdruck und letztem Token des Antezedenssatzes.
	- `anaph_pron (bool)` - Optional. Default=True. Einbezug des Features beim Training. Wortart des anaphorischen Ausdrucks ist Pronomen ja/nein.
	- `len_ante (bool)` - Optional. Default=True. Einbezug des Features beim Training. Anzahl der Token des Antezedenssatzes. 
	- `lexical_overlap (bool)` - Optional. Default=True. Einbezug des Features beim Training. Anteil der lexikalischen Überlappung des Satzes mit anaphorischem Ausdruck mit einem Antezedenssatz.
	- `part_of_shell_noun (bool)` - Optional. Default=True. Einbezug des Features beim Training. Anaphorischer Ausdruck ist Teil einer Shell-Noun-Konstruktion ja/nein.
	- `ante_inf_verb (bool)` - Optional. Default=True. Einbezug des Features beim Training. Antezedenssatz enthält infinites Verb ja/nein.	
	- Return: `model (sklearn.classifier)` - Trainiertes Modell mit Features, Gewichtungen und Bias Term. Kann an Funktionen, die `model` als Parameter verwenden, übergeben werden.


#### -- Funktion `export_model`
- Einen trainierten Klassifizierer in eine externe Datei exportieren. Datei wird mit dem Python-Modul `pickle` in Unterverzeichnis `./models/` geschrieben. Außerdem wird eine Textdatei mit Metadaten (Features, Gewichtungen) zu dem Modell geschrieben (= `filename_metadata.txt`)
- Parameter: `filename, model`
- Return: None -- externe Datei
- Beispielanwendung: `export_model('example_model', model)`

	- `filename (str)` - Name der zu schreibenden Datei. Erhält Endung `.pkl`. Schreibt in Unterverzeichnis `./models/`
	- `model (sklearn.classifier)` - Trainierter Klassifizierer. Zurückgegeben von der Funktion `train_model()`.


#### -- Funktion `load_model`
- Einen trainierten Klassifizierer als `.pkl`-Datei einlesen. Sucht Datei in Unterverzeichnis `./models/`.
- Parameter: `filename`
- Return: `model`
- Beispielanwendung: `model = load_model('example_model.pkl`

	- `filename (str)` - Name der einzulesenden Datei inklusive Dateiendung. Sucht automatisch im Unterverzeichnis `./models` nach der Datei.
	- Return: `model (sklearn.classifier)` - Trainierter Klassifizierer. Kann an Funktionen, die `model` als Parameter verwenden, übergeben werden.



### Anwendung

#### -- Funktion `classify`
- Einen Klassifizierer auf einen Testdatensatz anwenden, d.h. Testkandiaten aus dem Datensatz extrahieren und klassifizieren. Verwendete Features müssen den Features des Modells entsprechen. Bei `testfile` angegebene Datei wird im Unterverzeichnis `./data_annotated/` gesucht.
- Parameter: `testfile, model, console_output, ante_scope, form, sent_dist, tok_dist, anaph_pron, len_ante, lexical_overlap, part_of_shell_noun, ante_inf_verb`
- Return: `featDict_pred`
- Beispielanwendung: `feat_dict = classify('test/light_test.txt', model)`

	- `testfile (str)` - Pfad des Testdatensatzes, ausgehend vom Unterverzeichnis `./data_annotated/`. Z.B. `'test/AMI_test.txt'`
	- `model (sklearn.classifier)` - Trainierter Klassifizierer.
	- `console_output (bool)` - Optional. Default=False. Ausgabe der als positiv klassifizierten Instanzen auf der Konsole.
	- `ante_scope (int)` - Optional. Default=3. Skopus der vorangehenden Sätze, die als Antezedenskandidaten verwendet werden sollen.
	- `form, sent_dist, tok_dist, anaph_pron, len_ante, lexical_overlap, part_of_shell_noun, ante_inf_verb (bool)` - Optional. Jeweils Default=True. Einbezug der jeweiligen Features. Müssen den Features des Klassifizierer entsprechen.
	- Return: `featDict_pred (dict)` - Dictionary mit IDs und Features der Kandidatenpaare. Klassifizierung unter `featDict_pred[ent_id]['features']['is_instance']` = 0/1.


#### -- Funktion `classify_with_file`
- Einen Klassifizierer auf einen Testdatensatz anwenden, d.h. Testkandiaten aus dem Datensatz extrahieren und klassifizieren. Verwendete Features müssen den Features des Modells entsprechen. Bei `testfile` angegebene Datei wird im Unterverzeichnis `./data_annotated/` gesucht. Zusätzlich wird eine externe Datei in das Unterverzeichnis `./solution/` geschrieben nach den Vorgaben der SharedTask.
- Parameter: `testfile, outfilename, model, console_output, with_overview, ante_scope, form, sent_dist, tok_dist, anaph_pron, len_ante, lexical_overlap, part_of_shell_noun, ante_inf_verb`
- Return: `featDict_pred`
- Beispielanwendung: `feat_dict = classify_with_file('test/light_test.txt', 'example_predFile.txt', model)`

	- siehe Funktion `classify`, Zusatzparameter `outfilename, with_overview`
	- `outfilename (str)` - Name der zu schreibenden Datei. Schreibt in Unterverzeichnis "./solution/".
	- `with_overview (bool)` - Optional. Default=True. Instanzen, die als positiv klassifiziert wurden, in eine übersichtlichere Textdatei schreiben. Datei wird in Unterverzeichnis `./solution_overview/` geschrieben.


#### -- Funktion `sim_cross_val`
- Einen Durchlauf von CrossValidation simulieren. Trainiert fünf Modelle mit jeweils vier Datensätzen aus `./data_annotated/development/` und wendet diese jeweils auf einen Datensatz aus `./data_annotated/test/` an. Für jede Anwendung werden ausführliche Evaluationen auf der Konsole ausgegeben. Die Modelle werden in das Unterverzeichnis `./models/` exportiert.
- Parameter: `--`
- Return: `None` -- Konsolenausgabe und Dateien.



### Evaluation und Statistik

#### -- Funktion `evaluate_predictions`
- Einen Klassifizierer auf einen Testdatensatz anwenden und die Klassifizierungen evaluieren. Ausgabe der Evaluation auf Konsole. Bei `testfile` angegebene Datei wird im Unterverzeichnis `./data_annotated/` gesucht.
- Parameter: `testfile, model, console_output, ante_scope, form, sent_dist, tok_dist, anaph_pron, len_ante, lexical_overlap, part_of_shell_noun, ante_inf_verb`
- Return: `None` -- Konsolenausgabe
- Beispielanwendung: `evaluate_predictions('test/Persuasion_test.txt', model)`

	- `testfile (str)` - Pfad des Testdatensatzes, ausgehend vom Unterverzeichnis `./data_annotated/`.
	- `model (sklearn.classifier)` - Trainierter Klassifizierer.
	- `console_output (bool)` - Optional. Default=False. Ausgabe der als positiv klassifizierten Instanzen auf der Konsole.
	-  `ante_scope, form, sent_dist, tok_dist, anaph_pron, len_ante, lexical_overlap, part_of_shell_noun (bool)` - Optional. Jeweils Default=True. Einbezug der jeweiligen Features. Müssen den Features des Klassifizierer entsprechen.


#### -- Funktion `statistics_data`
- Statistische Kennzahlen fuer einen Datensatz auf Konsole ausgeben. Bei `datafile` angegebene Datei wird unter `./data_annotated/` gesucht.
- Parameter: `datafile`
- Return: `stats_dict` und Konsolenausgabe
- Beispielanwendung: `stats_dict = statistics_data('test/RST_DTreeBank_test.txt')`

	- `datafile (str)` - Pfad der einzulesenden Datei, ausgehend vom Unterverzeichnis `./data_annotated/`.
	- Return: `stats_dic (dict)` - Dictionary mit Kennzahlen. Außerdem Ausgabe auf Konsole. `stats_dict` enthält ausgegebene Statstiken als Keys.


#### -- Funktion `statistics_model`
- Statistische Kennzahlen fuer einen trainierten Klassifizierer auf Konsole ausgeben. Benötigt ein `model`-Objekt, welches z.B. durch `train_model()` oder `load_model()` zurückgegeben wird.
- Parameter: `model`
- Return: `stats_dict` und Konsolenausgabe
- Beispielanwendung: `stats_dict = statistics_model(model)`

	- `model (sklearn.classifier)` - Trainierter Klassifizierer.
	- Return: `stats_dict (dict)` - Dictionary mit Kennzahlen. Außerdem Ausgabe auf Konsole. `stats_dict` enthält ausgegebene Statstiken als Keys.


#### -- Funktion `statistics_traindata`
- Ausgabe von Statistischen Kennzahlen zu generierten Trainingsdaten auf Konsole. Bei `*trainFilename` angegebene Dateien werden im Unterverzeichnis `./data_annotated/` gesucht.
- Parameter: `*trainFilename, with_tn, ante_scope, form, sent_dist, tok_dist, anaph_pron, len_ante, lexical_overlap, part_of_shell_noun, ante_inf_verb`
- Return: `stats_dict` und Konsolenausgabe
- Beispielanwendung: `stats_dict = statistics_traindata('training/Pear_stories.txt', 'development/AMI_dev.txt')`

	- `*trainFilename (string)` - Pfad eines Trainingsdatensatzes der eingelesen werden soll, ausgehend von Unterverzeichnis `./data_annotated/`. Mehrfachnennung moeglich, z.B. `statistics_traindata('training/Pear_stories.txt', 'training/Gnome_Subset2.txt')`
	- `with_tn (bool)` - Optional. Default=True. Einbezug von True-Negative-Instanzen ja/nein
	- `ante_scope (int)` - Optional. Default=3. Skopus der vorangehenden Sätze, die als Antezedenzien für True Negatives verwendet werden sollen. Anzahl der True Negatives wird nicht verändert, nur der Skopus durch den bei Erstellung der TN-Instanzen rotiert wird.
	- `form, sent_dist, tok_dist, anaph_pron, len_ante, lexical_overlap, part_of_shell_noun (bool)` - Optionale Parameter. Jeweils Default=True. Einbezug des jeweiligen Features.
	- Return: `stats_dict (dict)` - Dictionary mit statistischen Kennzahlen. Außerdem Ausgabe auf Konsole. `stats_dict` enthält ausgegebene Statstiken als Keys.


#### -- Funktion `write_tp_instances`
- Ausgabe der True-Positive-Instanzen in einem annotierten Datensatz auf der Konsole. Gibt jeweils Antezedenssatz und Satz mit anaphorischem Ausdruck aus, mit dem anaphorischen Ausdruck markiert durch *Sterne*. Bei `*trainFilename` angegebene Dateien werden im Unterverzeichnis `./data_annotated/` gesucht.
- Parameter: `*trainFilename`
- Return: None -- Konsolenausgabe
- Beispielanwendung: `write_tp_instances('development/AMI_dev.txt', 'training/Gnome_Subset2.txt')`

	- `*trainFilename (string)` - Pfad eines Datensatzes der eingelesen werden soll, ausgehend von Unterverzeichnis `./data_annotated/`. Mehrfachnennung moeglich, z.B. `statistics_traindata('training/Pear_stories.txt', 'training/Gnome_Subset2.txt')`




## Allgemeine Hinweise

Das Programm ist für Datensätze der `CODI-CRAC 2021 Shared-Task: Anaphora Resolution in Dialogues` ausgelegt. Aus Gründen des Datenschutzes können die Dateien bei GitHub nicht hochgeladen werden. Für eine komfortable Anwendung sind weitere lokale Vorverarbeitungsschritte mit Funktionen aus `functions_basic.py`, die nicht auf Nutzerfreundlichkeit ausgelegt sind, notwendig. (Die bei der Abgabe der Bachelorarbeit mitgelieferten Dateien wurden schon vorverarbeitet, sodass die Anwendung der Nutzerfunktionen damit möglich ist)
Die Datensätze wurden außerdem mit freundlicher Genehmigung des Linguistic Data Consortium für die vorliegende Arbeit zur Verfügung gestellt.
- https://competitions.codalab.org/competitions/30312
- https://www.ldc.upenn.edu/

Das Programm wurde geschrieben in Python (Version 3.9) und konzipiert für die Anwendung mit Python.
- https://www.python.org/

Für die Anwendung ist außerdem eine Installation von Scikit-learn notwendig. Das Programm wurde mit der Scikit-learn Version 1.0 entwickelt.
- https://scikit-learn.org/stable/index.html
- https://scikit-learn.org/stable/install.html

Für export und import der trainierten Klassifizierer in/aus externen Dateien wird in den Funktionen `export_model()` und `load_model()` das Python-Modul `pickle` verwendet. Es sollten nur Pickle-Dateien importiert werden, die vertrauenswürdig sind.
- https://docs.python.org/3/library/pickle.html

Für lokale Aufbereitungsschritte der Datensätze wurde das Paket `Stanza` der Stanford NLP Group genutzt. Die Funktionen dazu finden sich in der Datei `stanza_preprocessing.py`. Eine Installation des Pakets ist für eine Anwendung der Nutzerfunktionen in `classifier_use.py` nicht notwendig.
- https://stanfordnlp.github.io/stanza/
- https://nlp.stanford.edu/
