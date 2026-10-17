"""
Hier sollen Sie Ihre Implementierung der Konto-Klasse erstellen.

TODO: Implementieren Sie die Konto-Klasse basierend auf dem KontoInterface
"""


from decimal import Decimal
from .interfaces import KontoInterface

class Konto(KontoInterface):
    """
    TODO: Implementieren Sie diese Klasse

    Regeln:
    - ID wird bei Erstellung mitgegeben (numerisch, darf nicht leer sein)
    - Konto darf nicht überzogen werden (Saldo < 0)
    - Fehler bei inkorrekter Nutzung werfen
    """

    def __init__(self, konto_id: int, saldo: Decimal = Decimal('0.00')):
        if konto_id is None or not isinstance(konto_id, int):
            raise ValueError("konto_id muss numerisch und darf nicht leer sein")

        if saldo < Decimal("0.00"):
            raise ValueError("Saldo darf nicht negativ sein")

        self._konto_id = konto_id
        self._saldo = saldo

    @property
    def konto_id(self) -> int:
        return self._konto_id

    @property
    def saldo(self) -> Decimal:
        return self._saldo

    def einzahlen(self, betrag: Decimal) -> None:
        if betrag <= Decimal("0.00"):
            raise ValueError("Einzahlungsbetrag muss größer als 0 sein")

        self._saldo += betrag

    def auszahlen(self, betrag: Decimal) -> None:
        if betrag <= Decimal("0.00"):
            raise ValueError("Auszahlungsbetrag muss größer als 0 sein")

        if self._saldo - betrag < Decimal("0.00"):
            raise RuntimeError("Konto darf nicht überzogen werden")

        self._saldo -= betrag
