import json

#Used to initialize json file, do not run again
#all json info in this file from https://realpython.com/python-json/
'''
data = {'gillian':[0]}
with open('highscores.json', 'w') as write_file:
    json.dump(data, write_file)
'''

#opens json file, initializes username, and displays previous high score
def gameStart(app):
    with open('highscores.json', 'r') as f:
        highscores = json.load(f)
    print('''
-----------------------------------------------
        ''')
    name = str(input('Enter your username, or a create a new one: '))
    app.name = name
    if name in highscores:
        print(f'Welcome Back, {name}!')
        scores = highscores[name]
        highscore = max(scores)
        plays = len(scores)
        sval = 's' if plays>1 else ''
        print(f'You have played Sands of Time {plays} time{sval}!')
        print(f'Your previous high score: {highscore}. Try to beat it!')
        
    else:
        print(f'Welcome, {name}')
    print('''
-----------------------------------------------
        ''')

#stores username and new score to json file, displays end info
def gameEnd(app):
    name = app.name
    with open('highscores.json', 'r') as f:
        highscores = json.load(f)
    print('''
-----------------------------------------------
        ''')
    if name in highscores:
        prevMaxScore = max(highscores[name])
        highscores[name].append(app.goldScore)
        if prevMaxScore > app.goldScore:
            print('You did not beat your previous high score. Better luck next time!')
        elif prevMaxScore == app.goldScore:
            print('You tied your previous best score! So close!')
        else:
            print('You achieved a new high score!')
    else:
        highscores[name] = [app.goldScore]
        print('Thanks for playing! Hope to see you again!')
    print('''
-----------------------------------------------
        ''')
    with open('highscores.json', 'w') as write_file:
        json.dump(highscores, write_file)
