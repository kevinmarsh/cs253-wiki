'''
/opt/google_appengine/dev_appserver.py ~/workspace/Wiki-Udacity253-Final
/opt/google_appengine/appcfg.py update ~/workspace/Wiki-Udacity253-Final
'''

from wiki import Homepage, WikiPage, EditPage, HistoryPage
from login import SignUp, Login, Logout

import webapp2

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([
                               ('/', Homepage),
                               ('/signup', SignUp),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/_edit' + PAGE_RE, EditPage),
                               ('/_history' + PAGE_RE, HistoryPage),
                               (PAGE_RE, WikiPage),
                               ],
                              debug=True)
