# Implementiert von: CSKK, BNWK

"""
Tests für die KontoService-Klasse

"""

import pytest
from decimal import Decimal

from ..Code.interfaces import KontoServiceInterface
from ..Code.konto_service import KontoService

UNGUELTIGE_DECIMAL_WERTE = [
    None,
    "100.00",
    100.0,
    Decimal("NaN"),
    Decimal("Infinity"),
]
UNGUELTIGE_BETRAEGE = UNGUELTIGE_DECIMAL_WERTE + [Decimal("0.00"), Decimal("-0.01")]
UNGUELTIGE_SALDEN = UNGUELTIGE_DECIMAL_WERTE + [Decimal("-0.01")]


@pytest.fixture
def service():
    return KontoService()


def saldo_von(service, konto_id):
    """Liest den Saldo eines Kontos aus der Kontenliste."""
    for konto in service.konten_auflisten():
        if konto["konto_id"] == konto_id:
            return konto["saldo"]
    raise AssertionError(f"Konto {konto_id} nicht in der Kontenliste")


class TestKontoServiceErstellung:
    """Tests für die KontoService-Erstellung"""

    def test_neuer_service_hat_keine_konten(self):
        # Act
        service = KontoService()

        # Assert
        assert service.konten_auflisten() == []

    def test_service_erfuellt_interface(self):
        # Act
        service = KontoService()

        # Assert
        assert isinstance(service, KontoServiceInterface)

    def test_services_teilen_keine_konten(self):
        # Arrange
        erster_service = KontoService()
        zweiter_service = KontoService()

        # Act
        erster_service.konto_erstellen(Decimal("10.00"))

        # Assert
        assert zweiter_service.konten_auflisten() == []


class TestKontoVerwaltung:
    """Tests für Konto-Erstellung und -Verwaltung"""

    def test_erstes_konto_erhaelt_id_1(self, service):
        # Act
        konto_id = service.konto_erstellen(Decimal("100.00"))

        # Assert
        assert konto_id == 1

    def test_konto_wird_zur_liste_hinzugefuegt(self, service):
        # Act
        service.konto_erstellen(Decimal("100.00"))

        # Assert
        assert len(service.konten_auflisten()) == 1

    def test_konto_uebernimmt_startsaldo(self, service):
        # Act
        konto_id = service.konto_erstellen(Decimal("42.50"))

        # Assert
        assert saldo_von(service, konto_id) == Decimal("42.50")

    def test_konto_ohne_saldo_startet_bei_null(self, service):
        # Act
        konto_id = service.konto_erstellen()

        # Assert
        assert saldo_von(service, konto_id) == Decimal("0.00")

    @pytest.mark.parametrize("saldo", UNGUELTIGE_SALDEN)
    def test_ungueltiger_saldo_wirft_value_error(self, service, saldo):
        # Act & Assert
        with pytest.raises(ValueError, match="Saldo"):
            service.konto_erstellen(saldo)

    def test_ungueltiger_saldo_legt_kein_konto_an(self, service):
        # Act
        with pytest.raises(ValueError):
            service.konto_erstellen(Decimal("-1.00"))

        # Assert
        assert service.konten_auflisten() == []

    def test_konten_auflisten_nennt_alle_konten(self, service):
        # Arrange
        service.konto_erstellen(Decimal("10.00"))
        service.konto_erstellen(Decimal("20.00"))

        # Act
        konten = service.konten_auflisten()

        # Assert
        assert konten == [
            {"konto_id": 1, "saldo": Decimal("10.00")},
            {"konto_id": 2, "saldo": Decimal("20.00")},
        ]


class TestTransaktionen:
    """Tests für Überweisung und Einzug über den Service"""

    def setup_method(self):
        self.service = KontoService()
        self.konto_a = self.service.konto_erstellen(Decimal("100.00"))
        self.konto_b = self.service.konto_erstellen(Decimal("50.00"))

    def test_ueberweisung_reduziert_saldo_des_senders(self):
        # Act
        self.service.ueberweisen(self.konto_a, self.konto_b, Decimal("30.00"))

        # Assert
        assert saldo_von(self.service, self.konto_a) == Decimal("70.00")

    def test_ueberweisung_erhoeht_saldo_des_empfaengers(self):
        # Act
        self.service.ueberweisen(self.konto_a, self.konto_b, Decimal("30.00"))

        # Assert
        assert saldo_von(self.service, self.konto_b) == Decimal("80.00")

    def test_ueberweisung_an_unbekanntes_konto_wirft_value_error(self):
        # Act & Assert
        with pytest.raises(ValueError, match="existiert nicht"):
            self.service.ueberweisen(self.konto_a, 99, Decimal("10.00"))

    def test_ueberweisung_von_unbekanntem_konto_wirft_value_error(self):
        # Act & Assert
        with pytest.raises(ValueError, match="existiert nicht"):
            self.service.ueberweisen(99, self.konto_a, Decimal("10.00"))

    def test_ueberweisung_auf_dasselbe_konto_wirft_value_error(self):
        # Act & Assert
        with pytest.raises(ValueError, match="verschieden"):
            self.service.ueberweisen(self.konto_a, self.konto_a, Decimal("10.00"))

    @pytest.mark.parametrize("betrag", UNGUELTIGE_BETRAEGE)
    def test_ueberweisung_mit_ungueltigem_betrag_wirft_value_error(self, betrag):
        # Act & Assert
        with pytest.raises(ValueError, match="Betrag"):
            self.service.ueberweisen(self.konto_a, self.konto_b, betrag)

    def test_einzug_reduziert_saldo_des_belasteten_kontos(self):
        # Act
        self.service.einziehen(self.konto_a, self.konto_b, Decimal("30.00"))

        # Assert
        assert saldo_von(self.service, self.konto_a) == Decimal("70.00")

    def test_einzug_erhoeht_saldo_des_einziehenden_kontos(self):
        # Act
        self.service.einziehen(self.konto_a, self.konto_b, Decimal("30.00"))

        # Assert
        assert saldo_von(self.service, self.konto_b) == Decimal("80.00")

    def test_einzug_von_unbekanntem_konto_wirft_value_error(self):
        # Act & Assert
        with pytest.raises(ValueError, match="existiert nicht"):
            self.service.einziehen(99, self.konto_a, Decimal("10.00"))

    @pytest.mark.parametrize("betrag", UNGUELTIGE_BETRAEGE)
    def test_einzug_mit_ungueltigem_betrag_wirft_value_error(self, betrag):
        # Act & Assert
        with pytest.raises(ValueError, match="Betrag"):
            self.service.einziehen(self.konto_a, self.konto_b, betrag)


class TestSaldoFunktionen:
    """Tests für die Berechnung des Gesamtsaldos"""

    def test_gesamtsaldo_ohne_konten_ist_null(self, service):
        # Act
        gesamtsaldo = service.gesamtsaldo_berechnen()

        # Assert
        assert gesamtsaldo == Decimal("0.00")

    def test_gesamtsaldo_mit_einem_konto(self, service):
        # Arrange
        service.konto_erstellen(Decimal("12.34"))

        # Act
        gesamtsaldo = service.gesamtsaldo_berechnen()

        # Assert
        assert gesamtsaldo == Decimal("12.34")

    def test_gesamtsaldo_mit_mehreren_konten(self, service):
        # Arrange
        service.konto_erstellen(Decimal("10.10"))
        service.konto_erstellen(Decimal("20.20"))
        service.konto_erstellen(Decimal("30.30"))

        # Act
        gesamtsaldo = service.gesamtsaldo_berechnen()

        # Assert
        assert gesamtsaldo == Decimal("60.60")

    def test_ueberweisung_aendert_gesamtsaldo_nicht(self, service):
        # Arrange
        konto_a = service.konto_erstellen(Decimal("100.00"))
        konto_b = service.konto_erstellen(Decimal("50.00"))

        # Act
        service.ueberweisen(konto_a, konto_b, Decimal("30.00"))

        # Assert
        assert service.gesamtsaldo_berechnen() == Decimal("150.00")


class TestUtilityFunktionen:
    """Tests für die ID-Verwaltung"""

    def test_max_konto_id_ohne_konten_ist_null(self, service):
        # Act
        max_konto_id = service.get_max_konto_id()

        # Assert
        assert max_konto_id == 0

    def test_max_konto_id_nach_einem_konto(self, service):
        # Arrange
        service.konto_erstellen()

        # Act
        max_konto_id = service.get_max_konto_id()

        # Assert
        assert max_konto_id == 1

    def test_max_konto_id_nach_mehreren_konten(self, service):
        # Arrange
        service.konto_erstellen()
        service.konto_erstellen()
        service.konto_erstellen()

        # Act
        max_konto_id = service.get_max_konto_id()

        # Assert
        assert max_konto_id == 3

    def test_ids_werden_fortlaufend_vergeben(self, service):
        # Act
        konto_ids = [service.konto_erstellen() for _ in range(3)]

        # Assert
        assert konto_ids == [1, 2, 3]

    def test_keine_doppelten_ids(self, service):
        # Act
        konto_ids = [service.konto_erstellen() for _ in range(3)]

        # Assert
        assert len(set(konto_ids)) == 3


class TestKontoServiceIntegration:
    """Integration-Tests zwischen Service und Konto-Klassen"""

    def setup_method(self):
        self.service = KontoService()
        self.konto_a = self.service.konto_erstellen(Decimal("100.00"))
        self.konto_b = self.service.konto_erstellen(Decimal("50.00"))

    def test_ueberweisung_ueber_saldo_wirft_runtime_error(self):
        # Act & Assert
        with pytest.raises(RuntimeError, match="überzogen"):
            self.service.ueberweisen(self.konto_a, self.konto_b, Decimal("100.01"))

    def test_einzug_ueber_saldo_wirft_runtime_error(self):
        # Act & Assert
        with pytest.raises(RuntimeError, match="überzogen"):
            self.service.einziehen(self.konto_a, self.konto_b, Decimal("100.01"))

    def test_ueberweisung_des_gesamten_saldos_ist_erlaubt(self):
        # Act
        self.service.ueberweisen(self.konto_a, self.konto_b, Decimal("100.00"))

        # Assert
        assert saldo_von(self.service, self.konto_a) == Decimal("0.00")
        assert saldo_von(self.service, self.konto_b) == Decimal("150.00")

    def test_ueberzogene_ueberweisung_aendert_keine_salden(self):
        # Act
        with pytest.raises(RuntimeError):
            self.service.ueberweisen(self.konto_a, self.konto_b, Decimal("100.01"))

        # Assert
        assert saldo_von(self.service, self.konto_a) == Decimal("100.00")
        assert saldo_von(self.service, self.konto_b) == Decimal("50.00")

    def test_ueberzogener_einzug_aendert_keine_salden(self):
        # Act
        with pytest.raises(RuntimeError):
            self.service.einziehen(self.konto_a, self.konto_b, Decimal("100.01"))

        # Assert
        assert saldo_von(self.service, self.konto_a) == Decimal("100.00")
        assert saldo_von(self.service, self.konto_b) == Decimal("50.00")

    def test_ueberweisung_an_unbekanntes_konto_aendert_saldo_nicht(self):
        # Act
        with pytest.raises(ValueError):
            self.service.ueberweisen(self.konto_a, 99, Decimal("10.00"))

        # Assert
        assert saldo_von(self.service, self.konto_a) == Decimal("100.00")

    def test_ueberweisung_mit_ungueltigem_betrag_aendert_keine_salden(self):
        # Act
        with pytest.raises(ValueError):
            self.service.ueberweisen(self.konto_a, self.konto_b, Decimal("-10.00"))

        # Assert
        assert saldo_von(self.service, self.konto_a) == Decimal("100.00")
        assert saldo_von(self.service, self.konto_b) == Decimal("50.00")

    def test_vollstaendiger_workflow(self):
        # Arrange
        service = KontoService()
        konto_1 = service.konto_erstellen(Decimal("200.00"))
        konto_2 = service.konto_erstellen(Decimal("50.00"))
        konto_3 = service.konto_erstellen()

        # Act
        service.ueberweisen(konto_1, konto_2, Decimal("75.50"))
        service.einziehen(konto_2, konto_3, Decimal("25.25"))
        with pytest.raises(RuntimeError):
            service.ueberweisen(konto_3, konto_1, Decimal("25.26"))

        # Assert
        assert service.konten_auflisten() == [
            {"konto_id": 1, "saldo": Decimal("124.50")},
            {"konto_id": 2, "saldo": Decimal("100.25")},
            {"konto_id": 3, "saldo": Decimal("25.25")},
        ]
        assert service.get_max_konto_id() == 3
        assert service.gesamtsaldo_berechnen() == Decimal("250.00")
