import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('tennis.db')

# Create a cursor object
cursor = conn.cursor()

# Create the 'players' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS players (
    playerId INTEGER PRIMARY KEY AUTOINCREMENT,
    playerRef TEXT,
    firstname TEXT,
    lastname TEXT,
    hand TEXT CHECK(hand IN ('L', 'R', 'A')),
    dob DATE,
    country TEXT,
    birthplace TEXT,
    residence TEXT,
    height INTEGER,
    weight INTEGER,
    turnedPro INTEGER
);
''')

# Create the 'tournaments' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS tournaments (
    tournamentId INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    surface TEXT,
    draw_size INTEGER,
    country TEXT,
    city TEXT,
    start_date DATE,
    end_date DATE
);
''')

# Create the 'matches' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS matches (
    matchId INTEGER PRIMARY KEY AUTOINCREMENT,
    tournamentId INTEGER,
    playerId1 INTEGER,
    playerId2 INTEGER,
    match_date DATE,
    round TEXT,
    winnerId INTEGER,
    score TEXT,
    duration TIME,
    FOREIGN KEY(tournamentId) REFERENCES tournaments(tournamentId),
    FOREIGN KEY(playerId1) REFERENCES players(playerId),
    FOREIGN KEY(playerId2) REFERENCES players(playerId),
    FOREIGN KEY(winnerId) REFERENCES players(playerId)
);
''')

# Create the 'rankings' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS rankings (
    rankingId INTEGER PRIMARY KEY AUTOINCREMENT,
    playerId INTEGER NOT NULL,
    rank INTEGER,
    points INTEGER,
    FOREIGN KEY(playerId) REFERENCES players(playerId)
);
''')

# Create the 'player_statistics' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS player_statistics (
    statsId INTEGER PRIMARY KEY AUTOINCREMENT,
    playerId INTEGER,
    aces INTEGER,
    doubleFaults INTEGER,
    firstServePercent INTEGER,
    firstServePointsWon INTEGER,
    secondServePointsWon INTEGER,
    breakPointsSaved INTEGER,
    breakPointsFaced INTEGER,
    matchesPlayed INTEGER,
    matchesWon INTEGER,
    tournamentsWon INTEGER,
    highestRanking INTEGER,
    currentRanking INTEGER,
    FOREIGN KEY(playerId) REFERENCES players(playerId)
);
''')

# Create the 'tournament_standings' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS tournament_standings (
    standingId INTEGER PRIMARY KEY AUTOINCREMENT,
    tournamentId INTEGER,
    playerId INTEGER,
    position INTEGER,
    pointsEarned INTEGER,
    FOREIGN KEY(tournamentId) REFERENCES tournaments(tournamentId),
    FOREIGN KEY(playerId) REFERENCES players(playerId)
);
''')

# Commit the changes
conn.commit()

# Close the connection
conn.close()

print("Tennis database tables created successfully.")
