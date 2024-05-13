import ast

# 读取quad_input.txt中的代码
with open("quad_input.txt", "r") as file:
    code = file.read()

# 生成抽象语法树
tree = ast.parse(code)

op_dict = {
    "Mult": "*",
    "Add": "+",
    "Sub": "-",
    "Gt": ">",
    "Lt": "<",
}


class QuadrupleGenerator(ast.NodeVisitor):
    def __init__(self):
        self.temp_var_counter = 0
        self.quadruples = []
        self.backpatches = []

    def new_temp_var(self):
        self.temp_var_counter += 1
        return f"t{self.temp_var_counter}"

    def visit_Assign(self, node):
        target = node.targets[0].id
        value = self.visit(node.value)
        self.quadruples.append(("=", value, "_", target))

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        result = self.new_temp_var()
        self.quadruples.append((op_dict[type(node.op).__name__], left, right, result))
        return result

    def visit_Name(self, node):
        return node.id

    def visit_Num(self, node):
        return str(node.n)

    def visit_Compare(self, node):
        left = self.visit(node.left)
        right = self.visit(node.comparators[0])
        return type(node.ops[0]).__name__, left, right

    def visit_If(self, node):
        op, left, right = self.visit(node.test)
        op = op_dict[op]
        self.quadruples.append(("j" + op, left, right, "_"))
        jTrue_position = len(self.quadruples) - 1
        self.quadruples.append(("j", "_", "_", "_"))
        self.backpatches.append((jTrue_position, len(self.quadruples)))
        jFalse_position = len(self.quadruples) - 1
        for stmt in node.body:
            self.visit(stmt)
        self.quadruples.append(("j", "_", "_", "_"))
        jEnd_position = len(self.quadruples) - 1
        self.backpatches.append((jFalse_position, len(self.quadruples)))
        for stmt in node.orelse:
            self.visit(stmt)
        self.backpatches.append((jEnd_position, len(self.quadruples)))

    def visit_While(self, node):
        start_position = len(self.quadruples)
        op, left, right = self.visit(node.test)
        op = op_dict[op]
        self.quadruples.append(("j" + op, left, right, "_"))
        jTrue_position = len(self.quadruples) - 1
        self.quadruples.append(("j", "_", "_", "_"))
        self.backpatches.append((jTrue_position, len(self.quadruples)))
        jFalse_position = len(self.quadruples) - 1
        for stmt in node.body:
            self.visit(stmt)
        self.quadruples.append(("j", "_", "_", start_position))
        self.backpatches.append((jFalse_position, len(self.quadruples)))


# 使用QuadrupleGenerator生成四元式
generator = QuadrupleGenerator()
generator.visit(tree)

# 回填
for i in range(len(generator.backpatches)):
    position, target = generator.backpatches[i]
    op, arg1, arg2, _ = generator.quadruples[position]
    if "j" in op:
        generator.quadruples[position] = (op, arg1, arg2, target)
    else:
        generator.quadruples[position] = (op, arg1, target, "_")

# 打印回填后的四元式
for i, quadruple in enumerate(generator.quadruples):
    print(i + 100, ":", quadruple)
