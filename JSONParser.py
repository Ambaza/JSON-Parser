class JSONParser:
    def __init__(self, json_str):
        self.json_str = json_str
        self.index = 0

    def parse(self):
        return self.parse_value()

    def parse_value(self):
        current_char = self.current_char()

        if current_char == '{':
            return self.parse_object()
        elif current_char == '[':
            return self.parse_array()
        elif current_char == '"':
            return self.parse_string()
        elif current_char.isdigit() or current_char == '-':
            return self.parse_number()
        elif current_char.isalpha():
            return self.parse_boolean_or_null()
        else:
            raise ValueError(f"Unexpected character: {current_char}")

    def parse_object(self):
        obj = {}
        self.consume_char('{')

        while self.current_char() != '}':
            key = self.parse_string()
            self.consume_char(':')
            value = self.parse_value()
            obj[key] = value

            if self.current_char() == ',':
                self.consume_char(',')

        self.consume_char('}')
        return obj

    def parse_array(self):
        arr = []
        self.consume_char('[')

        while self.current_char() != ']':
            value = self.parse_value()
            arr.append(value)

            if self.current_char() == ',':
                self.consume_char(',')

        self.consume_char(']')
        return arr

    def parse_string(self):
        self.consume_char('"')
        start_index = self.index
        while self.current_char() != '"':
            self.index += 1

        string_value = self.json_str[start_index:self.index]
        self.consume_char('"')
        return string_value

    def parse_number(self):
        start_index = self.index
        while self.current_char().isdigit() or self.current_char() == '.':
            self.index += 1

        number_value = self.json_str[start_index:self.index]
        return int(number_value) if '.' not in number_value else float(number_value)

    def parse_boolean_or_null(self):
        start_index = self.index
        while self.current_char().isalpha():
            self.index += 1

        value = self.json_str[start_index:self.index]

        if value == 'true':
            return True
        elif value == 'false':
            return False
        elif value == 'null':
            return None
        else:
            raise ValueError(f"Unexpected value: {value}")

    def consume_char(self, char):
        if self.current_char() == char:
            self.index += 1
        else:
            raise ValueError(f"Expected '{char}', got '{self.current_char()}'")

    def current_char(self):
        return self.json_str[self.index] if self.index < len(self.json_str) else None

# Example usage:
json_str = '{"name": "John", "age": 30, "is_student": false, "grades": [95, 89, 78]}'
parser = JSONParser(json_str)
parsed_data = parser.parse()
print(parsed_data)
