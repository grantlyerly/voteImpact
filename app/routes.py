from flask import render_template, redirect, url_for, request
from flask import Blueprint
from .methods import ZipCodeForm, AdditionalInfoForm, calcWeight, calcPower, voteInfo_address
from .models import President, EV, Senate, House, UpcomingElection, SenateClass
from time import localtime

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/home', methods=['GET', 'POST'])
def home():
    form1 = ZipCodeForm(prefix='form1')
    form2 = ZipCodeForm(prefix='form2')

    if form2.validate_on_submit():
        print('form 2 submitted')
        zip1 = int(form2.zip_code_1.data)
        zip2 = int(form2.zip_code_2.data)
        now = localtime()
        year = now[0]

        state1, cd1 = apiZipPack(zip1)
        state2, cd2 = apiZipPack(zip2)
        if not (cd1 and cd2):
            # Go to update address page
            return redirect(url_for('main.add_info2', zip1=zip1, zip2=zip2, year = year))
        
        return redirect(url_for('main.results2', state1=state1, state2=state2, cd1=cd1, cd2=cd2, year=year))
    
    if form1.validate_on_submit():
        print('form 1 submitted')
        zip1 = int(form1.zip_code_1.data)
        zip2 = int(form1.zip_code_2.data)
        year = form1.year.data

        state1, cd1 = apiZipPack(zip1)
        state2, cd2 = apiZipPack(zip2)
        if not (cd1 and cd2):
            # Go to update address page
            return redirect(url_for('main.add_info', zip1=zip1, zip2=zip2, year=year))

        # Directly redirect to the results page
        return redirect(url_for('main.results', state1=state1, state2=state2, cd1=cd1, cd2=cd2, year=year))
        
    return render_template('home.html', form1=form1, form2=form2)


@bp.route('/add_info2', methods=['GET', 'POST'])
def add_info2():
    form1 = AdditionalInfoForm(prefix='form1')
    form2 = AdditionalInfoForm(prefix='form2')

    zip1 = request.args.get('zip1')
    zip2 = request.args.get('zip2')
    year = request.args.get('year')

    # Calculate status
    state1, cd1 = apiZipPack(zip1)
    state2, cd2 = apiZipPack(zip2)

    status1 = True if cd1 else False
    status2 = True if cd2 else False

    if form1.validate_on_submit():
        zip1 = form1.zip_code.data
        address1 = form1.address.data
        city1 = form1.city.data
        state1 = form1.state.data

        state1, cd1 = apiZipPack(zip1, address1, city1, state1)

    else:
        state1, cd1 = apiZipPack(zip1)

    if form2.validate_on_submit():
        zip2 = form2.zip_code.data
        address2 = form2.address.data
        city2 = form2.city.data
        state2 = form2.state.data

        state2, cd2 = apiZipPack(zip2, address2, city2, state2)

    else:
        state2, cd2 = apiZipPack(zip2)

    if 'skip' in request.form:
    # The 'skip' button was pressed
    # You could check here whether state1, state2, cd1, cd2, and year have valid values
    # and handle the case where they don't
        print('going to results 2')
        return redirect(url_for('main.results2', state1=state1, state2=state2, cd1=cd1, cd2=cd2, year=year))
    
    if cd1 and cd2:
        print('going to results 2')
        return redirect(url_for('main.results2', state1=state1, state2=state2, cd1=cd1, cd2=cd2, year=year))

    print('on add_info2')
    return render_template('add_info.html', form1=form1, form2=form2, zip1=zip1, zip2=zip2, status1=status1, status2=status2)


@bp.route('/add_info', methods=['GET', 'POST'])
def add_info():
    form1 = AdditionalInfoForm(prefix='form1')
    form2 = AdditionalInfoForm(prefix='form2')

    zip1 = request.args.get('zip1')
    zip2 = request.args.get('zip2')
    year = request.args.get('year')

    # Calculate status
    state1, cd1 = apiZipPack(zip1)
    state2, cd2 = apiZipPack(zip2)

    status1 = True if cd1 else False
    status2 = True if cd2 else False

    if form1.validate_on_submit():
        zip1 = form1.zip_code.data
        address1 = form1.address.data
        city1 = form1.city.data
        state1 = form1.state.data
        year = form1.year.data

        state1, cd1 = apiZipPack(zip1, address1, city1, state1)

    else:
        state1, cd1 = apiZipPack(zip1)

    if form2.validate_on_submit():
        zip2 = form2.zip_code.data
        address2 = form2.address.data
        city2 = form2.city.data
        state2 = form2.state.data
        year = form2.year.data

        state2, cd2 = apiZipPack(zip2, address2, city2, state2)

    else:
        state2, cd2 = apiZipPack(zip2)

    if 'skip' in request.form:
    # The 'skip' button was pressed
    # You could check here whether state1, state2, cd1, cd2, and year have valid values
    # and handle the case where they don't
        return redirect(url_for('main.results', state1=state1, state2=state2, cd1=cd1, cd2=cd2, year=year))
    
    if cd1 and cd2:
        return redirect(url_for('main.results', state1=state1, state2=state2, cd1=cd1, cd2=cd2, year=year))

    return render_template('add_info.html', form1=form1, form2=form2, zip1=zip1, zip2=zip2, year=year, status1=status1, status2=status2)


@bp.route('/results2', methods = ['GET', 'POST'])
def results2():
    print('rendering results2')
    # Retrieve parameters depending on the type of request
    state1 = request.args.get('state1')
    state2 = request.args.get('state2')
    cd1 = request.args.get('cd1')
    cd2 = request.args.get('cd2')
    year = int(request.args.get('year'))


    # Set year to next election year
    if (year % 2) != 0:
        year += 1
    
    yr4 = year - 4
    yr8 = year - 8

    elections1 = UpcomingElection.get(state1, year)
    elections2 = UpcomingElection.get(state2, year)

    for race in elections1:
        if race['office'] == "US PRESIDENT":
            pres1_1 = presPack(state1, yr4)
            pres2_1 = presPack(state1, yr8)
        sen1_1 = None
        sen2_1 = None
        if race['office'] == "US SENATE":
            sen1_1 = (senPack(state1, (year-6)))['regular']
            sen2_1 = (senPack(state1, (year-12)))['regular']
        if race['office'] == "US HOUSE":
            house1_1 = (housePack(state1, cd1, yr4))['regular']
            house2_1 = (housePack(state1, cd1, (year-6)))['regular']

    for race in elections2:
        if race['office'] == "US PRESIDENT":
            pres1_2 = presPack(state2, yr4)
            pres2_2 = presPack(state2, yr8)
        sen1_2 = None
        sen2_2 = None
        if race['office'] == "US SENATE":
            sen1_2 = (senPack(state2, (year-6)))['regular']
            sen2_2 = (senPack(state2, (year-12)))['regular']
        if race['office'] == "US HOUSE":
            house1_2 = (housePack(state2, cd2, yr4))['regular']
            house2_2 = (housePack(state2, cd2, (year-6)))['regular']
    
    return render_template('results2.html', year=year, yr4=yr4, yr8=yr8, state1=state1, state2=state2,
                           pres1_1=pres1_1, pres1_2=pres1_2, pres2_1=pres2_1, pres2_2=pres2_2,
                           sen1_1=sen1_1, sen1_2=sen1_2, sen2_1=sen2_1, sen2_2=sen2_2,
                           house1_1=house1_1, house1_2=house1_2, house2_1=house2_1, house2_2=house2_2)


@bp.route('/results', methods=['GET', 'POST'])
def results():
    # Retrieve parameters depending on the type of request
    state1 = request.args.get('state1')
    state2 = request.args.get('state2')
    cd1 = request.args.get('cd1')
    cd2 = request.args.get('cd2')
    year = request.args.get('year')

    pres1, pres2, sen1, senspecial1, sen2, senspecial2, house1, housespecial1, house2, housespecial2 = packAll(state1, cd1, state2, cd2, year)

    return render_template('results.html', state1=state1, cd1=cd1, pres1=pres1, sen1=sen1,
                            senspecial1=senspecial1, house1=house1, housespecial1=housespecial1,
                            state2=state2, cd2=cd2, pres2=pres2, sen2=sen2,
                            senspecial2=senspecial2, house2=house2, housespecial2=housespecial2)


# ----- Helper Functions -----
def apiZipPack(zip:int, line1="", city="", state=""):
    """
    Queries Google API based on zip input to get corresponding state and congressional district, outputting them as a tuple (state, cd).

    If either cannot be found, returns None for that element.
    """
    apiPack = voteInfo_address(zip, line1, city, state)
    cd = None
    state = None

    code = apiPack['code']
    if code > 0:
        state = apiPack['data']['state']
    if code == 2:
        cd = apiPack['data']['cd']

    return state, cd


def presPack(state, year):
    """
    Triggers SQL functions to collect the following presidential info:

    year, state, totalVotes, margin, winner, ev, power

    If no return, still spits out the dictionary, but with empty values.
    """
    pres_ret = President.getPres(state, year)
    if pres_ret:
        winner = pres_ret[0]
        margin = President.calcMargin(pres_ret)
        pres = {'year':year, 'state':winner['state'], 'totalVotes':winner['totalVotes'], 'margin':margin, 'winner':winner['candidate']}
        ev = EV.get(state, year)
        pres['ev'] = ev
        weight = calcWeight(pres['totalVotes'], ev)
        pres['power'] = calcPower(weight, pres['margin'], 'pres')
        pres['margin']=pres['margin']*100
        return pres
    
    # If no return, return None
    return None


def senPack(state, year):
    """
    Triggers SQL functions to collect the following senate info:

    year, state, totalVotes, margin, winner, power. If no data returned, returns None.

    Returns a dictioanry, with up to two values; "regular" and "special."
    """
    sen_ret = Senate.getSen(state, year)
    # Pulls the dictionary that can contain keys "regular", "special"

    # If no returned data, return None
    if not sen_ret:
        return None
    
    ret = {}
    
    # Process both lists
    for election_type in sen_ret.keys():
        winner = sen_ret[election_type][0]
        margin = Senate.calcMargin(sen_ret[election_type])
        sen = {'year':year, 'state':winner['state'], 'totalVotes':winner['totalVotes'], 'margin':margin, 'winner':winner['candidate']}
        weight = calcWeight(sen['totalVotes'], 1)
        sen['power'] = calcPower(weight, sen['margin'], 'sen')
        sen['margin'] = sen['margin']*100
        sen['special'] = winner['special']
        ret[election_type] = sen
    
    return ret


def housePack(state, cd, year):
    """
    Triggers SQL functions to collect the following house info:

    year, state, cd, totalVotes, margin, winner, power. If no data returned, returns None.

    Returns a dictioanry, with up to two values; "regular" and "special."
    """
    house_ret = House.getHouse(state, cd, year)
    # Pulls the dictionary that can contain keys "regular", "special"

    if not house_ret:
        return None

    ret = {}
    # Process both lists
    for election_type in house_ret.keys():
        winner = house_ret[election_type][0]
        margin = House.calcMargin(house_ret[election_type])
        house = {'year':year, 'state':winner['state'], 'totalVotes':winner['totalVotes'], 'margin':margin, 'winner':winner['candidate']}
        weight = calcWeight(house['totalVotes'], 1)
        house['power'] = calcPower(weight, house['margin'], 'sen')
        house['margin'] = house['margin']*100
        house['special'] = winner['special']
        ret[election_type] = house
    
    return ret


def makePowerPercent(dict1, dict2):
    """
    Adds to each dictionary, if they exist, power as a percentage of their combined total.
    """
    total_power = 0
    if dict1:
        total_power += dict1['power']
    if dict2:
        total_power += dict2['power']

    if total_power > 0:
        if dict1:
            dict1['powerPercent'] = dict1['power'] / total_power
        if dict2:
            dict2['powerPercent'] = dict2['power'] / total_power


def packAll(state1:str, cd1:int, state2:str, cd2:int, year:int):
    """
    Package all President, State, and House info.

    Returns pres1, pres2, sen1, senspecial1, sen2, senspecial2, house1, housespecial1, house2, housespecial2.
    """

    #Process pres info
    pres1 = presPack(state1, year)
    pres2 = presPack(state2, year)

    makePowerPercent(pres1, pres2)

    # Package sen info
    sen1 = None
    senspecial1 = None
    sen2 = None
    senspecial2 = None

    sendict1 = senPack(state1, year)
    if sendict1:
        if 'regular' in sendict1.keys():
            sen1 = sendict1['regular']
        if 'special' in sendict1.keys():
            senspecial1 = sendict1['special']
    
    sendict2 = senPack(state2, year)
    if sendict2:
        if 'regular' in sendict2.keys():
            sen2 = sendict2['regular']
        if 'special' in sendict2.keys():
            senspecial2 = sendict2['special']

    makePowerPercent(sen1, sen2)
    makePowerPercent(senspecial1, senspecial2)

    # Package House info  
    house1 = None
    housespecial1 = None
    house2 = None
    housespecial2 = None

    if cd1:
        housedict1 = housePack(state1, cd1, year)
        # print(housedict1)
        if housedict1:
            if 'regular' in housedict1.keys():
                house1 = housedict1['regular']
            if 'special' in housedict1.keys():
                housespecial1 = housedict1['special']

    if cd2:
        housedict2 = housePack(state2, cd2, year)
        # print(housedict2)
        if housedict2:
            if 'regular' in housedict2.keys():
                house2 = housedict2['regular']
            if 'special' in housedict2.keys():
                housespecial2 = housedict2['special']

    makePowerPercent(house1, house2)
    makePowerPercent(housespecial1, housespecial2)

    return pres1, pres2, sen1, senspecial1, sen2, senspecial2, house1, housespecial1, house2, housespecial2