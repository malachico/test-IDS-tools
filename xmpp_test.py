import xmpp

jid = xmpp.JID("actual.user@gmail.com")
connection = xmpp.Client(jid.getDomain())
connection.connect()
