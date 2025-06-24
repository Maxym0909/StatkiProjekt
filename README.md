Multiplayer Battleship Game
Projekt gry w statki z graficznym interfejsem użytkownika (GUI), obsługą dwóch graczy przez sieć lokalną oraz możliwością rozbudowy. Gra została stworzona w Pythonie z wykorzystaniem bibliotek Pygame oraz socket.

Opis projektu
Gra umożliwia dwóch graczom rywalizację online w klasyczną grę w statki. Gracze rozmieszczają statki na planszy 10x10, a następnie na zmianę oddają strzały, próbując zatopić flotę przeciwnika.

W projekcie zastosowano:

obiektowe podejście do reprezentacji statków,

programowanie wielowątkowe po stronie serwera (obsługa dwóch klientów jednocześnie),

komunikację sieciową z wykorzystaniem gniazd TCP,

elementy programowania funkcyjnego (map, filter, reduce, funkcje lambda),

opcjonalnie — wizualizację wyników gry przy pomocy biblioteki matplotlib.

Dodatkowo projekt zawiera testy jednostkowe dla kluczowych elementów logiki gry.

Wymagania systemowe
Python 3.8 lub nowszy

Biblioteki:

pygame

matplotlib (opcjonalnie – do wykresów statystyk)

unittest (wbudowany w Pythona)

Instalacja wymaganych bibliotek:

bash
pip install pygame matplotlib
Uruchamianie gry
1. Uruchomienie serwera
W jednym terminalu uruchom serwer gry:

bash
python server.py
2. Uruchomienie klienta (gry)
Na tym samym komputerze lub innym urządzeniu w sieci uruchom klienta:

bash
python game.py
Wprowadź adres IP serwera (wyświetlany po uruchomieniu server.py).

Rozgrywka
Statki przeciągaj na planszę lewym przyciskiem myszy.

Obracaj statki klikając prawym przyciskiem myszy.

Po rozmieszczeniu wszystkich statków kliknij przycisk START.

Strzelaj klikając w planszę przeciwnika.

Trafienia oznaczone są kolorem czerwonym, pudła — niebieskim.

Wygrywa gracz, który pierwszy zatopi wszystkie statki przeciwnika.

Testy
W folderze projektu znajduje się skrypt testowy test_game.py, zawierający testy jednostkowe dla mechaniki rozmieszczania statków.

Aby uruchomić testy:

bash
python test_game.py
Struktura projektu
bash
.
├── game.py         # Klient z GUI
├── server.py       # Serwer gry (TCP)
├── test_game.py    # Testy jednostkowe
├── ship_images/    # Folder z opcjonalnymi grafikami statków (PNG)
└── README.md       # Dokumentacja projektu
