from PIL import Image
import io

bin_to_character_table = {
    "000000": "A", "000001": "B", "000010": "C", "000011": "D",
    "000100": "E", "000101": "F", "000110": "G", "000111": "H",
    "001000": "I", "001001": "J", "001010": "K", "001011": "L",
    "001100": "M", "001101": "N", "001110": "O", "001111": "P",
    "010000": "Q", "010001": "R", "010010": "S", "010011": "T",
    "010100": "U", "010101": "V", "010110": "W", "010111": "X",
    "011000": "Y", "011001": "Z", "011010": "a", "011011": "b",
    "011100": "c", "011101": "d", "011110": "e", "011111": "f",
    "100000": "g", "100001": "h", "100010": "i", "100011": "j",
    "100100": "k", "100101": "l", "100110": "m", "100111": "n",
    "101000": "o", "101001": "p", "101010": "q", "101011": "r",
    "101100": "s", "101101": "t", "101110": "u", "101111": "v",
    "110000": "w", "110001": "x", "110010": "y", "110011": "z",
    "110100": "0", "110101": "1", "110110": "2", "110111": "3",
    "111000": "4", "111001": "5", "111010": "6", "111011": "7",
    "111100": "8", "111101": "9", "111110": "+", "111111": "/",
}

character_to_bin_table = {
    'A': '000000', 'B': '000001', 'C': '000010', 'D': '000011',
    'E': '000100', 'F': '000101', 'G': '000110', 'H': '000111',
    'I': '001000', 'J': '001001', 'K': '001010', 'L': '001011',
    'M': '001100', 'N': '001101', 'O': '001110', 'P': '001111',
    'Q': '010000', 'R': '010001', 'S': '010010', 'T': '010011',
    'U': '010100', 'V': '010101', 'W': '010110', 'X': '010111',
    'Y': '011000', 'Z': '011001', 'a': '011010', 'b': '011011',
    'c': '011100', 'd': '011101', 'e': '011110', 'f': '011111',
    'g': '100000', 'h': '100001', 'i': '100010', 'j': '100011',
    'k': '100100', 'l': '100101', 'm': '100110', 'n': '100111',
    'o': '101000', 'p': '101001', 'q': '101010', 'r': '101011',
    's': '101100', 't': '101101', 'u': '101110', 'v': '101111',
    'w': '110000', 'x': '110001', 'y': '110010', 'z': '110011',
    '0': '110100', '1': '110101', '2': '110110', '3': '110111',
    '4': '111000', '5': '111001', '6': '111010', '7': '111011',
    '8': '111100', '9': '111101', '+': '111110', '/': '111111'
}


def binary_sum(array):
    word = ''
    equals = ''
    for string in array:
        binary_string = ''
        for char in string:
            # Add padding if the character is a '=' sign
            if char == '=':
                equals += '='
            else:
                # Convert the character to a binary string
                binary_string += bin(ord(char))[2:].rjust(8, '0')

        for i in range(0, len(binary_string), 6):
            # Split into 6 bit chunks
            chunk = binary_string[i:i + 6]
            # Add a character to the word based on the base64 mapping
            word += bin_to_character_table[chunk.ljust(6, '0')]
        # If there are any equals add them to the end
        word += equals
    return word


class Base64:
    def __init__(self, base_input, input_type):
        self.file_name = base_input
        self.input_type = input_type
        # If we get a media file we get the contents of it first
        if input_type == 'image' or input_type == 'video':
            self.binary_data = self.read_contents()
        elif input_type == 'string':
            self.binary_data = base_input
        else:
            print("Invalid input type. Please choose between 'image', 'video' or 'string'")
            exit()

    def read_contents(self):
        # Open image in read binary mode (returns a byte object)
        with open(self.file_name, 'rb') as image:
            content = image.read()

        binary_string = ""
        for byte in content:
            # Convert the byte to a binary string, remove the 'Ob' prefix and fill with padding if needed
            binary_value = bin(byte)[2:].zfill(8)
            # Add byte to our string
            binary_string += binary_value

        return binary_string

    def encode(self):
        if self.input_type == 'string':
            # Calculate the number of sub-strings needed
            num_substrings = (len(self.binary_data) + 2) // 3
            # Add padding to the input string with '=' characters as needed
            s = self.binary_data.ljust(num_substrings * 3, '=')
            # Split and group the string into 3 character long strings
            substrings = [s[i:i + 3] for i in range(0, num_substrings * 3, 3)]
            return binary_sum(substrings)
        else:
            # Store the binary string into an array with strings that are 6 characters long
            binary_chunks = [self.binary_data[i:i + 6] for i in range(0, len(self.binary_data), 6)]
            encoded_string = ""
            for binary_string in binary_chunks:
                if len(binary_string) != 6:
                    continue
                else:
                    # Map the binary chunk to an ASCII character
                    encoded_string += bin_to_character_table[binary_string]

            return encoded_string

    def decode(self, encoded_string):
        if self.input_type == 'string':
            word = ""
            binary_string = ''
            for char in encoded_string:
                # If the character is not a padding character map it to it's corresponding bits
                if char != '=':
                    binary_string += character_to_bin_table[char]
            # If there are two equal signs remove the last 4 characters since they're used for padding
            if encoded_string.count('=') == 2:
                binary_string = binary_string[:-4]
            # Get the binary string by 8 bit chunks and convert it to an ASCII character
            for i in range(0, len(binary_string), 8):
                word += chr(int(binary_string[i:i + 8], 2))

            print("Decoded message: " + word)

        elif self.input_type == 'video':
            print("A video cannot be constructed...yet")
            return

        else:
            binary_string = ""
            for char in encoded_string:
                # Map the binary chunk to an ASCII character
                binary_string += character_to_bin_table[char]

            # Convert the binary sting into a byte object
            byte_data = bytes(int(binary_string[i:i + 8], 2) for i in range(0, len(binary_string), 8))
            # Create an image from
            image = Image.open(io.BytesIO(byte_data))
            image.show()
