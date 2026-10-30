# Implementiert von: CSKK, BNWK, VRGA, NSBG

"""
Tests für die Konto-Klasse

"""

import pytest
from decimal import Decimal

from ..Code.interfaces import KontoInterface
from ..Code.konto import Konto


class TestKontoErstellung:
    """Tests für die Konto-Erstellung"""

    def test_konto_mit_gueltiger_id_und_positivem_saldo(self):
        # Arrange
        konto_id = 1
        saldo = Decimal("100.00")

        # Act
        konto = Konto(konto_id, saldo)

        # Assert
        assert konto.konto_id == 1
        assert konto.saldo == Decimal("100.00")

    def test_konto_mit_saldo_null(self):
        # Arrange
        saldo = Decimal("0.00")

        # Act
        konto = Konto(1, saldo)

        # Assert
        assert konto.saldo == Decimal("0.00")

    def test_konto_ohne_saldo_startet_bei_null(self):
        # Arrange
        konto_id = 1

        # Act
        konto = Konto(konto_id)

        # Assert
        assert konto.saldo == Decimal("0.00")

    def test_konto_erfuellt_interface(self):
        # Arrange
        konto_id = 1

        # Act
        konto = Konto(konto_id)

        # Assert
        assert isinstance(konto, KontoInterface)

    @pytest.mark.parametrize("ungueltige_id", [None, "", "abc", "1", 1.5])
    def test_leere_oder_nicht_numerische_id_wirft_value_error(self, ungueltige_id):
        # Arrange
        saldo = Decimal("100.00")

        # Act & Assert
        with pytest.raises(ValueError, match="konto_id"):
            Konto(ungueltige_id, saldo)

    def test_negativer_saldo_wirft_value_error(self):
        # Arrange
        saldo = Decimal("-0.01")

        # Act & Assert
        with pytest.raises(ValueError, match="Saldo"):
            Konto(1, saldo)


class TestKontoEigenschaften:
    """Tests für die Properties konto_id und saldo"""

    def setup_method(self):
        self.konto = Konto(7, Decimal("50.25"))

    def test_konto_id_gibt_korrekte_id_zurueck(self):
        # Act
        konto_id = self.konto.konto_id

        # Assert
        assert konto_id == 7

    def test_saldo_gibt_korrekten_saldo_zurueck(self):
        # Act
        saldo = self.konto.saldo

        # Assert
        assert saldo == Decimal("50.25")

    def test_konto_id_ist_read_only(self):
        # Act & Assert
        with pytest.raises(AttributeError):
            self.konto.konto_id = 8

    def test_saldo_ist_read_only(self):
        # Act & Assert
        with pytest.raises(AttributeError):
            self.konto.saldo = Decimal("1000000.00")


class TestEinzahlung:
    """Tests für die Einzahlungs-Funktionalität"""

    def setup_method(self):
        self.konto = Konto(1, Decimal("100.00"))

    def test_einzahlung_erhoeht_saldo(self):
        # Arrange
        betrag = Decimal("50.00")

        # Act
        self.konto.einzahlen(betrag)

        # Assert
        assert self.konto.saldo == Decimal("150.00")

    def test_mehrere_einzahlungen_summieren_sich(self):
        # Arrange
        betraege = [Decimal("10.00"), Decimal("20.00"), Decimal("30.00")]

        # Act
        for betrag in betraege:
            self.konto.einzahlen(betrag)

        # Assert
        assert self.konto.saldo == Decimal("160.00")

    @pytest.mark.parametrize("betrag", [Decimal("0.00"), Decimal("-0.01"), Decimal("-50.00")])
    def test_einzahlung_von_null_oder_negativ_wirft_value_error(self, betrag):
        # Act & Assert
        with pytest.raises(ValueError, match="Einzahlungsbetrag"):
            self.konto.einzahlen(betrag)

    def test_fehlgeschlagene_einzahlung_aendert_saldo_nicht(self):
        # Arrange
        betrag = Decimal("-50.00")

        # Act
        with pytest.raises(ValueError):
            self.konto.einzahlen(betrag)

        # Assert
        assert self.konto.saldo == Decimal("100.00")


class TestAuszahlung:
    """Tests für die Auszahlungs-Funktionalität"""

    def setup_method(self):
        self.konto = Konto(1, Decimal("100.00"))

    def test_auszahlung_reduziert_saldo(self):
        # Arrange
        betrag = Decimal("30.00")

        # Act
        self.konto.auszahlen(betrag)

        # Assert
        assert self.konto.saldo == Decimal("70.00")

    def test_auszahlung_des_gesamten_saldos_ist_erlaubt(self):
        # Arrange
        betrag = Decimal("100.00")

        # Act
        self.konto.auszahlen(betrag)

        # Assert
        assert self.konto.saldo == Decimal("0.00")

    def test_auszahlung_ueber_saldo_wirft_runtime_error(self):
        # Arrange
        betrag = Decimal("100.01")

        # Act & Assert
        with pytest.raises(RuntimeError, match="überzogen"):
            self.konto.auszahlen(betrag)

    @pytest.mark.parametrize("betrag", [Decimal("0.00"), Decimal("-0.01"), Decimal("-50.00")])
    def test_auszahlung_von_null_oder_negativ_wirft_value_error(self, betrag):
        # Act & Assert
        with pytest.raises(ValueError, match="Auszahlungsbetrag"):
            self.konto.auszahlen(betrag)

    def test_fehlgeschlagene_auszahlung_aendert_saldo_nicht(self):
        # Arrange
        betrag = Decimal("100.01")

        # Act
        with pytest.raises(RuntimeError):
            self.konto.auszahlen(betrag)

        # Assert
        assert self.konto.saldo == Decimal("100.00")


class TestKontoGrenzfaelle:
    """Tests für Grenzfälle und Besonderheiten"""

    def test_sehr_grosser_betrag(self):
        # Arrange
        konto = Konto(1, Decimal("999999999999.99"))

        # Act
        konto.einzahlen(Decimal("0.01"))

        # Assert
        assert konto.saldo == Decimal("1000000000000.00")

    def test_kleinster_centbetrag_einzahlen(self):
        # Arrange
        konto = Konto(1)

        # Act
        konto.einzahlen(Decimal("0.01"))

        # Assert
        assert konto.saldo == Decimal("0.01")

    def test_kleinster_centbetrag_auszahlen(self):
        # Arrange
        konto = Konto(1, Decimal("0.01"))

        # Act
        konto.auszahlen(Decimal("0.01"))

        # Assert
        assert konto.saldo == Decimal("0.00")

    def test_decimal_rechnung_bleibt_exakt(self):
        # Arrange: Mit float wäre 0.1 + 0.2 != 0.3
        konto = Konto(1, Decimal("0.10"))

        # Act
        konto.einzahlen(Decimal("0.20"))

        # Assert
        assert konto.saldo == Decimal("0.30")
