data = {
'start': {
            'name': 'start',
            'question': 'Did your applicant apply for asylum in Germany?',
            'answer_type': 'select',
            'answers': ['Ja', 'Nein'],
            'checks': None,
            'rules': {
            'Ja': 'zwei',
            'Nein': 'end'
            }
          },

'zwei': {
            'name': 'zwei',
            'question': 'Does your applicant have the obligation to live in refugee housing?',
            'answer_type': 'select',
            'answers': ['Ja', 'Nein'],
            'checks': None,
            'rules': {
            'Ja': 'end',
            'Nein': 'drei'
            }
          },

'drei': {
            'name': 'drei',
            'question': 'Kommt der Bewerber aus der EU oder aus Bosnien-Herzegowina, Mazedonien, Serbien, Montenegro, Albanien, Kosovo, Ghana oder Senegal?',
            'answer_type': 'select',
            'answers': ['Ja', 'Nein'],
            'checks': None,
            'rules': {
            'Ja': 'check_1',
            'Nein': 'vier'
            }
          },
'vier': {
            'name': '',
            'question': 'Wie lange ist der Bewerber schon in Deutschland?',
            'answer_type': 'select',
            'answers': ['Unter drei Monate', 'Drei Monate bis vier Jahre', 'Ueber vier Jahre'],
            'checks': None,
            'rules': {
            'Unter drei Monate': 'end',
            'Drei Monate bis vier Jahre': 'fuenf',
            'Ueber vier Jahre': 'success'
            }
          },
'check_1': {
            'name': 'drei',
            'question': 'Hat der Bewerber seinen Asyalantrag vor dem 31.08.2015 gestellt?',
            'answer_type': 'select',
            'answers': ['Ja', 'Nein'],
            'checks': None,
            'rules': {
            'Ja': 'vier',
            'Nein': 'end'
            }
          },
'fuenf': {
            'name': 'fuenf',
            'question': 'Welche Aufenthaltserlaubnis hat der Bewerber?',
            'answer_type': 'select',
            'answers': ['Arbeitserlaubnis', 'Gestattung', 'Duldung'],
            'checks': None,
            'rules': {
            'Arbeitserlaubnis': 'success',
            'Duldung': 'end',
            'Gestattung' : 'sechs'
            }
          },

'sechs': {
            'name': 'fuenf',
            'question': 'Welche Art von Beschaeftigung wollen Sie anbieten?',
            'answer_type': 'select',
            'answers': ['Praktikum', 'Freiwilligendienst', 'Abhaengige Beschaeftigung'],
            'checks': None,
            'rules': {
            'Praktikum': 'success',
            'Freiwilligendienst': 'success',
            'Abhaengige Beschaeftigung' : 'sieben'
            }
          },
'sieben': {
            'name': 'drei',
            'question': 'Hat der Bewerber einen Hochschulabschluss?',
            'answer_type': 'select',
            'answers': ['Ja', 'Nein'],
            'checks': None,
            'rules': {
            'Ja': 'vier',
            'Nein': 'end'
            }
          },
'acht': {
            'name': 'drei',
            'question': 'Hat der Bewerber einen Hochschulabschluss?',
            'answer_type': 'select',
            'answers': ['Ja', 'Nein'],
            'checks': None,
            'rules': {
            'Ja': 'success',
            'Nein': 'success'
            }
          },
'end': {
            'name': 'drei',
            'question': 'Leider kann der Bewerber nicht arbeiten. Schreibe /cancel um neuzustarten.',
            'answer_type': 'select',
            'answers': ['Ja', 'Nein'],
            'checks': None,
            'rules': {
            'Ja': 'success',
            'Nein': 'end'
            }
          },
'success': {
            'name': 'drei',
            'question': 'Der Bewerber darf arbeiten! Hier gibt es mehr Informationen. https://immigration-legaltech.herokuapp.com/nineth/results/5/results',
            'answer_type': 'select',
            'answers': ['/cancel', '/start'],
            'checks': None,
            'rules': {
            'Ja': 'success',
            'Nein': 'end'
            }
          }
    }
