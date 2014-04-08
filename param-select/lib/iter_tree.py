# Iterable tree. NOTE: not very good name!
class IterTree:
    at = [0]
    in_chain = None

    def __init__(self, chain):
        self.chain = chain

    def get_at(self, at):
        ret = self.chain
        for el in at[:-1]:
            ret = ret[el]
        return ret[at[-1]:]

    @property
    def cur(self):
        if self.in_chain is None:
            self.in_chain = self.get_at(self.at)
        return self.in_chain[0]

    # Next, or choose depending on 
    def next_choice(self, ni=0):
        self.at[-1] += 1

        if self.in_chain is None:
            self.in_chain = self.get_at(self.at)
        else:
            self.in_chain = self.in_chain[1:]

        if len(self.in_chain) == 0:
            self.at = self.at[:-2]
            self.at[-1] += 1
            self.in_chain = self.get_at(self.at)

        if type(self.cur) is list:
            self.in_chain = self.cur[ni]
            self.at.append(ni)
            self.at.append(1)

        return self.cur
