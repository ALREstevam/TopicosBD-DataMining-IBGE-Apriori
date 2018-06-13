class AprioriUnusedMethods:
    def combine(self, arrayToComb, maxCombs, maxOnly = False):
        groups = [c for i in range(maxCombs + 1) for c in combinations(arrayToComb, i)]
        answ = []

        if len(groups) > 1:
            groups = groups[1:]

        if maxOnly == True:
            for element in groups:
                if len(element) == maxCombs:
                    answ.append(element)
            return answ
        else:
            return groups


    def noSupport(self, tupArr) -> float:
        '''
        Suporte (X->Y) = número de registros contendo X e Y / Total de registros
        O método recebe um vetor com tuplas: [(nome_da_coluna, valor_a_testar), ...]

        :param tupArr: vetor de tuplas no formato (nome_da_coluna, valor_a_testar)
        :return: suporte dos itens enviados
        '''
        equal = 0 #contador de linhas com todos os registros enviados
        totalRegisters = self.rows #total de registros

        for line in self.df.iterrows():# para cada linha do dataframe
            localEqual = 0
            for element in tupArr: # para cada linha do vetor de tuplas
                templine = int(line[1][element[0]])#
                tempitem = int(element[1])
                if templine == tempitem:
                    localEqual += 1
            if localEqual == len(tupArr):
                equal += 1
        return equal / totalRegisters


    def permutate(self, arr, elements):
        return list(itertools.permutations(arr, elements))