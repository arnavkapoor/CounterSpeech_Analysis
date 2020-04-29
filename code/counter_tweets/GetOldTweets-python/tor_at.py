import socket
import socks
import urllib2

ipcheck_url = 'http://checkip.amazonaws.com/'

# Actual IP.
print(urllib2.urlopen(ipcheck_url).read())

# Tor IP.
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050)
socket.socket = socks.socksocket
print(urllib2.urlopen(ipcheck_url).read())