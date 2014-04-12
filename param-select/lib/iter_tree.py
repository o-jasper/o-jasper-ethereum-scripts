class IterTree:
    """Iterable tree. NOTE: not very good name!
    """
    at = [0]
    in_chain = None

    def __init__(self, chain):
        self.chain = chain

    def get_at(self, at):
        ret = self.chain
        for el in at[:-1]:
            if len(ret) >= el:
                return None
            ret = ret[el]
        return ret[at[-1]:]

    @property
    def cur(self):
        if self.at is None:
            return None
        if self.in_chain is None:
            self.in_chain = self.get_at(self.at)

        if (type(self.in_chain) is not list or len(self.in_chain) == 0):
            return None
        return self.in_chain[0]

    # Next, or choose depending on
    def next_choice(self, ni=0):
        if self.at is None:
            return None

        self.at[-1] += 1

        if self.in_chain is None:  # Chain not yet located.
            self.in_chain = self.get_at(self.at)
        else:  # Go forward in chain.
            self.in_chain = self.in_chain[1:]

        if len(self.in_chain) == 0:  # Ran out of chain, see if we can go up.
            if len(self.at) <= 2:
                self.at = None
                return None
            self.at = self.at[:-2]
            self.at[-1] += 1
            self.in_chain = self.get_at(self.at)

            assert not type(self.cur) is list  # This precludes selecting.
            return self.cur

        if type(self.cur) is list:  # Only now `ni` is used to select.
            self.in_chain = self.cur[ni]
            self.at.append(ni)
            self.at.append(1)

        return self.cur
