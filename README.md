#Bioinformatyka projekt 11
###Polecenie:
Kalkulator” drzew filogenetycznych ukorzenionych. Typ A. Drzewa wczytywane są z pliku tekstowego (można użyć jakiegoś gotowego parsera np. formatu NEWICK). Operacje: konwersja reprezentacji „rodzina zgodnych klastrów”⇔ drzewo jako graf z jakąś jego wizualizacją (oraz test poprawności danych tj. „czy podana rodzina była zgodna?”). Wyznaczanie odległości topologicznej RF między parą drzew, drzewa konsensusu (o podanym poziomie procentowym) dla zadanego zbioru drzew oraz jej wspólne rozszerzenie (jeśli takie istnieje). Obcięcie podanego drzewa do drzewa filogenetycznego do zadanego podzbioru liści.
###Opis:
Wykonany skrypt pozwala na tworzenie, modyfikację oraz porównywanie drzew filogenetycznych zapisanych w plikach w formacie newick.
##Dostępne funkcje:
####Tworzenie drzewa:
Drzewo można stworzyć przy pomocy funkcji `--create` lub `--random-tree`. Pierwsza z nich pozwala na zbudowanie drzewa przez dodawanie wybranych liści do odpowiednich rodzin. Druga natomiast tworzy losowe drzewo o zadanej liczbie liści.
Istnieje także możliwość dodawania liści do istniejących już drzew przy pomocy funkcji `--update`.
####Modyfikowanie drzew
Przy pomocy funkcji `--update` można dodawać liście, natomiast `--cut` pozwala na obcinanie drzew do zadanych podzbiorów liści.
####Porównywanie drzew
Funkcja `--consensus` pozwala na znalezienie drzewa konsensusu dla wybranych drzew. Możliwe jest wybranie drzew przez adres plików lub podanie folderu z drzewami, które chchemy porównać.
Funkcja `--rf` pozwala na znalezienie odległości RF między podanymi drzewami.