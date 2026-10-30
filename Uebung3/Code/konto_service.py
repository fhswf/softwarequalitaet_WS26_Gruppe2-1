# Implementiert von: CSKK, BNWK

"""
KontoService-Klasse basierend auf dem KontoServiceInterface
"""

from decimal import Decimal
from typing import List, Dict
from .interfaces import KontoServiceInterface, KontoInterface


# TODO: Team B - Später ersetzt ihr diesen Import durch Team A's Implementation:
# from .konto import Konto


class KontoService(KontoServiceInterface):
    """
    Verwaltet Konten und führt Transaktionen zwischen ihnen aus.

    HINWEIS für Team B - Parallele Entwicklung:
    - Arbeiten Sie mit dem KontoInterface, nicht der konkreten Konto-Klasse
    - Nutzen Sie die _create_konto() Factory-Methode für Konto-Erstellung
    - So können Sie sofort anfangen, ohne auf Team A zu warten!

    Funktionalitäten:
    - Konten verwalten (als List[KontoInterface])
    - Validierung der Benutzereingaben
    - Neue KontoID: max KontoID + 1
    - Export-Funktionen
    - Berechnungen
    """

    def __init__(self):
        self._konten: List[KontoInterface] = []

    def _create_konto(self, konto_id: int, saldo: Decimal) -> KontoInterface:
        """
        Factory-Methode für Konto-Erstellung - ermöglicht parallele Entwicklung!

        TODO: Team B - STARTEN SIE HIER! Diese Methode gibt Ihnen EXTREM EINFACHE Dummy-Objekte.

        JETZT: Verwenden Sie diese Dummy-Implementation für Ihre Service-Entwicklung
        SPÄTER: Ersetzen Sie durch `return Konto(konto_id, saldo)` wenn Team A fertig ist

        WICHTIG: Diese Dummy-Implementation macht fast NICHTS - das ist Absicht!
        Bei der Integration werden Sie Probleme entdecken, die Sie dann gemeinsam lösen.
        """

        # EXTREM EINFACHE DUMMY-IMPLEMENTATION für Team B:
        # Macht fast nichts, gibt nur konstante Werte zurück!
        class DummyKonto:
            def __init__(self, konto_id: int, saldo: Decimal):
                # Speichert die Werte, aber macht keine Validierung!
                pass

            @property
            def konto_id(self) -> int:
                return 1  # ← Immer konstant 1!

            @property
            def saldo(self) -> Decimal:
                return Decimal("100.00")  # ← Immer konstant 100!

            def einzahlen(self, betrag: Decimal) -> None:
                pass  # ← Macht nichts!

            def auszahlen(self, betrag: Decimal) -> None:
                pass  # ← Macht nichts, wirft keine Fehler!

        return DummyKonto(konto_id, saldo)

        # TODO: Team B - Später ersetzen Sie die obige Dummy-Implementation durch:
        # return Konto(konto_id, saldo)

    @staticmethod
    def _decimal_pruefen(wert: Decimal, name: str) -> None:
        """Stellt sicher, dass wert ein endlicher Decimal-Wert ist."""
        if not isinstance(wert, Decimal) or not wert.is_finite():
            raise ValueError(f"{name} muss ein endlicher Decimal-Wert sein")

    def _konto_finden(self, konto_id: int) -> KontoInterface:
        """Gibt das Konto mit der ID zurück oder wirft einen ValueError."""
        for konto in self._konten:
            if konto.konto_id == konto_id:
                return konto
        raise ValueError(f"Konto {konto_id} existiert nicht")

    def konten_auflisten(self) -> List[Dict]:
        return [
            {"konto_id": konto.konto_id, "saldo": konto.saldo}
            for konto in self._konten
        ]

    def konto_erstellen(self, saldo: Decimal = Decimal('0.00')) -> int:
        self._decimal_pruefen(saldo, "Saldo")
        if saldo < Decimal("0.00"):
            raise ValueError("Saldo darf nicht negativ sein")

        konto_id = self.get_max_konto_id() + 1
        konto = self._create_konto(konto_id, saldo)
        self._konten.append(konto)
        return konto_id

    def ueberweisen(self, von_konto_id: int, zu_konto_id: int, betrag: Decimal) -> None:
        self._decimal_pruefen(betrag, "Betrag")
        if betrag <= Decimal("0.00"):
            raise ValueError("Betrag muss größer als 0 sein")
        if von_konto_id == zu_konto_id:
            raise ValueError("Quell- und Zielkonto müssen verschieden sein")

        von_konto = self._konto_finden(von_konto_id)
        zu_konto = self._konto_finden(zu_konto_id)

        # Erst auszahlen: Bei Überziehung bleiben so beide Salden unverändert
        von_konto.auszahlen(betrag)
        zu_konto.einzahlen(betrag)

    def einziehen(self, von_konto_id: int, zu_konto_id: int, betrag: Decimal) -> None:
        self.ueberweisen(von_konto_id, zu_konto_id, betrag)

    def get_max_konto_id(self) -> int:
        return max((konto.konto_id for konto in self._konten), default=0)

    def gesamtsaldo_berechnen(self) -> Decimal:
        return sum((konto.saldo for konto in self._konten), Decimal("0.00"))
