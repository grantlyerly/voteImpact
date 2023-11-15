from app import db
from sqlalchemy import text, Column, String, Integer, Boolean

# ----- President Model -----
# Includes: election year, state name, office, candidate's name, candidate's party,
# whether they were a write in or not, how many votes the candidate reciever,
# and the total votes in that election.

class President(db.Model):
    __tablename__ = 'president'

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    state = Column(String(50), nullable=False)
    office = Column(String(50))
    candidate = Column(String(100), nullable=False)
    party = Column(String(50))
    writeIn = Column(Boolean)
    candidateVotes = Column(Integer)
    totalVotes = Column(Integer)

    def __init__(self, year, state, office, candidate, party, writeIn, 
                 candidateVotes, totalVotes):
        self.year = year
        self.state = state
        self.office = office
        self.candidate = candidate
        self.party = party
        self.writeIn = writeIn
        self.candidateVotes = candidateVotes
        self.totalVotes = totalVotes


    @staticmethod
    def getPres(state:str, year:int)->list:
        """
        Method to retrieve a list of candidates based on state & year.
        
        Returns a list of dictionaries, each represnting a candidate, 
        sorted from most candidateVotes to least.
        """
        
        # Check for shortened; fix if necessary.
        if len(state) < 3:
            state = convertShort(state)
        
        rows = db.session.execute(text('''
            SELECT *
            FROM president
            WHERE state = :state
            AND year = :year                           
            '''),
            ({'state': state.upper(),
            'year': year}))
        
        results = rows.fetchall()
        if not results:
            return None
        
        # Convert results to dictionaries for easier interpretation, then sort
        ret = []
        for row in results:
            result_dict = {"year": row[1], "state":state, "office":row[3],"candidate":row[4],
                           "party":row[5], "writeIn":row[6], "candidateVotes":row[7], "totalVotes":row[8]}
            ret.append(result_dict)
        
        return sort_by_votes(ret)
    

    @staticmethod
    def calcMargin(pres_ret:list)->float:
        """
        Function to return margin of victory from a state's presidential results
        Takes a list of dictionaries, returning a float for the % margin
        """
        winnerVotes = pres_ret[0].get('candidateVotes')
        secondVotes = pres_ret[1].get('candidateVotes')
        totalVotes = pres_ret[0].get('totalVotes')
        
        margin = abs(winnerVotes-secondVotes)/totalVotes

        return margin


# ----- Electoral Votes -----

class EV(db.Model):
    '''
    Related table to President that tracks electoral by state, by year
    '''
    __tablename__ = 'ev'

    year = Column(Integer, primary_key=True)
    state = Column(String(50), primary_key=True)
    electoralVotes = Column(Integer)
    votedFor = Column(String(10))

    def __init__(self, year, state, electoralVotes, votedFor):
        self.year = year
        self.state = state
        self.electoralVotes = electoralVotes
        self.votedFor=votedFor
    
    def get(state:str, year:int)->int:
        '''
        Returns number of electoral votes a state had in a certain year
        '''

        # Check for shortened; fix if necessary.
        if len(state) < 3:
            state = convertShort(state)
        
        rows = db.session.execute(text('''
            SELECT *
            FROM ev
            WHERE state = :state
            AND year = :year                           
            '''),
            ({'state': state,
            'year': year}))
        
        results = rows.fetchone()
        if not results:
            return None

        # Convert result to dictionary for easier interpretation
        ev = results[2]

        return ev

# ----- Helper Functions -----
# Various helper functions to assist with class calculations.

def sort_by_votes(lst:list)->list:
    '''
    Sorting a dictionary based on 'candidateVotes.'
    '''
    return sorted(lst, key=lambda d: d['candidateVotes'], reverse=True)


def convertShort(short:str):
    """
    Converts a shortened state name to its full name (e.g. 'NC' -> 'North Carolina').
    """
    shortToLong = {
    'AL': 'Alabama','AK': 'Alaska','AZ': 'Arizona','AR': 'Arkansas','CA': 'California',
    'CO': 'Colorado','CT': 'Connecticut','DE': 'Deleware','DC': 'District of Columbia','FL': 'Florida','GA': 'Georgia',
    'HI': 'Hawaii','ID': 'Idaho','IL': 'Illinois','IN': 'Indiana','IA': 'Iowa','KS': 'Kansas',
    'KY': 'Kentucky','LA': 'Louisiana','ME': 'Maine','MD': 'Maryland','MA': 'Massachusetts',
    'MI': 'Michigan','MN': 'Minnesota','MS': 'Mississippi','MO': 'Missouri','MT': 'Montana','NE': 'Nebraska',
    'NV': 'Nevada','NH': 'New Hampshire','NJ': 'New Jersey','NM': 'New Mexico','NY': 'New York',
    'NC': 'North Carolina','ND': 'North Dakota','OH': 'Ohio','OK': 'Oklahoma','OR': 'Oregon',
    'PA': 'Pennsylvania','RI': 'Rhode Island','SC': 'South Carolina','SD': 'South Dakota','TN': 'Tennessee',
    'TX': 'Texas','UT': 'Utah','VT': 'Vermont','VA': 'Virginia','WA': 'Washington',
    'WV': 'West Virginia','WI': 'Wisconsin','WY': 'Wyoming',
}
    if short in shortToLong.keys():
        return shortToLong[short.upper()]
    
    return ""