from datamining.util.RuleHandSize import RuleHandSize

class AssociationRule:
    def __init__(self, lhs : [RuleHandSize], rhs : RuleHandSize, support, confidence):
        self.rhs = rhs
        self.lhs = lhs
        self.support = support
        self.confidence = confidence

    def __str__(self):
        lhsrules = []
        for rule in self.lhs:
            lhsrules.append('{}:{}'.format(rule.column, rule.value))
        lhsrulesStr = ', '.join(lhsrules)
        rsp = 'RULE : {{{}}} => {{{}:{}}} [sup: {}, conf: {}]'.format(lhsrulesStr, self.rhs.column, self.rhs.value, self.support, self.confidence)
        return rsp





