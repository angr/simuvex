from .plugin import SimStatePlugin

class SimStateCGC(SimStatePlugin):
    '''
    This state plugin keeps track of CGC state.
    '''

    #__slots__ = [ 'heap_location', 'max_str_symbolic_bytes' ]

    def __init__(self):
        SimStatePlugin.__init__(self)

        self.allocation_base = 0x0c000000
        self.time = 0

        self.max_allocation = 0x0100000

        # CGC error codes
        self.EBADF = 1
        self.EFAULT = 2
        self.EINVAL = 3
        self.ENOMEM = 4
        self.ENOSYS = 5
        self.EPIPE = 6

        # other CGC constants
        self.FD_SETSIZE = 1024

    def addr_invalid(self, a):
        return not self.state.satisfiable(extra_constraints=[a!=0])

    def copy(self):
        c = SimStateCGC()
        c.allocation_base = self.allocation_base
        c.time = self.time
        return c

    def merge(self, others, merge_flag, flag_values):
        merging_occured = False

        new_allocation_base = max(o.allocation_base for o in others)
        if self.allocation_base != new_allocation_base:
            self.allocation_base = new_allocation_base
            merging_occured = True

        return merging_occured, [ ]

SimStatePlugin.register_default('cgc', SimStateCGC)