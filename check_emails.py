"""
Check Emails
2021
This program checks for received emails from one or more email addresses
and displays them in the console.
"""

from imapclient import IMAPClient
from imapclient.exceptions import LoginError
import os
import sys


def main():
    """
    Check for emails from one or more senders and display messages if found.
    
    Program will pause if emails are found or gmail login failed.
    Username and password should be set as environment variables:
    EMAIL_USERNAME: str of username (your email address)
    EMAIL_PASSWORD: str of password
    SENDER_ADDRESSES: comma-separated list of sender's email addresses
    (Leave out the comma if only one sender address is present).
    """
    username = os.getenv("EMAIL_USERNAME")
    password = os.getenv("EMAIL_PASSWORD")
    senders = os.getenv("SENDER_ADDRESSES").split(",")
    
    was_successful, email_ids = get_email_ids(username, password, senders)
    
    if was_successful:
        # If ids were found, display messages and pause console.
        if emails_were_found(email_ids):
            for sender in email_ids:
                # If emails were found from sender, display message.
                num_emails = len(email_ids[sender])
                if num_emails > 0:
                    sys.stdout.write(f"{num_emails} new email{'' if num_emails == 1 else 's'} from {sender.decode()}\n")
            os.system("pause")
    else:
        # If login failed, display error message and pause console.
        sys.stdout.write("Login failed; check credentials or enable less secure apps: https://myaccount.google.com/lesssecureapps\n")
        os.system("pause")


def emails_were_found(email_ids):
    """
    Return true if at least one email was found, otherwise false.
    
    :param dict email_ids: dict of sender addresses to list of ids
    :return: true or false
    :rtype: bool
    """
    for id_list in email_ids.values():
        if len(id_list) > 0:
            return True
    return False


def get_email_ids(username, password, senders):
    """
    Search for emails from senders using imapclient and return dict of ids.
    
    :param str username: your email username
    :param str password: your email password
    :param list senders: list of sender's email addresses
    :return: dictionary of sender addresses to list of found ids
    :rtype: dict
    """
    # Store ids as a dict of {sender: list of ids}
    email_ids = {bytes(sender, "ASCII"): [] for sender in senders}  # {b"example@gmail.com": [0, 12, 5643]}
    was_successful = True
    
    with IMAPClient("imap.gmail.com") as gmail:
        try:
            gmail.login(username, password)
            gmail.select_folder("INBOX", readonly=True)
            for sender in email_ids:
                # Add found ids to dict with key of sender.
                email_ids[sender] += gmail.search([b"FROM", bytes(sender), b"UNSEEN"])
        except LoginError:
            was_successful = False
        
    return was_successful, email_ids


if __name__ == '__main__':
    main()
