# # -*- coding: UTF-8 -*-
# TODO:
# - add warning, when street exists as a part of name in sym_ul dictionary or in ULIC

addr_map = {
 '1-go Maja': '1 Maja',
 '1-ego Maja': '1 Maja',
 '11-go Listopada': '11 Listopada',
 '15-go Grudnia': '15 Grudnia',
 '17-go Lipca': '17 Lipca',
 '21-go Stycznia': '21 Stycznia',
 '24-go Stycznia': '24 Stycznia',
 '27-go Stycznia': '27 Stycznia',
 '28-go Lutego': '28 Lutego',
 '3-go Kwietnia': '3 Kwietnia',
 '3-go Maja': '3 Maja',
 '3-ego Maja': '3 Maja',
 '35 Lecia PRL': '35-lecia PRL',
 '9-go Maja': '9 Maja',
 'A. Struga': 'Andrzeja Struga',
 'Abramskiego J. ks.': 'Księdza Jana Abramskiego',
 'Al. H. Kołłątaja': 'aleja Hugona Kołłątaja',
 'Al. Spacerowa': 'aleja Spacerowa',
 'Al. Wodniaków': 'aleja Wodniaków',
 'Andersa Władysława': 'Władysława Andersa',
 'Gen. Władysława Andersa': 'Generała Władysława Andersa',
 'Gen. Jerzego Ziętka': 'Generała Jerzego Ziętka',
 'Anny Św.': 'Świętej Anny',
 'Arciszewskiego Krzysztofa': 'Krzysztofa  Arciszewskiego',
 'Asnyka A.': 'Adama Asnyka',
 'Asnyka Adama': 'Adama Asnyka',
 'Asnyka': 'Adama Asnyka',
 'Baczewskiego Jana': 'Jana Baczewskiego',
 'Baczyńskiego K. K.': 'Krzysztofa Kamila Baczyńskiego',
 'Baczyńskiego' : 'Krzysztofa Kamila Baczyńskiego',
 'Barlickiego Norberta': 'Norberta Barlickiego',
 'Barlickiego': 'Norberta Barlickiego',
 'Bauera Jana': 'Jana Bauera',
 'Bałasza A.': 'Aleksandra Bałasza',
 'Bema Józefa': 'Józefa Bema',
 'Bema': 'Józefa Bema',
 'gen. Józefa Bema': 'Generała Józefa Bema',
 'Boguckiego': 'Teofila Boguckiego',
 'Boh. Stalingradu': 'Bohaterów Stalingradu',
 'Boh. Warszawy': 'Bohaterów Warszawy',
 'Bojara-Fijałkowskiego Gracjana': 'Gracjana Bojara-Fijałkowskiego',
 'Bony': 'Królowej Bony',
 'Bora-Komorowskiego T. gen.': 'Generała Tadeusza Bora-Komorowskiego',
 'Borzymowskiego Marcina': 'Marcina Borzymowskiego',
 'Boya Żeleńskiego': 'Tadeusza Boya-Żeleńskiego',
 'Boya-Żeleńskiego Tadeusza': 'Tadeusza Boya-Żeleńskiego',
 'Bożka Arkadiusza': 'Arkadiusza Bożka',
 'Broniewskiego W.': 'Władysława Broniewskiego',
 'Broniewskiego Władysława': 'Władysława Broniewskiego',
 'Broniewskiego': 'Władysława Broniewskiego',
 'Brzechwy J.': 'Jana Brzechwy',
 'Brzechwy Jana': 'Jana Brzechwy',
 'Brzechwy': 'Jana Brzechwy',
 'Buczka M.': 'Mariana Buczka',
 'Buczka': 'Mariana Buczka',
 'Chałubińskiego Tytusa': 'Tytusa Chałubińskiego',
 'Chałubińskiego': 'Tytusa Chałubińskiego',
 'Chełmońskiego J.': 'Józefa Chełmońskiego',
 'Chełmońskiego Józefa': 'Józefa Chełmońskiego',
 'Chodkiewicza Jana': 'Jana Chodkiewicza',
 'Chodkiewicza Karola': 'Karola Chodkiewicza',
 'Chodkiewicza': 'Karola Chodkiewicza',
 'Chopina F.': 'Fryderyka Chopina',
 'Chopina Fryderyka': 'Fryderyka Chopina',
 'Chopina': 'Fryderyka Chopina',
 'Chrobrego B.': 'Bolesława Chrobrego',
 'B. Chrobrego': 'Bolesława Chrobrego',
 'Chrobrego': 'Bolesława Chrobrego',
 'Chrzanowskiego Ignacego': 'Ignacego Chrzanowskiego',
 'Cieślaka W.': 'Cieślaka W.',
 'Ciołkowskiego': 'Konstantego Ciołkowskiego',
 'Conrada Korzeniowskiego Josepha': 'Josepha Conrada Korzeniowskiego',
 'Curie-Skłodowskiej': 'Marii Skłodowskiej-Curie',
 'Czarnieckiego S.': 'Stefana Czarnieckiego',
 'Czarnieckiego Stefana': 'Stefana Czarnieckiego',
 'Czarnieckiego': 'Stefana Czarnieckiego',
 'Daszyńskiego I.': 'Ignacego Daszyńskiego',
 'Daszyńskiego': 'Ignacego Daszyńskiego',
 'Derdowskiego': 'Jana Hieronima Derdowskiego',
 'Dmowskiego Romana': 'Romana Dmowskiego',
 'Domańskiego Bolesława': 'Bolesława Domańskiego',
 'Domina Czesława': 'Czesława Domina',
 'Drzymały M.': 'Michała Drzymały',
 'Drzymały Michała': 'Michała Drzymały',
 'Dubois Stanisława': 'Stanisława Dubois',
 'Dunikowskiego K.': 'Ksawerego Dunikowskiego',
 'Dzierżykraja-Morawskiego J. W.': 'Witolda Józefa Dzierżykraja-Morawskiego',
 'Dąbka Stanisława': 'Stanisława Dąbka',
 'Dąbrowskiego J. Ks.': 'Księdza Józefa Dąbrowskiego',
 'Dąbrowskiego J.': 'Jarosława Dąbrowskiego',
 'Dąbrowskiego Jarosława': 'Jarosława Dąbrowskiego',
 'Dąbrowskiej M.': 'Marii Dąbrowskiej',
 'Dąbrowskiej': 'Marii Dąbrowskiej',
 'Długosza J.': 'Jana Długosza',
 'Długosza': 'Jana Długosza',
 'F. Szopena': 'Fryderyka Chopina',
 'Fałata Juliana': 'Juliana Fałata',
 'Fitelberga': 'Grzegorza Fitelberga',
 'Fitio Jerzego': 'Jerzego Fitio',
 'Fornalskiej': 'Małgorzaty Fornalskiej',
 'Frankowskiego Jana': 'Jana Frankowskiego',
 'Fredry Aleksandra': 'Aleksandra Fredry',
 'Fredry': 'Aleksandra Fredry',
 'Gałczyńskiego K. I. ': 'Konstantego Ildefonsa Gałczyńskiego',
 'Gałczyńskiego Konstantego Ildefonsa': 'Konstantego Ildefonsa Gałczyńskiego',
 'Gałczyńskiego': 'Konstantego Ildefonsa Gałczyńskiego',
 'gen. Grota Roweckiego': 'Gererała Stefana Grota Roweckiego',
 'Głowackiego A.': 'Aleksandra Głowackiego',
 'Gierczak Emilii': 'Emilii Gierczak',
 'Gierymskich Aleksandra i Maksymiliana': 'Aleksandra i Maksymiliana Gierymskich',
 'Golisza Maksymiliana': 'Maksymiliana Golisza',
 'Grabskiego Wł.': 'Władysława Grabskiego',
 'Grochowskiego Maksymiliana': 'Maksymiliana Grochowskiego',
 'Grota Roweckiego S. gen.': 'Gererała Stefana Grota Roweckiego',
 'Grota-Roweckiego S. gen.': 'Gererała Stefana Grota Roweckiego',
 'Grottgera A.': 'Artura Grottgera',
 'Grottgera Artura': 'Artura Grottgera',
 'Górskiego Klaudiusza': 'Klaudiusza Górskiego',
 'Gąszczak Marii Magdaleny': 'Marii Magdaleny Gąszczak',
 'Głowackiego B.': 'Bartosza Głowackiego',
 'Głowackiego Bartosza': 'Bartosza Głowackiego',
 'Hirszfelda L.': 'Ludwika Hirszfelda',
 'Huberta Św.': 'Świętego Huberta',
 'I Armii W.P.' : 'I Armii Wojska Polskiego',
 'Iwaszkiewicza J.': 'Jarosława Iwaszkiewicza',
 'J. Kochanowskiego': 'Jana Kochanowskiego',
 'Jagiełły W.': 'Władysława Jagiełły',
 'Jagiełły': 'Władysława Jagiełły',
 'Jagoszewskiego Henryka': 'Henryka Jagoszewskiego',
 'Jankiel': 'Jankiela',
 'Jelec Jadwigi': 'Jadwigi Jelec',
 'Jordana Henryka': 'Henryka Jordana',
 'Joselewicza': 'Berka Joselewicza',
 'Jurkiewicza Kazimierza': 'Kazimierza Jurkiewicza',
 'Kajki': 'Michała Kajki',
 'Kajki Michała': 'Michała Kajki',
 'Kamińskiego A.': 'Aleksandra Kamińskiego',
 'Karłowicza Mieczysława': 'Mieczysława Karłowicza',
 'Karłowicza': 'Mieczysława Karłowicza',
 'Kasprowicza J.': 'Jana Kasprowicza',
 'Kasprowicza Jana': 'Jana Kasprowicza',
 'Kasprowicza': 'Jana Kasprowicza',
 'Kasprzaka': 'Marcina Kasprzaka',
 'Kiepury': 'Jana Kiepury',
 'Kilińskiego J.': 'Jana Kilińskiego',
 'Kilińskiego Jana': 'Jana Kilińskiego',
 'Kilińskiego': 'Jana Kilińskiego',
 'Kinga Martina': 'Martina Kinga',
 'Klemensiewicza Zenona': 'Zenona Klemensiewicza',
 'Kmicica Andrzeja': 'Andrzeja Kmicica',
 'Kniewskiego Władysława': 'Władysława Kniewskiego',
 'Kniewskiego': 'Władysława Kniewskiego',
 'Kochanowskiego J.': 'Jana Kochanowskiego',
 'Kochanowskiego Jana': 'Jana Kochanowskiego',
 'Kochanowskiego': 'Jana Kochanowskiego',
 'Kolumba Krzysztofa': 'Krzysztofa Kolumba',
 'Koniecpolskiego Stanisława': 'Stanisława Koniecpolskiego',
 'Konopnickiej M.': 'Marii Konopnickiej',
 'Konopnickiej Marii': 'Marii Konopnickiej',
 'Konopnickiej': 'Marii Konopnickiej',
 'Kopernika M.': 'Mikołaja Kopernika',
 'Kopernika Mikołaja': 'Mikołaja Kopernika',
 'Kopernika': 'Mikołaja Kopernika',
 'Korczaka J. dr': 'doktora Janusza Korczaka',
 'Korczaka Janusza': 'Janusza Korczaka',
 'Korczaka': 'Janusza Korczaka',
 'Korfantego W.': 'Wojciecha Korfantego',
 'Kosińskiego': 'Antoniego Kosińskiego',
 'Kossaka Juliusza': 'Juliusza Kossaka',
 'Kostenckiego Jerzego': 'Jerzego Kostenckiego',
 'Kostrzewy Wery': 'Wery Kostrzewy',
 'Kotarbińskiego Tadeusza': 'Tadeusza Kotarbińskiego',
 'Kołłątaja H.': 'Hugona Kołłątaja',
 'Kołłątaja Hugo': 'Hugona Kołłątaja',
 'Kołłątaja': 'Hugona Kołłątaja',
 'Kościuszki T. gen.': 'Generała Tadeusza Kościuszki',
 'Kościuszki T.': 'Tadeusza Kościuszki',
 'Kościuszki Tadeusza': 'Tadeusza Kościuszki',
 'Kościuszki': 'Tadeusza Kościuszki',
 'Kr. Jadwigi': 'Królowej Jadwigi',
 'Krasickiego Ignacego': 'Józefa Ignacego Kraszewskiego',
 'Krasickiego': 'Józefa Ignacego Kraszewskiego',
 'Krasińskiego Z.': 'Zygmunta Krasińskiego',
 'Kraszewskiego J. I.': 'Józefa Ignacego Kraszewskiego',
 'Kraszewskiego': 'Józefa Ignacego Kraszewskiego',
 'Kromera J.': 'Józefa Kromera',
 'Kruczkowskiego L.': 'Leona Kruczkowskiego',
 'Kruczkowskiego': 'Leona Kruczkowskiego',
 'Krzyżanowskiego Juliana': 'Juliana Krzyżanowskiego',
 'Ks. Elżbiety': 'Księżnej Elżbiety',
 'Ks. Jana Twardowskiego': 'Księdza Jana Twardowskiego',
 'ks. Józefa Kuropieski': 'Księdza Józefa Kuropieski',
 'ks. Adama Opalskiego': 'Księdza Adama Opalskiego',
 'Kuczkowskiego Ignacego': 'Ignacego Kuczkowskiego',
 'Kurpińskiego Karola': 'Karola Kurpińskiego',
 'Kusocińskiego J.': 'Janusza Kusocińskiego',
 'Kutrzeby Tadeusza': 'Tadeusza Kutrzeby',
 'Kwiatkowskiego Eugeniusza': 'Eugeniusza Kwiatkowskiego',
 'Lange Oskara': 'Oskara Lange',
 'Laskonogiego Władysława': 'Władysława Laskonogiego',
 'Lelewela Joachima': 'Joachima Lelewela',
 'Leśmiana B.': 'Bolesława Leśmiana',
 'Limanowskiego': 'Bolesława Limanowskiego',
 'Limanowskiego B.': 'Bolesława Limanowskiego',
 'Limanowskiego Bolesława': 'Bolesława Limanowskiego',
 'Łokietka': 'Władysława Łokietka',
 'M. Konopnickiej': 'Marii Konopnickiej',
 'Maciejewicza Konstantego': 'Konstantego Maciejewicza',
 'Makowskiego Tadeusza': 'Tadeusza Makowskiego',
 'Makuszyńskiego Kornela': 'Kornela Makuszyńskiego',
 'Malczewskiego Jacka': 'Jacka Malczewskiego',
 'Malczewskiego J.': 'Jacka Malczewskiego',
 'Matejki ': 'Jana Matejki',
 'Matejki J.': 'Jana Matejki',
 'Matejki Jana': 'Jana Matejki',
 'Matejki': 'Jana Matejki',
 'Matusewicz G. dr': 'Doktor Genowefy Matusewicz',
 'Maćkowicza Izydora': 'Izydora Maćkowicza',
 'Małachowskiego': 'Stanisława Małachowskiego',
 'Meczenników Unickich': 'Męczenników Unickich',
 'Miarki K.': 'Karola Miarki',
 'Michałowskiego Piotra': 'Piotra Michałowskiego',
 'Mickiewicza A.': 'Adama Mickiewicza',
 'Mickiewicza Adama': 'Adama Mickiewicza',
 'Mickiewicza': 'Adama Mickiewicza',
 'Mielczarskiego': 'Romualda Mielczarskiego',
 'Mierosławskiego': 'Ludwika Mierosławskiego',
 'Mireckiego Józefa': 'Józefa Mireckiego',
 'Miłosza C.': 'Czesława Miłosza',
 'Miłosza Cz.': 'Czesława Miłosza',
 'Mikołaja Św.': 'Świętego Mikołaja',
 'mjr. Sucharskiego': 'Majora Henryka Sucharskiego',
 'mjr. Romana Bielawskiego': 'Majora Romana Bielawskiego',
 'Modrzejewskiej Heleny': 'Heleny Modrzejewskiej',
 'Modrzewskiego': 'Andrzeja Frycza Modrzewskiego',
 'Moniuszki S.': 'Stanisława Moniuszki',
 'Moniuszki Stanisława': 'Stanisława Moniuszki',
 'Moniuszki': 'Stanisława Moniuszki',
 'Morcinka G.': 'Gustawa Morcinka',
 'Morcinka Gustawa': 'Gustawa Morcinka',
 'Morcinka': 'Gustawa Morcinka',
 'Narutowicza G.': 'Gabriela Narutowicza',
 'Narutowicza Gabriela': 'Gabriela Narutowicza',
 'Narutowicza': 'Gabriela Narutowicza',
 'Nałkowskiej': 'Zofii Nałkowskiej',
 'Nałkowskiej Z.': 'Zofii Nałkowskiej',
 'Nerudy Pablo': 'Pablo Nerudy',
 'Niedziałkowskiego': 'Mieczysława Niedziałkowskiego',
 'Niemcewicza': 'Juliana Ursyna Niemcewicza',
 'Nocznickiego': 'Tomasza Nocznickiego',
 'Norwida C. K. ': 'Cypriana Kamila Norwida',
 'Norwida C.K.': 'Cypriana Kamila Norwida',
 'Norwida Cypriana': 'Cypriana Kamila Norwida',
 'Norwida': 'Cypriana Kamila Norwida',
 'Cypriana Norwida': 'Cypriana Kamila Norwida',
 'Noskowskiego Zygmunta': 'Zygmunta Noskowskiego',
 'Nowotki M.': 'Marcelego Nowotki',
 'Nowotki': 'Marcelego Nowotki',
 'Nowowiejskiego Feliksa': 'Feliksa Nowowiejskiego',
 'Ogińskiego Michała Kleofasa': 'Michała Kleofasa Ogińskiego',
 'Ogińskiego Michała': 'Michała Kleofasa Ogińskiego',
 'Okrzei S.': 'Stefana Okrzei',
 'Okrzei St.': 'Stefana Okrzei',
 'Okrzei Stefana': 'Stefana Okrzei',
 'Okrzei': 'Stefana Okrzei',
 'Okulickiego Leopolda': 'Leopolda Okulickiego',
 'Okulickiego Niedźwiadka L. gen.': 'Generała Leopolda Okulickiego Niedźwiadka',
 'Ordona J.': 'Juliana Ordona',
 'Orkana': 'Władysława Orkana',
 'Orkana W.': 'Władysława Orkana',
 'Orzeszkowej E.': 'Elizy Orzeszkowej',
 'Orzeszkowej': 'Elizy Orzeszkowej',
 'Orłowskiego Aleksandra': 'Aleksandra Orłowskiego',
 'Paderewskiego Ignacego Jana': 'Ignacego Jana Paderewskiego',
 'Paderewskiego Ignacego': 'Ignacego Jana Paderewskiego',
 'Paderewskiego': 'Ignacego Jana Paderewskiego',
 'Picassa Pablo': 'Pablo Picassa',
 'Pieniężnego Seweryna': 'Seweryna Pieniężnego',
 'Pileckiego Witolda': 'Witolda Pileckiego',
 'Piłsudskiego J. Marsz.': 'marszałka Józefa Piłsudskiego',
 'Piłsudskiego J. marsz.': 'marszałka Józefa Piłsudskiego',
 'Piłsudskiego J.': 'Józefa Piłsudskiego',
 'Piłsudskiego Józefa': 'Józefa Piłsudskiego',
 'Piłsudskiego Marszałka': 'marszałka Józefa Piłsudskiego',
 'Piłsudskiego': 'Józefa Piłsudskiego',
 'Plater E.': 'Emilii Plater E.',
 'Pobożnego H.': 'Henryka Pobożnego',
 'Polipol Aleja': 'aleja Polipol',
 'Poniatowskiego J.': 'Józefa Poniatowskiego',
 'Popiełuszki Jerzego': 'Jerzego Popiełuszki',
 'Powstańców Wlkp.': 'Powstańców Wielkopolskich',
 'Poświatowskiej H.': 'Haliny Poświatowskiej',
 'Prusa B.': 'Bolesława Prusa',
 'Prusa Bolesława': 'Bolesława Prusa',
 'Prusa': 'Bolesława Prusa',
 'Próchnika Adama': 'Adama Próchnika',
 'Przerwy-Tetmajera K.': 'Kazimierza Przerwy-Tetmajera',
 'Pstrowskiego': 'Wincentego Pstrowskiego',
 'Pułaskiego K.': 'Kazimierza Pułaskiego',
 'Pułaskiego': 'Kazimierza Pułaskiego',
 'Rafińskiego Teodora': 'Teodora Rafińskiego',
 'Rataja M.': 'Macieja Rataja',
 'Ratajczaka Franciszka': 'Franciszka Ratajczaka',
 'Reja M.': 'Mikołaja Reja',
 'Reja Mikołaja': 'Mikołaja Reja',
 'Reja': 'Mikołaja Reja',
 'Rejtana Tadeusza': 'Tadeusza Rejtana',
 'Rejtana': 'Tadeusza Rejtana',
 'Reymonta W.': 'Władysława Reymonta',
 'Reymonta W. S.': 'Władysława Stanisława Reymonta',
 'Reymonta Władysława Stanisława': 'Władysława Stanisława Reymonta',
 'Reymonta Władysława': 'Władysława Reymonta',
 'Reymonta': 'Władysława Stanisława Reymonta',
 'Rodziewiczówny Marii': 'Marii Rodziewiczówny',
 'Roli-Żymierskiego M. marsz.': 'marszałka Michała Roli-Żymierskiego',
 'Roosevelta': 'Franklina Delano Roosevelta',
 'Ruszczyca Ferdynanda': 'Ferdynanda Ruszczyca',
 'Rzeckiego I.': 'Ignacego Rzeckiego',
 'Rzeckiego': 'Ignacego Rzeckiego',
 'Różyckiego Ludomira': 'Ludomira Różyckiego',
 'Samulowskiego Andrzeja': 'Andrzeja Samulowskiego',
 'Sanguszki A. ks.': 'księcia Andrzeja Sanguszki',
 'Sawickiej H.': 'Hanki Sawickiej',
 'Sawickiej Hanki': 'Hanki Sawickiej',
 'Sienkiewicza H.': 'Henryka Sienkiewicza',
 'Sienkiewicza Henryka': 'Henryka Sienkiewicza',
 'Sienkiewicza': 'Henryka Sienkiewicza',
 'Siennickiego Ryszarda': 'Ryszarda Siennickiego',
 'Sierocińskiego Romana': 'Romana Sierocińskiego',
 'Sierpińskiego Wacława': 'Wacława Sierpińskiego',
 'Sierpińskiego Z. prof.': 'profesora Zbigniewa Sierpińskiego',
 'Sikorskiego W. gen.': 'Generała Władysława Sikorskiego',
 'Sikorskiego W.': 'Generała Władysława Sikorskiego',
 'Sikorskiego Władysława': 'Generała Władysława Sikorskiego',
 'Sikorskiego': 'Generała Władysława Sikorskiego',
 'Gen. Władysława Sikorskiego': 'Generała Władysława Sikorskiego',
 'gen. Władysława Sikorskiego': 'Generała Władysława Sikorskiego',
 'Skalskiego': 'Generała Stanisława Skalskiego',
 'Skargi P.': 'Piora Skargi',
 'Skargi Piotra': 'Piotra Skargi',
 'Skoczylasa Władysława': 'Władysława Skoczylasa',
 'Skrzetuskiego J.': 'Jana Skrzetuskiego',
 'Skrzetuskiego Jana': 'Jana Skrzetuskiego',
 'Skłodowskiej': 'Marii Skłodowskiej-Curie',
 'Skłodowskiej- Curie M.': 'Marii Skłodowskiej-Curie',
 'Skłodowskiej-Curie M.': 'Marii Skłodowskiej-Curie',
 'Skłodowskiej-Curie Marii': 'Marii Skłodowskiej-Curie',
 'Skłodowskiej-Curie': 'Marii Skłodowskiej-Curie',
 'Sokołowskiego A.': 'Alfreda Sokołowskiego',
 'Soplicy J.': 'Jacka Soplicy',
 'Sowińskiego Józefa': 'Józefa Sowińskiego',
 'Spasowskiego Władysława': 'Władysława Spasowskiego',
 'Staffa Leopolda': 'Leopolda Staffa',
 'Staffa': 'Leopolda Staffa',
 'Stankiewicza Mamerta': 'Mamerta Stankiewicza',
 'Starzyńskiego Stefana': 'Stefana Starzyńskiego',
 'Staszica St.': 'Stanisława Staszica',
 'Staszica S.'  : 'Stanisława Staszica',
 'Staszica Stanisława': 'Stanisława Staszica',
 'Staszica': 'Stanisława Staszica',
 'Steffena Wiktora': 'Wiktora Steffena',
 'Struga Andrzeja': 'Andrzeja Struga',
 'Struka Księdza': 'księdza Struka',
 'Stryjeńskiej Z.': 'Zofii Stryjeńskiej',
 'Stwosza W.': 'Wita Stwosza',
 'Sucharskiego Henryka': 'Henryka Sucharskiego',
 'Sucharskiego': 'Majora Henryka Sucharskiego',
 'Sułkowskiego Antoniego': 'Antoniego Sułkowskiego',
 'Sygietyńskiego Tadeusza': 'Tadeusza Sygietyńskiego',
 'Syrokomli': 'Władysława Syrokomli',
 'Szafera W. prof.': 'Profesora Władysława Szafera',
 'Szarego F.': 'Floriana Szarego',
 'Szelburg-Zarembiny Ewy': 'Ewy Szelburg-Zarembiny',
 'Szenwalda Lucjana': 'Lucjana Szenwalda',
 'Szymanowskiego Karola': 'Karola Szymanowskiego',
 'Szymanowskiego': 'Karola Szymanowskiego',
 'Słowackiego J.': 'Juliusza Słowackiego',
 'Słowackiego Juliusza': 'Juliusza Słowackiego',
 'Słowackiego': 'Juliusza Słowackiego',
 'T. Kościuszki': 'Tadeusza Kościuszki',
 'Tarnowskiego Jana': 'Jana Tarnowskiego',
 'Tatarkiewicza Władysława': 'Władysława Tatarkiewicza',
 'Teligi Leonida': 'Leonida Teligi',
 'Teligi': 'Leonida Teligi',
 'Tetmajera Kazimierza': 'Kazimierza Tetmajera',
 'Tetmajera': 'Kazimierza Tetmajera',
 'Tokarzewskiego-Karaszewicza Torwida M. gen.': 'Generała Michała T. Tokarzewskiego-Karaszewicza Torwida',
 'Traugutta Romualda': 'Romualda Traugutta',
 'Traugutta R.' : 'Romualda Traugutta',
 'Traugutta': 'Romualda Traugutta',
 'Turowskiego Władysława': 'Władysława Turowskiego',
 'Tuwima J.': 'Juliana Tuwima',
 'Tuwima Juliana': 'Juliana Tuwima',
 'Tuwima': 'Juliana Tuwima',
 'Tysiąclecia PP': 'Tysiąclecia Państwa Polskiego',
 'W. Jagiełły': 'Władysława Jagiełły',
 'Wallenroda K.': 'Konrada Wallenroda',
 'Waresiaka E. Ks.': 'księdza Eugeniusza Waresiaka',
 'Warskiego Adolfa': 'Adolfa Warskiego',
 'Waryńskiego L.': 'Ludwika Waryńskiego',
 'Waryńskiego Ludwika': 'Ludwika Waryńskiego',
 'Waryńskiego': 'Ludwika Waryńskiego',
 'Wasilewskiej': 'Wandy Wasilewskiej',
 'Waszyngtona Jerzego': 'Jerzego Waszyngtona',
 'Walasiewiczówny S.': 'Stanisławy Walasiewiczówny',
 'Wańkowicza Melchiora': 'Melchiora Wańkowicza',
 'Wejhera Jakuba': 'Jakuba Wejhera',
 'Wieniawskiego Henryka': 'Henryka Wieniawskiego',
 'Wieniawskiego': 'Henryka Wieniawskiego',
 '"Wira" Bartoszewskiego': 'Konrada "Wira" Bartoszewskiego',
 'Witosa': 'Wincentego Witosa',
 'Witosa Wincentego': 'Wincentego Witosa',
 'Witosa W.': 'Wincentego Witosa',
 'Wołodyjowskiego Michała': 'Michała Wołodyjowskiego',
 'Wojciecha św.': 'świętego Wojciecha',
 'Wróblewskiego Walerego': 'Walerego Wróblewskiego',
 'Wybickiego J. gen.': 'Generała Józefa Wybickiego',
 'Wybickiego Józefa': 'Józefa Wybickiego',
 'Wybickiego': 'Józefa Wybickiego',
 'Wyczółkowskiego Leona': 'Leona Wyczółkowskiego',
 'Wyki Kazimierza': 'Kazimierza Wyki',
 'Wyspiańskiego S.': 'Stanisława Wyspiańskiego',
 'Wyspiańskiego Stanisława': 'Stanisława Wyspiańskiego',
 'Wyspiańskiego': 'Stanisława Wyspiańskiego',
 'Wyszyńskiego S. kard.': 'Kardynała Stefana Wyszyńskiego',
 'Wyszyńskiego S.': 'Kardynała Stefana Wyszyńskiego',
 'Wyszyńskiego Stefana': 'Stefana Wyszyńskiego',
 'Wyszyńskiego kard.': 'Kardynała Stefana Wyszyńskiego',
 'Zamenhofa Ludwika': 'Ludwika Zamenhofa',
 'Zana T.': 'Tomasza Zana',
 'Zana': 'Tomasza Zana',
 'Zelenay A.': 'Anny Zelenay',
 'Zapolskiej G.': 'Gabrieli Zapolskiej',
 'Zapolskiej': 'Gabrieli Zapolskiej',
 'Zaruskiego Mariusza': 'Mariusza Zaruskiego',
 'Zubrzyckiego Franciszka': 'Franciszka Zubrzyckiego',
 'Łopuskiego Edmunda': 'Edmunda Łopuskiego',
 'Łukasiewicza I.': 'Ignacego Łukasiewicza',
 'Łukasiewicza Ignacego': 'Ignacego Łukasiewicza',
 'Łukasińskiego W.': 'Waleriana Łukasińskiego',
 'Łukasińskiego Waleriana': 'Waleriana Łukasińskiego',
 'Łęckiej': 'Izabeli Łęckiej',
 'Ściegiennego Piotra': 'Piotra Ściegiennego',
 'Śliwińskiego Józefa': 'Józefa Śliwińskiego',
 'Śnieżka Adama': 'Adama Śnieżka',
 'Św. Ducha': 'Świętego Ducha',
 'Św. Floriana': 'Świętego Floriana',
 'Św. Huberta': 'Świętego Huberta',
 'Św. Jana': 'Świętego Jana',
 'Św. Kingi': 'Świętej Kingi',
 'Św. Marcina': 'Świętego Marcina',
 'Św. Marka': 'Świętego Marka',
 'Marcina św.': 'Świętego Marcina',
 'Św. Rozalii': 'Świętej Rozalii',
 'Św. Wojciecha': 'Świętego Wojciecha',
 'Świerczewskiego': 'Karola Świerczewskiego',
 'Świerczewskiego K. gen.': 'Generała Karola Świerczewskiego',
 'Świerczewskiego K.gen.': 'Generała Karola Świerczewskiego',
 'Żebrowskiego Michała': 'Michała Żebrowskiego',
 'Żeromskiego S.': 'Stefana Żeromskiego',
 'Żeromskiego Stefana': 'Stefana Żeromskiego',
 'Żeromskiego': 'Stefana Żeromskiego',
 'Żymierskiego': 'Generała Michała Roli-Żymierskiego',
 'Żółkiewskiego Stanisława': 'Stanisława Żółkiewskiego',
}
import sys
if sys.version_info.major == 2:
    addr_map = dict(map(lambda x: (x[0].decode('utf-8'), x[1].decode('utf-8')), addr_map.items()))
    from urllib2 import urlopen
else:
    from urllib.request import urlopen

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
    soup = BeautifulSoup(urlopen("http://www.stat.gov.pl/broker/access/prefile/listPreFiles.jspa"))
    fileLocation = soup.find('td', text="Katalog ulic").parent.find_all('a')[1]['href']
    dictionary_zip = zipfile.ZipFile(io.BytesIO(urlopen("http://www.stat.gov.pl/broker/access/prefile/" + fileLocation).read()))
    def get(elem, tag):
        col = elem.find("col[@name='%s']" % tag)
        if col.text:
            return col.text
        return ""

    tree = ET.fromstring(dictionary_zip.read("ULIC.xml"))
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
        new = fetcher()
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
            if not street.upper().startswith(teryt_entry.cecha.upper()) and \
                not street.upper().startswith(__CECHA_MAPPING.get(teryt_entry.cecha, '').upper()):
                __log.debug("Adding TERYT.CECHA=%s to street=%s (addr:street:sym_ul=%s)" % (__CECHA_MAPPING.get(teryt_entry.cecha, ''), street, symul))
                return "%s %s" % (__CECHA_MAPPING.get(teryt_entry.cecha, ''), street)
        return street

    try:
        ret = checkAndAddCecha(addr_map[strname])
        __log.info("mapping street %s -> %s, TERYT: %s (addr:street:sym_ul=%s) " % (strname, ret, teryt_entry.nazwa if teryt_entry else 'N/A', symul))
        return ret
    except KeyError:
        try:
            ret = __mapping_symul[symul]
            if len(ret) > 1:
                __log.info("Inconsitent mapping for addr:street:sym_ul = %s. Original value: %s, TERYT: %s, OSM values: %s. Leaving original value.", symul, strname, teryt_entry.nazwa if teryt_entry else 'N/A',  ", ".join(ret))
                return strname
            ret = checkAndAddCecha(next(iter(ret.keys()))) # check and add for first and only key
            if ret != strname:
                __log.info("mapping street %s -> %s, TERYT: %s (addr:street:sym_ul=%s) " % (strname, ret, teryt_entry.nazwa if teryt_entry else 'N/A', symul))
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
