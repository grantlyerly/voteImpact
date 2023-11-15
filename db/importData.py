import csv
from app.main import create_app
from app import db
from app.models import Governor, President, EV, Senate, House, SenateClass, UpcomingElection

"""
To Run:
flask shell
from db.importData import main
main()
"""

# Resets db to prevent overlap
def reset_db():
    app = create_app() 

    with app.app_context():
        db.drop_all()
        db.create_all()


# Adds data from Presidents 1976-2020 into the database
def add_pres_to_db():
    with open('db/data/1976-2020-president.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip the header

        for row in reader:
            year = int(row[0])
            state = row[1]
            office = row[6]
            candidate = row[7]
            party = row[8]
            writeIn = bool(row[9])
            candidateVotes = int(row[10])
            totalVotes = int(row[11])
        
            president = President(year, state, office, candidate, party, writeIn, candidateVotes, totalVotes)

            db.session.add(president)
        
        db.session.commit()


# Adds data from Electoral Votes csv into the database
def add_ev_to_db():
    with open('db/data/electoralvotes.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            year = int(row[0])
            state = row[1]
            electoralVotes = row[2]
            votedFor = row[3]

            ev = EV(year, state, electoralVotes, votedFor)
            db.session.add(ev)
        
        db.session.commit()

def add_sen_to_db():
    # Add data from the 1976-2020-senate.csv file first.
    with open('db/data/1976-2020-senate.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip the header

        for row in reader:
            year = int(row[0])
            state = row[1]
            office = row[6]
            candidate = row[10]
            party = row[11]
            writeIn = True if row[12].lower() == 'true' else False
            candidateVotes = int(row[14])
            if int(row[15]):
                totalVotes = int(row[15])
            else:
                totalVotes = 0
            special = True if row[9].lower() == 'true' else False
        
            senate = Senate(year, state, office, candidate, party, writeIn, candidateVotes, totalVotes, special)

            db.session.add(senate)
        
        db.session.commit()
    
    # Add data from 2022 file now.
    with open('db/data/2022senate.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            year = int(row[0])
            state = row[1]
            office = row[2]
            candidate = row[3]
            party = row[4]
            writeIn = False
            candidateVotes = int(row[5])
            totalVotes = int(row[6])
            special = special = True if row[7].lower() == 'true' else False
            senate = Senate(year, state, office, candidate, party, writeIn, candidateVotes, totalVotes, special)

            db.session.add(senate)
        
        db.session.commit()


# Adds house data to the database
def add_house_to_db():
    with open('db/data/1976-2022-house.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            year = int(row[0])
            state = row[1]
            cd = row[7]
            office = row[6]
            candidate = row[11]
            party = row[12]
            writeIn = True if row[13].lower() == 'true' else False
            candidateVotes = int(row[15])
            if int(row[16]):
                totalVotes = int(row[15])
            else:
                totalVotes = 0
            runoff = True if row[9].lower() == 'true' else False
            special = True if row[10].lower() == 'true' else False

            house = House(year, state, cd, office, candidate, party, 
                          writeIn, candidateVotes, totalVotes, runoff, special)
            
            db.session.add(house)
        
        db.session.commit()


# Add schedule data to the databse
def add_schedules():
    with open('db/data/senateclasses.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            state = row[0]
            incumbent = row[1]
            party = row[2]
            senateclass = int(row[3])
            next_election = int(row[4])
        
            sc = SenateClass(state, incumbent, party, senateclass, next_election)
            db.session.add(sc)
        
        db.session.commit()

    with open('db/data/upcomingelections.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            year = int(row[0])
            office = row[1]
            state = row[2]
            special = True if row[3].lower() == "true" else False

            ue = UpcomingElection(year, office, state, special)
            db.session.add(ue)
        
        db.session.commit()


# Add Governor to database
def add_governor():
    with open('db/data/governor2000-2022.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            state = row[0]
            office = row[1]
            year = int(row[2])
            candidate = row[3]
            party = row[4]
            candidateVotes = int(row[5])
            totalVotes = int(row[6])
            rankedChoice = True if row[7].lower() == 'true' else False

            gov = Governor(state, office, year, candidate, party, candidateVotes,
                           totalVotes, rankedChoice)
            db.session.add(gov)

        db.session.commit()
              

# Runs all previous functions
def import_all():
    reset_db()
    print("DB Reset")
    add_pres_to_db()
    print("Pres Added")
    add_ev_to_db()
    print("EVs added")
    add_sen_to_db()
    print("Sen added")
    add_house_to_db()
    print("House added")
    add_schedules()
    print("Schedules added")
    add_governor()
    print("Governor added")