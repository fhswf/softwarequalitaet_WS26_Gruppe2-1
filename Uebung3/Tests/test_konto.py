# VRGA, NSBG

"""
Test-Template für die Konto-Klasse (Test-After Approach)
========================================================

TODO: Team A - Implementieren Sie hier Ihre Tests NACH der Konto-Implementierung!

Arbeitsablauf:
1. Implementieren Sie zuerst die Konto-Klasse in Code/konto.py
2. Schreiben Sie dann hier umfassende Tests für Ihren Code
3. Testen Sie normale Fälle UND Grenzfälle
4. Dokumentieren Sie Ihre Autorschaft in den Tests

Tipps für gute Tests:
- Verwenden Sie aussagekräftige Test-Namen
- Testen Sie eine Sache pro Test
- Nutzen Sie pytest.raises() für Exception-Tests
- Denken Sie an Grenzwerte (0, negative Zahlen)
"""

import pytest
from decimal import Decimal

# TODO: Team A - Entkommentiert nach eurer Implementierung:
from ..Code.konto import Konto


class TestKontoErstellung:
    """
    Tests für die Konto-Erstellung
    """

    def test_konto_mit_id_und_saldo(self):
        # Konto mit ID 1 und 100€ anlegen
        konto = Konto(1, Decimal("100.00"))

        # Stimmen ID und Saldo?
        assert konto.konto_id == 1
        assert konto.saldo == Decimal("100.00")


    def test_negativer_startsaldo_wirft_fehler(self):
        # Ein Konto mit -10€ darf nicht erstellt werden
        with pytest.raises(ValueError):
            Konto(1, Decimal("-10.00"))  
    
    def test_id_als_text_wirft_fehler(self):
        # Ein Konto mit Text als ID darf nicht erstellt werden
        with pytest.raises(ValueError):
            Konto("abc", Decimal("10.00"))            




class TestKontoEigenschaften:
    """
    Tests für Konto-Eigenschaften (Properties)
    """

    def test_saldo_ist_lesbar(self):
        konto = Konto(1, Decimal("100.00"))
        assert konto.saldo == Decimal("100.00")

    def test_saldo_kann_nicht_ueberschrieben_werden(self):
        konto = Konto(1, Decimal("100.00"))

        # Saldo manuell setzen ist nicht erlaubt
        with pytest.raises(AttributeError):
            konto.saldo = Decimal("1000.00")

    def test_ID_kann_nicht_ueberschrieben_werden(self):
        konto = Konto(1, Decimal("100.00"))

        # ID manuell setzen ist nicht erlaubt
        with pytest.raises(AttributeError):
            konto.konto_id = 99



class TestEinzahlung:
    """
    Tests für die Einzahlungs-Funktionalität
    """

    def test_einzahlung_erhoeht_saldo(self):
        # Konto mit 100€ anlegen
        konto = Konto(1,Decimal("100.00"))

        # 50€ einzahlen
        konto.einzahlen(Decimal("50.00"))

        #es sollten 150€ drauf sein
        assert konto.saldo == Decimal("150.00")

    def test_einzahlung_null_wirft_fehler(self):
        # Konto anlegen
        konto = Konto(1, Decimal("100.00"))
        # 0€ einzahlen muss einen Fehler auslösen
        with pytest.raises(ValueError):
            konto.einzahlen(Decimal("0.00"))

class TestAuszahlung:
    """
    Tests für die Auszahlungs-Funktionalität 
    """

    def test_auszahlung_senkt_saldo(self):
       
        # Konto mit 100€ anlegen
        konto = Konto(1, Decimal("100.00"))

        # 50€ auszahlen
        konto.auszahlen(Decimal("50.00"))

        # Es sollten 50€ drauf sein
        assert konto.saldo == Decimal("50.00")

    def test_auszahlung_ins_negative_wirft_fehler(self):
        # Konto anlegen
        konto = Konto(1, Decimal("100.00"))
        # 150€ auszahlen muss einen Fehler auslösen, da weniger auf dem Konto ist
        with pytest.raises(RuntimeError):
            konto.auszahlen(Decimal("150.00"))

class TestKontoGrenzfaelle:
    """
    Tests für Grenzfälle und Besonderheiten
    """

    def test_kompletten_saldo_abheben(self):
        konto = Konto(1, Decimal("100.00"))

        # Genau alles abheben ist erlaubt -> Saldo wird 0
        konto.auszahlen(Decimal("100.00"))

        assert konto.saldo == Decimal("0.00")

    def test_ein_cent_zu_viel_abheben(self):
        konto = Konto(1, Decimal("100.00"))

        # 1 Cent mehr als vorhanden -> Konto wäre im Minus -> Fehler
        with pytest.raises(RuntimeError):
            konto.auszahlen(Decimal("100.01"))


# TODO: Team A - Erweitern Sie diese Klassen oder fügen Sie neue hinzu!
# Weitere mögliche Test-Klassen:
# - TestKontoStringRepresentation
# - TestKontoEquality
# - TestKontoValidation
