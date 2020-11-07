#!/usr/bin/env python

# Written November 6, 2020 and released per the free MIT license.
#
# For my black and brown fellow citizens who stood in line to reject
# the most corrupt, racist, unhinged, narcisstic, and incompetent
# president in history. Thank you, fellow citizens. Fellow white
# people, especially fellow white men: Get a clue already.

# Arizona data current with the New York Times's tabulation as of 8 AM
# Pacific, 11/7/2020.


import textwrap


class Messenger(object):
    line_length = 50

    def __init__(self):
        self.w = textwrap.TextWrapper(
            width=self.line_length,
            subsequent_indent=self.space(2),
            break_long_words=False)

    def space(self, N):
        return " "*N

    def dashes(self):
        print("-"*self.line_length)

    def linebreak(self):
        print("\n")

    def __call__(self, proto, *args):
        text = proto.format(*args)
        print(self.w.fill(text))

    def table_row(self, first, second, third):
        """
        Call with the contents of a single row of a text table.
        """
        self("{:>16s}  {:6d}  {:6d}", first, second, third)

        
class County(object):
    """
    I represent one county of a state with votes yet to be counted.
    """
    def __init__(self, name, pct_reported, total, biden_margin):
        """
        Construct with county I{name}, percentage reported I{pct_reported}
        (0-100), I{total} votes cast thus far, and percentage margin
        of votes going to Biden (-100 to +100), I{biden_margin}.
        """
        self.name = name
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

    @property
    def B(self):
        return self.share(self.biden_margin)

    @property
    def T(self):
        return self.share(-self.biden_margin)

    @property
    def p_BT(self):
        return float(self.NT_B + self.NT_T) / self.NT

    def __int__(self):
        return int(round(self.total))

    def __add__(self, other):
        return int(self) + int(other)

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
    NT_B = 1627902
    NT_T = 1606714
    NT  = 3285927
    
    
class NV_County(County):
    NT_B = 642604
    NT_T = 616905
    NT  = 1287403
    
    
AZ = [
    AZ_County('Apache',           75,      25355,          +38     ),
    AZ_County('Pinal',            86,      163455,         -15     ),
    AZ_County('Cochise',          89,      54381,          -17     ),
    AZ_County('Navajo',           90,      51464,          -8      ),
    AZ_County('Santa Cruz',       93,      19546,          +36     ),
    AZ_County('Pima',             95,      501058,         +20     ),
    AZ_County('La Paz',           95,      6677,           -37     ),
    AZ_County('Yuma',             97,      68427,          -6      ),
    AZ_County('Maricopa',         98,      2039433,        +2      ),
    AZ_County('Mohave',           98,      103836,         -51     ),
    AZ_County('Yavapai',          99,      141719,         -29     ),
    AZ_County('Coconino',         99,      72413,          +24     ),
    AZ_County('Gila',             99,      27726,          -34     ),
    AZ_County('Graham',           99,      15026,          -45     ),
    AZ_County('Greenlee',         99,      3692,           -34     ),
]

NV = [
    NV_County('Lincoln',          87,      2312,          -71      ),
    NV_County('Mineral',          88,      2179,          +27      ),
    NV_County('White Pine',       89,      4177,          +58      ),
    NV_County('Lander',           89,      2653,          +62      ),
    NV_County('Clark',            90,      866924,         +9      ),
    NV_County('Storey',           90,      2870,          +35      ),
    NV_County('Esmeralda',        90,      474,           +67      ),
    NV_County('Elko',             92,      21063,         +55      ),
    NV_County('Churchill',        92,      12503,         +49      ),
    NV_County('Humboldt',         92,      7324,          +54      ),
    NV_County('Carson City',      94,      29126,         +11      ),
    NV_County('Washoe',           97,      245674,         +4      ),
    NV_County('Douglas',          97,      33537,         +29      ),
    NV_County('Pershing',         91,      2232,          +51      ),
    NV_County('Lyon',             99,      29392,         +41      ),
    NV_County('Nye',              99,      24021,         +40      ),
    NV_County('Eureka',           99,      942,           +79      ),
]


msg = Messenger()
for name, counties in (("Arizona", AZ), ("Nevada", NV)):
    N = sum([int(vv) for vv in counties])
    B_now = sum([vv.B for vv in counties])
    T_now = sum([vv.T for vv in counties])

    msg(name)
    msg.dashes()
    msg("County, +Votes expected for Biden, +Total expected")
    msg.dashes()
    for c in counties:
        msg.table_row(c.name, c.expected_share(), c.N_remaining())
    msg.dashes()
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

    msg.linebreak()

    
