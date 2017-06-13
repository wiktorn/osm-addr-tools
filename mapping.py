# # -*- coding: UTF-8 -*-
# TODO:
# - add warning, when street exists as a part of name in sym_ul dictionary or in ULIC

addr_map = {
# !sort -t : -b -k 2
 '1-ego Maja':                          '1 Maja',
 '1-go Maja':                           '1 Maja',
 '11-go Listopada':                     '11 Listopada',
 '15-go Grudnia':                       '15 Grudnia',
 '17-go Lipca':                         '17 Lipca',
 '21-go Stycznia':                      '21 Stycznia',
 '24-go Stycznia':                      '24 Stycznia',
 '27-go Stycznia':                      '27 Stycznia',
 '28-go Lutego':                        '28 Lutego',
 '3-go Kwietnia':                       '3 Kwietnia',
 '3-ego Maja':                          '3 Maja',
 '3-go Maja':                           '3 Maja',
 '35 Lecia PRL':                        '35-lecia PRL',
 '9-go Maja':                           '9 Maja',
 'Asnyka A.':                           'Adama Asnyka',
 'Asnyka Adama':                        'Adama Asnyka',
 'Asnyka':                              'Adama Asnyka',
 'A. Branickiego':                      'Adama Branickiego',
 'A. Ciołkosza':                        'Adama Ciołkosza',
 'D. A. Chłapowskiego':                 'Adama Dezyderego Chłapowskiego',
 'A. Mickiewicza':                      'Adama Mickiewicza',
 'Mickiewicza A.':                      'Adama Mickiewicza',
 'Mickiewicza Adama':                   'Adama Mickiewicza',
 'Mickiewicza':                         'Adama Mickiewicza',
 'A. Próchnika':                        'Adama Próchnika',
 'Próchnika Adama':                     'Adama Próchnika',
 'Śnieżka Adama':                       'Adama Śnieżka',
 'A. Suligowskiego':                    'Adolfa Suligowskiego',
 'Warskiego Adolfa':                    'Adolfa Warskiego',
 'A. Einsteina':                        'Alberta Einsteina', 
 'Al. H. Kołłątaja':                    'Aleja Hugona Kołłątaja',
 'al. J. Ch. Szucha':                   'Aleja Jana Chrystiana Szucha',
 'al. Komisji Edukacji Narodowej ( KEN )': 'Aleja Komisji Edukacji Narodowej',
 'Polipol Aleja':                       'Aleja Polipol',
 'al. T. Hopfera':                      'Aleja Tomasza Hopfera',
 'al. W. Reymonta':	                    'Aleja Władysława Reymonta',
 'al. gen. A. Chruściela "Montera"':    'Aleja generała Antoniego Chruściela "Montera"',
 'Aleja gen. W. Sikorskiego':           'Aleja generała Władysława Sikorskiego',
 'al. marsz. J. Piłsudskiego':          'Aleja marszałka Józefa Piłsudskiego',
 'Aleja Jerozolimskie':                 'Aleje Jerozolimskie',
 'al. Jerozolimskie':                   'Aleje Jerozolimskie',
 'al. Ujazdowskie':                     'Aleje Ujazdowskie',
 'A. Bardiniego':                       'Aleksandra Bardiniego',
 'Bałasza A.':                          'Aleksandra Bałasza',
 'A. Brücknera':                        'Aleksandra Brücknera',
 'A. Dyżewskiego':                      'Aleksandra Dyżewskiego',
 'A. Fleminga':                         'Aleksandra Fleminga',
 'Fredry Aleksandra':                   'Aleksandra Fredry',
 'Fredry':                              'Aleksandra Fredry',
 'A. Gajkowicza':                       'Aleksandra Gajkowicza',
 'A. Gierymskiego':                     'Aleksandra Gierymskiego',
 'A. Gieysztora':                       'Aleksandra Gieysztora',
 'Głowackiego A.':                      'Aleksandra Głowackiego',
 'A. Janowskiego':                      'Aleksandra Janowskiego',
 'A. Kamińskiego':                      'Aleksandra Kamińskiego',
 'Kamińskiego A.':                      'Aleksandra Kamińskiego',
 'A. Kostki Napierskiego':              'Aleksandra Kostki Napierskiego',
 'A. Krywulta':                         'Aleksandra Krywulta',
 'A. Orłowskiego':                      'Aleksandra Orłowskiego',
 'Orłowskiego Aleksandra':              'Aleksandra Orłowskiego',
 'A. Prystora':                         'Aleksandra Prystora',
 'A. Sulkiewicza':                      'Aleksandra Sulkiewicza',
 'A. Wejnerta':                         'Aleksandra Wejnerta',
 'Gierymskich Aleksandra i Maksymiliana': 'Aleksandra i Maksymiliana Gierymskich',
 'A. Śląskiej':                         'Aleksandry Śląskiej',
 'Sokołowskiego A.':                    'Alfreda Sokołowskiego',
 'A. Felińskiego':                      'Alojzego Felińskiego',
 'A. Kowalczyka':                       'Anastazego Kowalczyka',
 'Modrzewskiego':                       'Andrzeja Frycza Modrzewskiego',
 'Kmicica Andrzeja':                    'Andrzeja Kmicica',
 'A. Munka':                            'Andrzeja Munka',
 'Samulowskiego Andrzeja':              'Andrzeja Samulowskiego',
 'A. Sołtana':                          'Andrzeja Sołtana',
 'A. Struga':                           'Andrzeja Struga',
 'Struga Andrzeja':                     'Andrzeja Struga',
 'A. Szomańskiego':                     'Andrzeja Szomańskiego',
 'A. Krzywoń':                          'Anieli Krzywoń',
 'A. German':                           'Anny German',
 'Zelenay A.':                          'Anny Zelenay',
 'A. Corazziego':                       'Antonia Corazziego',
 'A. Vivaldiego':                       'Antonia Vivaldiego',
 'A. Dobiszewskiego':                   'Antoniego Dobiszewskiego',
 'A. E. Odyńca':                        'Antoniego Edwarda Odyńca',
 'A. Fontany':                          'Antoniego Fontany',
 'A. J. Madalińskiego' :                'Antoniego Józefa Madalińskiego',
 'A. Kacpury':                          'Antoniego Kacpury',
 'A. Kocjana':                          'Antoniego Kocjana',
 'Kosińskiego':                         'Antoniego Kosińskiego',
 'A. Magiera':                          'Antoniego Magiera',
 'A. Malczewskiego':                    'Antoniego Malczewskiego',
 'A. Pajdaka':                          'Antoniego Pajdaka',
 'A. P. Łaguny':                        'Antoniego Pankracego Łaguny',
 'A. Parola':                           'Antoniego Parola',
 'A. Ponikowskiego':                    'Antoniego Ponikowskiego',
 'Sułkowskiego Antoniego':              'Antoniego Sułkowskiego',
 'abp. J. Teodorowicza':                'Arcybiskupa Józefa Teodorowicza',
 'Bożka Arkadiusza':                    'Arkadiusza Bożka',
 'Grottgera A.':                        'Artura Grottgera',
 'Grottgera Artura':                    'Artura Grottgera',
 'A. Locciego':                         'Augustyna Locciego',
 'B. Głowackiego':                      'Bartosza Głowackiego',
 'Głowackiego B.':                      'Bartosza Głowackiego',
 'Głowackiego Bartosza':                'Bartosza Głowackiego',
 'B. Hertza':                           'Benedykta Hertza',
 'Joselewicza':                         'Berka Joselewicza',
 'B. Wapowskiego':                      'Bernarda Wapowskiego',
 'B. Zuga':                             'Bogumiła Zuga',
 'Boh. Stalingradu':                    'Bohaterów Stalingradu',
 'Boh. Warszawy':                       'Bohaterów Warszawy',
 'B. Chrobrego':                        'Bolesława Chrobrego',
 'Chrobrego B.':                        'Bolesława Chrobrego',
 'Chrobrego':                           'Bolesława Chrobrego',
 'Domańskiego Bolesława':               'Bolesława Domańskiego',
 'Leśmiana B.':                         'Bolesława Leśmiana',
 'Limanowskiego B.':                    'Bolesława Limanowskiego',
 'Limanowskiego Bolesława':             'Bolesława Limanowskiego',
 'Limanowskiego':                       'Bolesława Limanowskiego',
 'Prusa B.':                            'Bolesława Prusa',
 'Prusa Bolesława':                     'Bolesława Prusa',
 'Prusa':                               'Bolesława Prusa',
 'B. Pietraszewicza "Lota"':            'Bronisława "Lota" Pietraszewicza',
 'B. Bartóka':                          'Béli Bartóka',
 'C. Śniegockiej':                      'Cecylii Śniegockiej',
 'Ch. Botewa':                          'Christa Botewa',
 'Cieślaka W.':                         'Cieślaka W.',
 'C. Godebskiego':                      'Cypriana Godebskiego',
 'Cypriana Norwida':                    'Cypriana Kamila Norwida',
 'Norwida C. K. ':                      'Cypriana Kamila Norwida',
 'Norwida C.K.':                        'Cypriana Kamila Norwida',
 'Norwida Cypriana':                    'Cypriana Kamila Norwida',
 'Norwida':                             'Cypriana Kamila Norwida',
 'Domina Czesława':                     'Czesława Domina',
 'Cz. Kłosia':                          'Czesława Kłosia',
 'Miłosza C.':                          'Czesława Miłosza',
 'Miłosza Cz.':                         'Czesława Miłosza',
 'pl. C. Niemena':                      'Czesława Niemena',
 'Cz. Przybylskiego':                   'Czesława Przybylskiego',
 'Matusewicz G. dr':                    'Doktor Genowefy Matusewicz',
 'Korczaka J. dr':                      'Doktora Janusza Korczaka',
 'D. Merliniego':                       'Dominika Merliniego',
 'D. Mendelejewa':                      'Dymitra Mendelejewa',
 'E. J. Osmańczyka':                    'Edmunda Jana Osmańczyka',
 'Łopuskiego Edmunda':                  'Edmunda Łopuskiego',
 'E. Dembowskiego':                     'Edwarda Dembowskiego',
 'E. Gibalskiego':                      'Edwarda Gibalskiego',
 'E. Jelinka':                          'Edwarda Jelinka',
 'E. J. Abramowskiego':                 'Edwarda Józefa Abramowskiego',
 'E. Warchałowskiego':                  'Edwarda Warchałowskiego',
 'E. Schroegera':                       'Efraima Schroegera',
 'Orzeszkowej E.':                      'Elizy Orzeszkowej',
 'Orzeszkowej':                         'Elizy Orzeszkowej',
 'E. Barszczewskiej':                   'Elżbiety Barszczewskiej',
 'E. Ringelbluma':                      'Emanuela Ringelbluma',
 'E. Gierczak':                         'Emilii Gierczak',
 'Gierczak Emilii':                     'Emilii Gierczak',
 'E. Plater':                           'Emilii Plater',
 'Plater E.':                           'Emilii Plater',
 'E. Ciołka':                           'Erazma Ciołka',
 'E. Malinowskiego':                    'Ernesta Malinowskiego',
 'E. Bocheńskiego "Dubańca"':           'Eugeniusza Bocheńskiego "Dubańca"',
 'E. Bodo':                             'Eugeniusza Bodo',
 'Kwiatkowskiego Eugeniusza':           'Eugeniusza Kwiatkowskiego',
 'E. Lokajskiego':                      'Eugeniusza Lokajskiego',
 'E. Romera':                           'Eugeniusza Romera',
 'E. Szwankowskiego':                   'Eugeniusza Szwankowskiego',
 'E. Tyszkiewicza':                     'Eustachego Tyszkiewicza',
 'Szelburg-Zarembiny Ewy':              'Ewy Szelburg-Zarembiny',
 'Nowowiejskiego Feliksa':              'Feliksa Nowowiejskiego',
 'F. Pancera':                          'Feliksa Pancera',
 'Ruszczyca Ferdynanda':                'Ferdynanda Ruszczyca',
 'F. Płaskowickiej':                    'Filipiny Płaskowickiej',
 'F. Marciniaka':                       'Floriana Marciniaka',
 'Szarego F.':                          'Floriana Szarego',
 'F. Nulla':                            'Francesca Nullo',
 'F. A. Achera':                        'Franciszka Adolfa Achera',
 'F. Bartoszka':                        'Franciszka Bartoszka',
 'F. Hynka':                            'Franciszka Hynka',
 'F. Ilskiego':                         'Franciszka Ilskiego',
 'F. Kawy':                             'Franciszka Kawy',
 'F. Klimczaka':                        'Franciszka Klimczaka',
 'F. Kostrzewskiego':                   'Franciszka Kostrzewskiego',
 'F. M. Lanciego':                      'Franciszka Marii Lanciego',
 'F. Raszei':                           'Franciszka Raszei',
 'Ratajczaka Franciszka':               'Franciszka Ratajczaka',
 'F. Rymkiewicza':                      'Franciszka Rymkiewicza',
 'F. S. Jezierskiego':                  'Franciszka Salezego Jezierskiego',
 'F. Szuberta':                         'Franciszka Szuberta',
 'Zubrzyckiego Franciszka':             'Franciszka Zubrzyckiego',
 'F. Łukaszczyka':                      'Franciszka Łukaszczyka',
 'Roosevelta':                          'Franklina Delano Roosevelta',
 'Chopina F.':                          'Fryderyka Chopina',
 'Chopina Fryderyka':                   'Fryderyka Chopina',
 'Chopina':                             'Fryderyka Chopina',
 'F. Szopena':                          'Fryderyka Chopina',
 'F. Joliot-Curie':                     'Fryderyka Joliot-Curie',
 'G. Narutowicza':                      'Gabriela Narutowicza',
 'Narutowicza G.':                      'Gabriela Narutowicza',
 'Narutowicza Gabriela':                'Gabriela Narutowicza',
 'Narutowicza':                         'Gabriela Narutowicza',
 'G. P. Boduena':                       'Gabriela Piotra Boduena',
 'Zapolskiej G.':                       'Gabrieli Zapolskiej',
 'Zapolskiej':                          'Gabrieli Zapolskiej',
 'gen. F. S. Składkowskiego':           'Generała Felicjana Sławoja Składkowskiego',
 'Gen. Jerzego Ziętka':                 'Generała Jerzego Ziętka',
 'gen. Józefa Bema':                    'Generała Józefa Bema',
 'Wybickiego J. gen.':                  'Generała Józefa Wybickiego',
 'gen. K. Ziemskiego "Wachnowskiego"':  'Generała Karola Ziemskiego Wachnowskiego',
 'Świerczewskiego K. gen.':             'Generała Karola Świerczewskiego',
 'Świerczewskiego K.gen.':              'Generała Karola Świerczewskiego',
 'gen. K. Sosnkowskiego':               'Generała Kazimierza Sosnkowskiego',
 'Okulickiego Niedźwiadka L. gen.':     'Generała Leopolda Okulickiego Niedźwiadka',
 'gen. L. Rayskiego':                   'Generała Ludomiła Rayskiego',
 'M. Zaruskiego':                       'Generała Mariusza Zaruskiego',
 'gen. M. C. Coopera':                  'Generała Meriana Caldwella Coopera',
 'Żymierskiego':                        'Generała Michała Roli-Żymierskiego',
 'Tokarzewskiego-Karaszewicza Torwida M. gen.': 'Generała Michała Tadeusz Tokarzewskiego-Karaszewicza Torwida',
 'gen. M. Tokarzewskiego-Karaszewicza': 'Generała Michała Tokarzewskiego-Karaszewicza',
 'S. Rostworowskiego':                  'Generała Stanisława Rostworowskiego',
 'Skalskiego':                          'Generała Stanisława Skalskiego',
 'gen. S. Kaliskiego':                  'Generała Sylwestra Kaliskiego',
 'Bora-Komorowskiego T. gen.':          'Generała Tadeusza Bora-Komorowskiego',
 'Kościuszki T. gen.':                  'Generała Tadeusza Kościuszki',
 'gen. T. Pełczyńskiego':               'Generała Tadeusza Pełczyńskiego',
 'gen. W. Czumy':                       'Generała Waleriana Czumy',
 'Gen. Władysława Andersa':             'Generała Władysława Andersa',
 'Gen. Władysława Sikorskiego':         'Generała Władysława Sikorskiego',
 'Sikorskiego W. gen.':                 'Generała Władysława Sikorskiego',
 'Sikorskiego W.':                      'Generała Władysława Sikorskiego',
 'Sikorskiego Władysława':              'Generała Władysława Sikorskiego',
 'Sikorskiego':                         'Generała Władysława Sikorskiego',
 'gen. W. Sikorskiego':                 'Generała Władysława Sikorskiego',
 'gen. Władysława Sikorskiego':         'Generała Władysława Sikorskiego',
 'Grota Roweckiego S. gen.':            'Gererała Stefana Grota Roweckiego',
 'Grota-Roweckiego S. gen.':            'Gererała Stefana Grota Roweckiego',
 'gen. Grota Roweckiego':               'Gererała Stefana Grota Roweckiego',
 'G. Rossiniego':                       'Gioacchino Rossiniego',
 'G. Leibniza':                         'Gottfrieda Leibniza',
 'G. Daimlera':                         'Gottlieba Daimlera',
 'Bojara-Fijałkowskiego Gracjana':      'Gracjana Bojara-Fijałkowskiego',
 'G. Bacewiczówny':                     'Grażyny Bacewiczówny',
 'Fitelberga':                          'Grzegorza Fitelberga',
 'G. Daniłowskiego':                    'Gustawa Daniłowskiego',
 'G. Morcinka':                         'Gustawa Morcinka',
 'Morcinka G.':                         'Gustawa Morcinka',
 'Morcinka Gustawa':                    'Gustawa Morcinka',
 'Morcinka':                            'Gustawa Morcinka',
 'Poświatowskiej H.':                   'Haliny Poświatowskiej',
 'H. Czaki':                            'Hanki Czaki',
 'H. Ordonówny':                        'Hanki Ordonówny',
 'Sawickiej H.':                        'Hanki Sawickiej',
 'Sawickiej Hanki':                     'Hanki Sawickiej',
 'H. Ch. Andersena':                    'Hansa Christiana Andersena',
 'H. Krahelskiej':                      'Heleny Krahelskiej',
 'Modrzejewskiej Heleny':               'Heleny Modrzejewskiej',
 'H. Dembińskiego':                     'Henryka Dembińskiego',
 'Jagoszewskiego Henryka':              'Henryka Jagoszewskiego',
 'Jordana Henryka':                     'Henryka Jordana',
 'H. Melcera-Szczawińskiego':           'Henryka Melcera-Szczawińskiego',
 'H. Opieńskiego':                      'Henryka Opieńskiego',
 'Pobożnego H.':                        'Henryka Pobożnego',
 'H. Raabego':                          'Henryka Raabego',
 'H. Rodakowskiego':                    'Henryka Rodakowskiego',
 'Sienkiewicza H.':                     'Henryka Sienkiewicza',
 'Sienkiewicza Henryka':                'Henryka Sienkiewicza',
 'Sienkiewicza':                        'Henryka Sienkiewicza',
 'H. Sternhela':                        'Henryka Sternhela',
 'Sucharskiego Henryka':                'Henryka Sucharskiego',
 'Wieniawskiego Henryka':               'Henryka Wieniawskiego',
 'Wieniawskiego':                       'Henryka Wieniawskiego',
 'H. Wierzchowskiego':                  'Henryka Wierzchowskiego',
 'H. Łasaka':                           'Henryka Łasaka',
 'H. Billewicza':                       'Herakliusza Billewicza',
 'H. Wawelberga':                       'Hipolita Wawelberga',
 'Kołłątaja H.':                        'Hugona Kołłątaja',
 'Kołłątaja Hugo':                      'Hugona Kołłątaja',
 'Kołłątaja':                           'Hugona Kołłątaja',
 'I Armii W.P.' :                       'I Armii Wojska Polskiego',
 'I. L. Pereca':                        'Icchoka Lejba Pereca',
 'Chrzanowskiego Ignacego':             'Ignacego Chrzanowskiego',
 'Daszyńskiego I.':                     'Ignacego Daszyńskiego',
 'Daszyńskiego':                        'Ignacego Daszyńskiego',
 'I. Paderewskiego':                    'Ignacego Jana Paderewskiego',
 'Paderewskiego Ignacego Jana':         'Ignacego Jana Paderewskiego',
 'Paderewskiego Ignacego':              'Ignacego Jana Paderewskiego',
 'Paderewskiego':                       'Ignacego Jana Paderewskiego',
 'I. Krasickiego':                      'Ignacego Krasickiego',
 'Kuczkowskiego Ignacego':              'Ignacego Kuczkowskiego',
 'Rzeckiego I.':                        'Ignacego Rzeckiego',
 'Rzeckiego':                           'Ignacego Rzeckiego',
 'Łukasiewicza I.':                     'Ignacego Łukasiewicza',
 'Łukasiewicza Ignacego':               'Ignacego Łukasiewicza',
 'I. Gandhi':                           'Indiry Gandhi',
 'Łęckiej':                             'Izabeli Łęckiej',
 'Maćkowicza Izydora':                  'Izydora Maćkowicza',
 'Malczewskiego J.':                    'Jacka Malczewskiego',
 'Malczewskiego Jacka':                 'Jacka Malczewskiego',
 'Soplicy J.':                          'Jacka Soplicy',
 'Jelec Jadwigi':                       'Jadwigi Jelec',
 'J. Smosarskiej':                      'Jadwigi Smosarskiej',
 'J. Mortkowicza':                      'Jakuba Mortkowicza',
 'Wejhera Jakuba':                      'Jakuba Wejhera',
 'J. G. Bennetta':                      'Jamesa Gordona Bennetta',
 'Baczewskiego Jana':                   'Jana Baczewskiego',
 'Bauera Jana':                         'Jana Bauera',
 'J. Blatona':                          'Jana Blatona',
 'J. Brożka':                           'Jana Brożka',
 'Brzechwy J.':                         'Jana Brzechwy',
 'Brzechwy Jana':                       'Jana Brzechwy',
 'Brzechwy':                            'Jana Brzechwy',
 'J. Bułhaka':                          'Jana Bułhaka',
 'Chodkiewicza Jana':                   'Jana Chodkiewicza',
 'J. Cybisa':                           'Jana Cybisa',
 'Długosza J.':                         'Jana Długosza',
 'Długosza':                            'Jana Długosza',
 'J. Długosza':                         'Jana Długosza',
 'J. F. Piwarskiego':                   'Jana Feliksa Piwarskiego',
 'Frankowskiego Jana':                  'Jana Frankowskiego',
 'Derdowskiego':                        'Jana Hieronima Derdowskiego',
 'J. Husa':                             'Jana Husa',
 'J. Jeziorańskiego':                   'Jana Jeziorańskiego',
 'J. K. Chodkiewicza':                  'Jana Karola Chodkiewicza',
 'J. Kasprowicza':                      'Jana Kasprowicza',
 'Kasprowicza J.':                      'Jana Kasprowicza',
 'Kasprowicza Jana':                    'Jana Kasprowicza',
 'Kasprowicza':                         'Jana Kasprowicza',
 'Kiepury':                             'Jana Kiepury',
 'J. Kilińskiego':                      'Jana Kilińskiego',
 'Kilińskiego J.':                      'Jana Kilińskiego',
 'Kilińskiego Jana':                    'Jana Kilińskiego',
 'Kilińskiego':                         'Jana Kilińskiego',
 'J. Kochanowskiego':                   'Jana Kochanowskiego',
 'Kochanowskiego J.':                   'Jana Kochanowskiego',
 'Kochanowskiego Jana':                 'Jana Kochanowskiego',
 'Kochanowskiego':                      'Jana Kochanowskiego',
 'J. Kossakowskiego':                   'Jana Kossakowskiego',
 'J. Kozietulskiego':                   'Jana Kozietulskiego',
 'J. Krysta':                           'Jana Krysta',
 'J. Maklakiewicza':                    'Jana Maklakiewicza',
 'J. M. Szancera':                      'Jana Marcina Szancera',
 'Matejki ':                            'Jana Matejki',
 'Matejki J.':                          'Jana Matejki',
 'Matejki Jana':                        'Jana Matejki',
 'Matejki':                             'Jana Matejki',
 'J. Miklaszewskiego':                  'Jana Miklaszewskiego',
 'J. Ostroroga':                        'Jana Ostroroga',
 'J. P. Woronicza':                     'Jana Pawła Woronicza',
 'J. Piekałkiewicza':                   'Jana Piekałkiewicza',
 'J. Rosoła':                           'Jana Rosoła',
 'Sabały':                              'Jana Sabały',
 'Skrzetuskiego J.':                    'Jana Skrzetuskiego',
 'Skrzetuskiego Jana':                  'Jana Skrzetuskiego',
 'S. J. Jabłonowskiego':                'Jana Stanisława Jabłonowskiego',
 'J. Szczepanika':                      'Jana Szczepanika',
 'J. Szymczaka':                        'Jana Szymczaka',
 'Tarnowskiego Jana':                   'Jana Tarnowskiego',
 'J. Wasilkowskiego':                   'Jana Wasilkowskiego',
 'J. Zaorskiego':                       'Jana Zaorskiego',
 'J. Skrzyneckiego':                    'Jana Zygmunta Skrzyneckiego',
 'J. Żabińskiego':                      'Jana Żabińskiego',
 'J. Żiżki':                            'Jana Żiżki',
 'Jankiel':                             'Jankiela',
 'Korczaka Janusza':                    'Janusza Korczaka',
 'Korczaka':                            'Janusza Korczaka',
 'Kusocińskiego J.':                    'Janusza Kusocińskiego',
 'Dąbrowskiego J.':                     'Jarosława Dąbrowskiego',
 'Dąbrowskiego Jarosława':              'Jarosława Dąbrowskiego',
 'J. Dąbrowskiego':                     'Jarosława Dąbrowskiego',
 'Iwaszkiewicza J.':                    'Jarosława Iwaszkiewicza',
 'J. Bajana':                           'Jerzego Bajana',
 'Fitio Jerzego':                       'Jerzego Fitio',
 'J. Iwanowa-Szajnowicza':              'Jerzego Iwanowa-Szajnowicza',
 'Kostenckiego Jerzego':                'Jerzego Kostenckiego',
 'J. Kukuczki':                         'Jerzego Kukuczki',
 'J. Michałowicza':                     'Jerzego Michałowicza',
 'Popiełuszki Jerzego':                 'Jerzego Popiełuszki',
 'J. Waldorffa':                        'Jerzego Waldorffa',
 'Waszyngtona Jerzego':                 'Jerzego Waszyngtona',
 'J. Zaruby':                           'Jerzego Zaruby',
 'J. i W. Włoczewskich':                'Jerzego i Władysławy Włoczewskich',
 'Lelewela Joachima':                   'Joachima Lelewela',
 'Conrada Korzeniowskiego Josepha':     'Josepha Conrada Korzeniowskiego',
 'J. Conrada':                          'Josepha Conrada',
 'J. Bartoszewicza':                    'Juliana Bartoszewicza',
 'J. Bruna':                            'Juliana Bruna',
 'Fałata Juliana':                      'Juliana Fałata',
 'Krzyżanowskiego Juliana':             'Juliana Krzyżanowskiego',
 'J. Kulskiego':                        'Juliana Kulskiego',
 'Ordona J.':                           'Juliana Ordona',
 'Tuwima J.':                           'Juliana Tuwima',
 'Tuwima Juliana':                      'Juliana Tuwima',
 'Tuwima':                              'Juliana Tuwima',
 'Niemcewicza':                         'Juliana Ursyna Niemcewicza',
 'J. Kaden-Bandrowskiego':              'Juliusza Kaden-Bandrowskiego',
 'J. K. Ordona':                        'Juliusza Konstantego Ordona',
 'Kossaka Juliusza':                    'Juliusza Kossaka',
 'J. Osterwy':                          'Juliusza Osterwy',
 'Słowackiego J.':                      'Juliusza Słowackiego',
 'Słowackiego Juliusza':                'Juliusza Słowackiego',
 'Słowackiego':                         'Juliusza Słowackiego',
 'J. Bellottiego':                      'Józefa Bellottiego',
 'Bema Józefa':                         'Józefa Bema',
 'Bema':                                'Józefa Bema',
 'Chełmońskiego J.':                    'Józefa Chełmońskiego',
 'Chełmońskiego Józefa':                'Józefa Chełmońskiego',
 'J. Czechowicza':                      'Józefa Czechowicza',
 'J. Dwernickiego':                     'Józefa Dwernickiego',
 'J. F. Ciszewskiego':                  'Józefa Feliksa Ciszewskiego',
 'J. Chłopickiego':                     'Józefa Grzegorza Chłopickiego',
 'J. Hauke-Bosaka':                     'Józefa Hauke-Bosaka',
 'Krasickiego Ignacego':                'Józefa Ignacego Krasickiego',
 'Krasickiego':                         'Józefa Ignacego Krasickiego',
 'J. I. Kraszewskiego':                 'Józefa Ignacego Kraszewskiego',
 'Kraszewskiego J. I.':                 'Józefa Ignacego Kraszewskiego',
 'Kraszewskiego':                       'Józefa Ignacego Kraszewskiego',
 'Kromera J.':                          'Józefa Kromera',
 'J. Lewartowskiego':                   'Józefa Lewartowskiego',
 'J. Mehoffera':                        'Józefa Mehoffera',
 'Mireckiego Józefa':                   'Józefa Mireckiego',
 'Piłsudskiego J.':                     'Józefa Piłsudskiego',
 'Piłsudskiego Józefa':                 'Józefa Piłsudskiego',
 'Piłsudskiego':                        'Józefa Piłsudskiego',
 'Poniatowskiego J.':                   'Józefa Poniatowskiego',
 'J. Sowińskiego':                      'Józefa Sowińskiego',
 'Sowińskiego Józefa':                  'Józefa Sowińskiego',
 'J. Strusia':                          'Józefa Strusia',
 'J. Sułkowskiego':                     'Józefa Sułkowskiego',
 'J. Szymańskiego':                     'Józefa Szymańskiego',
 'J. Wybickiego':                       'Józefa Wybickiego',
 'Wybickiego Józefa':                   'Józefa Wybickiego',
 'Wybickiego':                          'Józefa Wybickiego',
 'Śliwińskiego Józefa':                 'Józefa Śliwińskiego',
 'K. Karlińskiego':                     'Kacpra Karlińskiego',
 'K. Garbińskiego':                     'Kajetana Garbińskiego',
 'K. Sołtyka':                          'Kajetana Sołtyka',
 'K. Jędrusik':                         'Kaliny Jędrusik',
 'kpt. W. Raginisa':                    'Kapitana Władysława Raginisa',
 'Wyszyńskiego S. kard.':               'Kardynała Stefana Wyszyńskiego',
 'Wyszyńskiego S.':                     'Kardynała Stefana Wyszyńskiego',
 'Wyszyńskiego kard.':                  'Kardynała Stefana Wyszyńskiego',
 'Chodkiewicza Karola':                 'Karola Chodkiewicza',
 'Chodkiewicza':                        'Karola Chodkiewicza',
 'K. Irzykowskiego':                    'Karola Irzykowskiego',
 'Kurpińskiego Karola':                 'Karola Kurpińskiego',
 'Miarki K.':                           'Karola Miarki',
 'Szymanowskiego Karola':               'Karola Szymanowskiego',
 'Szymanowskiego':                      'Karola Szymanowskiego',
 'Świerczewskiego':                     'Karola Świerczewskiego',
 'K. Gierdziejewskiego':                'Kazimierza Gierdziejewskiego',
 'Jurkiewicza Kazimierza':              'Kazimierza Jurkiewicza',
 'K. Karasia':                          'Kazimierza Karasia',
 'K. Króla':                            'Kazimierza Króla',
 'K. Kuratowskiego':                    'Kazimierza Kuratowskiego',
 'K. Promyka':                          'Kazimierza Promyka',
 'Przerwy-Tetmajera K.':                'Kazimierza Przerwy-Tetmajera',
 'K. Pułaskiego':                       'Kazimierza Pułaskiego',
 'Pułaskiego K.':                       'Kazimierza Pułaskiego',
 'Pułaskiego':                          'Kazimierza Pułaskiego',
 'K. Siemienowicza':                    'Kazimierza Siemienowicza',
 'K. Sotta "Sokoła"':                   'Kazimierza Sotta "Sokoła"',
 'K. Szałasa':                          'Kazimierza Szałasa',
 'K. Szpotańskiego':                    'Kazimierza Szpotańskiego',
 'Tetmajera Kazimierza':                'Kazimierza Tetmajera',
 'Tetmajera':                           'Kazimierza Tetmajera',
 'K. Wyki':                             'Kazimierza Wyki',
 'Wyki Kazimierza':                     'Kazimierza Wyki',
 'K. Wóycickiego':                      'Kazimierza Wóycickiego',
 'Górskiego Klaudiusza':                'Klaudiusza Górskiego',
 '"Wira" Bartoszewskiego':              'Konrada "Wira" Bartoszewskiego',
 'Wallenroda K.':                       'Konrada Wallenroda',
 'Ciołkowskiego':                       'Konstantego Ciołkowskiego',
 'Gałczyńskiego K. I. ':                'Konstantego Ildefonsa Gałczyńskiego',
 'Gałczyńskiego Konstantego Ildefonsa': 'Konstantego Ildefonsa Gałczyńskiego',
 'Gałczyńskiego':                       'Konstantego Ildefonsa Gałczyńskiego',
 'Maciejewicza Konstantego':            'Konstantego Maciejewicza',
 'Makuszyńskiego Kornela':              'Kornela Makuszyńskiego',
 'Arciszewskiego Krzysztofa':           'Krzysztofa  Arciszewskiego',
 'Baczyńskiego K. K.':                  'Krzysztofa Kamila Baczyńskiego',
 'Baczyńskiego' :                       'Krzysztofa Kamila Baczyńskiego',
 'K. Kieślowskiego':                    'Krzysztofa Kieślowskiego',
 'K. Kolumba':                          'Krzysztofa Kolumba',
 'Kolumba Krzysztofa':                  'Krzysztofa Kolumba',
 'Bony':                                'Królowej Bony',
 'Kr. Jadwigi':                         'Królowej Jadwigi',
 'K. Bronikowskiego':                   'Ksawerego Bronikowskiego',
 'Dunikowskiego K.':                    'Ksawerego Dunikowskiego',
 'Sanguszki A. ks.':                    'Księcia Andrzeja Sanguszki',
 'ks. Adama Opalskiego':                'Księdza Adama Opalskiego',
 'Waresiaka E. Ks.':                    'Księdza Eugeniusza Waresiaka',
 'ks. I. Skorupki':                     'Księdza Ignacego Jana Skorupki',
 'Abramskiego J. ks.':                  'Księdza Jana Abramskiego',
 'ks. J. Sitnika':                      'Księdza Jana Sitnika',
 'Ks. Jana Twardowskiego':              'Księdza Jana Twardowskiego',
 'ks. J. Popiełuszki':                  'Księdza Jerzego Popiełuszki',
 'ks. J. Chrościckiego':                'Księdza Juliana Chrościckiego',
 'Dąbrowskiego J. Ks.':                 'Księdza Józefa Dąbrowskiego',
 'ks. J. Iwaniuka':                     'Księdza Józefa Iwaniuka',
 'ks. Józefa Kuropieski':               'Księdza Józefa Kuropieski',
 'ks. K. Czarkowskiego':                'Księdza Kazimierza Czarkowskiego',
 'ks. P. Skargi':                       'Księdza Piotra Skargi',
 'Prymasa A. Hlonda':                   'Księdza Prymasa Augusta Hlonda',
 'Struka Księdza':                      'Księdza Struka',
 'ks. S. Szulczyka':                    'Księdza Sylwestra Szulczyka',
 'ks. T. Boguckiego':                   'Księdza Teofila Boguckiego',
 'Ks. Elżbiety':                        'Księżnej Elżbiety',
 'L. Kossutha':                         'Lajosa Kossutha',
 'L. Berensona':                        'Leona Berensona',
 'Kruczkowskiego L.':                   'Leona Kruczkowskiego',
 'Kruczkowskiego':                      'Leona Kruczkowskiego',
 'L. Kruczkowskiego':                   'Leona Kruczkowskiego',
 'Wyczółkowskiego Leona':               'Leona Wyczółkowskiego',
 'Teligi Leonida':                      'Leonida Teligi',
 'Teligi':                              'Leonida Teligi',
 'Okulickiego Leopolda':                'Leopolda Okulickiego',
 'L. Staffa':                           'Leopolda Staffa',
 'Staffa Leopolda':                     'Leopolda Staffa',
 'Staffa':                              'Leopolda Staffa',
 'L. Rudnickiego':                      'Lucjana Rudnickiego',
 'Szenwalda Lucjana':                   'Lucjana Szenwalda',
 'L. Messal':                           'Lucyny Messal',
 'Różyckiego Ludomira':                 'Ludomira Różyckiego',
 'Hirszfelda L.':                       'Ludwika Hirszfelda',
 'L. Hirszfelda':                       'Ludwika Hirszfelda',
 'L. Kondratowicza':                    'Ludwika Kondratowicza',
 'L. Mierosławskiego':                  'Ludwika Mierosławskiego',
 'Mierosławskiego':                     'Ludwika Mierosławskiego',
 'L. Nabielaka':                        'Ludwika Nabielaka',
 'L. Narbutta':                         'Ludwika Narbutta',
 'L. Rydygiera':                        'Ludwika Rydygiera',
 'L. Waryńskiego':                      'Ludwika Waryńskiego',
 'Waryńskiego L.':                      'Ludwika Waryńskiego',
 'Waryńskiego Ludwika':                 'Ludwika Waryńskiego',
 'Waryńskiego':                         'Ludwika Waryńskiego',
 'Zamenhofa Ludwika':                   'Ludwika Zamenhofa',
 'M. Kamieńskiego':                     'Macieja Kamieńskiego',
 'M. Rataja':                           'Macieja Rataja',
 'Rataja M.':                           'Macieja Rataja',
 'M. Sarbiewskiego':                    'Macieja Sarbiewskiego',
 'M. Gandhiego':                        'Mahatmy Gandhiego',
 'mjr. F. M. Amałowicza "Tatara"':      'Majora Franciszka Amałowicza',
 'H. Dobrzańskiego "Hubala"':           'Majora Henryka "Hubala" Dobrzańskiego',
 'Sucharskiego':                        'Majora Henryka Sucharskiego',
 'mjr. Sucharskiego':                   'Majora Henryka Sucharskiego',
 'mjr. Romana Bielawskiego':            'Majora Romana Bielawskiego',
 'Golisza Maksymiliana':                'Maksymiliana Golisza',
 'Grochowskiego Maksymiliana':          'Maksymiliana Grochowskiego',
 'Stankiewicza Mamerta':                'Mamerta Stankiewicza',
 'Nowotki M.':                          'Marcelego Nowotki',
 'Nowotki':                             'Marcelego Nowotki',
 'Borzymowskiego Marcina':              'Marcina Borzymowskiego',
 'Kasprzaka':                           'Marcina Kasprzaka',
 'M. Kasprzaka':                        'Marcina Kasprzaka',
 'M. Kątskiego':                        'Marcina Kątskiego',
 'Buczka M.':                           'Mariana Buczka',
 'Buczka':                              'Mariana Buczka',
 'M. Falskiego':                        'Mariana Falskiego',
 'M. Keniga':                           'Mariana Keniga',
 'M. Krawczyka':                        'Mariana Krawczyka',
 'M. Sengera "Cichego"':                'Mariana Sengera "Cichego"',
 'M. Smoluchowskiego':                  'Mariana Smoluchowskiego',
 'M. Wyrzykowskiego':                   'Mariana Wyrzykowskiego',
 'Dąbrowskiej M.':                      'Marii Dąbrowskiej',
 'Dąbrowskiej':                         'Marii Dąbrowskiej',
 'Konopnickiej M.':                     'Marii Konopnickiej',
 'Konopnickiej Marii':                  'Marii Konopnickiej',
 'Konopnickiej':                        'Marii Konopnickiej',
 'M. Konopnickiej':                     'Marii Konopnickiej',
 'Gąszczak Marii Magdaleny':            'Marii Magdaleny Gąszczak',
 'M. Pawlikowskiej-Jasnorzewskiej':     'Marii Pawlikowskiej-Jasnorzewskiej',
 'M. Rodziewiczówny':                   'Marii Rodziewiczówny',
 'Rodziewiczówny Marii':                'Marii Rodziewiczówny',
 'Curie-Skłodowskiej':                  'Marii Skłodowskiej-Curie',
 'Skłodowskiej':                        'Marii Skłodowskiej-Curie',
 'Skłodowskiej- Curie M.':              'Marii Skłodowskiej-Curie',
 'Skłodowskiej-Curie M.':               'Marii Skłodowskiej-Curie',
 'Skłodowskiej-Curie Marii':            'Marii Skłodowskiej-Curie',
 'Skłodowskiej-Curie':                  'Marii Skłodowskiej-Curie',
 'Zaruskiego Mariusza':                 'Mariusza Zaruskiego',
 'Piłsudskiego J. Marsz.':              'Marszałka Józefa Piłsudskiego',
 'Piłsudskiego J. marsz.':              'Marszałka Józefa Piłsudskiego',
 'Piłsudskiego Marszałka':              'Marszałka Józefa Piłsudskiego',
 'Roli-Żymierskiego M. marsz.':         'Marszałka Michała Roli-Żymierskiego',
 'Kinga Martina':                       'Martina Kinga',
 'Fornalskiej':                         'Małgorzaty Fornalskiej',
 'Wańkowicza Melchiora':                'Melchiora Wańkowicza',
 'Drzymały M.':                         'Michała Drzymały',
 'Drzymały Michała':                    'Michała Drzymały',
 'M. Drzymały':                         'Michała Drzymały',
 'Kajki Michała':                       'Michała Kajki',
 'Kajki':                               'Michała Kajki',
 'M. Kajki':                            'Michała Kajki',
 'M. K. Ogińskiego':                    'Michała Kleofasa Ogińskiego',
 'Ogińskiego Michała Kleofasa':         'Michała Kleofasa Ogińskiego',
 'Ogińskiego Michała':                  'Michała Kleofasa Ogińskiego',
 'M. Oczapowskiego':                    'Michała Oczapowskiego',
 'M. Okurzałego':                       'Michała Okurzałego',
 'M. Ossowskiego':                      'Michała Ossowskiego',
 'M. Spisaka':                          'Michała Spisaka',
 'Wołodyjowskiego Michała':             'Michała Wołodyjowskiego',
 'Żebrowskiego Michała':                'Michała Żebrowskiego',
 'M. Fersta':                           'Mieczysława Fersta',
 'M. Frenkla':                          'Mieczysława Frenkla',
 'Karłowicza Mieczysława':              'Mieczysława Karłowicza',
 'Karłowicza':                          'Mieczysława Karłowicza',
 'M. Niedziałkowskiego':                'Mieczysława Niedziałkowskiego',
 'Niedziałkowskiego':                   'Mieczysława Niedziałkowskiego',
 'płk. M. Niedzielskiego „Żywiciela”':  'Mieczysława Niedzielskiego "Żywiciela"',
 'M. Orłowicza':                        'Mieczysława Orłowicza',
 'M. Pożaryskiego':                     'Mieczysława Pożaryskiego',
 'Kopernika M.':                        'Mikołaja Kopernika',
 'Kopernika Mikołaja':                  'Mikołaja Kopernika',
 'Kopernika':                           'Mikołaja Kopernika',
 'M. Kopernika':                        'Mikołaja Kopernika',
 'N. Paganiniego':                      'Mikołaja Paganiniego',
 'Reja M.':                             'Mikołaja Reja',
 'Reja Mikołaja':                       'Mikołaja Reja',
 'Reja':                                'Mikołaja Reja',
 'M. Trąby':                            'Mikołaja Trąby',
 'M. Wierzynka':                        'Mikołaja Wierzynka',
 'M. Anielewicza':                      'Mordechaja Anielewicza',
 'Meczenników Unickich':                'Męczenników Unickich',
 'N. Gąsiorowskiej':                    'Natalii Gąsiorowskiej',
 'Barlickiego Norberta':                'Norberta Barlickiego',
 'Barlickiego':                         'Norberta Barlickiego',
 'O. Boznańskiej':                      'Olgi Boznańskiej',
 'os. Przyjaźń':                        'Osiedle Przyjaźń',
 'Lange Oskara':                        'Oskara Lange',
 'O. Sosnowskiego':                     'Oskara Sosnowskiego',
 'P. Nurmiego':                         'Paavo Nurmiego',
 'P. Nerudy':                           'Pabla Nerudy',
 'Nerudy Pablo':                        'Pablo Nerudy',
 'Picassa Pablo':                       'Pablo Picassa',
 'P. Suzina':                           'Pawła Suzina',
 'Skargi P.':                           'Piora Skargi',
 'Michałowskiego Piotra':               'Piotra Michałowskiego',
 'Skargi Piotra':                       'Piotra Skargi',
 'P. Wysockiego':                       'Piotra Wysockiego',
 'Ściegiennego Piotra':                 'Piotra Ściegiennego',
 'Plac Czerwca 1976 r.':                'Plac Czerwca 1976 roku',
 'pl. J. Lelewela':                     'Plac Joachima Lelewela',
 'pl. T. W. Wilsona':                   'Plac Thomasa Woodrowa Wilsona',
 'pl. marsz. J. Piłsudskiego':          'Plac marszałka Józefa Piłsudskiego',
 'P. Gojawiczyńskiej':                  'Poli Gojawiczyńskiej',
 'P. Negri':                            'Poli Negri',
 'Powstańców Wlkp.':                    'Powstańców Wielkopolskich',
 'Szafera W. prof.':                    'Profesora Władysława Szafera',
 'Sierpińskiego Z. prof.':              'Profesora Zbigniewa Sierpińskiego',
 'płk. K. Leskiego':                    'Pułkownika Kazimierza Leskiego',
 'płk. W. Łokuciewskiego':              'Pułkownika Witolda Łokuciewskiego',
 'płk. Z. Baló':                        'Pułkownika Zoltána Baló',
 'Dmowskiego Romana':                   'Romana Dmowskiego',
 'R. Maciejewskiego':                   'Romana Maciejewskiego',
 'R. Palestera':                        'Romana Palestera',
 'R. Pazińskiego':                      'Romana Pazińskiego',
 'R. Popiołka':                         'Romana Popiołka',
 'Sierocińskiego Romana':               'Romana Sierocińskiego',
 'R. Statkowskiego':                    'Romana Statkowskiego',
 'R. Gutta':                            'Romualda Gutta',
 'Mielczarskiego':                      'Romualda Mielczarskiego',
 'R. Millera':                          'Romualda Millera',
 'R. Traugutta':                        'Romualda Traugutta',
 'Traugutta R.' :                       'Romualda Traugutta',
 'Traugutta Romualda':                  'Romualda Traugutta',
 'Traugutta':                           'Romualda Traugutta',
 'Rondo I. Daszyńskiego':               'Rondo Ignacego Daszyńskiego',
 'Rondo ONZ':                           'Rondo Organizacji Narodów Zjednoczonych',
 'R. Bailly':                           'Rosy Bailly',
 'rtm. W. Pileckiego':                  'Rotmistrza Witolda Pileckiego',
 'Siennickiego Ryszarda':               'Ryszarda Siennickiego',
 'S. Klonowicza':                       'Sebastiana Fabiana Klonowicza',
 'S. Krzyżanowskiego':                  'Seweryna Krzyżanowskiego',
 'Pieniężnego Seweryna':                'Seweryna Pieniężnego',
 'S. Bolívara':                         'Simona Bolivara',
 'S. Bodycha':                          'Stanisława Bodycha',
 'S. Chudoby':                          'Stanisława Chudoby',
 'Dubois Stanisława':                   'Stanisława Dubois',
 'S. Dygata':                           'Stanisława Dygata',
 'Dąbka Stanisława':                    'Stanisława Dąbka',
 'S. Fiszera':                          'Stanisława Fiszera',
 'S. Grzesiuka':                        'Stanisława Grzesiuka',
 'S. Herbsta':                          'Stanisława Herbsta',
 'S. Hozjusza':                         'Stanisława Hozjusza',
 'S. Jachowicza':                       'Stanisława Jachowicza',
 'S. Kazury':                           'Stanisława Kazury',
 'S. Kierbedzia':                       'Stanisława Kierbedzia',
 'Koniecpolskiego Stanisława':          'Stanisława Koniecpolskiego',
 'S. Kostki Potockiego':                'Stanisława Kostki Potockiego',
 'S. Kulczyńskiego':                    'Stanisława Kulczyńskiego',
 'S. Lentza':                           'Stanisława Lentza',
 'Małachowskiego':                      'Stanisława Małachowskiego',
 'S. Miłkowskiego':                     'Stanisława Miłkowskiego',
 'Moniuszki S.':                        'Stanisława Moniuszki',
 'Moniuszki Stanisława':                'Stanisława Moniuszki',
 'Moniuszki':                           'Stanisława Moniuszki',
 'S. Moniuszki':                        'Stanisława Moniuszki',
 'S. Noakowskiego':                     'Stanisława Noakowskiego',
 'S. Rychlińskiego':                    'Stanisława Rychlińskiego',
 'Staszica S.'  :                       'Stanisława Staszica',
 'Staszica St.':                        'Stanisława Staszica',
 'Staszica Stanisława':                 'Stanisława Staszica',
 'Staszica':                            'Stanisława Staszica',
 'S. Szobera':                          'Stanisława Szobera',
 'S. Worcella':                         'Stanisława Worcella',
 'Wyspiańskiego S.':                    'Stanisława Wyspiańskiego',
 'Wyspiańskiego Stanisława':            'Stanisława Wyspiańskiego',
 'Wyspiańskiego':                       'Stanisława Wyspiańskiego',
 'S. Żaryna':                           'Stanisława Żaryna',
 'Żółkiewskiego Stanisława':            'Stanisława Żółkiewskiego',
 'Walasiewiczówny S.':                  'Stanisławy Walasiewiczówny',
 'S. Bryły':                            'Stefana Bryły',
 'Czarnieckiego S.':                    'Stefana Czarnieckiego',
 'Czarnieckiego Stefana':               'Stefana Czarnieckiego',
 'Czarnieckiego':                       'Stefana Czarnieckiego',
 'S. Czarnieckiego':                    'Stefana Czarnieckiego',
 'S. Dembego':                          'Stefana Dembego',
 'S. Kopcińskiego':                     'Stefana Kopcińskiego',
 'Okrzei S.':                           'Stefana Okrzei',
 'Okrzei St.':                          'Stefana Okrzei',
 'Okrzei Stefana':                      'Stefana Okrzei',
 'Okrzei':                              'Stefana Okrzei',
 'Starzyńskiego Stefana':               'Stefana Starzyńskiego',
 'Wyszyńskiego Stefana':                'Stefana Wyszyńskiego',
 'S. Łyszkiewicza "Pechowca"':          'Stefana Łyszkiewicza "Pechowca"',
 'S. Żeromskiego':                      'Stefana Żeromskiego',
 'Żeromskiego S.':                      'Stefana Żeromskiego',
 'Żeromskiego Stefana':                 'Stefana Żeromskiego',
 'Żeromskiego':                         'Stefana Żeromskiego',
 'Boya Żeleńskiego':                    'Tadeusza Boya-Żeleńskiego',
 'Boya-Żeleńskiego Tadeusza':           'Tadeusza Boya-Żeleńskiego',
 'T. Hennela':                          'Tadeusza Hennela',
 'T. Korzona':                          'Tadeusza Korzona',
 'Kotarbińskiego Tadeusza':             'Tadeusza Kotarbińskiego',
 'Kościuszki T.':                       'Tadeusza Kościuszki',
 'Kościuszki Tadeusza':                 'Tadeusza Kościuszki',
 'Kościuszki':                          'Tadeusza Kościuszki',
 'T. Kościuszki':                       'Tadeusza Kościuszki',
 'T. Kulisiewicza':                     'Tadeusza Kulisiewicza',
 'Kutrzeby Tadeusza':                   'Tadeusza Kutrzeby',
 'Makowskiego Tadeusza':                'Tadeusza Makowskiego',
 'T. Regera':                           'Tadeusza Regera',
 'Rejtana Tadeusza':                    'Tadeusza Rejtana',
 'Rejtana':                             'Tadeusza Rejtana',
 'Sygietyńskiego Tadeusza':             'Tadeusza Sygietyńskiego',
 'T. Duracza':                          'Teodora Duracza',
 'Rafińskiego Teodora':                 'Teodora Rafińskiego',
 'Boguckiego':                          'Teofila Boguckiego',
 'T. Lenartowicza':                     'Teofila Lenartowicza',
 'T. Edisona':                          'Tomasza Edisona',
 'Nocznickiego':                        'Tomasza Nocznickiego',
 'T. Nocznickiego':                     'Tomasza Nocznickiego',
 'Zana T.':                             'Tomasza Zana',
 'Zana':                                'Tomasza Zana',
 'Tysiąclecia PP':                      'Tysiąclecia Państwa Polskiego',
 'Chałubińskiego Tytusa':               'Tytusa Chałubińskiego',
 'Chałubińskiego':                      'Tytusa Chałubińskiego',
 'V. van Gogha':                        'Vincenta van Gogha',
 'W. Berenta':                          'Wacława Berenta',
 'W. Borowego':                         'Wacława Borowego',
 'W. Lachmana':                         'Wacława Lachmana',
 'Sierpińskiego Wacława':               'Wacława Sierpińskiego',
 'W. Tokarza':                          'Wacława Tokarza',
 'W. Wojtyszki':                        'Wacława Wojtyszki',
 'Wróblewskiego Walerego':              'Walerego Wróblewskiego',
 'Łukasińskiego W.':                    'Waleriana Łukasińskiego',
 'Łukasińskiego Waleriana':             'Waleriana Łukasińskiego',
 'Wasilewskiej':                        'Wandy Wasilewskiej',
 'W. Surowieckiego':                    'Wawrzyńca Surowieckiego',
 'Kostrzewy Wery':                      'Wery Kostrzewy',
 'Steffena Wiktora':                    'Wiktora Steffena',
 'W. Kaweckiej':                        'Wiktorii Kaweckiej',
 'W. K. Roentgena':                     'Wilhelma Konrada Roentgena',
 'W. Szekspira':                        'Wiliama Szekspira',
 'Pstrowskiego':                        'Wincentego Pstrowskiego',
 'Witosa W.':                           'Wincentego Witosa',
 'Witosa Wincentego':                   'Wincentego Witosa',
 'Witosa':                              'Wincentego Witosa',
 'Stwosza W.':                          'Wita Stwosza',
 'Dzierżykraja-Morawskiego J. W.':      'Witolda Józefa Dzierżykraja-Morawskiego',
 'Pileckiego Witolda':                  'Witolda Pileckiego',
 'W. B. Jastrzębowskiego':              'Wojciecha Bogumiła Jastrzębowskiego',
 'W. Bogusławskiego':                   'Wojciecha Bogusławskiego',
 'W. Górskiego':                        'Wojciecha Górskiego',
 'Korfantego W.':                       'Wojciecha Korfantego',
 'W. Żywnego':                          'Wojciecha Żywnego',
 'W. A. Mozarta':                       'Wolfganga Amadeusza Mozarta',
 'Andersa Władysława':                  'Władysława Andersa',
 'W. Bandurskiego':                     'Władysława Bandurskiego',
 'W. Bełzy':                            'Władysława Bełzy',
 'W. Bieńczaka':                        'Władysława Bieńczaka',
 'Broniewskiego W.':                    'Władysława Broniewskiego',
 'Broniewskiego Władysława':            'Władysława Broniewskiego',
 'Broniewskiego':                       'Władysława Broniewskiego',
 'W. Broniewskiego':                    'Władysława Broniewskiego',
 'Grabskiego Wł.':                      'Władysława Grabskiego',
 'W. Hassa':                            'Władysława Hassa',
 'W. Hańczy':                           'Władysława Hańczy',
 'Jagiełły W.':                         'Władysława Jagiełły',
 'Jagiełły':                            'Władysława Jagiełły',
 'W. Jagiełły':                         'Władysława Jagiełły',
 'W. J. Grabskiego':                    'Władysława Jana Grabskiego',
 'Kniewskiego Władysława':              'Władysława Kniewskiego',
 'Kniewskiego':                         'Władysława Kniewskiego',
 'Laskonogiego Władysława':             'Władysława Laskonogiego',
 'Orkana W.':                           'Władysława Orkana',
 'Orkana':                              'Władysława Orkana',
 'W. Przanowskiego':                    'Władysława Przanowskiego',
 'W. Pytlasińskiego':                   'Władysława Pytlasińskiego',
 'Reymonta W.':                         'Władysława Reymonta',
 'Reymonta Władysława':                 'Władysława Reymonta',
 'Skoczylasa Władysława':               'Władysława Skoczylasa',
 'W. Smoleńskiego':                     'Władysława Smoleńskiego',
 'Spasowskiego Władysława':             'Władysława Spasowskiego',
 'Reymonta W. S.':                      'Władysława Stanisława Reymonta',
 'Reymonta Władysława Stanisława':      'Władysława Stanisława Reymonta',
 'Reymonta':                            'Władysława Stanisława Reymonta',
 'Syrokomli':                           'Władysława Syrokomli',
 'W. Syrokomli':                        'Władysława Syrokomli',
 'W. Szeflera "Włada"':                 'Władysława Szeflera "Włada"',
 'Tatarkiewicza Władysława':            'Władysława Tatarkiewicza',
 'Turowskiego Władysława':              'Władysława Turowskiego',
 'Łokietka':                            'Władysława Łokietka',
 'W. Perzyńskiego':                     'Włodzimierza Perzyńskiego',
 'Z. Cybulskiego':                      'Zbyszka Cybulskiego',
 'Klemensiewicza Zenona':               'Zenona Klemensiewicza',
 'Z. Klemensiewicza':                   'Zenona Klemensiewicza',
 'Nałkowskiej Z.':                      'Zofii Nałkowskiej',
 'Nałkowskiej':                         'Zofii Nałkowskiej',
 'Stryjeńskiej Z.':                     'Zofii Stryjeńskiej',
 'ZWM':                                 'Związku Walki Młodych ( ZWM )',
 'Z. Jórskiego':                        'Zygmunta Jórskiego',
 'Krasińskiego Z.':                     'Zygmunta Krasińskiego',
 'Z. Krasińskiego':                     'Zygmunta Krasińskiego',
 'Z. Markerta':                         'Zygmunta Markerta',
 'Z. Modzelewskiego':                   'Zygmunta Modzelewskiego',
 'Noskowskiego Zygmunta':               'Zygmunta Noskowskiego',
 'Z. Noskowskiego':                     'Zygmunta Noskowskiego',
 'Z. Stojowskiego':                     'Zygmunta Stojowskiego',
 'Z. Słomińskiego':                     'Zygmunta Słomińskiego',
 'Z. Vogla':                            'Zygmunta Vogla',
 'Ł. Drewny':                           'Łukasza Drewny',
 'św. Andrzeja Boboli':                 'Świętego Andrzeja Boboli',
 'św. Bonifacego':                      'Świętego Bonifacego',
 'Św. Ducha':                           'Świętego Ducha',
 'Św. Floriana':                        'Świętego Floriana',
 'św. Hieronima':                       'Świętego Hieronima',
 'Huberta Św.':                         'Świętego Huberta',
 'Św. Huberta':                         'Świętego Huberta',
 'św. J. Odrowąża':                     'Świętego Jacka Odrowąża',
 'Św. Jana':                            'Świętego Jana',
 'św. Maksymiliana Kolbego':            'Świętego Maksymiliana Kolbego',
 'Marcina św.':                         'Świętego Marcina',
 'Św. Marcina':                         'Świętego Marcina',
 'Św. Marka':                           'Świętego Marka',
 'Mikołaja Św.':                        'Świętego Mikołaja',
 'św. Stanisława':                      'Świętego Stanisława',
 'św. Szczepana':                       'Świętego Szczepana',
 'św. Wincentego':                      'Świętego Wincentego',
 'Św. Wojciecha':                       'Świętego Wojciecha',
 'św. Wojciecha':                       'Świętego Wojciecha',
 'Anny Św.':                            'Świętej Anny',
 'Św. Kingi':                           'Świętej Kingi',
 'Św. Rozalii':                         'Świętej Rozalii',
 'św. Urszuli Ledóchowskiej':           'Świętej Urszuli Ledóchowskiej',
 'Wojciecha św.':                       'świętego Wojciecha',
}
import sys
if sys.version_info.major == 2:
    addr_map = dict(map(lambda x: (x[0].decode('utf-8'), x[1].decode('utf-8')), addr_map.items()))
    from urllib2 import urlopen
else:
    from urllib.request import urlopen
    from urllib.parse import urlencode

from bs4 import BeautifulSoup
import io
import json
import logging
import os
import overpass
import pickle
import time
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from itertools import groupby
from collections import namedtuple
import functools
import base64
import zeep
from zeep.wsse.username import UsernameToken

__log = logging.getLogger(__name__)

TerytUlicEntry = namedtuple('TerytUlicEntry', ['sym_ul', 'nazwa', 'cecha'])

__CECHA_MAPPING = {
        'UL.': '',
        'AL.': 'Aleja',
        'PL.': 'Plac',
        'SKWER': 'Skwer',
        'BULW.': 'Bulwar',
        'RONDO': 'Rondo',
        'PARK': 'Park',
        'RYNEK': 'Rynek',
        'SZOSA': 'Szosa',
        'DROGA': 'Droga',
        'OS.': 'Osiedle',
        'OGRÓD': 'Ogród',
        'WYB.': 'Wybrzeże',
        'INNE': '' 
    }

def downloadULIC():
    __log.info("Updating ULIC data from TERYT, it may take a while")
    wsdl = 'https://uslugaterytws1.stat.gov.pl/wsdl/terytws1.wsdl'
    wsse = UsernameToken('osmaddrtools', '#06JWOWutt4')

    client = zeep.Client(wsdl=wsdl, wsse=wsse)
    data = client.service.PobierzDateAktualnegoKatUlic()
    dane = client.service.PobierzKatalogULIC(data)

    binary = base64.decodestring(dane.plik_zawartosc.encode('utf-8'))
    dictionary_zip = zipfile.ZipFile(
        io.BytesIO(binary
        )
    )

    def get(elem, tag):
        col = elem.find(tag)
        if col.text:
            return col.text
        return ""

    dicname = [x for x in dictionary_zip.namelist() if x.endswith(".xml")][0]
    tree = ET.fromstring(dictionary_zip.read(dicname))
    data = tuple(TerytUlicEntry(
                get(row, "SYM_UL"), 
                " ".join((get(row, 'NAZWA_2'), get(row,'NAZWA_1'))),
                get(row, "CECHA").upper()
            ) for row in tree.find('catalog').iter('row'))
    
    # sanity check
    for tentry, duplist in groupby(data, lambda x: x.sym_ul):
        if len(set(duplist)) > 1:
            __log.info("Duplicate entry in TERYT for symul: %s, values: %s", tentry.sym_ul, ", ".join(duplist))

    ret = dict((x.sym_ul, x) for x in data)

    __log.info("Entries in TERYT ULIC: %d", len(ret))
    return ret

def getDict(keyname, valuename, coexitingtags=None):
    __log.info("Updating %s data from OSM, it may take a while", keyname)
    tags = [keyname, valuename]
    if coexitingtags:
        tags.extend(coexitingtags)
    soup = json.loads(overpass.getNodesWaysWithTags(tags, 'json'))
    ret = {}
    for tag in soup['elements']:
        symul = tag['tags'][keyname]
        street = tag['tags'][valuename]
        if street:
            try:
                entry = ret[symul]
            except KeyError:
                entry = {}
                ret[symul] = entry
            try:
                entry[street] += 1
            except KeyError:
                entry[street] = 1
    # ret = dict(symul, dict(street, count))
    inconsistent = dict((x[0], x[1].keys()) for x in filter(lambda x: len(x[1]) > 1, ret.items()))
    for (symul, streetlst) in inconsistent.items():
        __log.info("Inconsitent mapping for %s = %s, values: %s", keyname, symul, ", ".join(streetlst))
    return ret

def storedDict(fetcher, filename):
    try:
        with open(filename, "rb") as f:
            data = pickle.load(f)
    except IOError:
        __log.debug("Can't read a file: %s, starting with a new one", filename, exc_info=True)
        data = {
            'time': 0
        }
    if data['time'] < time.time() - 21*24*60*60:
        try:
            new = fetcher()
        except:
            __log.warn("Failed to download dictionary: %s", filename, exc_info=True)
            __log.warn("Using dictionary from: %s", time.asctime(time.localtime(data['time'])))
            return data['dct']
        data['dct'] = new
        data['time'] = time.time()
        try:
            with open(filename, "w+b") as f:
                pickle.dump(data, f)
        except: 
            __log.debug("Can't write file: %s", filename, exc_info=True)
    return data['dct']


import utils

__DB_OSM_TERYT_SYMUL = os.path.join(tempfile.gettempdir(), 'osm_teryt_symul_v2.db')
__DB_OSM_TERYT_SIMC = os.path.join(tempfile.gettempdir(), 'osm_teryt_simc_v2.db')
__DB_TERYT_ULIC = os.path.join(tempfile.gettempdir(), 'teryt_ulic_v3.db')
__DB_OSM_SIMC_POSTCODE = os.path.join(tempfile.gettempdir(), 'osm_teryt_simc_postcode_v1.db')
__mapping_symul = {}
__mapping_simc = {}
__teryt_ulic = {}
__mapping_simc_postcode = {}

import threading
__init_lock = threading.Lock()
__is_initialized = False

def __init():
    global __is_initialized, __init_lock, __mapping_symul, __mapping_simc, __teryt_ulic, __mapping_simc_postcode
    if not __is_initialized:
        with __init_lock:
            if not __is_initialized:
                __mapping_symul = storedDict(lambda: getDict('addr:street:sym_ul', 'addr:street'), __DB_OSM_TERYT_SYMUL)
                __mapping_simc = storedDict(lambda: getDict('teryt:simc' , 'name', ['place']), __DB_OSM_TERYT_SIMC) # check based on place names, not addresses
                __teryt_ulic = storedDict(downloadULIC, __DB_TERYT_ULIC)
                __mapping_simc_postcode = storedDict(lambda: getDict('teryt:simc', 'addr:postcode', ['place',]), __DB_OSM_SIMC_POSTCODE)
                __is_initialized = True

@functools.lru_cache(maxsize=None)
def mapstreet(strname, symul):
    __init()
    teryt_entry = __teryt_ulic.get(symul)
    def checkAndAddCecha(street):
        if teryt_entry and teryt_entry.cecha:
            if street.upper().startswith(teryt_entry.cecha.upper()):
                # remove short version cecha and prepand full version
                street = "%s %s" % (__CECHA_MAPPING.get(teryt_entry.cecha, '') , strname[len(teryt_entry.cecha):].strip())
                street = street.strip()
            if street.upper().startswith('UL.') and teryt_entry.cecha.upper() == 'UL.':
                street = street[3:].strip()
            if not street.upper().startswith(teryt_entry.cecha.upper()) and \
                not street.upper().startswith(__CECHA_MAPPING.get(teryt_entry.cecha, '').upper()):
                __log.debug("Adding TERYT.CECHA=%s to street=%s (addr:street:sym_ul=%s)" % (__CECHA_MAPPING.get(teryt_entry.cecha, ''), street, symul))
                return "%s %s" % (__CECHA_MAPPING.get(teryt_entry.cecha, ''), street)
        else:
            if street.upper().startswith('AL. '):
                return 'Aleja ' + street[4:]
            if street.upper().startswith('PL. '):
                return 'Plac ' + street[4:]
            if street.upper().startswith('UL. '):
                return street[4:]
        return street

    try:
        strname = strname.replace('„', '"').replace('”', '"')
        ret = checkAndAddCecha(addr_map[strname])
        log_level = logging.INFO
        if max(strname.split(' '), key=len) in ret:
            # if longest part of strname is in ret, then lower the log message level
            log_level = logging.DEBUG
        __log.log(log_level, "mapping street %s -> %s, TERYT: %s (addr:street:sym_ul=%s) " % (strname, ret, teryt_entry.nazwa if teryt_entry else 'N/A', symul))
        return ret
    except KeyError:
        try:
            ret = __mapping_symul[symul]
            if len(ret) > 1:
                __log.info("Inconsitent mapping for addr:street:sym_ul = %s. Original value: %s, TERYT: %s, OSM values: %s. Leaving original value.", symul, strname, teryt_entry.nazwa if teryt_entry else 'N/A',  ", ".join(ret))
                return strname
            ret = checkAndAddCecha(next(iter(ret.keys()))) # check and add for first and only key
            if ret != strname:
                log_level = logging.INFO
                if max(strname.split(' '), key=len) in ret:
                    log_level = logging.DEBUG
                __log.log(log_level, "mapping street %s -> %s, TERYT: %s (addr:street:sym_ul=%s) " % (strname, ret, teryt_entry.nazwa if teryt_entry else 'N/A', symul))
            return ret
        except KeyError:
            return checkAndAddCecha(strname)

@functools.lru_cache(maxsize=None)
def mapcity(cityname, simc):
    __init()
    try:
        ret = __mapping_simc[simc]
        if len(ret) > 1:
            __log.info("Inconsitent mapping for addr:city:simc = %s. Original value: %s, OSM values: %s. Leaving original value.", simc, cityname, ", ".join(ret))
            return cityname
        ret = next(iter(ret.keys())) # take first (and the only one) key
        if ret != cityname:
            __log.info("mapping city %s -> %s (addr:city:simc=%s)" % (cityname, ret, simc))
        return ret
    except KeyError:
        return cityname.replace(' - ', '-')

import re
__POSTCODE = re.compile('^[0-9]{2}-[0-9]{3}$')

@functools.lru_cache(maxsize=None)
def mappostcode(postcode, simc):
    __init()
    if postcode:
        return postcode
    try:
        ret = __mapping_simc_postcode[simc]
        if len(ret) > 1:
            __log.info("Inconsistent mapping for teryt:simc = %s to postcode. OSM values: %s", simc, ", ".join(ret))
            return postcode
        ret = next(iter(ret.keys())) # take first (and the only one) key
        if not __POSTCODE.match(ret):
            __log.info("Postcode for simc: %s doesn't look good: %s", simc, ret)
            return postcode
        if ret != postcode:
            __log.info("Adding postcode %s for teryt:simc=%s", ret, simc)
        return ret
    except KeyError:
        return postcode

def main():
      logging.basicConfig(level=10)
      print(mapstreet('Głowackiego', 'x'))
      print(mapcity('Kostrzyń', 'x'))

if __name__ == '__main__':
    main()
