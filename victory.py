#!/usr/bin/env python

# Written November 6, 2020 and released per the free MIT license.
#
# For my black and brown fellow citizens who stood in line to reject
# the most corrupt, racist, unhinged, narcisstic, and incompetent
# president in history. Thank you, fellow citizens. Fellow white
# people, especially fellow white men: Get a clue already.

# Arizona data current with the New York Times's tabulation as of 9:09
# PM Pacific, 11/6/2020.

def msg(proto, *args):
    print(proto.format(*args))


class County(object):
    """
    I represent one county of a state with votes yet to be counted.
    """
    def __int__(self):
        return int(round(self.total))

    def __add__(self, other):
        return int(self) + int(other)

    @property
    def B(self):
        return self.share(self.biden_margin)

    @property
    def T(self):
        return self.share(-self.biden_margin)

    @property
    def p_BT(self):
        return float(self.NT_B + self.NT_T) / self.NT
    
    def __init__(self, pct_reported, total, biden_margin):
        """
        Construct with percentage reported I{pct_reported} (0-100),
        I{total} votes cast thus far, and percentage margin of votes
        going to Biden (-100 to +100), I{biden_margin}.
        """
        self.pr = 0.01 * pct_reported
        self.total = total
        self.biden_margin = biden_margin
        # With a 10% margin, pb is 0.55, because 1-pb = 0.45.
        self.pb = 0.5 + 0.005*biden_margin
        B = self.B
        NT_B = int(self.pb*self.p_BT*self.total)
        if abs(B - NT_B) > 10:
            raise ValueError(
                "Too much error in computation of Biden vote share thus far: "+\
                "B={:d}, pb*p_BT*NT={:d} != {:d}", B, NT_B)

    def N_remaining(self):
        """
        Returns the number of votes expected for one of the two candidates
        that remain uncounted.
        """
        N_expected = int(round(float(self.total) / self.pr))
        return N_expected - int(self)
        
    def share(self, pct_margin):
        """
        Call with the percentage margin I{pct_margin} between the
        candidate of interest and his opponent. Returns that
        candidate's share of the votes counted thus far.
        """
        total = self.p_BT * self.total
        difference = 0.01*pct_margin * total
        return int(0.5*(total + difference))
    
    def expected_share(self, votes=None):
        """
        Call with a number of I{votes}, or the number not yet counted, and
        returns Biden's expected share, given his share thus far.
        """
        if votes is None:
            votes = self.N_remaining()
        share = int(round(float(self.B) / (self.B + self.T) * votes))
        # Sanity check
        share2 = int(round(self.pb * votes))
        if abs(share - share2) > 10:
            raise ValueError("Sanity check failed computing expected_share!")
        return share


class AZ_County(County):
    NT_B = 1604067
    NT_T = 1574206
    NT  = 3235450
    
    
class NV_County(County):
    NT_B = 632558
    NT_T = 609901
    NT  = 1269513
    
    
AZ = {
    'Apache':           AZ_County(72,      24333,          +37     ),
    'Pinal':            AZ_County(82,      156460,         -15     ),
    'Cochise':          AZ_County(89,      54381,          -17     ),
    'Navajo':           AZ_County(90,      51464,          -8      ),
    'Santa Cruz':       AZ_County(93,      19546,          +36     ),
    'Pima':             AZ_County(95,      501058,         +20     ),
    'Yuma':             AZ_County(95,      66677,          -6      ),
    'La Paz':           AZ_County(95,      6677,           -37     ),
    'Maricopa':         AZ_County(96,      1991563,        +3      ),
    'Mohave':           AZ_County(98,      103836,         -51     ),
    'Yavapai':          AZ_County(99,      141719,         -29     ),
    'Coconino':         AZ_County(98,      72110,          +24     ),
    'Gila':             AZ_County(99,      27726,          -34     ),
    'Graham':           AZ_County(99,      15026,          -45     ),
    'Greenlee':         AZ_County(99,      3692,           -34     ),
}

NV = {
    'Lincoln':          NV_County(87,      2312,          -71      ),
    'Clark':            NV_County(88,      852228,         +9      ),
    'Mineral':          NV_County(88,      2179,          +27      ),
    'Elko':             NV_County(89,      20575,         +56      ),
    'White Pine':       NV_County(89,      4177,          +58      ),
    'Lander':           NV_County(89,      2653,          +62      ),
    'Storey':           NV_County(90,      2870,          +35      ),
    'Esmeralda':        NV_County(90,      474,           +67      ),
    'Pershing':         NV_County(91,      2232,          +51      ),
    'Churchill':        NV_County(92,      12503,         +49      ),
    'Humboldt':         NV_County(92,      7324,          +54      ),
    'Carson City':      NV_County(94,      29126,         +11      ),
    'Nye':              NV_County(94,      22857,         +40      ),
    'Washoe':           NV_County(97,      244132,         +4      ),
    'Douglas':          NV_County(97,      33537,          +29     ),
    'Lyon':             NV_County(99,      29392,          +41     ),
    'Eureka':           NV_County(99,      942,            +79     ),
}

for name, State in (("Arizona", AZ), ("Nevada", NV)):
    counties = State.values()
    N = sum([int(vv) for vv in counties])
    B_now = sum([vv.B for vv in counties])
    T_now = sum([vv.T for vv in counties])
    
    msg("\n{}\n{}", name, '-'*79)
    msg("There have been "+\
        "{:d} votes cast for either Biden or Trump.", N)
    msg("Biden currently has {:d} of the votes cast.", B_now)
    msg("Trump currently has {:d} of the votes cast.", T_now)
    C = counties[0]
    msg("Difference (absolute) between sum of expected current "+\
        "per-candidate totals vs current BT votes cast: {:d}",
        abs(B_now + T_now - (C.NT_B + C.NT_T)))
    
    N_remaining = sum([vv.N_remaining() for vv in counties])
    B_expected = sum([vv.expected_share() for vv in counties])
    msg("Biden's expected share of the votes estimated "+\
        "still uncounted: {:d}", B_expected)
    T_expected = sum([
        int(vv.N_remaining() - vv.expected_share()) for vv in counties])
    msg("Trump's expected share of the votes estimated "+\
        "still uncounted: {:d}", T_expected)
    
    B_total_expected = B_now + B_expected
    msg("Total Biden votes expected: {:d}", B_total_expected)
    T_total_expected = T_now + T_expected
    msg("Total Trump votes expected: {:d}", T_total_expected)
    N_total_expected = B_total_expected + T_total_expected
    msg("Biden's expected total % of Biden+Trump votes: {:+.1f}",
        100.0*B_total_expected/N_total_expected)
    
    msg("Expected total vote difference: {:d}",
        B_total_expected - T_total_expected)

    
