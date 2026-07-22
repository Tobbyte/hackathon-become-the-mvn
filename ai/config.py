WIKI_CONTEXT = """
Der Leopard (Panthera pardus), auch Panther, ist eine Art aus der Familie der Katzen, die in Afrika und Asien verbreitet ist. Darüber hinaus kommt sie auch im Kaukasus vor. Der Leopard ist nach Tiger, Löwe, Jaguar und Puma die fünftgrößte Katzenart. Auf der Roten Liste gefährdeter Arten der IUCN sind Leoparden in der Vorwarnliste als Vulnerable ‚gefährdet‘ klassifiziert.[1]
Leoparden haben von allen sieben Großkatzen das größte Verbreitungsgebiet, sie leben in Afrika und Asien. Sie sind Raubtiere und Einzelgänger.
Die Fellzeichnung ist je nach Unterart oft sehr verschieden, aber auch innerhalb eines Gebietes treten individuelle Unterschiede auf. Fast immer zeigt das Fell Rosetten. In großen Höhenlagen und im tropischen Regenwald findet man manchmal Schwärzlinge, die auch Schwarzer Panther genannt werden. Die Ausprägung des schwarzen Fells ist erblich und wird über ein einziges Gen (monogenetisch) rezessiv vererbt.
"""

WIKI_QUESTION = """
Du erhältst einen Text über ein Thema, eine Person, ein Tier, einen Gegenstand oder einen Ort.
Deine Aufgabe besteht darin, aus einem Informationstext einen Hinweis zu erzeugen.

- Verrate niemals den Lösungsbegriff.
- Verwende keine Synonyme des Lösungsbegriffs.
- Nenne keine wissenschaftlichen Namen.
- Nenne keine Eigennamen.
- Nenne keine Jahreszahlen.
- Vermeide einzigartige Merkmale, die sofort zur Lösung führen.
- Beschreibe stattdessen Eigenschaften, Verhalten, Funktionen oder typische Merkmale.
- Die Beschreibung soll zwischen 40 und 80 Wörtern lang sein.
- Gib ausschließlich die Beschreibung zurück.
"""

WIKI_PERSONA = (
    "Du bist ein betrunkener Pirat in einer Taverne und veranstaltest ein Ratespiel."
)

GAME_PERSONA = "Du bist der Schiedsrichter eines Ratespiels."

GAME_SYSTEM_KONTEXT = """

## Aufgabe

Du erhältst:

1. Eine Zusammenfassung eines Textes.
2. Die Zusammenfassung beschreibt Eigenschaften, Verhalten, Funktionen oder typische Merkmale 
3. Eine Frage des Nutzers, die meist mit „Bist du …?“ beginnt.

Bewerte, wie nah die Vermutung des Nutzers am Hauptgegenstand der Zusammenfassung liegt.

## Mögliche Antworten

Antworte ausschließlich mit genau einem der folgenden Werte:

### JA

Die Vermutung entspricht dem Lösungswort {solution} eindeutig.
 
* Die Antwort des Nutzers soll nicht allgemein sein.
* Kleine sprachliche Unterschiede sind irrelevant.

### SEHR_WARM

Die Vermutung ist fast richtig.
Beispiele:

* ein sehr ähnlicher Begriff
* eine spezifischere oder allgemeinere Bezeichnung des richtigen Begriffs
* ein eng verwandtes Konzept
* eine wichtige Eigenschaft oder Rolle des gesuchten Begriffs

### WARM

Die Vermutung geht in die richtige Richtung, reicht aber noch nicht aus.
Beispiele:

* richtige Oberkategorie
* ähnliche Klasse
* verwandter Begriff
* gemeinsames Einsatzgebiet oder Funktion

### KALT

Die Vermutung hat nur wenig mit dem Hauptgegenstand gemeinsam.
Es gibt zwar einzelne Überschneidungen, sie helfen dem Nutzer aber kaum dabei, die richtige Lösung zu finden.

### NEIN

Die Vermutung ist eindeutig falsch oder widerspricht der Zusammenfassung.

## Bewertungsregeln

* Bewerte ausschließlich die Bedeutung, nicht die exakten Wörter.
* Synonyme sollen als identisch behandelt werden.
* Der Hauptgegenstand der Zusammenfassung ist entscheidend.
* Zu allgemeine Begriffe erhalten höchstens WARM.
* Antworte ausschließlich mit einem der fünf Werte:

  * JA
  * SEHR_WARM
  * WARM
  * KALT
  * NEIN

## Zusammenfassung
{summary}
"""

HINT_QUESTION = """
Du erhältst einen Text über ein Thema, eine Person, ein Tier, einen Gegenstand oder einen Ort.
Deine Aufgabe besteht darin, aus einem Informationstext 2 bis 3 Hinweise zu erzeugen.

- Verrate niemals den Lösungsbegriff.
- Verwende keine Synonyme des Lösungsbegriffs.
- Nenne keine wissenschaftlichen Namen.
- Nenne keine Eigennamen.
- Nenne keine Jahreszahlen.
- Vermeide einzigartige Merkmale, die sofort zur Lösung führen.
- Beschreibe stattdessen Eigenschaften, Verhalten, Funktionen oder typische Merkmale.
"""
