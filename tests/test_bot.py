# -*- coding: utf-8 -*-
from irc3.testing import BotTestCase


class TestBot(BotTestCase):

    def test_plugin(self):
        bot = self.callFTU()
        bot.include('irc3.plugins.log')
        plugin = bot.get_plugin('irc3.plugins.log.RawLog')
        self.assertTrue(plugin is not None)
        self.assertRaises(LookupError, bot.get_plugin,
                          'irc3.plugins.command.Commands')

    def test_event(self):
        bot = self.callFTU()
        bot.include('irc3.plugins.core')
        self.assertIn('<event ', repr(bot.events[0]))

    def test_log(self):
        bot = self.callFTU()
        bot.include('irc3.plugins.log')
        bot.dispatch('PING :youhou')
        bot.dispatch(':gawel!user@host PRIVMSG #chan :youhou')

    def test_ping(self):
        bot = self.callFTU()
        bot.include('irc3.plugins.core')
        bot.dispatch('PING :youhou')
        self.assertSent(['PONG youhou'])

    def test_nick(self):
        bot = self.callFTU()
        bot.include('irc3.plugins.core')
        self.assertEqual(bot.nick, 'foo')
        bot.dispatch(':foo!user@host NICK bar')
        self.assertEqual(bot.nick, 'bar')
        bot.dispatch(':h.net 432 * bar :xx')
        self.assertSent(['NICK bar_'])

    def test_part(self):
        bot = self.callFTU()
        bot.part('#foo')
        self.assertSent(['PART #foo'])
        bot.part('#foo', 'bye')
        self.assertSent(['PART #foo :bye'])

    def test_autojoin(self):
        bot = self.callFTU(autojoins=['#foo'])
        bot.include('irc3.plugins.core')
        bot.dispatch(':hobana.freenode.net 376 irc3 :End of /MOTD command.')
        self.assertSent(['JOIN #foo'])
