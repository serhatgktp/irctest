"""
Regression tests for bugs in oragono.
"""

from irctest import cases

class RegressionsTestCase(cases.BaseServerTestCase):

    @cases.SpecificationSelector.requiredBySpecification('RFC1459')
    def testFailedNickChange(self):
        # see oragono commit d0ded906d4ac8f
        self.connectClient('alice')
        self.connectClient('bob')

        # bob tries to change to an in-use nickname; this MUST fail
        self.sendLine(2, 'NICK alice')
        ms = self.getMessages(2)
        self.assertEqual(len(ms), 1)
        self.assertMessageEqual(ms[0], command='433') # ERR_NICKNAMEINUSE

        # bob MUST still own the bob nick, and be able to receive PRIVMSG as bob
        self.sendLine(1, 'PRIVMSG bob hi')
        ms = self.getMessages(1)
        self.assertEqual(len(ms), 0)
        ms = self.getMessages(2)
        self.assertEqual(len(ms), 1)
        self.assertMessageEqual(ms[0], command='PRIVMSG', params=['bob', 'hi'])