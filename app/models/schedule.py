from app import db
from sqlalchemy import text, Column, String, Integer, Boolean
from app.models.president import convertShort

# ---- Schedule Models -----
"""
Helps categorize existing senate classes and upcoming elections with 2 table.
Accounts for all non-special elections with senate classes, while upcoming elections
does include special elections as well.
"""

class SenateClass(db.Model):
    __tablename__ = 'senateclasses'

    state = Column(String, nullable=False, primary_key = True)
    incumbent = Column(String(50))
    party = Column(String(3))
    senateclass = Column(Integer, nullable=False, primary_key = True)
    next_election = Column(Integer)

    def __init__(self, state, incumbent, party, senateclass, next_election):

        self.state = state
        self.incumbent = incumbent
        self.party = party
        self.senateclass = senateclass
        self.next_election = next_election


class UpcomingElection(db.Model):
    __tablename__ = 'upcomingelection'

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    office = Column(String(50))
    state = Column(String(50))
    special = Column(Boolean)

    def __init__(self, year, office, state, special):

        self.year = year
        self.office = office
        self.state = state
        self.special = special
    
    @staticmethod
    def get(state:str, year:int):
        """
        Method to retrieve upcoming elections for a particular state.
        """

        # Check for shortened; fix if necessary.
        if len(state) < 2:
            state = convertShort(state)

        rows = db.session.execute(text('''
            SELECT *
            FROM upcomingelection
            WHERE year = :year
            AND (state = :state OR state = 'ALL')
            '''),
            ({'state':state,'year':year})
            )
        
        results = rows.fetchall()
        if not results:
            return None
        
        # Convert to dict for easier use
        ret = []

        for row in results:
            result_dict = {'office':row[2], 'special':row[4]}
            ret.append(result_dict)
        
        return ret

