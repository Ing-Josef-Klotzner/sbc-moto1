# sbc-Moto1
Raspberry Pi 3 Python Modul motor.py for "sbc-moto1" (Conrad Elektronik) with 1 step motor

Programm / Python Modul für 1 Schrittmotor - Modul "sbc-moto1" (Conrad Elektronik)
Autor: Ing. Josef Klotzner
20190225

Beschreibung:
Das Getriebe hat 1/512
Zusammen mit 8 Motorsteps macht das 512 x 8 = 4096 Schritte für eine Umdrehung

das Programm hier kann auch als Python Modul "motor" geladen werden um die darin definierten Funktionen zu nutzen wie

motor.vor (512 [, 2[, False]])
... macht eine Drehung des Motors (512 Schritte) im Uhrzeigersinn (auf Motorachse gesehen mit Zeitfaktor 2 (= halbe Geschwindigkeit)) mit 8 Halbschritten für eine Motorumdrehung (False Parameter; True wären nur 4 Vollschritte - 40% höhere  Geschwindigkeit)

Mit Strg-C läßt sich Programm unterbrechen ... mit beliebiger Taste wieder fortsetzen.
Bei Unterbrechung wird sicher gestellt, dass Motor letzte Bewegung vollendet und sich kein Stromfluß durch Spulen ergibt (stromlos sicher gestellt)
Es ist sicher gestellt, dass bei völliger Programmunterbrechung und bei Beenden des Programms GPIO sauber ausgeschalten wird.

Beim Zeitfaktor über 10 wurde durch Tests ermittelt, dass 0,01 s Strom zum Anfahren für Einzelschritte ein dennoch hohes Drehmoment sicher stellt. Der Rest des geforderten Zeitfaktors wird stromlos abgewartet (geringer Stromverbrauch und sicher stellen, dass Motor kalt bleibt). Es sind dadurch beliebig lange Zeitfaktoren möglich. Für Uhren oder ähnliches mit geringem Drehmomentbedarf kann MaximumPulseWidth von 10 auf 6 oder 4 reduziert werden (weniger nicht empfehlenswert, weil sonst Anfahren im Motor nicht mehr gewährleistet ist)

Verzeichnis RPi nur auf anderen Computern als dem Raspberry Pi zu verwenden (NICHT auf den Raspberry kopieren!).
Dies dient dazu GPIO zu emulieren, damit man auch mit GPIO Code Programme auf anderen Computern als einem Raspberry entwickeln und auch laufen lassen kann. Man bekommt hiermit eben keine Fehlermeldungen von wegen nicht vorhandenem GPIO  :)

