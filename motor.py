#!/usr/bin/env python3
# -*- coding: utf-8 -*
from __future__ import print_function
# modul motor

from time import sleep
import RPi.GPIO as GPIO

from sys import version_info
if version_info.major == 3:
    pass
elif version_info.major == 2:
    input = raw_input
else:
    print ("Unknown python version - input function not safe")
"""
Programm / Python Modul für 2 Schrittmotore - Modul "sbc-Moto1" (Conrad Elektronik)
Autor: Ing. Josef Klotzner
20190111

Beschreibung:
Das Getriebe hat 1/512
Zusammen mit 8 Motorsteps macht das 512 x 8 = 4096 Schritte für eine Umdrehung

das Programm hier kann auch als Python Modul "motor" geladen werden um die darin definierten Funktionen zu nutzen wie

motor.vor (512 [, 2[, False]])
... macht eine Drehung des Motors (512 Schritte) im Uhrzeigersinn (auf Motorachse gesehen mit Zeitfaktor 2 (= halbe Geschwindigkeit)) mit 8 Halbschritten für eine Motorumdrehung (False Parameter; True wären nur 4 Vollschritte - 40% höhere Geschwindigkeit)

Mit Strg-C läßt sich Programm unterbrechen ... mit beliebiger Taste wieder fortsetzen.
Bei Unterbrechung wird sicher gestellt, dass Motor letzte Bewegung vollendet und sich kein Stromfluß durch Spulen ergibt (stromlos sicher gestellt)
Es ist sicher gestellt, dass bei völliger Programmunterbrechung und bei Beenden des Programms GPIO sauber ausgeschalten wird.

Beim Zeitfaktor über 10 wurde durch Tests ermittelt, dass 0,01 s Strom zum Anfahren für Einzelschritte ein dennoch hohes Drehmoment sicher stellt. Der Rest des geforderten Zeitfaktors wird stromlos abgewartet (geringer Stromverbrauch und sicher stellen, dass Motor kalt bleibt). Es sind dadurch beliebig lange Zeitfaktoren möglich. Für Uhren oder ähnliches mit geringem Drehmomentbedarf kann MaximumPulseWidth von 10 auf 6 oder 4 reduziert werden (weniger nicht empfehlenswert, weil sonst Anfahren im Motor nicht mehr gewährleistet ist)
"""
# PIN-Zuweisung am Raspberry
A = 18
B = 23
C = 24
D = 25
TIME = 0.001

# PINS initialisieren
def init ():
    # Motor definiert auf Position des Step1 setzen
    GPIO.setmode (GPIO.BCM)
    for x in [A, B, C, D]:
        GPIO.setup (x, GPIO.OUT)
        GPIO.output (x, False)
    initToStep1 ()
    
# Ansteuerung der Spulen des Motors
# Lauf Step1, Step2, Step3, Step4, ... im Uhrzeigersinn
# Lauf Step8, Step7, Step6, Step5, ... gegen Uhrzeigersinn

# Schritt mit halbem Drehmoment
def StepH (s, Puls, Wait):
    GPIO.output (s, True)
    sleep (TIME * Puls)
    GPIO.output (s, False)
    sleep (TIME * Wait)
# Schritt mit vollem Drehmoment
def StepV (s1, s2, Puls, Wait):
    GPIO.output (s1, True)
    GPIO.output (s2, True)
    sleep (TIME * Puls)
    GPIO.output (s1, False)
    GPIO.output (s2, False)
    sleep (TIME * Wait)

def PulseWait (Faktor):
    MaximumPulseWidth = 10
    if Faktor <= MaximumPulseWidth:
        return (Faktor, 0)
    else:
        return (MaximumPulseWidth, Faktor - MaximumPulseWidth)

def Step1 (Puls, Wait): StepH (A, Puls, Wait)
def Step2 (Puls, Wait): StepV (A, B, Puls, Wait)
def Step3 (Puls, Wait): StepH (B, Puls, Wait)
def Step4 (Puls, Wait): StepV (B, C, Puls, Wait)
def Step5 (Puls, Wait): StepH (C, Puls, Wait)
def Step6 (Puls, Wait): StepV (C, D, Puls, Wait)
def Step7 (Puls, Wait): StepH (D, Puls, Wait)
def Step8 (Puls, Wait): StepV (D, A, Puls, Wait)

# Eine komplette Umdrehung der Achse = 512 Teilungen
# im Uhrzeigersinn
#               Zeitfaktor 1 ist Maximalgeschwindigkeit
def vor (Teilungen, Faktor = 1, x2 = False): go (Teilungen, Faktor, 0, x2)
# gegen Uhrzeigersinn
def retour (Teilungen, Faktor = 1, x2 = False): go (Teilungen, Faktor, 1, x2)
def go (Teilungen, Faktor, d, x2):
    Faktor = abs (Faktor)
    if Faktor < 1: Faktor = 1
    if x2: funcs = [Step2, Step4, Step6, Step8]; Faktor *= 1.6
    else: funcs = [Step1, Step2, Step3, Step4, Step5, Step6, Step7, Step8]
    (p, w) = PulseWait (Faktor)
    if d == 1: 
        text = "retour"
        funcs = funcs [::-1]
    else: text = "vor"
    for i in range (Teilungen):
        for func in funcs:
            try:
                func (p, w)
            except KeyboardInterrupt:
                func (p, w)
                print ("Unterbrechung in Funktion", text, "in", func, "in Teilung", i)
                input ("Fortsetzen mit ENTER")
                print ("Es wird fortgesetzt ...")

# Einzelschritte (4096 Schritte für eine Achsendrehung)
def vorSteps (Teilungsliste, Pause = 1, Faktor = 1): goS (Teilungsliste, Pause, Faktor, 0)
def retourSteps (Teilungsliste, Pause = 1, Faktor = 1): goS (Teilungsliste, Pause, Faktor, 1)
def goS (Teilungsliste, Pause, Faktor, d):
    TEILUNGEN = 4096
    ListCnt = 0
    Faktor = abs (Faktor)
    if Faktor < 1: Faktor = 1
    funcs = [Step1, Step2, Step3, Step4, Step5, Step6, Step7, Step8]
    (p, w) = PulseWait (Faktor)
    if d == 1: 
        text = "retour"
        funcs = funcs [::-1]
    else: text = "vor"
    Schritte_gesamt = 0
    for i in range (1, TEILUNGEN + 1, 8):
        for step8, func in zip (range (8), funcs):
            try:
                func (p, w)
                if i + step8 == Schritte_gesamt + Teilungsliste [ListCnt] and i + step8 != TEILUNGEN:
                    print ("Pause zwischen Teilungsschritten von", Pause, "Sekunden", end = ", ")
                    print ("bei step", i + step8)
                    sleep (Pause)
                    Schritte_gesamt += Teilungsliste [ListCnt]
                    ListCnt += 1
            except KeyboardInterrupt:
                func (p, w)
                print ("Unterbrechung in Funktion", text,\
                    "in", func, "in Teilschritt", i + step8)
                if i + step8 == Schritte_gesamt + Teilungsliste [ListCnt]:
                    Schritte_gesamt += Teilungsliste [ListCnt]
                    ListCnt += 1
                input ("Fortsetzen mit ENTER")
                print ("Es wird fortgesetzt ...")
 
# wird erstmalig benötigt für Feinpositionierung
# (stop zwischen Step1 und Step8), um Motor anfangs
# definiert auf Position des Step1 zu bringen
def initToStep1 ():
    vor (1)
    retour (1)

def main():
    # Hauptprogramm

    # x2 Geschwindigkeit durch überspringen der Halbschritte
    x2 = True
    # Zeitfaktor kann Fließkommazahl sein größer oder gleich 1
    fak = 1.0
    # Umdrehungen muss ganze Zahl sein
    umdr = 1
    print ("Motorachse dreht sich", umdr, "mal im Uhrzeigersinn, Zeitfaktor", fak, "x2", x2)
    vor (umdr * 512, fak, x2)
    x2 = False
    fak = 1
    print ("Motorachse dreht sich", umdr, "mal gegen Uhrzeigersinn, Zeitfaktor", fak, "x2", x2)
    retour (umdr * 512, fak)
    #print (GPIO.input (1))

    # Ende Hauptprogramm

if __name__ == "__main__":
    try:
        init()
        main()
        GPIO.cleanup ()
    except KeyboardInterrupt:
        print ("Programm unterbrochen. GPIO wurde ausgeschalten")
        GPIO.cleanup ()
