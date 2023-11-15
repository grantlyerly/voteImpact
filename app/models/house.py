from app import db
from sqlalchemy import text, Column, String, Integer, Boolean
from app.models.president import sort_by_votes, convertShort

"""
----- House Model ----
Includes: election year, state name, district, office, candidate's name, candidate's party, whether
they were a write in, how many votes the candidate recieved, total votes, if it was a runoff, 
and if it was a special election.

Takes data from the 1976-2020 data sheet, soon to add data for 2022 as well.
"""

class House(db.Model):
    __tablename__ = 'house'

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    state = Column(String(50), nullable=False)
    cd = Column(Integer, nullable=False)
    office = Column(String(50))
    candidate = Column(String(100), nullable=False)
    party = Column(String(50))
    writeIn = Column(Boolean)
    candidateVotes = Column(Integer)
    totalVotes = Column(Integer)
    runoff = Column(Boolean)
    special = Column(Boolean)

    def __init__(self, year, state, cd, office, candidate, party, writeIn, 
                 candidateVotes, totalVotes, runoff, special):
        self.year = year
        self.state = state
        self.cd = cd
        self.office = office
        self.candidate = candidate
        self.party = party
        self.writeIn = writeIn
        self.candidateVotes = candidateVotes
        self.totalVotes = totalVotes
        self.runoff = runoff
        self.special = special
    
    @staticmethod
    def getHouse(state:str, cd:int, year:int):
        """
        Method to retrieve a list of candidates based on state & year.
        
        Returns up to two lists, in a dictionary; one for "regular" if it exists, one for "special" if it exists.

        Ignore runoffs, given that they do not occur during the same, usual period.
        """

        # Check for shortened; fix if necessary.
        if len(state) < 3:
            state = convertShort(state)
        
        if not int(cd):
            return None
        
        rows = db.session.execute(text('''
            SELECT *
            FROM house
            WHERE state = :state
            AND year = :year
            AND cd = :cd
            AND NOT runoff
            '''),
            ({'state': state.upper(), 'year': year,
              'cd': cd}))

        results = rows.fetchall()
        if not results:
            return None
        
        ret = {}

        # Convert results to dictionaries for easier interpretation, then sort
        # Two different dictionaries, one for regular, one fo special.

        for row in results:
            election_type = "regular"
            if row[11]:
                election_type = "special"
        
            result_dict = {"year": row[1], "state":state, "cd":row[3], "office":row[4],"candidate":row[5],
                           "party":row[6], "writeIn":row[7], "candidateVotes":row[8], "totalVotes":row[9], "runoff":row[10], "special":row[11]}

            if election_type not in ret.keys():
                ret[election_type] = [result_dict]
            
            ret[election_type].append(result_dict)
        
        for key in ret:
            ret[key] = sort_by_votes(ret[key])
        
        return ret
    
    @staticmethod
    def calcMargin(house_ret:list)->float:
        """
        Function to return margin of victory from a state's house results
        Takes a list of dictionaries, returning a float for the % margin.
        (note: Currently, essentially identical to senate calcMargin)
        
        We assume that 'special' only refers to a single election in a single year; return an error if not the case.
        """
        winnerVotes = house_ret[0].get('candidateVotes')

        indx = 1
        secondVotes = 0

        while indx < len(house_ret):
            if house_ret[indx].get('party') != house_ret[0].get('party'):
                secondVotes = house_ret[indx].get('candidateVotes')
                totalVotes = house_ret[0].get('totalVotes')

                return abs(winnerVotes-secondVotes) / totalVotes
            
            indx += 1
        
        return 98




    
