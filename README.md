# Studienarbeit: Sudoku Helper
Mit dieser Studienarbeit soll ein Web-Frontend entwickelt werden, welches einem Sudoku-Spieler
bei der Lösung eines schwierigen Sudokus unterstützt.

Ziel ist es **nicht** ein Sudoku automatisch zu lösen, sondern dem Benutzer **Schritt für Schritt** den Weg
zur Lösung aufzuzeigen.

Dazu gehört die Benennung der Lösungsstrategie (bspw. X-Wing, drittes-Auge), sowie die Erklärung
dieser Strategie angewandt auf das aktuelle Rätsel. So soll der Benutzer neue Strategie kennenlernen
und auch für zukünftige Rätsel anwenden können.

## Ablauf:
* der Benutzer öffnet die Webseite und gibt in das leere Sudoku-Grid die bekannten
Zahlen/Werte ein
* das Programm validiert, ob es sich um ein echtes Sudoku handelt
* das Programm bietet dem Nutzer an, alle Kandidaten einblenden zu lassen
* das Programm prüft mit welcher Strategie ein Fortschritt erzielt werden kann.
  * Reihenfolge: von einfach nach komplex
  * Hilfe 1: das Programm nennt dem Benutzer die anzuwendende Strategie und hebt
dem Bereich hervor, auf dem die Strategie angewendet werden soll
  * Hilfe 2: das Programm markiert die konkreten Zellen und Kandidaten, die von der
Strategie betroffen sind
  * Hilfe 3: das Programm erklärt, warum bestimmte Kandidaten laut Strategie
gestrichen werden können
  * Hilfe 4: das Programm löscht den/die Kanditen

Das Programm soll bei dem jedem (lösbaren) Sudoku unterstützen – daher sind ca. 25
Lösungsstrategien zu implementieren.

Diverse Lösungsstrategien sind bspw. hier gut erklärt: <br>
[Lösungsstrategien-1](https://www.thinkgym.de/r%C3%A4tselarten/sudoku/l%C3%B6sungsstrategien-1/) <br>
[Lösungsstrategien-2](https://www.thinkgym.de/r%C3%A4tselarten/sudoku/l%C3%B6sungsstrategien-2/)<br>
[Lösungsstrategien-3](https://www.thinkgym.de/r%C3%A4tselarten/sudoku/l%C3%B6sungsstrategien-3/)

Das Frontend soll sowohl für SmallScreen (Smartphone) als auch BigScreen (Laptop)
benutzeroptimierte Darstellungen liefern.

Final soll das Programm auf ein Ubuntu Server mit Apache und Django laufen. Der Zugang zu diesem
Server wird über die Dauer der Studienarbeit zur Verfügung gestellt.
Alternative: Entwicklung als Android-App.
