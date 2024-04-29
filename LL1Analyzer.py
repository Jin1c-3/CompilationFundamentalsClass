from tabulate import tabulate


class LL1Analyzer:
    def __init__(self, grammar_file):
        self.grammar_file = grammar_file
        self.grammar = self.read_grammar()
        self.non_terminals = set()
        self.terminals = set()
        self.terminals_without_epsilon = set()
        self.first_sets = {}
        self.follow_sets = {}
        self.LL1_table = {}
        for line in self.grammar:
            left, right = line.split("→")
            self.non_terminals.add(left.strip())
            for symbol in right:
                if symbol.islower() or symbol in ["(", "ε", ")", "*", "+"]:
                    self.terminals.add(symbol)
                if symbol.isupper():
                    self.non_terminals.add(symbol)

        self.terminals_without_epsilon = self.terminals - {"ε"} | {"#"}


    def read_grammar(self):
        with open(self.grammar_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        _, lines[0] = lines[0].split("：")
        lines = [line.replace(" ", "").strip() for line in lines]
        new_lines = []
        for line in lines:
            if "|" in line:
                left, rights = line.split("→")
                rights = rights.split("|")
                for right in rights:
                    new_lines.append(f"{left}→{right}")
            else:
                new_lines.append(line)
        return new_lines

    def compute_first_sets(self):
        self.first_sets = {nt: set() for nt in self.non_terminals}

        # 初始化 FIRST 集
        for line in self.grammar:
            left, right = line.split("→")
            if right[0] in self.terminals:
                self.first_sets[left].add(right[0])

        # 不断迭代直到 FIRST 集不再变化
        while True:
            old_first_sets = {nt: set(self.first_sets[nt]) for nt in self.non_terminals}
            for line in self.grammar:
                left, right = line.split("→")
                for symbol in right:
                    if symbol in self.terminals:
                        self.first_sets[left].add(symbol)
                        break
                    else:
                        self.first_sets[left] = self.first_sets[left].union(
                            self.first_sets[symbol] - {"ε"}
                        )
                        if "ε" not in self.first_sets[symbol]:
                            break
                else:
                    self.first_sets[left].add("ε")
            if old_first_sets == self.first_sets:
                break

    def compute_follow_sets(self):
        self.follow_sets = {nt: set() for nt in self.non_terminals}
        self.follow_sets[self.grammar[0].split("→")[0]].add(
            "#"
        )  # 添加结束符到开始符号的 FOLLOW 集

        # 不断迭代直到 FOLLOW 集不再变化
        while True:
            old_follow_sets = {
                nt: set(self.follow_sets[nt]) for nt in self.non_terminals
            }
            for line in self.grammar:
                left, right = line.split("→")
                for i in range(len(right)):
                    if right[i] in self.non_terminals:
                        if i + 1 < len(right):
                            if right[i + 1] in self.non_terminals:
                                self.follow_sets[right[i]] = self.follow_sets[
                                    right[i]
                                ].union(
                                    self.first_sets.get(right[i + 1], set()) - {"ε"}
                                )
                            else:
                                self.follow_sets[right[i]].add(right[i + 1])
                        if i + 1 == len(right) or "ε" in self.first_sets.get(
                            right[i + 1], set()
                        ):
                            self.follow_sets[right[i]] = self.follow_sets[
                                right[i]
                            ].union(self.follow_sets[left])
            if old_follow_sets == self.follow_sets:
                break

    def compute_LL1_table(self):
        self.LL1_table = {
            nt: {t: "" for t in self.terminals_without_epsilon}
            for nt in self.non_terminals
        }

        for line in self.grammar:
            left, right = line.split("→")
            symbol = right[0]
            if symbol in self.terminals and symbol != "ε":
                self.LL1_table[left][symbol] = "→" + right
            else:
                if "ε" in self.first_sets[left] and symbol == "ε":
                    for token in self.follow_sets[left]:
                        self.LL1_table[left][token] = "→" + right
                else:
                    for token in self.first_sets[left]:
                        self.LL1_table[left][token] = "→" + right

    def __str__(self) -> str:
        result = ""
        for nt in self.non_terminals:
            result += f"FIRST({nt}) = {{{', '.join(self.first_sets[nt])}}}\n"
        result += "\n"
        for nt in self.non_terminals:
            result += f"FOLLOW({nt}) = {{{', '.join(self.follow_sets[nt])}}}\n"
        result += "\n"
        table = tabulate(
            [
                [nt] + [self.LL1_table[nt][t] for t in self.terminals_without_epsilon]
                for nt in self.non_terminals
            ],
            headers=[""] + list(self.terminals_without_epsilon),
            tablefmt="grid",
        )
        result += table
        return result

    def dump(self, file_name):
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(str(self))

    def analyze(self):
        # 计算 FIRST 集
        self.compute_first_sets()
        # 计算 FOLLOW 集
        self.compute_follow_sets()
        # 计算 LL(1) 分析表
        self.compute_LL1_table()


if __name__ == "__main__":
    ll1Analyzer = LL1Analyzer("grammar.txt")
    ll1Analyzer.analyze()
    print(ll1Analyzer)
    ll1Analyzer.dump("output1.txt")
