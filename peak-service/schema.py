# peak-service/schema.py

import graphene
from mock_peaks import get_mock_peaks  # Importujemy dane ze sztucznego źródła (mock)

# Definicja typu obiektu, który można pobierać w zapytaniach GraphQL
class Peak(graphene.ObjectType):
    name = graphene.String()             # nazwa szczytu
    height = graphene.Int()              # wysokość w metrach
    pasmo = graphene.String()            # pasmo górskie
    wojewodztwo = graphene.String()      # województwo, w którym znajduje się szczyt

# Główna klasa zawierająca definicje zapytań (query fields)
class Query(graphene.ObjectType):
    # Definiujemy pole `peaks`, które można odpytywać z opcjonalnymi filtrami
    peaks = graphene.List(
        Peak,                            # typ danych zwracanych przez zapytanie (lista obiektów Peak)
        min_height=graphene.Int(),       # opcjonalny parametr: minimalna wysokość
        wojewodztwo=graphene.String()    # opcjonalny parametr: filtracja po województwie
    )

    # 🔍 Funkcja resolve_<pole> służy do obsługi logiki dla danego pola zapytania
    # W tym przypadku: `resolve_peaks` odpowiada za zwracanie danych dla pola `peaks`

    def resolve_peaks(self, info, min_height=None, wojewodztwo=None):
        """
        Funkcja wywoływana automatycznie przez graphene, gdy klient wykonuje zapytanie o pole `peaks`.

        Parametry:
        - info: kontekst wykonania zapytania (dostęp do nagłówków, użytkownika, itp.)
        - min_height: opcjonalna filtracja po minimalnej wysokości
        - wojewodztwo: opcjonalna filtracja po województwie

        Zwraca: listę obiektów Peak spełniających zadane kryteria
        """

        all_peaks = get_mock_peaks()  # pobranie wszystkich szczytów z mocka

        # Filtrowanie po wysokości
        if min_height:
            all_peaks = [p for p in all_peaks if p["height"] >= min_height]

        # Filtrowanie po województwie
        if wojewodztwo:
            all_peaks = [p for p in all_peaks if p["wojewodztwo"] == wojewodztwo]

        # Zwracamy listę obiektów typu Peak
        return [
            Peak(
                name=p["name"],
                height=p["height"],
                pasmo=p["pasmo"],
                wojewodztwo=p["wojewodztwo"]
            ) for p in all_peaks
        ]

# Zdefiniowanie schematu głównego GraphQL – potrzebne w app.py do wykonania zapytań
schema = graphene.Schema(query=Query)
