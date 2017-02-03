from . import SimIRStmt, SimStatementError

class SimIRStmt_WrTmp(SimIRStmt):
    def _execute(self):
        # get data and track data reads
        data = self._translate_expr(self.stmt.data)

        subactions_count = len(self.actions)

        self.state.scratch.store_tmp(self.stmt.tmp, data.expr, data.reg_deps(), data.tmp_deps(),
                                     action_holder=self.actions
                                     )

        # create links in between
        if subactions_count > 0:
            for new_action in self.actions[ subactions_count : ]:
                for old_action in self.actions[ : subactions_count]:
                    new_action.subactions.append(old_action)

        actual_size = data.size_bits()
        expected_size = self.stmt.data.result_size(self.state.scratch.tyenv)
        if actual_size != expected_size:
            raise SimStatementError("WrTmp expected length %d but got %d" % (actual_size, expected_size))
