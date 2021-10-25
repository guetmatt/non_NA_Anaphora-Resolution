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





## Funktionen von `classifier_use.py`

### Training

#### -- **Funktion `train_model`**
- Trainiert einen Klassifizierer mit angegebenen Trainingsdaten und angegebenen Features.
- Parameter: `*trainFilename, class_weight, with_stats, ante_scope, form, sent_dist, tok_dist, anaph_pron, len_ante, lexical_overlap, part_of_shell_noun`
- Return: `model`
- Beispielanwendung:

	- `*trainFilename (string)` - Pfad eines Trainingsdatensatzes der eingelesen werden soll, ausgehend von Unterverzeichnis `./data_annotated/`. Mehrfachnennung moeglich, z.B. `statistics_traindata("training/Pear_stories.txt", "training/Gnome_Subset2.txt")`
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
	- Return: `model (sklearn.classifier)` - Trainiertes Modell mit Features, Gewichtungen und Bias Term. Kann an Funktionen, die `model` als Parameter verwenden, übergeben werden.


#### -- **Funktion `export_model`**
- Einen trainierten Klassifizierer in eine externe Datei exportieren. Datei wird mit dem Python-Modul `pickle` in Unterverzeichnis `./models` geschrieben. Außerdem wird eine Textdatei mit Metadaten (Features, Gewichtungen) zu dem Modell geschrieben (= `filename_metadata.txt`)
- Parameter: `filename, model`
- Return: `None` -- externe Datei
- Beispielanwendung:

	- `filename (str)` - Name der zu schreibenden Datei. Erhält Endung `.pkl`.
	- `model (sklearn.classifier)` - Trainierter Klassifizierer. Zurückgegeben von der Funktion `train_model()`.



#### -- **Funktion `load_model`**
- Einen trainierten Klassifizierer als `.pkl`-Datei einlesen.
- Parameter: `filename`
- Return: `model`
- Beispielanwendung:

	- `filename (str)` - Name der einzulesenden Datei inklusive Dateiendung. Sucht automatisch im Unterverzeichnis `./models` nach der Datei.
	- Return: `model (sklearn.classifier)` - Trainierter Klassifizierer. Kann an Funktionen, die `model` als Parameter verwenden, übergeben werden.


### Anwendung

#### -- **Funktion `classify`**
- Einen Klassifizierer auf einen Testdatensatz anwenden, d.h. Testkandiaten aus dem Datensatz extrahieren und klassifizieren. Verwendete Features müssen den Features des Modells entsprechen.
- Parameter: `testfile, model, console_output, ante_scope, form, sent_dist, tok_dist, anaph_pron, len_ante, lexical_overlap, part_of_shell_noun`
- Return: `featDict_pred`
- Beispielanwendung:

	- `testfile (str)` - Pfad des Testdatensatzes, ausgehend vom Unterverzeichnis `./data_annotated/`. Z.B. `"test/AMI_test.txt"`
	- `model (sklearn.classifier)` - Trainierter Klassifizierer.
	- `console_output (bool)` - Optional. Default=False. Ausgabe der als positiv klassifizierten Instanzen auf der Konsole.
	- `ante_scope (int)` - Optional. Default=3. Skopus der vorangehenden Sätze, die als Antezedenskandidaten verwendet werden sollen.
	- `form, sent_dist, tok_dist, anaph_pron, len_ante, lexical_overlap, part_of_shell_noun` (bool) - Optional. Jeweils Default=True. Einbezug der jeweiligen Features. Müssen den Features des Klassifizierer entsprechen.
	- Return: `featDict_pred (dict)` - Dictionary mit IDs und Features der Kandidatenpaare. Klassifizierung unter `featDict_pred[ent_id]["features"]["is_instance"]` = 0/1.


#### -- **Funktion `classify_with_file`**
- Einen Klassifizierer auf einen Testdatensatz anwenden, d.h. Testkandiaten aus dem Datensatz extrahieren und klassifizieren. Verwendete Features müssen den Features des Modells entsprechen. Zusätzlich wird eine externe Datei in das Unterverzeichnis `./solution/` geschrieben nach den Vorgaben der SharedTask.
- Parameter: `testfile, outfilename, model, console_output, with_overview, ante_scope, form, sent_dist, tok_dist, anaph_pron, len_ante, lexical_overlap, part_of_shell_noun`
- Return: `featDict_pred`
- Beispielanwendung:

	- siehe Funktion `classify`, Zusatzparameter `outfilename, with_overview`
	- `outfilename (str)` - Name der zu schreibenden Datei. Schreibt in Unterverzeichnis `./solution/`.
	- `with_overview (bool) - Optional. Default=True. Instanzen, die als positive klassifiziert wurden, in eine übersichtlichere Textdatei schreiben. Datei wird in Unterverzeichnis `./solution_overview/` geschrieben und bekommt den Namen `outfilename_overview.txt`.



### Evaluation und Statistik


#### -- **Funktion `evaluate_predictions`**
- Einen Klassifizierer auf einen Testdatensatz anwenden und die Klassifizierungen evaluieren. Ausgabe der Evaluation auf Konsole.
- Parameter: `testfile, model, console_output, ante_scope, form, sent_dist, tok_dist, anaph_pron, len_ante, lexical_overlap, part_of_shell_noun`
- Return: `None`-- Konsolenausgabe
- Beispielanwendung:

	- `testfile (str)` - Pfad des Testdatensatzes, ausgehend vom Unterverzeichnis `./data_annotated/`. Z.B. `"test/AMI_test.txt"`.
	- `model (sklearn.classifier)` - Trainierter Klassifizierer.
	- `console_output (bool)` - Optional. Default=False. Ausgabe der als positiv klassifizierten Instanzen auf der Konsole.
	-  `ante_scope, form, sent_dist, tok_dist, anaph_pron, len_ante, lexical_overlap, part_of_shell_noun (bool)` - Optional. Jeweils Default=True. Einbezug der jeweiligen Features. Müssen den Features des Klassifizierer entsprechen.


#### -- **Funktion `statistics_data`**
- Statistische Kennzahlen fuer einen Datensatz auf Konsole ausgeben.
- Parameter: `datafile`
- Return: `stats_dict` und Konsolenausgabe
- Beispielanwendung:

	- `datafile (str)` - Pfad der einzulesenden Datei, ausgehend vom Unterverzeichnis `./data_annotated/`.
	- Return: `stats_dic (dict)`- Dictionary mit Kennzahlen. Außerdem Ausgabe auf Konsole.


#### -- **Funktion `statistics_model`**
- Statistische Kennzahlen fuer einen trainierten Klassifizierer auf Konsole ausgeben.
- Parameter: `model`
- Return: `stats_dict` und Konsolenausgabe
- Beispielanwendung:

	- `model (sklearn.classifier)` - Trainierter Klassifizierer.
	- Return: `stats_dict (dict)` - Dictionary mit Kennzahlen. Außerdem Ausgabe auf Konsole.


#### -- **Funktion `statistics_traindata`**
- Ausgabe von Statistischen Kennzahlen zu generierten Trainingsdaten auf Konsole. Rückgabe als Dictionary.
- Parameter: `*trainFilename, with_tn, ante_scope, form, sent_dist, tok_dist, anaph_pron, len_ante, lexical_overlap, part_of_shell_noun`
- Return: `stats_dict` und Konsolenausgabe
- Beispielanwendung:

	- `*trainFilename (string)` - Pfad eines Trainingsdatensatzes der eingelesen werden soll, ausgehend von Unterverzeichnis `./data_annotated/`. Mehrfachnennung moeglich, z.B. `statistics_traindata("training/Pear_stories.txt", "training/Gnome_Subset2.txt")`
	- `with_tn (bool)` - Optional. Default=True. Einbezug von True-Negative-Instanzen ja/nein
	- `ante_scope (int)` - Optional. Default=3. Skopus der vorangehenden Sätze, die als Antezedenzien für True Negatives verwendet werden sollen. Anzahl der True Negatives wird nicht verändert, nur der Skopus durch den bei Erstellung der TN-Instanzen rotiert wird.
	- `form, sent_dist, tok_dist, anaph_pron, len_ante, lexical_overlap, part_of_shell_noun (bool)` - Optionale Parameter. Jeweils Default=True. Einbezug des jeweiligen Features.
	- Return: `stats_dict (dict)` - Dictionary mit statistischen Kennzahlen.


#### -- **Funktion `write_tp_instances`**
- Ausgabe der True-Positive-Instanzen in einem annotierten Datensatz auf der Konsole. Gibt jeweils Antezedenssatz und Satz mit anaphorischem Ausdruck aus, mit dem anaphorischen Ausdruck markiert durch \*Sterne\*.
- Parameter: `*trainFilename`
- Return: `None` -- Konsolenausgabe
- Beispielanwendung:

	- - `*trainFilename (string)` - Pfad eines Datensatzes der eingelesen werden soll, ausgehend von Unterverzeichnis `./data_annotated/`. Mehrfachnennung moeglich, z.B. `statistics_traindata("training/Pear_stories.txt", "training/Gnome_Subset2.txt")`


## Allgemeine Hinweise









