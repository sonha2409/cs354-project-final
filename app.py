from flask import Flask, request, render_template_string
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Time, text
from sqlalchemy.orm import relationship 
from models import db, Player, Ranking
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tennis.db'
db.init_app(app)
engine = create_engine('sqlite:///tennis.db', isolation_level="SERIALIZABLE")
Session = sessionmaker(bind=engine)



# Template strings to render HTML pages
ADD_PLAYER_FORM = '''
<!doctype html>
<html lang="en">
<head>
    <title>Add Player</title>
    <!-- Include Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-5">
        <h2 class="mb-4">Add a New Tennis Player</h2>
        <form method="post" action="/add_player">
            <div class="form-group">
                <label for="firstname">First Name</label>
                <input type="text" class="form-control" name="firstname" id="firstname" required>
            </div>
            <div class="form-group">
                <label for="lastname">Last name</label>
                <input type="text" class="form-control" name="lastname" id="lastname" required>
            </div>
            <div class="form-group">
                <label for="hand">Hand</label>
                <select class="form-control" name="hand" id="hand">
                    <option value="L">Left</option>
                    <option value="R">Right</option>
                </select>
            </div>
            <div class="form-group">
                <label for="dob">DOB</label>
                <input type="date" class="form-control" name="dob" id="dob" required>
            </div>
            <div class="form-group">
                <label for="country">Country</label>
                <input type="text" class="form-control" name="country" id="country" required>
            </div>
            <div class="form-group">
                <label for="birthplace">Birthplace</label>
                <input type="text" class="form-control" name="birthplace" id="birthplace">
            </div>
            <div class="form-group">
                <label for="residence">Residence</label>
                <input type="text" class="form-control" name="residence" id="residence">
            </div>
            <div class="form-group">
                <label for="height">Height (cm)</label>
                <input type="number" class="form-control" name="height" id="height">
            </div>
            <div class="form-group">
                <label for="weight">Weight (kg)</label>
                <input type="number" class="form-control" name="weight" id="weight">
            </div>
            <div class="form-group">
                <label for="turnedPro">Turned Pro (Year)</label>
                <input type="number" class="form-control" name="turnedPro" id="turnedPro">
            </div>
            <div class="form-group">
                <label for="rankingPoints">Ranking Points</label>
                <input type="number" class="form-control" name="rankingPoints" id="rankingPoints">
            </div>
            <button type="submit" class="btn btn-primary">Add Player</button>
            
        </form>
    </div>
    <div class="container">
        <a href="/" class="btn btn-secondary my-3">Home</a>
        <!-- ... (rest of your form elements) ... -->
    </div>
    <!-- Include Bootstrap JS and its dependencies below, if you need any Bootstrap JS components -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.7.0/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
'''


DISPLAY_PLAYERS = '''
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">

    <title>List of Players</title>
  </head>
  <body>
    <div class="container mt-3">
      <h2 class="mb-3">List of Tennis Players</h2>
      <table class="table table-hover">
        <thead class="thead-dark">
          <tr>
            <th>Firstname</th>
            <th>Lastname</th>
            <th>Hand</th>
            <th>DOB</th>
            <th>Country</th>
            <th>Birthplace</th>
            <th>Residence</th>
            <th>Height</th>
            <th>Weight</th>
            <th>Turned Pro</th>
          </tr>
        </thead>
        <tbody>
          {% for player in players %}
          <tr>
            <td>{{ player.firstname }}</td>
            <td>{{ player.lastname }}</td>
            <td>{{ player.hand }}</td>
            <td>{{ player.dob }}</td>
            <td>{{ player.country }}</td>
            <td>{{ player.birthplace }}</td>
            <td>{{ player.residence }}</td>
            <td>{{ player.height }}</td>
            <td>{{ player.weight }}</td>
            <td>{{ player.turnedPro }}</td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
      <a href="/add_player" class="btn btn-primary">Add another player</a>
    </div>

    <!-- Optional JavaScript; choose one of the two! -->

    <!-- Option 1: jQuery and Bootstrap Bundle (includes Popper) -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.bundle.min.js"></script>
    <div class="container">
        <a href="/" class="btn btn-secondary my-3">Home</a>
        <!-- ... (rest of your form elements) ... -->
    </div>
  </body>
</html>
'''

HOME_PAGE = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tennis Tracker App</title>
    <!-- Include Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container text-center mt-5">
        <h1>Welcome to the Tennis Tracker App</h1>
        <p class="lead mt-4">Track your favorite tennis players and their stats!</p>
        
        <div class="row justify-content-center mt-5">
            <!-- Player buttons -->
            <div class="col-sm-12 col-md-6 mb-3">
                <a href="/add_player" class="btn btn-primary btn-lg btn-block">Add Player</a>
            </div>
            <div class="col-sm-12 col-md-6 mb-3">
                <a href="/players" class="btn btn-success btn-lg btn-block">View Players</a>
            </div>
        </div>
        

        <div class="row justify-content-center">
            <!-- Tournament buttons -->
            <div class="col-sm-12 col-md-6 mb-3">
                <a href="/delete_player" class="btn btn-warning btn-lg btn-block">Delete Player</a>
            </div>
            <div class="col-sm-12 col-md-6 mb-3">
                <a href="/find_player" class="btn btn-info btn-lg btn-block">Find Player</a>
            </div>
        </div>
        <div class="row justify-content-center mt-5">
            <!-- Player buttons -->
            <div class="col-sm-12 col-md-6 mb-3">
                <a href="/update_points" class="btn btn-primary btn-lg btn-block">Update points</a>
            </div>
            <div class="col-sm-12 col-md-6 mb-3">
                <a href="/rankings" class="btn btn-success btn-lg btn-block">Rankings</a>
            </div>
        </div>
    </div>
    <!-- Include Bootstrap JS and its dependencies below -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.7.0/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
'''

DELETE_PLAYER_FORM = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Delete Player</title>
    <!-- Include Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <nav class="navbar navbar-dark bg-primary">
        <a class="navbar-brand" href="/">Tennis Tracker App</a>
    </nav>
    <div class="container mt-4">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header bg-danger text-white">Delete a Tennis Player</div>
                    <div class="card-body">
                        <form method="post" action="/delete_player">
                            <div class="form-group">
                                <label for="firstname">Firstname</label>
                                <input type="text" class="form-control" id="firstname" name="firstname" required>
                            </div>
                            <div class="form-group">
                                <label for="lastname">Lastname</label>
                                <input type="text" class="form-control" id="lastname" name="lastname" required>
                            </div>
                            <button type="submit" class="btn btn-danger">Delete Player</button>
                        </form>
                    </div>
                </div>
                <div class="mt-2">
                    <a href="/" class="btn btn-secondary">Back to Home</a>
                </div>
            </div>
        </div>
    </div>
    <a href="/" class="btn btn-secondary my-3">Home</a>
    <!-- Include Bootstrap JS and its dependencies -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.7.0/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
'''


RANKINGS_PAGE_TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tennis Player Rankings</title>
    <!-- Include Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-5">
        <h2>Tennis Player Rankings</h2>
        <table class="table">
            <thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">Name</th>
                    <th scope="col">Ranking Points</th>
                </tr>
            </thead>
            <tbody>
                {% for player in rankings %}
                <tr>
                    <td>{{ player['rank'] }}</td>
                    <td>{{ player['full_name'] }}</td>
                    <td>{{ player['points'] or 'N/A' }}</td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="3">No rankings available.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        <a href="/" class="btn btn-secondary my-3">Home</a>
    </div>
    
    <!-- Include Bootstrap JS and its dependencies -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.7.0/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
'''
FIND_PLAYER_FORM = '''
<!doctype html>
<html lang="en">
<head>
    <title>Find Player</title>
    <!-- Include Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-5">
        <h2 class="mb-4">Find Tennis Player</h2>
        <form method="post" action="/find_player">
            <div class="form-group">
                <label for="lastname">Last Name</label>
                <input type="text" class="form-control" name="lastname" id="lastname">
            </div>
            <div class="form-group">
                <label for="firstname">First Name</label>
                <input type="text" class="form-control" name="firstname" id="firstname">
            </div>
            <div class="form-group">
                <label for="country">Country</label>
                <input type="text" class="form-control" name="country" id="country">
            </div>
            <div class="form-group">
                <label for="dob_from">DOB From (Year)</label>
                <input type="number" class="form-control" name="dob_from" id="dob_from">
            </div>
            <div class="form-group">
                <label for="dob_to">DOB To (Year)</label>
                <input type="number" class="form-control" name="dob_to" id="dob_to">
            </div>

            <!-- New field for hand preference -->
            <div class="form-group">
                <label for="hand">Hand</label>
                <select class="form-control" name="hand" id="hand">
                    <option value="">Any</option>
                    <option value="L">Left</option>
                    <option value="R">Right</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary">Search</button>
        </form>
    </div>
    <!-- Include Bootstrap JS and its dependencies below, if you need any Bootstrap JS components -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.7.0/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
'''
SEARCH_RESULTS_TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
    <title>Search Results</title>
    <!-- Include Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-5">
        <h2>Search Results</h2>
        <table class="table">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>DOB</th>
                    <th>Hand</th>
                    <th>Country</th>
                </tr>
            </thead>
            <tbody>
                {% for player in players %}
                <tr>
                    <td>{{ player.firstname }} {{ player.lastname }}</td>
                    <td>{{ player.dob }}</td>
                    <td>{{ player.hand }}</td>
                    <td>{{ player.country }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
'''



UPDATE_POINTS_FORM = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Update Player Points</title>
    <!-- Include Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-5">
        <h2 class="mb-4">Update Player Ranking Points</h2>
        <form method="post" action="/update_points">
            <div class="form-group">
                <label for="firstname">First Name</label>
                <input type="text" class="form-control" name="firstname" id="firstname" required>
            </div>
            <div class="form-group">
                <label for="lastname">Last Name</label>
                <input type="text" class="form-control" name="lastname" id="lastname" required>
            </div>
            <div class="form-group">
                <label for="points">New Points</label>
                <input type="number" class="form-control" name="points" id="points" required>
            </div>
            <button type="submit" class="btn btn-primary">Update Points</button>
        </form>
        <a href="/" class="btn btn-secondary my-3">Home</a>
    </div>
    <!-- Include Bootstrap JS and its dependencies -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.7.0/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
'''


# Flask route for home page
@app.route('/')
def home():
    return HOME_PAGE


# Route for adding a new player (GET to display form, POST to add player)
from datetime import datetime
from flask import request


@app.route('/add_player', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST':
        dob_str = request.form['dob']
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()  # Convert string to date

        new_player = Player(
            firstname=request.form['firstname'],
            lastname=request.form['lastname'],
            hand=request.form['hand'],
            dob=dob,  # Use the converted date
            country=request.form['country'],
            birthplace=request.form['birthplace'],
            residence=request.form['residence'],
            height=int(request.form['height']),
            weight=int(request.form['weight']),
            turnedPro=int(request.form['turnedPro'])
        )
        db.session.add(new_player)
        db.session.commit()

        # Assuming rankingPoints is an optional field
        ranking_points = request.form.get('rankingPoints')
        if ranking_points:
            new_ranking = Ranking(
                playerId=new_player.playerId,
                points=int(ranking_points)
            )
            db.session.add(new_ranking)
            db.session.commit()

        return 'Player and ranking added successfully! <a href="/players">See all players</a>'
    return render_template_string(ADD_PLAYER_FORM)



# Route for displaying all players
@app.route('/players')
def players():
    players = Player.query.all()  # Use SQLAlchemy ORM to query the Player model
    return render_template_string(DISPLAY_PLAYERS, players=players)


@app.route('/delete_player', methods=['GET'])
def delete_player_form():
    return render_template_string(DELETE_PLAYER_FORM)



@app.route('/delete_player', methods=['POST'])
def delete_player():
    firstname = request.form['firstname']
    lastname = request.form['lastname']

    # Create a connection and execute a prepared statement for deletion
    with db.engine.connect() as connection:
        sql = text("DELETE FROM players WHERE firstname = :firstname AND lastname = :lastname")
        result = connection.execute(sql, {"firstname": firstname, "lastname": lastname})
        connection.commit()

        if result.rowcount > 0:
            message = "Player successfully deleted."
        else:
            message = "No player found with the provided name."
    return message



@app.route('/rankings')
def show_rankings():
    sql = text(
        """
        SELECT players.firstname, players.lastname, rankings.points 
        FROM players 
        LEFT OUTER JOIN rankings ON players.playerId = rankings.playerId 
        ORDER BY rankings.points DESC, players.lastname ASC
        """
    )

    with db.engine.connect() as connection:
        result = connection.execute(sql)
        ranked_players = [
            {'rank': idx + 1, 'full_name': f"{row.firstname} {row.lastname}", 'points': row.points}
            for idx, row in enumerate(result)
        ]

    return render_template_string(RANKINGS_PAGE_TEMPLATE, rankings=ranked_players)



@app.route('/update_points', methods=['GET', 'POST'])
def update_points():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        new_points = request.form['points']

        try:
            # Start a transaction


            # Find the player
            player = Player.query.filter_by(firstname=firstname, lastname=lastname).first()
            if player:
                # Update or add points in rankings
                ranking = Ranking.query.filter_by(playerId=player.playerId).first()
                if ranking:
                    ranking.points = new_points
                    message = "Points modified"
                else:
                    new_ranking = Ranking(playerId=player.playerId, points=new_points)
                    db.session.add(new_ranking)
                    message = "Points added"

                # Commit the transaction
                db.session.commit()
            else:
                message = "Player does not exist"
        except Exception as e:
            # Rollback in case of error
            db.session.rollback()
            message = f"An error occurred: {e}"

        return message
    else:
        return UPDATE_POINTS_FORM  # Replace with actual form rendering


# Route for finding players
@app.route('/find_player', methods=['GET', 'POST'])
def find_player():
    if request.method == 'POST':
        lastname = request.form['lastname']
        firstname = request.form['firstname']
        country = request.form['country']
        dob_from = request.form.get('dob_from')
        dob_to = request.form.get('dob_to')
        hand = request.form.get('hand')

        query = Player.query
        if lastname:
            query = query.filter(Player.lastname.like(f'%{lastname}%'))
        if firstname:
            query = query.filter(Player.firstname.like(f'%{firstname}%'))
        if country:
            query = query.filter(Player.country.like(f'%{country}%'))
        if dob_from:
            query = query.filter(Player.dob >= dob_from)
        if dob_to:
            query = query.filter(Player.dob <= dob_to)
        if hand and hand != '':
            query = query.filter(Player.hand == hand)

        players = query.all()

        return render_template_string(SEARCH_RESULTS_TEMPLATE, players=players)
    return render_template_string(FIND_PLAYER_FORM)


# Run the Flask application
if __name__ == '__main__':
    app.run(port=2409, debug=True)
