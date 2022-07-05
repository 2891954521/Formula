import re

class BaseAnalyzer():

    def __init__(self):
        pass

class FourArithmetic(BaseAnalyzer):

        regAddOrSub = re.compile(r'[0-9.]+[\+\-][0-9.]+')
        regMultiplyOrDivide = re.compile(r'[0-9.]+[\*\/][0-9.]+')

        def __init__(self):
            pass
    
        def analyze(self, formula: str):
            try:
                hasOperation = True

                while hasOperation:
                    hasOperation = False
                        
                    # 找一个乘除表达式
                    matcher = re.search(self.regMultiplyOrDivide, formula)
                    if matcher is not None:
                        formula = formula[0 : matcher.start()] + '{:.2f}'.format(eval(matcher.group(0))).rstrip('0').rstrip('.') + formula[matcher.end() : ]
                        hasOperation = True
                        continue

                    # 找一个加减表达式
                    matcher = re.search(self.regAddOrSub, formula)
                    if matcher is not None:
                        formula = formula[0 : matcher.start()] + str(eval(matcher.group(0))) + formula[matcher.end() : ]
                        hasOperation = True
                        continue

                return formula
            except:
                return ''