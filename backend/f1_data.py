"""
Historical Formula 1 data (1950-2025).
Compact dataset with real champions and top drivers per season.
Ratings 60-100 are derived from real historical performance.
"""

# Format per season:
# year: {
#   "champion": str, "champion_team": str,
#   "constructors_champion": str,
#   "num_races": int,
#   "drivers": [ (name, team, rating), ... ]  # top ~10-14 drivers
# }

def _D(*args):
    return [(n, t, r) for n, t, r in args]

SEASONS = {
    1950: {"champion": "Giuseppe Farina", "champion_team": "Alfa Romeo", "constructors_champion": "Alfa Romeo", "num_races": 7,
        "drivers": _D(("Giuseppe Farina","Alfa Romeo",95),("Juan Manuel Fangio","Alfa Romeo",96),("Luigi Fagioli","Alfa Romeo",88),("Louis Rosier","Talbot-Lago",78),("Alberto Ascari","Ferrari",90),("Johnnie Parsons","Kurtis Kraft",76),("Bill Holland","Deidt",74),("Prince Bira","Maserati",70),("Reg Parnell","Alfa Romeo",80),("Louis Chiron","Maserati",72))},
    1951: {"champion": "Juan Manuel Fangio", "champion_team": "Alfa Romeo", "constructors_champion": "Ferrari", "num_races": 8,
        "drivers": _D(("Juan Manuel Fangio","Alfa Romeo",97),("Alberto Ascari","Ferrari",93),("Froilan Gonzalez","Ferrari",86),("Giuseppe Farina","Alfa Romeo",90),("Luigi Villoresi","Ferrari",82),("Piero Taruffi","Ferrari",80),("Felice Bonetto","Alfa Romeo",76),("Emmanuel de Graffenried","Alfa Romeo",72),("Louis Rosier","Talbot-Lago",70),("Reg Parnell","BRM",68))},
    1952: {"champion": "Alberto Ascari", "champion_team": "Ferrari", "constructors_champion": "Ferrari", "num_races": 8,
        "drivers": _D(("Alberto Ascari","Ferrari",98),("Giuseppe Farina","Ferrari",90),("Piero Taruffi","Ferrari",84),("Rudi Fischer","Ferrari",76),("Mike Hawthorn","Cooper",82),("Robert Manzon","Gordini",74),("Luigi Villoresi","Ferrari",80),("Jose Froilan Gonzalez","Maserati",83),("Ken Wharton","Frazer Nash",68),("Dennis Poore","Connaught",66))},
    1953: {"champion": "Alberto Ascari", "champion_team": "Ferrari", "constructors_champion": "Ferrari", "num_races": 9,
        "drivers": _D(("Alberto Ascari","Ferrari",97),("Juan Manuel Fangio","Maserati",94),("Giuseppe Farina","Ferrari",90),("Mike Hawthorn","Ferrari",85),("Luigi Villoresi","Ferrari",82),("Jose Froilan Gonzalez","Maserati",84),("Emmanuel de Graffenried","Maserati",72),("Felice Bonetto","Maserati",74),("Onofre Marimon","Maserati",76),("Louis Rosier","Ferrari",70))},
    1954: {"champion": "Juan Manuel Fangio", "champion_team": "Mercedes", "constructors_champion": "Mercedes", "num_races": 9,
        "drivers": _D(("Juan Manuel Fangio","Mercedes",98),("Jose Froilan Gonzalez","Ferrari",87),("Mike Hawthorn","Ferrari",84),("Maurice Trintignant","Ferrari",78),("Karl Kling","Mercedes",80),("Hans Herrmann","Mercedes",76),("Bill Vukovich","Kurtis Kraft",82),("Roberto Mieres","Maserati",74),("Luigi Musso","Maserati",78),("Sergio Mantovani","Maserati",72))},
    1955: {"champion": "Juan Manuel Fangio", "champion_team": "Mercedes", "constructors_champion": "Mercedes", "num_races": 7,
        "drivers": _D(("Juan Manuel Fangio","Mercedes",99),("Stirling Moss","Mercedes",93),("Eugenio Castellotti","Ferrari",80),("Maurice Trintignant","Ferrari",78),("Giuseppe Farina","Ferrari",82),("Piero Taruffi","Mercedes",76),("Bob Sweikert","Kurtis Kraft",74),("Luigi Musso","Maserati",77),("Jean Behra","Maserati",81),("Roberto Mieres","Maserati",72))},
    1956: {"champion": "Juan Manuel Fangio", "champion_team": "Ferrari", "constructors_champion": "Ferrari", "num_races": 8,
        "drivers": _D(("Juan Manuel Fangio","Ferrari",97),("Stirling Moss","Maserati",94),("Peter Collins","Ferrari",85),("Jean Behra","Maserati",81),("Pat Flaherty","Watson",76),("Eugenio Castellotti","Ferrari",80),("Paul Frere","Ferrari",74),("Francisco Godia","Maserati",70),("Jack Fairman","Connaught",68),("Cesare Perdisa","Maserati",72))},
    1957: {"champion": "Juan Manuel Fangio", "champion_team": "Maserati", "constructors_champion": "Maserati", "num_races": 8,
        "drivers": _D(("Juan Manuel Fangio","Maserati",99),("Stirling Moss","Vanwall",95),("Luigi Musso","Ferrari",83),("Mike Hawthorn","Ferrari",86),("Tony Brooks","Vanwall",84),("Harry Schell","Maserati",78),("Peter Collins","Ferrari",82),("Jean Behra","Maserati",80),("Sam Hanks","Salih",74),("Jim Rathmann","Epperly",72))},
    1958: {"champion": "Mike Hawthorn", "champion_team": "Ferrari", "constructors_champion": "Vanwall", "num_races": 11,
        "drivers": _D(("Mike Hawthorn","Ferrari",92),("Stirling Moss","Vanwall",96),("Tony Brooks","Vanwall",88),("Roy Salvadori","Cooper",82),("Peter Collins","Ferrari",84),("Harry Schell","BRM",78),("Maurice Trintignant","Cooper",80),("Luigi Musso","Ferrari",83),("Stuart Lewis-Evans","Vanwall",81),("Phil Hill","Ferrari",85))},
    1959: {"champion": "Jack Brabham", "champion_team": "Cooper", "constructors_champion": "Cooper", "num_races": 9,
        "drivers": _D(("Jack Brabham","Cooper",92),("Tony Brooks","Ferrari",89),("Stirling Moss","Cooper",95),("Phil Hill","Ferrari",86),("Maurice Trintignant","Cooper",78),("Bruce McLaren","Cooper",83),("Dan Gurney","Ferrari",81),("Jean Behra","Ferrari",80),("Cliff Allison","Ferrari",76),("Olivier Gendebien","Ferrari",74))},
    1960: {"champion": "Jack Brabham", "champion_team": "Cooper", "constructors_champion": "Cooper", "num_races": 10,
        "drivers": _D(("Jack Brabham","Cooper",94),("Bruce McLaren","Cooper",87),("Stirling Moss","Lotus",96),("Innes Ireland","Lotus",81),("Phil Hill","Ferrari",86),("Wolfgang von Trips","Ferrari",84),("Olivier Gendebien","Cooper",76),("Jim Clark","Lotus",89),("Graham Hill","BRM",83),("Richie Ginther","Ferrari",80))},
    1961: {"champion": "Phil Hill", "champion_team": "Ferrari", "constructors_champion": "Ferrari", "num_races": 8,
        "drivers": _D(("Phil Hill","Ferrari",93),("Wolfgang von Trips","Ferrari",89),("Stirling Moss","Lotus",95),("Dan Gurney","Porsche",84),("Richie Ginther","Ferrari",82),("Jim Clark","Lotus",90),("Innes Ireland","Lotus",78),("Jack Brabham","Cooper",88),("Bruce McLaren","Cooper",85),("Giancarlo Baghetti","Ferrari",80))},
    1962: {"champion": "Graham Hill", "champion_team": "BRM", "constructors_champion": "BRM", "num_races": 9,
        "drivers": _D(("Graham Hill","BRM",92),("Jim Clark","Lotus",95),("Bruce McLaren","Cooper",86),("John Surtees","Lola",84),("Dan Gurney","Porsche",83),("Phil Hill","Ferrari",85),("Tony Maggs","Cooper",78),("Richie Ginther","BRM",80),("Jack Brabham","Brabham",88),("Trevor Taylor","Lotus",76))},
    1963: {"champion": "Jim Clark", "champion_team": "Lotus", "constructors_champion": "Lotus", "num_races": 10,
        "drivers": _D(("Jim Clark","Lotus",99),("Graham Hill","BRM",90),("Richie Ginther","BRM",82),("John Surtees","Ferrari",87),("Dan Gurney","Brabham",84),("Bruce McLaren","Cooper",83),("Jack Brabham","Brabham",85),("Tony Maggs","Cooper",76),("Innes Ireland","BRP",74),("Lorenzo Bandini","Ferrari",78))},
    1964: {"champion": "John Surtees", "champion_team": "Ferrari", "constructors_champion": "Ferrari", "num_races": 10,
        "drivers": _D(("John Surtees","Ferrari",93),("Graham Hill","BRM",92),("Jim Clark","Lotus",96),("Lorenzo Bandini","Ferrari",81),("Richie Ginther","BRM",80),("Dan Gurney","Brabham",85),("Bruce McLaren","Cooper",83),("Jack Brabham","Brabham",84),("Peter Arundell","Lotus",76),("Jo Siffert","Brabham",74))},
    1965: {"champion": "Jim Clark", "champion_team": "Lotus", "constructors_champion": "Lotus", "num_races": 10,
        "drivers": _D(("Jim Clark","Lotus",99),("Graham Hill","BRM",91),("Jackie Stewart","BRM",89),("Dan Gurney","Brabham",85),("John Surtees","Ferrari",87),("Lorenzo Bandini","Ferrari",80),("Richie Ginther","Honda",78),("Mike Spence","Lotus",76),("Bruce McLaren","Cooper",82),("Jack Brabham","Brabham",84))},
    1966: {"champion": "Jack Brabham", "champion_team": "Brabham", "constructors_champion": "Brabham", "num_races": 9,
        "drivers": _D(("Jack Brabham","Brabham",92),("John Surtees","Ferrari",86),("Jochen Rindt","Cooper",84),("Denny Hulme","Brabham",86),("Graham Hill","BRM",88),("Jim Clark","Lotus",94),("Jackie Stewart","BRM",89),("Lorenzo Bandini","Ferrari",80),("Mike Parkes","Ferrari",78),("Ludovico Scarfiotti","Ferrari",76))},
    1967: {"champion": "Denny Hulme", "champion_team": "Brabham", "constructors_champion": "Brabham", "num_races": 11,
        "drivers": _D(("Denny Hulme","Brabham",90),("Jack Brabham","Brabham",89),("Jim Clark","Lotus",96),("John Surtees","Honda",84),("Chris Amon","Ferrari",85),("Pedro Rodriguez","Cooper",81),("Graham Hill","Lotus",88),("Dan Gurney","Eagle",82),("Jackie Stewart","BRM",90),("Mike Spence","BRM",76))},
    1968: {"champion": "Graham Hill", "champion_team": "Lotus", "constructors_champion": "Lotus", "num_races": 12,
        "drivers": _D(("Graham Hill","Lotus",90),("Jackie Stewart","Matra",93),("Denny Hulme","McLaren",86),("Jacky Ickx","Ferrari",84),("Bruce McLaren","McLaren",84),("Pedro Rodriguez","BRM",80),("Jo Siffert","Lotus",78),("John Surtees","Honda",82),("Jean-Pierre Beltoise","Matra",76),("Chris Amon","Ferrari",83))},
    1969: {"champion": "Jackie Stewart", "champion_team": "Matra", "constructors_champion": "Matra", "num_races": 11,
        "drivers": _D(("Jackie Stewart","Matra",97),("Jacky Ickx","Brabham",87),("Bruce McLaren","McLaren",83),("Jochen Rindt","Lotus",90),("Denny Hulme","McLaren",84),("Graham Hill","Lotus",85),("Piers Courage","Brabham",80),("Jo Siffert","Lotus",78),("Jack Brabham","Brabham",85),("John Surtees","BRM",81))},
    1970: {"champion": "Jochen Rindt", "champion_team": "Lotus", "constructors_champion": "Lotus", "num_races": 13,
        "drivers": _D(("Jochen Rindt","Lotus",96),("Jacky Ickx","Ferrari",89),("Clay Regazzoni","Ferrari",84),("Denny Hulme","McLaren",83),("Jack Brabham","Brabham",85),("Jackie Stewart","Tyrrell",94),("Jo Siffert","March",79),("Emerson Fittipaldi","Lotus",85),("Chris Amon","March",82),("Pedro Rodriguez","BRM",80))},
    1971: {"champion": "Jackie Stewart", "champion_team": "Tyrrell", "constructors_champion": "Tyrrell", "num_races": 11,
        "drivers": _D(("Jackie Stewart","Tyrrell",98),("Ronnie Peterson","March",84),("Francois Cevert","Tyrrell",83),("Jacky Ickx","Ferrari",87),("Jo Siffert","BRM",80),("Emerson Fittipaldi","Lotus",86),("Clay Regazzoni","Ferrari",82),("Mario Andretti","Ferrari",84),("Chris Amon","Matra",81),("Peter Gethin","BRM",76))},
    1972: {"champion": "Emerson Fittipaldi", "champion_team": "Lotus", "constructors_champion": "Lotus", "num_races": 12,
        "drivers": _D(("Emerson Fittipaldi","Lotus",95),("Jackie Stewart","Tyrrell",94),("Denny Hulme","McLaren",83),("Jacky Ickx","Ferrari",85),("Peter Revson","McLaren",81),("Ronnie Peterson","March",84),("Francois Cevert","Tyrrell",82),("Mike Hailwood","Surtees",78),("Clay Regazzoni","Ferrari",80),("Chris Amon","Matra",80))},
    1973: {"champion": "Jackie Stewart", "champion_team": "Tyrrell", "constructors_champion": "Lotus", "num_races": 15,
        "drivers": _D(("Jackie Stewart","Tyrrell",97),("Emerson Fittipaldi","Lotus",93),("Ronnie Peterson","Lotus",90),("Francois Cevert","Tyrrell",84),("Peter Revson","McLaren",83),("Denny Hulme","McLaren",82),("Carlos Reutemann","Brabham",84),("James Hunt","March",83),("Jacky Ickx","Ferrari",82),("Jean-Pierre Beltoise","BRM",76))},
    1974: {"champion": "Emerson Fittipaldi", "champion_team": "McLaren", "constructors_champion": "McLaren", "num_races": 15,
        "drivers": _D(("Emerson Fittipaldi","McLaren",94),("Clay Regazzoni","Ferrari",88),("Jody Scheckter","Tyrrell",89),("Niki Lauda","Ferrari",91),("Ronnie Peterson","Lotus",87),("Carlos Reutemann","Brabham",85),("Denny Hulme","McLaren",81),("James Hunt","Hesketh",84),("Patrick Depailler","Tyrrell",82),("Jean-Pierre Beltoise","BRM",76))},
    1975: {"champion": "Niki Lauda", "champion_team": "Ferrari", "constructors_champion": "Ferrari", "num_races": 14,
        "drivers": _D(("Niki Lauda","Ferrari",96),("Clay Regazzoni","Ferrari",85),("Emerson Fittipaldi","McLaren",91),("Jody Scheckter","Tyrrell",88),("James Hunt","Hesketh",86),("Carlos Reutemann","Brabham",85),("Carlos Pace","Brabham",83),("Patrick Depailler","Tyrrell",81),("Jochen Mass","McLaren",80),("Tom Pryce","Shadow",78))},
    1976: {"champion": "James Hunt", "champion_team": "McLaren", "constructors_champion": "Ferrari", "num_races": 16,
        "drivers": _D(("James Hunt","McLaren",93),("Niki Lauda","Ferrari",95),("Jody Scheckter","Tyrrell",88),("Patrick Depailler","Tyrrell",84),("Clay Regazzoni","Ferrari",83),("Mario Andretti","Lotus",86),("John Watson","Penske",82),("Jochen Mass","McLaren",80),("Gunnar Nilsson","Lotus",78),("Carlos Reutemann","Ferrari",84))},
    1977: {"champion": "Niki Lauda", "champion_team": "Ferrari", "constructors_champion": "Ferrari", "num_races": 17,
        "drivers": _D(("Niki Lauda","Ferrari",95),("Jody Scheckter","Wolf",90),("Mario Andretti","Lotus",93),("Carlos Reutemann","Ferrari",87),("James Hunt","McLaren",88),("Jochen Mass","McLaren",80),("Alan Jones","Shadow",84),("Patrick Depailler","Tyrrell",82),("Ronnie Peterson","Tyrrell",84),("Gunnar Nilsson","Lotus",81))},
    1978: {"champion": "Mario Andretti", "champion_team": "Lotus", "constructors_champion": "Lotus", "num_races": 16,
        "drivers": _D(("Mario Andretti","Lotus",96),("Ronnie Peterson","Lotus",92),("Carlos Reutemann","Ferrari",89),("Niki Lauda","Brabham",90),("Patrick Depailler","Tyrrell",83),("John Watson","Brabham",84),("Jody Scheckter","Wolf",85),("Jacques Laffite","Ligier",83),("Emerson Fittipaldi","Fittipaldi",82),("Gilles Villeneuve","Ferrari",89))},
    1979: {"champion": "Jody Scheckter", "champion_team": "Ferrari", "constructors_champion": "Ferrari", "num_races": 15,
        "drivers": _D(("Jody Scheckter","Ferrari",92),("Gilles Villeneuve","Ferrari",93),("Alan Jones","Williams",91),("Jacques Laffite","Ligier",85),("Clay Regazzoni","Williams",82),("Patrick Depailler","Ligier",83),("Carlos Reutemann","Lotus",85),("Rene Arnoux","Renault",83),("Jean-Pierre Jabouille","Renault",82),("Niki Lauda","Brabham",88))},
    1980: {"champion": "Alan Jones", "champion_team": "Williams", "constructors_champion": "Williams", "num_races": 14,
        "drivers": _D(("Alan Jones","Williams",94),("Nelson Piquet","Brabham",92),("Carlos Reutemann","Williams",88),("Jacques Laffite","Ligier",85),("Didier Pironi","Ligier",84),("Rene Arnoux","Renault",84),("Elio de Angelis","Lotus",81),("Gilles Villeneuve","Ferrari",90),("Jody Scheckter","Ferrari",84),("John Watson","McLaren",80))},
    1981: {"champion": "Nelson Piquet", "champion_team": "Brabham", "constructors_champion": "Williams", "num_races": 15,
        "drivers": _D(("Nelson Piquet","Brabham",94),("Carlos Reutemann","Williams",92),("Alan Jones","Williams",89),("Jacques Laffite","Ligier",86),("Alain Prost","Renault",90),("John Watson","McLaren",85),("Gilles Villeneuve","Ferrari",89),("Elio de Angelis","Lotus",82),("Rene Arnoux","Renault",83),("Nigel Mansell","Lotus",81))},
    1982: {"champion": "Keke Rosberg", "champion_team": "Williams", "constructors_champion": "Ferrari", "num_races": 16,
        "drivers": _D(("Keke Rosberg","Williams",90),("Didier Pironi","Ferrari",89),("John Watson","McLaren",86),("Alain Prost","Renault",92),("Niki Lauda","McLaren",89),("Rene Arnoux","Renault",84),("Michele Alboreto","Tyrrell",83),("Patrick Tambay","Ferrari",85),("Nelson Piquet","Brabham",90),("Elio de Angelis","Lotus",83))},
    1983: {"champion": "Nelson Piquet", "champion_team": "Brabham", "constructors_champion": "Ferrari", "num_races": 15,
        "drivers": _D(("Nelson Piquet","Brabham",94),("Alain Prost","Renault",93),("Rene Arnoux","Ferrari",87),("Patrick Tambay","Ferrari",86),("Keke Rosberg","Williams",86),("John Watson","McLaren",83),("Eddie Cheever","Renault",82),("Andrea de Cesaris","Alfa Romeo",80),("Niki Lauda","McLaren",89),("Nigel Mansell","Lotus",84))},
    1984: {"champion": "Niki Lauda", "champion_team": "McLaren", "constructors_champion": "McLaren", "num_races": 16,
        "drivers": _D(("Niki Lauda","McLaren",93),("Alain Prost","McLaren",96),("Elio de Angelis","Lotus",85),("Michele Alboreto","Ferrari",86),("Nelson Piquet","Brabham",90),("Rene Arnoux","Ferrari",84),("Derek Warwick","Renault",83),("Keke Rosberg","Williams",87),("Nigel Mansell","Lotus",85),("Ayrton Senna","Toleman",90))},
    1985: {"champion": "Alain Prost", "champion_team": "McLaren", "constructors_champion": "McLaren", "num_races": 16,
        "drivers": _D(("Alain Prost","McLaren",97),("Michele Alboreto","Ferrari",89),("Keke Rosberg","Williams",88),("Ayrton Senna","Lotus",93),("Elio de Angelis","Lotus",85),("Nigel Mansell","Williams",88),("Stefan Johansson","Ferrari",83),("Nelson Piquet","Brabham",89),("Jacques Laffite","Ligier",82),("Niki Lauda","McLaren",89))},
    1986: {"champion": "Alain Prost", "champion_team": "McLaren", "constructors_champion": "Williams", "num_races": 16,
        "drivers": _D(("Alain Prost","McLaren",96),("Nigel Mansell","Williams",93),("Nelson Piquet","Williams",92),("Ayrton Senna","Lotus",94),("Stefan Johansson","Ferrari",83),("Keke Rosberg","McLaren",87),("Rene Arnoux","Ligier",81),("Michele Alboreto","Ferrari",84),("Jacques Laffite","Ligier",80),("Gerhard Berger","Benetton",83))},
    1987: {"champion": "Nelson Piquet", "champion_team": "Williams", "constructors_champion": "Williams", "num_races": 16,
        "drivers": _D(("Nelson Piquet","Williams",94),("Nigel Mansell","Williams",93),("Ayrton Senna","Lotus",95),("Alain Prost","McLaren",95),("Gerhard Berger","Ferrari",87),("Stefan Johansson","McLaren",83),("Michele Alboreto","Ferrari",83),("Thierry Boutsen","Benetton",82),("Teo Fabi","Benetton",80),("Eddie Cheever","Arrows",78))},
    1988: {"champion": "Ayrton Senna", "champion_team": "McLaren", "constructors_champion": "McLaren", "num_races": 16,
        "drivers": _D(("Ayrton Senna","McLaren",98),("Alain Prost","McLaren",97),("Gerhard Berger","Ferrari",88),("Thierry Boutsen","Benetton",84),("Michele Alboreto","Ferrari",84),("Nelson Piquet","Lotus",89),("Ivan Capelli","March",82),("Derek Warwick","Arrows",81),("Nigel Mansell","Williams",90),("Alessandro Nannini","Benetton",83))},
    1989: {"champion": "Alain Prost", "champion_team": "McLaren", "constructors_champion": "McLaren", "num_races": 16,
        "drivers": _D(("Alain Prost","McLaren",96),("Ayrton Senna","McLaren",98),("Riccardo Patrese","Williams",86),("Nigel Mansell","Ferrari",92),("Thierry Boutsen","Williams",85),("Alessandro Nannini","Benetton",85),("Gerhard Berger","Ferrari",87),("Nelson Piquet","Lotus",87),("Jean Alesi","Tyrrell",84),("Derek Warwick","Arrows",80))},
    1990: {"champion": "Ayrton Senna", "champion_team": "McLaren", "constructors_champion": "McLaren", "num_races": 16,
        "drivers": _D(("Ayrton Senna","McLaren",98),("Alain Prost","Ferrari",96),("Nelson Piquet","Benetton",89),("Gerhard Berger","McLaren",88),("Nigel Mansell","Ferrari",92),("Thierry Boutsen","Williams",84),("Riccardo Patrese","Williams",86),("Alessandro Nannini","Benetton",84),("Jean Alesi","Tyrrell",85),("Ivan Capelli","Leyton House",82))},
    1991: {"champion": "Ayrton Senna", "champion_team": "McLaren", "constructors_champion": "McLaren", "num_races": 16,
        "drivers": _D(("Ayrton Senna","McLaren",99),("Nigel Mansell","Williams",93),("Riccardo Patrese","Williams",87),("Gerhard Berger","McLaren",88),("Alain Prost","Ferrari",93),("Nelson Piquet","Benetton",87),("Jean Alesi","Ferrari",86),("Stefano Modena","Tyrrell",81),("Andrea de Cesaris","Jordan",78),("Michael Schumacher","Benetton",92))},
    1992: {"champion": "Nigel Mansell", "champion_team": "Williams", "constructors_champion": "Williams", "num_races": 16,
        "drivers": _D(("Nigel Mansell","Williams",97),("Riccardo Patrese","Williams",88),("Michael Schumacher","Benetton",94),("Ayrton Senna","McLaren",96),("Gerhard Berger","McLaren",87),("Martin Brundle","Benetton",84),("Jean Alesi","Ferrari",85),("Mika Hakkinen","Lotus",84),("Andrea de Cesaris","Tyrrell",78),("Michele Alboreto","Footwork",78))},
    1993: {"champion": "Alain Prost", "champion_team": "Williams", "constructors_champion": "Williams", "num_races": 16,
        "drivers": _D(("Alain Prost","Williams",96),("Damon Hill","Williams",89),("Ayrton Senna","McLaren",97),("Michael Schumacher","Benetton",94),("Riccardo Patrese","Benetton",85),("Jean Alesi","Ferrari",84),("Martin Brundle","Ligier",82),("Gerhard Berger","Ferrari",86),("Johnny Herbert","Lotus",82),("Mark Blundell","Ligier",78))},
    1994: {"champion": "Michael Schumacher", "champion_team": "Benetton", "constructors_champion": "Williams", "num_races": 16,
        "drivers": _D(("Michael Schumacher","Benetton",97),("Damon Hill","Williams",91),("Gerhard Berger","Ferrari",86),("Mika Hakkinen","McLaren",87),("Jean Alesi","Ferrari",84),("Rubens Barrichello","Jordan",84),("Martin Brundle","McLaren",82),("David Coulthard","Williams",84),("Nigel Mansell","Williams",90),("Nicola Larini","Ferrari",76))},
    1995: {"champion": "Michael Schumacher", "champion_team": "Benetton", "constructors_champion": "Benetton", "num_races": 17,
        "drivers": _D(("Michael Schumacher","Benetton",98),("Damon Hill","Williams",90),("David Coulthard","Williams",87),("Johnny Herbert","Benetton",84),("Jean Alesi","Ferrari",85),("Gerhard Berger","Ferrari",85),("Mika Hakkinen","McLaren",88),("Olivier Panis","Ligier",82),("Heinz-Harald Frentzen","Sauber",83),("Mark Blundell","McLaren",78))},
    1996: {"champion": "Damon Hill", "champion_team": "Williams", "constructors_champion": "Williams", "num_races": 16,
        "drivers": _D(("Damon Hill","Williams",93),("Jacques Villeneuve","Williams",90),("Michael Schumacher","Ferrari",97),("Jean Alesi","Benetton",85),("Mika Hakkinen","McLaren",87),("Gerhard Berger","Benetton",84),("David Coulthard","McLaren",85),("Rubens Barrichello","Jordan",82),("Olivier Panis","Ligier",81),("Eddie Irvine","Ferrari",82))},
    1997: {"champion": "Jacques Villeneuve", "champion_team": "Williams", "constructors_champion": "Williams", "num_races": 17,
        "drivers": _D(("Jacques Villeneuve","Williams",93),("Heinz-Harald Frentzen","Williams",85),("Michael Schumacher","Ferrari",96),("Mika Hakkinen","McLaren",89),("David Coulthard","McLaren",86),("Jean Alesi","Benetton",83),("Gerhard Berger","Benetton",83),("Eddie Irvine","Ferrari",83),("Giancarlo Fisichella","Jordan",84),("Olivier Panis","Prost",80))},
    1998: {"champion": "Mika Hakkinen", "champion_team": "McLaren", "constructors_champion": "McLaren", "num_races": 16,
        "drivers": _D(("Mika Hakkinen","McLaren",95),("Michael Schumacher","Ferrari",97),("David Coulthard","McLaren",87),("Eddie Irvine","Ferrari",84),("Jacques Villeneuve","Williams",86),("Damon Hill","Jordan",85),("Heinz-Harald Frentzen","Williams",83),("Alexander Wurz","Benetton",81),("Giancarlo Fisichella","Benetton",83),("Ralf Schumacher","Jordan",82))},
    1999: {"champion": "Mika Hakkinen", "champion_team": "McLaren", "constructors_champion": "Ferrari", "num_races": 16,
        "drivers": _D(("Mika Hakkinen","McLaren",95),("Eddie Irvine","Ferrari",88),("Heinz-Harald Frentzen","Jordan",86),("David Coulthard","McLaren",87),("Michael Schumacher","Ferrari",97),("Ralf Schumacher","Williams",83),("Rubens Barrichello","Stewart",84),("Johnny Herbert","Stewart",81),("Giancarlo Fisichella","Benetton",82),("Mika Salo","Ferrari",80))},
    2000: {"champion": "Michael Schumacher", "champion_team": "Ferrari", "constructors_champion": "Ferrari", "num_races": 17,
        "drivers": _D(("Michael Schumacher","Ferrari",97),("Mika Hakkinen","McLaren",95),("David Coulthard","McLaren",89),("Rubens Barrichello","Ferrari",88),("Ralf Schumacher","Williams",85),("Giancarlo Fisichella","Benetton",83),("Jacques Villeneuve","BAR",83),("Jenson Button","Williams",83),("Heinz-Harald Frentzen","Jordan",83),("Jarno Trulli","Jordan",82))},
    2001: {"champion": "Michael Schumacher", "champion_team": "Ferrari", "constructors_champion": "Ferrari", "num_races": 17,
        "drivers": _D(("Michael Schumacher","Ferrari",98),("David Coulthard","McLaren",89),("Rubens Barrichello","Ferrari",87),("Ralf Schumacher","Williams",86),("Mika Hakkinen","McLaren",93),("Juan Pablo Montoya","Williams",88),("Nick Heidfeld","Sauber",82),("Jacques Villeneuve","BAR",82),("Jarno Trulli","Jordan",82),("Kimi Raikkonen","Sauber",85))},
    2002: {"champion": "Michael Schumacher", "champion_team": "Ferrari", "constructors_champion": "Ferrari", "num_races": 17,
        "drivers": _D(("Michael Schumacher","Ferrari",99),("Rubens Barrichello","Ferrari",90),("Juan Pablo Montoya","Williams",89),("Ralf Schumacher","Williams",86),("David Coulthard","McLaren",87),("Kimi Raikkonen","McLaren",89),("Jenson Button","Renault",83),("Jarno Trulli","Renault",82),("Eddie Irvine","Jaguar",80),("Nick Heidfeld","Sauber",81))},
    2003: {"champion": "Michael Schumacher", "champion_team": "Ferrari", "constructors_champion": "Ferrari", "num_races": 16,
        "drivers": _D(("Michael Schumacher","Ferrari",97),("Kimi Raikkonen","McLaren",93),("Juan Pablo Montoya","Williams",90),("Rubens Barrichello","Ferrari",88),("Ralf Schumacher","Williams",86),("Fernando Alonso","Renault",90),("David Coulthard","McLaren",86),("Jarno Trulli","Renault",84),("Jenson Button","BAR",83),("Mark Webber","Jaguar",83))},
    2004: {"champion": "Michael Schumacher", "champion_team": "Ferrari", "constructors_champion": "Ferrari", "num_races": 18,
        "drivers": _D(("Michael Schumacher","Ferrari",99),("Rubens Barrichello","Ferrari",89),("Jenson Button","BAR",86),("Fernando Alonso","Renault",90),("Juan Pablo Montoya","Williams",87),("Jarno Trulli","Renault",83),("Kimi Raikkonen","McLaren",91),("Takuma Sato","BAR",82),("Ralf Schumacher","Williams",84),("David Coulthard","McLaren",84))},
    2005: {"champion": "Fernando Alonso", "champion_team": "Renault", "constructors_champion": "Renault", "num_races": 19,
        "drivers": _D(("Fernando Alonso","Renault",96),("Kimi Raikkonen","McLaren",94),("Michael Schumacher","Ferrari",94),("Juan Pablo Montoya","McLaren",88),("Giancarlo Fisichella","Renault",84),("Ralf Schumacher","Toyota",84),("Jarno Trulli","Toyota",83),("Rubens Barrichello","Ferrari",84),("Jenson Button","BAR",84),("Mark Webber","Williams",82))},
    2006: {"champion": "Fernando Alonso", "champion_team": "Renault", "constructors_champion": "Renault", "num_races": 18,
        "drivers": _D(("Fernando Alonso","Renault",97),("Michael Schumacher","Ferrari",96),("Felipe Massa","Ferrari",87),("Giancarlo Fisichella","Renault",84),("Kimi Raikkonen","McLaren",92),("Jenson Button","Honda",86),("Rubens Barrichello","Honda",83),("Juan Pablo Montoya","McLaren",85),("Ralf Schumacher","Toyota",82),("Nick Heidfeld","BMW Sauber",83))},
    2007: {"champion": "Kimi Raikkonen", "champion_team": "Ferrari", "constructors_champion": "Ferrari", "num_races": 17,
        "drivers": _D(("Kimi Raikkonen","Ferrari",95),("Lewis Hamilton","McLaren",93),("Fernando Alonso","McLaren",95),("Felipe Massa","Ferrari",88),("Nick Heidfeld","BMW Sauber",84),("Robert Kubica","BMW Sauber",85),("Heikki Kovalainen","Renault",83),("Giancarlo Fisichella","Renault",82),("Nico Rosberg","Williams",83),("David Coulthard","Red Bull",81))},
    2008: {"champion": "Lewis Hamilton", "champion_team": "McLaren", "constructors_champion": "Ferrari", "num_races": 18,
        "drivers": _D(("Lewis Hamilton","McLaren",95),("Felipe Massa","Ferrari",94),("Kimi Raikkonen","Ferrari",92),("Robert Kubica","BMW Sauber",88),("Fernando Alonso","Renault",93),("Nick Heidfeld","BMW Sauber",84),("Heikki Kovalainen","McLaren",84),("Sebastian Vettel","Toro Rosso",88),("Jarno Trulli","Toyota",82),("Timo Glock","Toyota",81))},
    2009: {"champion": "Jenson Button", "champion_team": "Brawn", "constructors_champion": "Brawn", "num_races": 17,
        "drivers": _D(("Jenson Button","Brawn",92),("Sebastian Vettel","Red Bull",93),("Rubens Barrichello","Brawn",87),("Mark Webber","Red Bull",87),("Lewis Hamilton","McLaren",94),("Kimi Raikkonen","Ferrari",90),("Nico Rosberg","Williams",85),("Jarno Trulli","Toyota",83),("Fernando Alonso","Renault",92),("Timo Glock","Toyota",82))},
    2010: {"champion": "Sebastian Vettel", "champion_team": "Red Bull", "constructors_champion": "Red Bull", "num_races": 19,
        "drivers": _D(("Sebastian Vettel","Red Bull",96),("Fernando Alonso","Ferrari",95),("Mark Webber","Red Bull",89),("Lewis Hamilton","McLaren",94),("Jenson Button","McLaren",89),("Felipe Massa","Ferrari",86),("Nico Rosberg","Mercedes",86),("Robert Kubica","Renault",88),("Michael Schumacher","Mercedes",89),("Rubens Barrichello","Williams",83))},
    2011: {"champion": "Sebastian Vettel", "champion_team": "Red Bull", "constructors_champion": "Red Bull", "num_races": 19,
        "drivers": _D(("Sebastian Vettel","Red Bull",99),("Jenson Button","McLaren",90),("Mark Webber","Red Bull",88),("Fernando Alonso","Ferrari",95),("Lewis Hamilton","McLaren",93),("Felipe Massa","Ferrari",85),("Nico Rosberg","Mercedes",87),("Michael Schumacher","Mercedes",87),("Adrian Sutil","Force India",83),("Vitaly Petrov","Renault",81))},
    2012: {"champion": "Sebastian Vettel", "champion_team": "Red Bull", "constructors_champion": "Red Bull", "num_races": 20,
        "drivers": _D(("Sebastian Vettel","Red Bull",97),("Fernando Alonso","Ferrari",96),("Kimi Raikkonen","Lotus",91),("Lewis Hamilton","McLaren",94),("Jenson Button","McLaren",89),("Mark Webber","Red Bull",88),("Felipe Massa","Ferrari",85),("Romain Grosjean","Lotus",85),("Nico Rosberg","Mercedes",87),("Sergio Perez","Sauber",85))},
    2013: {"champion": "Sebastian Vettel", "champion_team": "Red Bull", "constructors_champion": "Red Bull", "num_races": 19,
        "drivers": _D(("Sebastian Vettel","Red Bull",99),("Fernando Alonso","Ferrari",95),("Mark Webber","Red Bull",88),("Lewis Hamilton","Mercedes",95),("Kimi Raikkonen","Lotus",90),("Nico Rosberg","Mercedes",88),("Romain Grosjean","Lotus",86),("Felipe Massa","Ferrari",84),("Jenson Button","McLaren",87),("Nico Hulkenberg","Sauber",85))},
    2014: {"champion": "Lewis Hamilton", "champion_team": "Mercedes", "constructors_champion": "Mercedes", "num_races": 19,
        "drivers": _D(("Lewis Hamilton","Mercedes",97),("Nico Rosberg","Mercedes",93),("Daniel Ricciardo","Red Bull",90),("Valtteri Bottas","Williams",86),("Sebastian Vettel","Red Bull",92),("Fernando Alonso","Ferrari",92),("Felipe Massa","Williams",85),("Jenson Button","McLaren",84),("Nico Hulkenberg","Force India",85),("Sergio Perez","Force India",84))},
    2015: {"champion": "Lewis Hamilton", "champion_team": "Mercedes", "constructors_champion": "Mercedes", "num_races": 19,
        "drivers": _D(("Lewis Hamilton","Mercedes",98),("Nico Rosberg","Mercedes",92),("Sebastian Vettel","Ferrari",94),("Kimi Raikkonen","Ferrari",89),("Valtteri Bottas","Williams",87),("Felipe Massa","Williams",85),("Daniil Kvyat","Red Bull",83),("Daniel Ricciardo","Red Bull",89),("Max Verstappen","Toro Rosso",88),("Sergio Perez","Force India",84))},
    2016: {"champion": "Nico Rosberg", "champion_team": "Mercedes", "constructors_champion": "Mercedes", "num_races": 21,
        "drivers": _D(("Nico Rosberg","Mercedes",95),("Lewis Hamilton","Mercedes",97),("Daniel Ricciardo","Red Bull",90),("Sebastian Vettel","Ferrari",93),("Max Verstappen","Red Bull",92),("Kimi Raikkonen","Ferrari",89),("Sergio Perez","Force India",85),("Valtteri Bottas","Williams",86),("Nico Hulkenberg","Force India",85),("Fernando Alonso","McLaren",89))},
    2017: {"champion": "Lewis Hamilton", "champion_team": "Mercedes", "constructors_champion": "Mercedes", "num_races": 20,
        "drivers": _D(("Lewis Hamilton","Mercedes",97),("Sebastian Vettel","Ferrari",95),("Valtteri Bottas","Mercedes",89),("Kimi Raikkonen","Ferrari",88),("Daniel Ricciardo","Red Bull",90),("Max Verstappen","Red Bull",93),("Sergio Perez","Force India",85),("Esteban Ocon","Force India",84),("Carlos Sainz","Toro Rosso",84),("Nico Hulkenberg","Renault",85))},
    2018: {"champion": "Lewis Hamilton", "champion_team": "Mercedes", "constructors_champion": "Mercedes", "num_races": 21,
        "drivers": _D(("Lewis Hamilton","Mercedes",98),("Sebastian Vettel","Ferrari",94),("Kimi Raikkonen","Ferrari",88),("Max Verstappen","Red Bull",95),("Valtteri Bottas","Mercedes",89),("Daniel Ricciardo","Red Bull",89),("Nico Hulkenberg","Renault",85),("Sergio Perez","Force India",85),("Kevin Magnussen","Haas",83),("Fernando Alonso","McLaren",88))},
    2019: {"champion": "Lewis Hamilton", "champion_team": "Mercedes", "constructors_champion": "Mercedes", "num_races": 21,
        "drivers": _D(("Lewis Hamilton","Mercedes",98),("Valtteri Bottas","Mercedes",90),("Max Verstappen","Red Bull",96),("Charles Leclerc","Ferrari",92),("Sebastian Vettel","Ferrari",92),("Carlos Sainz","McLaren",85),("Pierre Gasly","Red Bull",83),("Alexander Albon","Toro Rosso",83),("Daniel Ricciardo","Renault",87),("Sergio Perez","Racing Point",85))},
    2020: {"champion": "Lewis Hamilton", "champion_team": "Mercedes", "constructors_champion": "Mercedes", "num_races": 17,
        "drivers": _D(("Lewis Hamilton","Mercedes",99),("Valtteri Bottas","Mercedes",90),("Max Verstappen","Red Bull",96),("Sergio Perez","Racing Point",86),("Daniel Ricciardo","Renault",88),("Carlos Sainz","McLaren",86),("Alexander Albon","Red Bull",83),("Charles Leclerc","Ferrari",91),("Lando Norris","McLaren",87),("Pierre Gasly","AlphaTauri",86))},
    2021: {"champion": "Max Verstappen", "champion_team": "Red Bull", "constructors_champion": "Mercedes", "num_races": 22,
        "drivers": _D(("Max Verstappen","Red Bull",98),("Lewis Hamilton","Mercedes",97),("Valtteri Bottas","Mercedes",89),("Sergio Perez","Red Bull",87),("Carlos Sainz","Ferrari",88),("Lando Norris","McLaren",90),("Charles Leclerc","Ferrari",90),("Daniel Ricciardo","McLaren",85),("Pierre Gasly","AlphaTauri",86),("Fernando Alonso","Alpine",88))},
    2022: {"champion": "Max Verstappen", "champion_team": "Red Bull", "constructors_champion": "Red Bull", "num_races": 22,
        "drivers": _D(("Max Verstappen","Red Bull",99),("Charles Leclerc","Ferrari",93),("Sergio Perez","Red Bull",89),("George Russell","Mercedes",89),("Carlos Sainz","Ferrari",88),("Lewis Hamilton","Mercedes",92),("Lando Norris","McLaren",88),("Esteban Ocon","Alpine",85),("Fernando Alonso","Alpine",87),("Valtteri Bottas","Alfa Romeo",85))},
    2023: {"champion": "Max Verstappen", "champion_team": "Red Bull", "constructors_champion": "Red Bull", "num_races": 22,
        "drivers": _D(("Max Verstappen","Red Bull",99),("Sergio Perez","Red Bull",88),("Lewis Hamilton","Mercedes",92),("Fernando Alonso","Aston Martin",89),("Charles Leclerc","Ferrari",92),("Lando Norris","McLaren",91),("Carlos Sainz","Ferrari",88),("George Russell","Mercedes",88),("Oscar Piastri","McLaren",87),("Lance Stroll","Aston Martin",82))},
    2024: {"champion": "Max Verstappen", "champion_team": "Red Bull", "constructors_champion": "McLaren", "num_races": 24,
        "drivers": _D(("Max Verstappen","Red Bull",98),("Lando Norris","McLaren",93),("Charles Leclerc","Ferrari",93),("Oscar Piastri","McLaren",91),("Carlos Sainz","Ferrari",90),("George Russell","Mercedes",89),("Lewis Hamilton","Mercedes",91),("Sergio Perez","Red Bull",83),("Fernando Alonso","Aston Martin",88),("Nico Hulkenberg","Haas",83))},
    2025: {"champion": "Lando Norris", "champion_team": "McLaren", "constructors_champion": "McLaren", "num_races": 24,
        "drivers": _D(("Lando Norris","McLaren",96),("Oscar Piastri","McLaren",95),("Max Verstappen","Red Bull",97),("George Russell","Mercedes",90),("Charles Leclerc","Ferrari",92),("Lewis Hamilton","Ferrari",91),("Andrea Kimi Antonelli","Mercedes",87),("Fernando Alonso","Aston Martin",86),("Carlos Sainz","Williams",88),("Alexander Albon","Williams",84))},
}

# Iconic circuits pool for each era. We select a subset of size num_races.
CIRCUITS_BY_ERA = {
    (1950, 1969): ["Silverstone","Monaco","Indianapolis","Spa-Francorchamps","Reims","Monza","Nurburgring","Zandvoort","Aintree","Sebring","Watkins Glen","East London","Riverside","Rouen","Mexico City","Kyalami","Clermont-Ferrand","Brands Hatch"],
    (1970, 1989): ["Kyalami","Jarama","Long Beach","Interlagos","Imola","Zolder","Monaco","Detroit","Montreal","Paul Ricard","Silverstone","Hockenheim","Osterreichring","Zandvoort","Monza","Estoril","Suzuka","Adelaide","Nurburgring"],
    (1990, 2005): ["Interlagos","Melbourne","Sepang","Sakhir","Imola","Barcelona","Monaco","Montreal","Nurburgring","Magny-Cours","Silverstone","Hockenheim","Hungaroring","Spa-Francorchamps","Monza","Indianapolis","Shanghai","Suzuka","Estoril","Adelaide","Buenos Aires","Kyalami","Istanbul"],
    (2006, 2025): ["Sakhir","Jeddah","Melbourne","Suzuka","Shanghai","Miami","Imola","Monaco","Barcelona","Montreal","Spielberg","Silverstone","Hungaroring","Spa-Francorchamps","Zandvoort","Monza","Baku","Marina Bay","Austin","Mexico City","Interlagos","Las Vegas","Losail","Yas Marina","Hockenheim","Nurburgring","Sochi","Istanbul","Paul Ricard","Portimao","Mugello","Sepang"],
}

def get_circuits_for_year(year: int, num: int):
    for (start, end), pool in CIRCUITS_BY_ERA.items():
        if start <= year <= end:
            # deterministic selection: take first num from pool (padded if needed)
            selected = []
            i = 0
            while len(selected) < num:
                selected.append(pool[i % len(pool)])
                i += 1
            return selected
    return ["Silverstone"] * num


def get_all_years():
    return sorted(SEASONS.keys())


def get_season(year: int):
    return SEASONS.get(year)
