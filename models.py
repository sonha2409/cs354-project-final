from flask import Flask, request, render_template_string
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Time
from sqlalchemy.orm import relationship 


db = SQLAlchemy()

class Player(db.Model):
    __tablename__ = 'players'
    playerId = Column(Integer, primary_key=True, autoincrement=True)
    playerRef = Column(String)
    firstname = db.Column(db.String, index=True)
    lastname = db.Column(db.String, index=True)
    hand = Column(String)
    dob = Column(Date)
    country = Column(String)
    birthplace = Column(String)
    residence = Column(String)
    height = Column(Integer)
    weight = Column(Integer)
    turnedPro = Column(Integer)

class Tournament(db.Model):
    __tablename__ = 'tournaments'
    tournamentId = Column(Integer, primary_key=True)
    name = Column(String)
    surface = Column(String)
    draw_size = Column(Integer)
    country = Column(String)
    city = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    matches = relationship('Match', backref='tournament')

class Match(db.Model):
    __tablename__ = 'matches'
    matchId = Column(Integer, primary_key=True)
    tournamentId = Column(Integer, ForeignKey('tournaments.tournamentId'))
    playerId1 = Column(Integer, ForeignKey('players.playerId'))
    playerId2 = Column(Integer, ForeignKey('players.playerId'))
    match_date = Column(Date)
    round = Column(String)
    winnerId = Column(Integer, ForeignKey('players.playerId'))
    score = Column(String)
    duration = Column(Time)

class Ranking(db.Model):
    __tablename__ = 'rankings'
    rankingId = Column(Integer, primary_key=True)
    playerId = Column(Integer, ForeignKey('players.playerId'), nullable=False)
    rank = Column(Integer)
    points = db.Column(db.Integer, index=True) 
    rankingDate = Column(Date)

class PlayerStatistics(db.Model):
    __tablename__ = 'player_statistics'
    statsId = Column(Integer, primary_key=True)
    playerId = Column(Integer, ForeignKey('players.playerId'))
    aces = Column(Integer)
    doubleFaults = Column(Integer)
    firstServePercent = Column(Integer)
    firstServePointsWon = Column(Integer)
    secondServePointsWon = Column(Integer)
    breakPointsSaved = Column(Integer)
    breakPointsFaced = Column(Integer)
    matchesPlayed = Column(Integer)
    matchesWon = Column(Integer)
    tournamentsWon = Column(Integer)
    highestRanking = Column(Integer)
    currentRanking = Column(Integer)

class TournamentStandings(db.Model):
    __tablename__ = 'tournament_standings'
    standingId = Column(Integer, primary_key=True)
    tournamentId = Column(Integer, ForeignKey('tournaments.tournamentId'))
    playerId = Column(Integer, ForeignKey('players.playerId'))
    position = Column(Integer)
    pointsEarned = Column(Integer)

