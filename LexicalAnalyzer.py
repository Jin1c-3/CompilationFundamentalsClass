import re
from enum import Enum


class LexicalAnalyzer:
    def __init__(
        self,
        category: Enum,
        reslist: list[str],
        operators: list[str],
        delimiters: list[str],
        legal_characters: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_+-*/%()[]{}=<>!&|^~,:;.# \n\t'\"\\",
        file_name="test.c",
    ):
        self.word_categories = category
        self.reserved_words = reslist
        self.operators = operators
        self.delimiters = delimiters
        self.legal_characters = legal_characters
        """
        读取输入文件的函数，从input文件中读取C语言源程序语句
        """
        try:
            with open(file_name, "r") as file:
                self.data = file.read()
                print(f"Successfully read input file named {file_name}.")
        except FileNotFoundError:
            print("Error: input file not found.")
        except Exception as e:
            print(f"Error: {e}")

    def identify_identifiers(self) -> list[dict]:
        """
        识别标识符的函数，识别以字母、_等字符打头的用户标识符，并将其添加到用户标识符表idlist中
        idlist包含标识符名称、类型、存储长度等字段。
        词法分析器运行过程中将用户源程序中出现的用户标识符(包括用户变量名、用户函数名等)填入用户标识符表中的标识符名字段，而标识符类型、存储长度等字段在词法分析阶段为空，这些字段在编译过程的后续阶段填入。
        源程序中若某个用户标识符(比如变量x)出现多次则对应着多个单词，即每次出现都对应一个单词二元式，但其在用户标识符表中只对应1项。
        源程序中的单词二元式必须按出现顺序排列，而用户标识符表中的标识符由于需要查重故可以按ASCII码排序也可以按出现顺序排列{分别对应折半查找和顺序查找}。
        """
        self.identified_identifiers = []
        pattern = r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"
        identifiers = re.findall(pattern, self.data)
        for identifier in identifiers:
            # 检查这个标识符是否是关键字
            if identifier not in self.reserved_words:
                # 创建一个字典来存储标识符名称、类型和存储长度
                identifier_info = {
                    "name": identifier,
                    "type": None,
                    "storage_length": None,
                }
                # 检查这个标识符是否已经在idlist中
                if not any(
                    d["name"] == identifier for d in self.identified_identifiers
                ):
                    self.identified_identifiers.append(identifier_info)
        # 按照标识符在源代码中出现的顺序对idlist进行排序
        self.identified_identifiers.sort(key=lambda x: identifiers.index(x["name"]))
        return self.identified_identifiers

    def identify_unsigned_integers(self):
        """
        识别无符号整数的函数，并将其添加到常数表uintlist中
        uintlist包含数值、类型、存储长度等字段。
        词法分析器运行过程中将用户源程序中出现的无符号整数填入数值字段，而类型、存储长度等字段为空，这些字段在编译过程的后续阶段填入。
        """
        self.identified_unsigned_integers = []
        pattern = r"\b[0-9]+\b"
        unsigned_integers = re.findall(pattern, self.data)
        for unsigned_integer in unsigned_integers:
            # 创建一个字典来存储数值、类型和存储长度
            integer_info = {
                "value": unsigned_integer,
                "type": None,
                "storage_length": None,
            }
            # 检查这个整数是否已经在uintlist中
            if not any(
                d["value"] == unsigned_integer
                for d in self.identified_unsigned_integers
            ):
                self.identified_unsigned_integers.append(integer_info)
        return self.identified_unsigned_integers

    def identify_unsigned_floats(self):
        """
        识别无符号浮点数的函数，并将其添加到常数表ufdlist中
        ufdlist包含数值、类型、存储长度等字段。
        词法分析器运行过程中将用户源程序中出现的无符号浮点数填入数值字段，而类型、存储长度等字段为空，这些字段在编译过程的后续阶段填入。
        """
        self.identified_unsigned_floats = []
        pattern = r"\b[0-9]*\.[0-9]+\b"
        unsigned_floats = re.findall(pattern, self.data)
        for unsigned_float in unsigned_floats:
            # 创建一个字典来存储数值、类型和存储长度
            float_info = {"value": unsigned_float, "type": None, "storage_length": None}
            # 检查这个浮点数是否已经在ufdlist中
            if not any(
                d["value"] == unsigned_float for d in self.identified_unsigned_floats
            ):
                self.identified_unsigned_floats.append(float_info)
        return self.identified_unsigned_floats

    def identify_reserved_words(self):
        """
        识别保留字的函数，在reslist中识别保留字(包括系统函数名)
        保留字在事先存好的保留字表reslist中
        """
        self.identified_reserved_words = []
        for word in self.reserved_words:
            if word in self.data:
                self.identified_reserved_words.append(word)
        return self.identified_reserved_words

    def identify_operators(self):
        """
        识别运算符的函数，识别算术运算符、逻辑运算符和关系运算符
        """
        self.identified_operators = []
        for operator in self.operators:
            if operator in self.data:
                self.identified_operators.append(operator)
        return self.identified_operators

    def identify_delimiters(self):
        """
        识别分隔符的函数，识别括号、逗号、分号等分隔符
        """
        self.identified_delimiters = []
        for delimiter in self.delimiters:
            if delimiter in self.data:
                self.identified_delimiters.append(delimiter)
        return self.identified_delimiters

    def handle_illegal_characters(self):
        """
        错误处理函数，识别非法字符并报错
        """
        errors = []
        for character in self.data:
            if character not in self.legal_characters:
                errors.append(character)
        if errors:
            print("Error: Illegal characters found - ", set(errors))
        else:
            print("No illegal characters found.")

    def generate_lexical_tuples(self):
        """
        生成词法二元式的函数，识别源代码中的所有单词，并将它们的二元式存储在一个字典列表中
        """
        # 初始化词法二元式列表
        self.lexical_tuples = []

        # 使用正则表达式分割字符串
        words = [
            word
            for word in re.findall(
                r"[^\s"
                + re.escape("".join(self.operators))
                + re.escape("".join(self.delimiters))
                + r"]+|["
                + re.escape("".join(self.operators))
                + re.escape("".join(self.delimiters))
                + r"]",
                self.data,
            )
            if word
        ]

        # 遍历源代码，识别出所有的单词
        for word in words:
            # 初始化词法二元式
            lexical_tuple = {"category": None, "value": word}

            # 判断单词的种别，并将种别和值存储在词法二元式中
            if any(word == id_dict["name"] for id_dict in self.identified_identifiers):
                lexical_tuple["category"] = self.word_categories.IDENTIFIER.value
            elif any(
                word == uint_dict["value"]
                for uint_dict in self.identified_unsigned_integers
            ):
                lexical_tuple["category"] = self.word_categories.UNSIGNED_INTEGER.value
            elif any(
                word == ufd_dict["value"]
                for ufd_dict in self.identified_unsigned_floats
            ):
                lexical_tuple["category"] = self.word_categories.UNSIGNED_FLOAT.value
            elif word in self.identified_reserved_words:
                lexical_tuple["category"] = self.word_categories.RESERVED_WORD.value
            elif word in self.operators:
                lexical_tuple["category"] = self.word_categories.OPERATOR.value
            elif word in self.delimiters:
                lexical_tuple["category"] = self.word_categories.DELIMITER.value

            # 将词法二元式添加到列表中
            self.lexical_tuples.append(lexical_tuple)
        return self.lexical_tuples

    def analyze(self):
        """
        主函数，用于调用其他函数完成词法分析器的功能
        """
        # 处理错误，识别非法字符并报错
        print("Handling errors...")
        if self.handle_illegal_characters():
            return

        # 识别用户标识符并添加到用户标识符表idlist中
        print("Identifying identifiers...")
        self.identify_identifiers()

        # 识别无符号整数并添加到常数表uintlist中
        print("Identifying unsigned integers...")
        self.identify_unsigned_integers()

        # 识别无符号浮点数并添加到常数表ufdlist中
        print("Identifying unsigned floats...")
        self.identify_unsigned_floats()

        # 识别保留字并将其存入保留字表reslist中
        print("Identifying reserved words...")
        self.identify_reserved_words()

        # 识别算术运算符、逻辑运算符和关系运算符
        print("Identifying operators...")
        self.identify_operators()

        # 识别分隔符
        print("Identifying delimiters...")
        self.identify_delimiters()

        # 调用 generate_lexical_tuples 函数
        print("Generating lexical tuples...")
        self.generate_lexical_tuples()

        print("Lexical analysis completed.")

        return (
            self.lexical_tuples,
            self.identified_identifiers,
            self.identified_unsigned_integers,
            self.identified_unsigned_floats,
            self.identified_reserved_words,
            self.identified_operators,
            self.identified_delimiters,
        )
