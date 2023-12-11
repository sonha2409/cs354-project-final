import sqlite3
import random
from datetime import datetime, timedelta

# Function to generate a random date
def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

# Function to generate dummy data for players
def insert_dummy_players(cursor, num_players=10):
    for _ in range(num_players):
        cursor.execute('''
        INSERT INTO players (playerRef, firstname, lastname, hand, dob, country, birthplace, residence, height, weight, turnedPro)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            "REF" + str(random.randint(1000, 9999)),
            "FirstName" + str(random.randint(1, num_players)),
            "LastName" + str(random.randint(1, num_players)),
            random.choice(['L', 'R', 'A']),
            random_date(datetime(1970, 1, 1), datetime(2000, 1, 1)).date(),
            "Country" + str(random.randint(1, num_players)),
            "Birthplace" + str(random.randint(1, num_players)),
            "Residence" + str(random.randint(1, num_players)),
            random.randint(160, 210),  # height in cm
            random.randint(60, 100),  # weight in kg
            random.randint(1980, 2010)  # year turned pro
        ))

# Function to generate dummy data for tournaments
def insert_dummy_tournaments(cursor, num_tournaments=5):
    for _ in range(num_tournaments):
        start_date = random_date(datetime(2020, 1, 1), datetime(2022, 1, 1))
        end_date = start_date + timedelta(days=7)  # 1 week duration
        cursor.execute('''
        INSERT INTO tournaments (name, surface, draw_size, country, city, start_date, end_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            "Tournament" + str(random.randint(1, num_tournaments)),
            random.choice(['Hard', 'Clay', 'Grass']),
            random.choice([32, 64, 128]),
            "Country" + str(random.randint(1, num_tournaments)),
            "City" + str(random.randint(1, num_tournaments)),
            start_date.date(),
            end_date.date()
        ))
def insert_dummy_rankings(cursor, num_players=10):
    date_today = datetime.now().date()
    for player_id in range(1, num_players + 1):
        cursor.execute('''
        INSERT INTO rankings (playerId, rank, points, rankingDate)
        VALUES (?, ?, ?, ?)
        ''', (
            player_id,
            random.randint(1, 500),  # rank
            random.randint(1, 10000),  # points
            date_today  # rankingDate
        ))

# Function to generate dummy data for tournament_standings
def insert_dummy_tournament_standings(cursor, num_tournaments=5, num_players=10):
    for tournament_id in range(1, num_tournaments + 1):
        for player_id in range(1, num_players + 1):
            cursor.execute('''
            INSERT INTO tournament_standings (tournamentId, playerId, position, pointsEarned)
            VALUES (?, ?, ?, ?)
            ''', (
                tournament_id,
                player_id,
                random.randint(1, num_players),  # position
                random.randint(1, 2000)  # pointsEarned
            ))

# Connect to SQLite database
conn = sqlite3.connect('tennis.db')
cursor = conn.cursor()

# Generate dummy data for players
insert_dummy_players(cursor)

# Generate dummy data for tournaments
insert_dummy_tournaments(cursor)

# Generate dummy data for rankings
insert_dummy_rankings(cursor)

# Generate dummy data for tournament_standings
insert_dummy_tournament_standings(cursor)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Dummy data for players and tournaments inserted successfully.")
