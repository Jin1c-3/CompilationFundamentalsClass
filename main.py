import LexicalAnalyzer
from enum import Enum
from tabulate import tabulate


# 定义单词的种别
class WordCategory(Enum):
    IDENTIFIER = 1
    UNSIGNED_INTEGER = 2
    UNSIGNED_FLOAT = 3
    RESERVED_WORD = 4
    OPERATOR = 5
    DELIMITER = 6


reslist = [
    "auto",
    "break",
    "case",
    "char",
    "const",
    "continue",
    "default",
    "double",
    "do",
    "else",
    "enum",
    "extern",
    "float",
    "for",
    "goto",
    "if",
    "int",
    "long",
    "register",
    "return",
    "short",
    "signed",
    "sizeof",
    "static",
    "struct",
    "switch",
    "typedef",
    "union",
    "unsigned",
    "void",
    "volatile",
    "while",
    "scanf",
    "main"
]

operators = [
    "++",
    "--",
    "==",
    ">=",
    "<=",
    "&&",
    "||",
    "<<",
    ">>",
    "!=",
    ">",
    "<",
    "!",
    "&",
    "|",
    "^",
    "~",
    "+",
    "-",
    "*",
    "/",
    "%",
    "=",
]

delimiters = ["(", ")", "[", "]", "{", "}", ",", ";", ":"]

legal_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_+-*/%()[]{}=<>!&|^~,:;.# \n\t'\"\\"


def output_lexical_analyzer_results(
    lexical_tuples, idlist, uintlist, ufdlist, reslist, op_list, delimiters_list
):
    """
    输出结果的函数，将所有单词的二元式按顺序输出到output文件，并将用户标识符表idlist、常数表uintlist和常数表ufdlist输出到相应的文件
    """
    try:
        with open("output.txt", "w") as file:
            # 打印WordCategory枚举类的所有成员
            file.write("Lexical Categories:\n")
            file.write(
                "\n".join(f"{member.name}: {member.value}" for member in WordCategory)
                + "\n\n"
            )

            file.write("Lexical Tuples:\n")
            file.write(
                "\n".join(
                    f"ERROR()" if tuple['category'] is None else f"({WordCategory(tuple['category']).name}, {tuple['value']})"
                    for tuple in lexical_tuples
                )
                + "\n\n"
            )

            file.write("Identifiers:\n")
            file.write(tabulate([[id['name'], id['type'], id['storage_length']] for id in idlist], tablefmt='plain', headers=["Name", "Type", "Storage Length"]) + "\n\n")

            file.write("Unsigned Integers:\n")
            file.write(tabulate([[uint['value'], uint['type'], uint['storage_length']] for uint in uintlist], tablefmt='plain', headers=["Value", "Type", "Storage Length"], numalign="left", stralign="left") + "\n\n")

            file.write("Unsigned Floats:\n")
            header = "Value\tType\tStorage Length\n"
            rows = [f"{float(ufd['value']):.4f}\t\t" for ufd in ufdlist]
            table = header + "\n".join(rows)
            file.write(table + "\n\n")

            file.write("Reserved Words: " + ", ".join(reslist) + "\n\n")
            file.write("Operators: " + ", ".join(op_list) + "\n\n")
            file.write("Delimiters: " + ", ".join(delimiters_list) + "\n\n")

            print("Successfully wrote to output file.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":

    """
    主函数，用于调用其他函数完成词法分析器的功能
    """
    la = LexicalAnalyzer.LexicalAnalyzer(
        category=WordCategory,
        reslist=reslist,
        operators=operators,
        delimiters=delimiters,
        legal_characters=legal_characters,
    )

    (
        lexical_tuples,
        idlist,
        uintlist,
        ufdlist,
        reslist,
        identified_operators,
        identified_delimiters,
    ) = la.analyze()

    output_lexical_analyzer_results(
        lexical_tuples,
        idlist,
        uintlist,
        ufdlist,
        reslist,
        identified_operators,
        identified_delimiters,
    )
