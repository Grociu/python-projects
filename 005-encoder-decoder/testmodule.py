import encoder
import unittest

# function definitions
encode_message = encoder.encode_message
decode_message = encoder.decode_message


class TestEncoding(unittest.TestCase):

    def test_if_encodes_correctly(self):
        self.assertEqual(
            encode_message('Use this key', 'Is this encoded?'),
            'wp7DpsKFwpTDnMORw5zCk8KFw5nDiMOowrnDmMOJXw=='
        )

    def test_encodes_with_no_key(self):
        self.assertEqual(
            encode_message("", "message"),
            'bWVzc2FnZQ=='
        )

    def test_decodes_with_no_key(self):
        self.assertEqual(
            decode_message("", "dGVzdCBtZXNzYWdl"),
            "test message"
        )

    def test_encode_no_error_if_no_message(self):
        self.assertEqual(
            encode_message("key", ""),
            ""
        )

    def test_decode_if_no_message(self):
        self.assertEqual(
            decode_message("key", ""),
            ""
        )

    def test_functions_reverse_each_other(self):
        key = 'password'
        message = 'This is a test message 12345!'
        self.assertEqual(
            decode_message(key, encode_message(key, message)),
            message
        )

    def test_key_longer_than_message_is_fine(self):
        key = 'String of high length'
        message = 'Short'
        encoded = 'wqbDnMOhw5vDog=='
        with self.assertRaises(Exception):  # essentially assertNotRaises
            try:
                encode_message(key, message)
                decode_message(key, encoded)
            except:   # if an error is raised, the test will fail
                pass  # as Exception error is not raised
            else:     # if everyting is fine, raise Exception
                raise Exception


if __name__ == '__main__':
    unittest.main()
