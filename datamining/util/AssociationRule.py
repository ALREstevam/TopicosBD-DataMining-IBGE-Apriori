from datamining.util.RuleHandSize import RuleHandSize

class AssociationRule:
    def __init__(self, lhs : [RuleHandSize], rhs : RuleHandSize, support, confidence):
        self.rhs = rhs
        self.lhs = lhs
        self.support = support
        self.confidence = confidence
        self.sum = support + confidence

    def __str__(self):
        lhsrules = []
        for rule in self.lhs:
            lhsrules.append(' [\"{}\" = {}]'.format(str(rule.column).strip(), rule.value))
        lhsrulesStr = ', '.join(lhsrules)
        rsp0 = ' >>> {{{}}} => {{ \"{}\" = {} }} '.format(lhsrulesStr, self.rhs.column, self.rhs.value)
        rsp1 = '[sup: {:.2f}, conf: {:.2f}]'.format(self.support, self.confidence)
        rsp = '{:<100s}{:>40s}'.format(rsp0, rsp1)
        return rsp





