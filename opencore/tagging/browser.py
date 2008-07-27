from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.viewlet.viewlet import ViewletBase
from opencore.browser.base import BaseView
from opencore.tagging.interfaces import ITaggable
from opencore.tagging.interfaces import ITagValidator
from opencore.tagging.interfaces import ITagQuery
from zope.component import getUtility

class TagViewlet(ViewletBase):

    title = "Taglist"
    sort_order = 0
    
    def __init__(self, context, request, view, manager):
        self.taggable = ITaggable(context)
        self.context = context
        
    def tags(self):
        return self.taggable.tags()

    def search_link(self, tag):
        # XXX should be generated?
        # XXX could be relative link instead of absolute;
        #     TagQueryView could then search within current context
        return "/@@search-by-tag?tag=%s" % tag 

class TagEditViewlet(ViewletBase):

    title = "Tags"
    sort_order = 1
    render = ZopeTwoPageTemplateFile('tag-edit.pt')

    def __init__(self, context, request, view, manager):
        self.context = context
        self.taggable = ITaggable(context)
        self.request = request

    def tags(self):
        validator = getUtility(ITagValidator)
        return validator.tags()

    def selected_tags(self):
        tags = self.request.form.get('tag',[])
        if isinstance(tags, basestring):
	    tags=[tags]
        return tags
        
    def validate(self):
        validator = getUtility(ITagValidator)
        errors = {}
        for tag in self.selected_tags():
            is_valid = validator.can_add(tag)
            if not is_valid:
                errors['tag'] = "Invalid tag"
        return errors

    def save(self):
        self.taggable.update(self.selected_tags())

class TagQueryView(BaseView):

    def results(self):
        query = self.request.form.get('tag')
        cat = ITagQuery(self.portal)
        return cat.findall(query)
        
