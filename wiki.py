import urllib
import jinja2
import os
from jinjahandler import Handler
from google.appengine.ext import db

jinja_environment = jinja2.Environment(autoescape=False,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

class Page(db.Model):
    "GAE db entity for wiki page"
    #subject = db.StringProperty(required = True)
    content = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    #modified = db.DateTimeProperty(auto_now = True)
    url = db.StringProperty(required = True)
    version = db.IntegerProperty(required = True)

class Homepage(Handler):
    "display the homepage, a list of wiki pages"
    def get(self):
        '''
        self.write('This is the homepage, "get"')
        '''
        wikiPages = list(db.GqlQuery('SELECT * '
                                     'FROM Page '
                                     'ORDER BY modified DESC'))
        cookie = self.request.cookies.get('username', '')
        self.render('wiki_home.html', 
                    cookie=cookie[:cookie.find('|')], 
                    wikiPages=wikiPages)

class WikiPage(Handler):
    "creates a new blog post, ensures no duplicate urls"
    def get(self, resource):
        urlSlug = urllib.unquote(resource)
        ver = self.request.get('version')
        cookie = self.request.cookies.get('username', '')

        '''
        self.write(dbPage)
        self.write('<br>')
        self.write(dbPage[0].version)
        
                self.write(page.version)
                self.write('<br>')

        self.write(ver)
        self.write('<br>')
        self.write(urlSlug)
        self.write('<br>')
        '''
        
        dbPage = list(db.GqlQuery('SELECT * FROM Page '
                                  'WHERE url = :1 '
                                  'ORDER BY version DESC', urlSlug)) #use list to only hit the db once
          
        if ver:
            for page in dbPage:
                if int(page.version) == int(ver):
                    temp = page
            dbPage.insert(0, temp)
        if len(dbPage) > 0: #display page from db
            self.render('wiki_page.html', 
                        content=dbPage[0].content, 
                        urlSlug=dbPage[0].url, 
                        edit=True,
                        cookie=cookie[:cookie.find('|')])
        else: #if page doesn't exist, redirect to create it
            if cookie: #if signed in allow them to edit
                self.redirect('/_edit%s' % urlSlug)
            else:
                self.write('You must be <a href="/login?page=%s">signed in</a> to create a page' % urlSlug) 
            
class EditPage(Handler):
    def get(self, resource):
        urlSlug = urllib.unquote(resource)
        cookie = self.request.cookies.get('username', '')
        dbPage = list(db.GqlQuery('SELECT * FROM Page '
                                  'WHERE url = :1 '
                                  'ORDER BY version DESC', urlSlug)) #use list to only hit the db once
        if len(dbPage) > 0 and dbPage[0]:
            self.render('wiki_edit.html', 
                        content=dbPage[0].content,
                        cookie=cookie[:cookie.find('|')])
        else:
            self.render('wiki_edit.html', 
                        content='', 
                        cookie=cookie[:cookie.find('|')])
    def post(self, resource):
        urlSlug = urllib.unquote(resource)
        cookie = self.request.cookies.get('username', '')
        dbPage = list(db.GqlQuery('SELECT * FROM Page '
                                  'WHERE url = :1 '
                                  'ORDER BY version DESC', urlSlug)) #use list to only hit the db once
        content = self.request.get('content')
        
        if content:
            newPage = Page(content = content, url = urlSlug, version = len(dbPage) + 1)
            newPage.put() #commit the blog post to the db
            '''
            dbPage[0].content = content
            dbPage[0].url = urlSlug
            dbPage[0].version = len(dbPage) + 1
            dbPage.put() #commit the blog post to the db
            '''
            self.redirect('%s' % urlSlug)
        else:
            errorContent = ' - Please add some content' if not content else ''
            
            self.render('wiki_edit.html', 
                        #subject=subject,
                        content=content,
                        #errorSubject=errorSubject, 
                        errorContent=errorContent,
                        cookie=cookie[:cookie.find('|')])

class HistoryPage(Handler):
    def get(self, resource):
        urlSlug = urllib.unquote(resource)
        cookie = self.request.cookies.get('username', '')
        dbPage = list(db.GqlQuery('SELECT * FROM Page '
                                  'WHERE url = :1 '
                                  'ORDER BY version DESC', urlSlug)) #use list to only hit the db once
        if len(dbPage) > 0 and dbPage[0]: #display page from db
            self.render('wiki_history.html', 
                        dbPage=dbPage, 
                        cookie=cookie[:cookie.find('|')])
        else: #if page doesn't exist, redirect to create it
            if cookie: #if signed in allow them to edit
                self.redirect('/_edit%s' % urlSlug)
            else:
                self.write('You must be <a href="/login?page=%s">signed in</a> to create a page' % urlSlug) 