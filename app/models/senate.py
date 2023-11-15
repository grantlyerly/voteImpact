from app import db
from sqlalchemy import text, Column, String, Integer, Boolean
from app.models.president import sort_by_votes, convertShort

# ----- Senate Model -----
# Includes: election year, state name, office, candidate's name, candidate's party,
# whether theyt were a write in, how many votes the candidate recieved,
# the total votes in that election, and if it was a special election.
# Takes data from 2 different sheets: the 1976-2020 data, and the 2022 data.

class Senate(db.Model):
    __tablename__ = 'senate'

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    state = Column(String(50), nullable=False)
    office = Column(String(50))
    candidate = Column(String(100), nullable=False)
    party = Column(String(50))
    writeIn = Column(Boolean)
    candidateVotes = Column(Integer)
    totalVotes = Column(Integer)
    special = Column(Boolean)

    def __init__(self, year, state, office, candidate, party, writeIn, 
                 candidateVotes, totalVotes, special):
        self.year = year
        self.state = state
        self.office = office
        self.candidate = candidate
        self.party = party
        self.writeIn = writeIn
        self.candidateVotes = candidateVotes
        self.totalVotes = totalVotes
        self.special = special


    @staticmethod
    def getSen(state:str, year:int):
        """
        Method to retrieve a list of candidates based on state & year.
        
        Returns up to two lists, in a dictionary; one for "regular" if it exists, one for "special" if it exists.
        """
        
        # Check for shortened; fix if necessary.
        if len(state) < 3:
            state = convertShort(state)

        rows = db.session.execute(text('''
            SELECT *
            FROM senate
            WHERE state = :state
            AND year = :year                           
            '''),
            ({'state': state.upper(),
            'year': year}))
        
        results = rows.fetchall()
        if not results:
            return None
        
        # Convert results to dictionaries for easier interpretation, then sort
        ret = {}

        for row in results:

            # Note what type of election for proper categorization
            election_type = "regular"
            if row[9]:
                election_type = "special"

            result_dict = {"year": row[1], "state":state, "office":row[3],"candidate":row[4],
                           "party":row[5], "writeIn":row[6], "candidateVotes":row[7], "totalVotes":row[8], "special":row[9]}
            
            if election_type not in ret.keys():
                ret[election_type] = []
            
            ret[election_type].append(result_dict)

        for key in ret:
            ret[key] = sort_by_votes(ret[key])
        
        return ret
    

    @staticmethod
    def calcMargin(sen_ret:list)->float:
        """
        Function to return margin of victory from a state's senate results
        Takes a list of dictionaries, returning a float for the % margin.
        
        We assume that 'special' only refers to a single election in a single year; return an error if not the case.
        """
        winnerVotes = sen_ret[0].get('candidateVotes')

        indx = 1
        secondVotes = 0
        
        # Calculates margin between different parties, skipping if top finishers were of the same.
        while indx < len(sen_ret):
            if sen_ret[indx].get('party') != sen_ret[0].get('party'):
                secondVotes = sen_ret[indx].get('candidateVotes')
                totalVotes = sen_ret[0].get('totalVotes')
        
                return abs(winnerVotes-secondVotes)/totalVotes
            
            indx += 1
            
        return 98

        
