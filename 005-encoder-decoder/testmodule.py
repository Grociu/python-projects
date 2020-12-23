import encoder
import unittest

# function definitions
encode_message = encoder.encode_message
decode_message = encoder.decode_message


class TestEncoding(unittest.TestCase):

    def test_if_encodes_correctly(self):
        pass

    def encode_raises_error_if_no_key(self):
        pass

    def decode_raises_error_if_no_key(self):
        pass

    def encode_raises_error_if_no_message(self):
        pass

    def decode_raises_error_if_no_message(self):
        pass

    def key_longer_than_message_is_fine(self):
        pass

    def message_is_longer_than_key_is_fine(self):
        pass

    def functions_reverse_each_other(self):
        key = 'password'
        message = 'This is a test message 12345!'
        self.assertEqual(
            decode_message(key, encode_message(key, message)),
            message
            )


if __name__ == '__main__':
    unittest.main()
