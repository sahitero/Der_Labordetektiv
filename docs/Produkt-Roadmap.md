# Produkt-Roadmap

1. Produktbeschreibung

Das „Lab Diagnose Game“ ist eine interaktive Lern-App, welche Studierenden ermöglicht, medizinische Fälle spielerisch zu analysieren und Diagnosen zu stellen. 
Die Nutzer arbeiten mit verschiedenen Laborstationen (Blutwerte, Mikroskop, Agarplatten), um Hinweise zu sammeln und eine korrekte Diagnose zu treffen.

Diese Roadmap beschreibt die schrittweise Entwicklung der Streamlit-App. 
Jede Version erweitert die Anwendung um genau ein neues funktionales Element, 
wobei die App jederzeit lauffähig bleibt.



2. Priorisierung der Funktionen

Must-Have (Minimum Viable Product)
Diese Funktionen sind notwendig, damit die App funktioniert:

- Navigation zwischen Screens (Home, Level, Lab)
- Auswahl von Fällen (Cases)
- Anzeige von Blutwerten (zentrale Informationsquelle)
- Anzeige von mikrobiologischen Tests (ergänzende Diagnose)
- Diagnose-Auswahl (macht die Interaktion aus im Spiel)
- Grundlegende Benutzerführung (stellt sicher, dass Nutzer durch die App geführt wird)

Should-Have (wichtig, aber nicht zwingend)
Diese Funktionen verbessern die User Experience:

- Hinweise / Interpretation der Laborwerte (Unterstützt Nutzer bei der Auswertung der Daten)
- Einfaches Feedback, richtig/falsch (gibt direkte Rückmeldung zur Diagnose)
- Strukturierte Darstellung der Ergebnisse (reduziert Überforderung durch bessere Übersicht)
- Verbesserung der Navigation
- Erste visuelle Elemente (Design, um Attraktivität zu erhöhen)

Could-Have (optional / Erweiterungen)
Diese Funktionen machen die App „besonders“ & spannender:

- Tutorial für neue Nutzer (addressiert die im Nutzertest beobachtete Einstiegshürde)
- Fortschrittsanzeige (z. B. Step 1/3) (gibt Orientierung im Diagnoseprozess)
- Gamification (Punkte, Level, Unlocks, um das Spiel attraktiver zu machen)
- Glossar für medizinische Begriffe (vor allem für Nutzern mit wenig Vorwissen)
- Erweiterte Cases (erhöht Vielfalt und Lernwert)


# Version 1
Das Grundgerüst der App aufbauen, um damit weiterarbeiten zu können

## V0.1
Grundstruktur der Streamlit-App mit Startdatei und leerer Oberfläche

## V1.0
Einfache Benutzeroberfläche mit Titel, Navigation und ersten Eingabefeldern


# Version 2
Ziel: MVP (Minimum Viable Product), Ziel ist es die Grundfunktionalität sicherzustellen
-	Ein Case «spielbar»
-	Navigation zwischen den verschiedenen Screens
-	Anzeigen von Laborwerten
-	Diagnose auswählbar
Fokus liegt auf der technischen Funktionsfähigkeit der App

## V2.0
Schreiben der Codes für die interaktiven Laborarbeiten

## V2.1
Aufteilung der Anwendung in mehrere Seiten (Navigation mit Views)


# Version 3
Ziel: Die Nutzerfreundlichkeit erhöhen 
Basierend auf dem Nutzertest werden folgende Verbesserungen umgesetzt:
-	Bessere Struktur der Informationen (hilft gegen Orientierungslosigkeit beim Einstieg)
-	Hinzufügen klarere Hinweise (Erleichterung der nächsten Handlungsschritte)
-	Feedback-System (richtig/falsch) (Unterstützung Lernprozess)
-	Optimierung der Navigation
Fokus liegt auf Nutzerfreundlichkeit und Lernerfolg

## V3.0
Anzeige der berechneten Ergebnisse/ Laborresultate für den Benutzer mit kurzer Interpretation als Hilfe

## V3.1
Feedbacksystem einbauen mit Korrekturhinweisen bei Nutzerentscheidungen

## V3.2
Idee für zukünftige Erweiterung: PDF-Export der Laborresultate


# Version 4
Ziel: App attraktiver machen
-	Tutorial für Einsteiger (hilft bei der Erstbenutzung der App)
-	Evtl eine Fortschrittsanzeige (für mehr und klarere Orientierung)
-	Glossar für die Begriffe (Unterstütz fachliches Verständnis)
-	Erweiterte Gamification (Punktesystem, Level-Syste, Unlock-System, Achievements etc.), erhöht Engagement und Motivation
-	Speicherung der Spielerdaten (um richtiges Gamegefühl zu bekommen)
-	Erweiterung des Designs, um es visuell attraktiver zu machen
Fokus liegt auf langfristiger Nutzung und Erweiterbarkeit

## V4.0
Erweiterung um medizinische Hinweise, Hintergrundinformationen und Empfehlungen basierend auf den Diagnosen

## V4.1
Darstellung der Verlaufsdaten in Form einer Tabelle und eines Diagramms, Erfolgskurve, Auszeichnungen für richtige Diagnosen

## V4.2
Geplante Erweiterung: Persistente Speicherung der Daten über den DataManager (z. B. CSV-Dateien)

## V4.3
Finalisierung des visuellen Stils und letzte Korrekturen an der Benutzerführung für ein flüssiges Spielerlebnis



3. Fazit
Die Roadmap zeigt eine klare Entwicklung von einer grundlegenden funktionierenden App (MVP) hin zu einer benutzerfreundlichen und erweiterten Lernplattform.  
Die Priorisierung ermöglicht eine effiziente Umsetzung der wichtigsten Funktionen und somit die Sicherstellung dass das Grundgerüst der App steht.
