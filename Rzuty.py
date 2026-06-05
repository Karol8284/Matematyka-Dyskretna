import random
from collections import Counter

# dane do testów od AI

dane_testowe = {
    "test_1": {
        "nazwa": "Sumaryczna analiza 100 rzutów kostką 6-ścienną",
        "ilosc_kosci": 1,
        "typ_kosci": 6,
        "rzutow": 100,
        "warunek": {"min_powtorzen_wyniku": (6, 18)}  # np. czy wypadnie '6' co najmniej 18 razy
    },
    "test_2": {
        "nazwa": "Analiza 3x3 kości, 10 rzutów (suma ≥ 15)",
        "ilosc_kosci": 3,
        "typ_kosci": 3,
        "rzutow": 10,
        "warunek": {"min_sum": 15}  # suma w jednym rzucie (wszystkich kości) ≥ 15
    },
    "test_3": {
        "nazwa": "Rzuty 2x4-kości, sprawdź parę szóstek w 30 rzutach",
        "ilosc_kosci": 2,
        "typ_kosci": 4,
        "rzutow": 30,
        "warunek": {"min_powtorzen_pary": ((4, 4), 2)}  # para 4,4 co najmniej 2 razy
    },
    "test_4": {
        "nazwa": "Jeden rzut 10x6, czy w ogóle powtórzył się jakiś wynik?",
        "ilosc_kosci": 10,
        "typ_kosci": 6,
        "rzutow": 1,
        "warunek": {"jakikolwiek_powtorzony": True}
    }
}

# opcje
def rzuty_kosciami(ilosc_kosci, typ_kosci, rzutow):
    return [tuple(random.randint(1, typ_kosci) for _ in range(ilosc_kosci)) for _ in range(rzutow)]

def sprawdz_warunek(serie, warunek):
    if warunek is None:
        return None
    if "min_powtorzen_wyniku" in warunek:
        oczko, min_powt = warunek["min_powtorzen_wyniku"]
        ilosc = sum(rzut.count(oczko) for rzut in serie)
        return ilosc >= min_powt, ilosc

    if "min_sum" in warunek:
        min_sum = warunek["min_sum"]
        ilosc = sum(1 for rzut in serie if sum(rzut) >= min_sum)
        return ilosc > 0, ilosc

    if "min_powtorzen_pary" in warunek:
        para, min_powt = warunek["min_powtorzen_pary"]
        ilosc = sum(1 for rzut in serie if tuple(sorted(rzut)) == tuple(sorted(para)))
        return ilosc >= min_powt, ilosc

    if "jakikolwiek_powtorzony" in warunek:
        for rzut in serie:
            licz = Counter(rzut)
            if any(v > 1 for v in licz.values()):
                return True, licz
        return False, None
    return None

def wypisz_serię(serie):
    for i, rzut in enumerate(serie, 1):
        print(f"  {i:2d}. " + " ".join(str(x) for x in rzut))

def szansa_powtorzen(ilosc_rzutow, typ_kosci, oczko, min_powt, symulacji=10000):
    traf = 0
    for _ in range(symulacji):
        seria = rzuty_kosciami(1, typ_kosci, ilosc_rzutow)
        ile = sum(1 for rzut in seria if oczko in rzut)
        if ile >= min_powt:
            traf += 1
    return f"{traf/symulacji:.3%} (aproksymacja)"

# UI
def wyswietl_menu():
    print("\n" + "="*65)
    print("SYMULOWANIE RZUTÓW KOŚĆMI Z WARUNKAMI")
    print("="*65)
    print("1️ -> Test 1: 100 rzutów 1x6, czy '6' wypadnie co najmniej 18 razy?")
    print("2️ -> Test 2: 10 rzutów 3x3, czy suma kości ≥ 15 choć raz?")
    print("3️ -> Test 3: 30 rzutów 2x4, czy para [4,4] padnie co najmniej 2x?")
    print("4️ -> Test 4: 1 rzut 10x6, czy wypadł jakikolwiek dubel?")
    print("5️ -> Własne parametry")
    print("0️ -> Wyjście")
    print("="*65)

def uruchom_test(nr):
    klucz = f"test_{nr}"
    if klucz not in dane_testowe:
        print("Test nie istnieje!")
        return
    test = dane_testowe[klucz]
    print(f"\n🧪 {test['nazwa']}")
    print(f"Kości: {test['ilosc_kosci']}xD{test['typ_kosci']}; Rzutów: {test['rzutow']}\n")
    serie = rzuty_kosciami(test['ilosc_kosci'], test['typ_kosci'], test['rzutow'])
    wypisz_serię(serie)
    if test['warunek']:
        result, ile = sprawdz_warunek(serie, test['warunek'])
        print(f"\nWarunek: {test['warunek']}")
        if isinstance(ile, int):
            print(f"Wynik: {'TAK' if result else 'NIE'} (szukane: {ile})")
        else:
            print(f"Wynik: {'TAK' if result else 'NIE'}")
    print()

def wlasne_parametry():
    print("\nWłasna symulacja:")
    try:
        ilosc_kosci = int(input("Ile kości jednocześnie rzucasz? "))
        typ_kosci = int(input("Ile ścian ma każda kość? "))
        rzutow = int(input("Ile razy chcesz powtórzyć rzucanie? "))
        serie = rzuty_kosciami(ilosc_kosci, typ_kosci, rzutow)
        wypisz_serię(serie)
        if input("Czy chcesz dodać warunek? (t/n): ").lower() == "t":
            print("Rodzaje warunków:")
            print(" 1. min_powtorzen_wyniku")
            print(" 2. min_sum")
            print(" 3. min_powtorzen_pary")
            print(" 4. jakikolwiek_powtorzony")
            war_type = input("Typ warunku (np. 1,2,...): ").strip()
            warunek = {}
            if war_type == "1":
                oczko = int(input("Które oczko chcesz śledzić? "))
                min_powt = int(input("Ile razy minimum? "))
                warunek = {"min_powtorzen_wyniku": (oczko, min_powt)}
            elif war_type == "2":
                min_sum = int(input("Minimalna suma oczek w jednym rzucie: "))
                warunek = {"min_sum": min_sum}
            elif war_type == "3":
                a = int(input("Pierwsza wartość w parze: "))
                b = int(input("Druga wartość w parze: "))
                ile = int(input("Ile razy minimum taka para musi wypaść? "))
                warunek = {"min_powtorzen_pary": ((a,b), ile)}
            elif war_type == "4":
                warunek = {"jakikolwiek_powtorzony": True}
            else:
                print("Nieznany warunek, pomijam...")
                warunek = None

            result, ile = sprawdz_warunek(serie, warunek)
            print(f"Warunek: {warunek}")
            if isinstance(ile, int):
                print(f"Wynik: {'TAK' if result else 'NIE'} (szukane: {ile})")
            else:
                print(f"Wynik: {'TAK' if result else 'NIE'}")
            if war_type == "1":
                print("Symulowana szansa (10 000 powtórzeń):", szansa_powtorzen(rzutow, typ_kosci, oczko, min_powt))

    except Exception as e:
        print("Zły format albo inny błąd:", e)

# Main  kod wykonywalny
if __name__ == "__main__":
    while True:
        wyswietl_menu()
        wybor = input("\n Wybrane: ").strip()
        if wybor in "1234":
            uruchom_test(int(wybor))
        elif wybor == "5":
            wlasne_parametry()
        elif wybor == "0":
            print("\n !Koniec!")
            break
        else:
            print("Błędna opcja!")
