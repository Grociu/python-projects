import email_grab
import unittest


# function definitions
grab_emails = email_grab.grab_emails


class TestEmailValidator(unittest.TestCase):

    def test_if_validating_mails(self):
        """
        Some valid addresses don't pass the test, given the basic simplicity of
        regex used. See comment in the next test.
        """
        valid_emails = [
            'email@example.com', 'firstname.lastname@example.com',
            'email@subdomain.example.com', 'firstname+lastname@example.com',
            'email@123.123.123.123', '1234567890@example.com',
            'email@example-one.com', '_______@example.com',
            'email@example.name', 'email@example.museum',
            'email@example.co.jp', 'firstname-lastname@example.com'
        ]
        for mail in valid_emails:
            self.assertEquals(grab_emails(mail), [mail])

    def test_invalid_mails(self):
        """
        These examples are SPECIFICALLY selected for the regex to pass,
        There exist invalid e-mail addresses that get 'found' by the function,
        but this is not the scope of this exercise.
        An e-mail validation formula can be found on StackOverflow if needed,
        but it ain't pretty.
        """
        invalid_emails = [
            'plainaddress', '#@%^%#$@#$@#.com', '@example.com',
            'Joe Smith <email@example.com>', 'email.example.com',
            'email@example@example.com', 'あいうえお@example.com',
            'email@example.com (Joe Smith)', 'email@example'
        ]
        for mail in invalid_emails:
            self.assertEquals(grab_emails(mail), [])


if __name__ == '__main__':
    unittest.main()
