"""
Basic Definitions

Vote Weight: # of votes per Electoral Vote (pres) or for position (in 1000s).

    Calculation: 
        Presidential: (Total Voters / Electoral Votes) * .001

Vote Power: Attempts to standardize and quantify impact each individual vote has on outcome.
                (essentially, ability to swing the election per vote)

    Calculation: VB / (Weight x Margin)
        (0 if seat not available during the election cycle)

        VB = # of of voting blocks (for example, pres is 51 for 50 states + DC, senate is 100). 
            In order to ensure no error, if P is 0, VP = 0.
        
        Margin: |Winner - Runnerup|
        Weight: Vote Weight
        x100 for readability

Variables:
    Margin
"""

# ----- Functions -----
def calcWeight(voters, units):
    """
    Calculates the weight of each vote in relation to the total number of votes required for a unit of political power (in thousands).

    (e.g. in the case of President, # of votes per electoral vote. For Congress, # of votes per seat)
    """
    return (voters / units) * .001


def calcPower(weight:float, margin:float, race:str)->float:
    """
    Calcualtes the voting power based on input weight, margin, and type of race (to calculate voting blocks).

    Race: pres, sen, house. Converts to 51, 100, and 435, respectively.
    """
    votingBlocks = {"pres": 51, "sen": 100, "house": 435}
    vb = votingBlocks[race]

    return vb / (weight * margin)