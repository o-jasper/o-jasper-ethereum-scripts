from random import randrange
import math

def binomial(n, k):
    return math.factorial(n)/(math.factorial(k)*math.factorial(n-k))

class Board:
    def __init__(self, g,b):
        self.g = g
        self.b = b

    def attack_mode(self):  # Probability of attacking via adding bad/removing good.
        return 0.7

    def threshhold_n(self):
        return math.ceil(0.7*self.n)  # 70% must agree.

    def broken(self):
        # The baddies always win or the goodies never do => totally broken.
        return self.threshold_n() <= self.b or self.g < self.threshold_n()
    
    def vote_prob(self, q):
        assert not self.broken()
        sum = 0  # Probably a better algo exists for this.
        for i in range(self.threshold_n(), self.g):
            sum += binomial(i, self.g)*(q**n)*(1-q)**n
        return sum

    def probs(self):
        p_accuse_gb, p_accuse_gg  = self.p_good_accuse()
        p_accuse = p_accuse_gb + p_accuse_gg  # Whether even accusing.

        mode_p = self.attack_mode()
        
        p_rid_good = (p_accuse_gb*self.g + mode_p*self.b)/self.n
        p_rid_bad  = p_accuse_gg*self.g/self.n

        p_add_good = (1-p_accuse)*(1 - self.p_good_add_bad())*self.g/self.n
        p_add_bad  = ((1-p_accuse)*self.p_good_add_bad()*self.g + (1-mode_p)*self.b)/self.n

        assert p_rid_good + p_rid_bad + p_add_good + p_add_bad == 1
        
        # Reduces the probabilities by the chance the vote succeeds.
        p_rid_good *= self.vote_prob(0.9)
        p_rid_bad  *= self.vote_prob(0.1)

        p_add_good *= self.vote_prob(0.9)
        p_add_bad  *= self.vote_prob(0.1)
        
        return p_rid_good, p_rid_bad, p_add_good, p_add_bad

    def sums(self)
        rg,rb,ag,ab = self.probs()
        return rg, rg + rb, rg + rb +ag, rg + rb + ag + ab

    @property
    def n(self):
        return self.g + self.b

    def p_ka(know_p, sphere_p, other_p):
        know_n = 4
        sphere_n = 100        
        if self.n < know_n:
            return know_p
        if self.n < sphere_n:
            return (know_p*know_n + sphere_p*(self.n - know_n))/self.n

        return (know_p*know_n + sphere_p*sphere_n + other_p*(self.n - sphere_n))/self.n

    # Probability of accusing a bad one.
    def p_good_accuse(self):
        investigate_p = 0.2  # Probability of investigating.
        
        know_p = 0.5  # Probability of detecting if you know/dont know.
        investigate_know_p = 0.8
        know_fp = 0.03  # False positives of it.

        sphere_p  = 0.2
        investigate_sphere_p = 0.5
        sphere_fp = 0.05        
        
        other_p = 0.01
        investigate_other_p = 0.2
        other_fp = 0.1

        # Probability if investigating.
        p_i = self.p_ka(investigate_know_p, investigate_sphere_p investigate_other_p)
        # Passive probability.
        p_p = self.p_ka((know_p, sphere_p, other_p)

        # Probability of (false) positive
        pg = investigate_p*p_i + (1-investigate_p)*p_p
        return pg, pg*p_ka(know_fp, sphere_fp, other_fp)

    def p_good_add_bad(self):
        bad_p = 0.5
        detect_p = 0.7
        return bad_p*(1 - detect_p)

# Monte-Carlo.
def timestep(field, g,b, n):
    for _ in range(n):
        if not (g,b) in field:
            field[g,b] = {}
        el = field[g,b]
        if "sums" not in el:
            el["sums"] = Board(g, b).sums()
        rg, rb, ag, ab = el["sums"]
        r = random()
        if r < rg:
            g -= 1
        elif r < rb:
            b -= 1
        elif r < ag:
            g += 1
        elif r < ab:
            b += 1
        el["visits"] = el.get("visits", 0) + 1
    el["final"] = el.get("final", 0) + 1

def addfield(field, index, what, to):
    if not index in field:
        field[index] = {}
    field[[index][what] += to

# Calculating probabilities.
def flow_timestep(n, field):
    n = n or 100
    field = field or {}    
    for k in range(2*n):
        for g,b in field:
            if g > 0 and b >= 0 and not Board(g,b).broken():  #Gotta be people.
                el = field[g,b] 
                if "probs" not in el:
                    el["probs"] = Board(g, b).probs()
                rg, rb, ag, ab = el["sums"]
                p = el.get("prob" if n%2 == 0 else "prob2", 0)
                to_i = "prob2" if n%2 == 0 else "prob"

                addfield(field, (g-1,b),   to_i, p*rg)
                addfield(field, (g,  b-1), to_i, p*rb)
                addfield(field, (g+1,b),   to_i, p*ag)
                addfield(field, (g,  b+1), to_i, p*ab)
    return field

