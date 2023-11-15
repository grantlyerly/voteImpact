from app import db
from sqlalchemy import text, Column, String, Integer, Boolean
from app.models.president import sort_by_votes, convertShort

class Governor(db.Model):
    __tablename__ = 'governor'

    id = Column(Integer, primary_key=True)
    state = Column(String(50), nullable=False)
    office = Column(String(50))
    year = Column(Integer, nullable=False)
    candidate = Column(String(100), nullable=False)
    party = Column(String(50))
    candidateVotes = Column(Integer)
    totalVotes = Column(Integer)
    rankedChoice = Column(Boolean)

    def __init__(self, state, office, year, candidate, party, 
                 candidateVotes, totalVotes, rankedChoice):
        self.state = state
        self.office = office
        self.year = year
        self.candidate = candidate
        self.party = party
        self.candidateVotes = candidateVotes
        self.totalVotes = totalVotes
        self.rankedChoice = rankedChoice