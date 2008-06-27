from Products.CMFCore.utils import getToolByName
from opencore.tagging.interfaces import ITaggable
from opencore.tagging.interfaces import ITagQuery
from opencore.tagging.interfaces import ITagValidator
from opencore.utility.interfaces import IProvideSiteConfig
from zope.component import getUtility
from zope.interface import implements

class DCSubjectTaggable(object):
    implements(ITaggable)
    
    def __init__(self, context):
        self.context = context

    def tags(self):
        return self.context.Subject() #??

    def has_tag(self, tag):
        return tag in self.context.Subject() #??

    def append(self, tag):
        self.context.Subject().append(tag) #??

    def remove(self, tag):
        self.context.Subject().remove(tag) #??

class DCSubjectTagQuery(object):
    implements(ITagQuery)    

    def __init__(self, site):
        self.site = site

    def findall(self, tag):
        cat = getToolByName(self.site, 'portal_catalog')
        return cat(Subject=tag) #??

class SitewideTagVocabularyValidator(object):
    implements(ITagValidator)

    def can_add(self, tag):
        config = getUtility(IProvideSiteConfig)
        tags = config.get('taglist').split(',')
        return tag in tags
