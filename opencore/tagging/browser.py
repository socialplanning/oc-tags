from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from opencore.browser.base import BaseView
from opencore.framework.editform import EditFormViewlet
from opencore.tagging.interfaces import ITaggable
from opencore.tagging.interfaces import ITagValidator
from opencore.tagging.interfaces import ITagQuery
from zope.component import getUtility

class TagViewlet(object):

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

class TagEditViewlet(EditFormViewlet):

    title = "Tags"
    sort_order = 1

    def taggable(self, context):
        """
        adapts the context to ITaggable, for use in templates

        i'd prefer to use a tales namespace, i think:
          context/adapters:ITaggable
          context/adapters:IGeoreferenced
        might be interesting?
        """
        return ITaggable(context)

    def tags(self):
        validator = getUtility(ITagValidator)
        return validator.tags()

    def selected_tags(self, request):
        tags = request.form.get('tag',[])
        if isinstance(tags, basestring):
	    tags=[tags]
        return tags
        
    def validate(self, context, request):
        validator = getUtility(ITagValidator)
        errors = {}
        for tag in self.selected_tags(request):
            is_valid = validator.can_add(tag)
            if not is_valid:
                errors['tag'] = "Invalid tag"
        return errors

    def save(self, context, request):
        ITaggable(context).update(self.selected_tags(request))

class TagQueryView(BaseView):

    def results(self):
        query = self.request.form.get('tag')
        cat = ITagQuery(self.portal)
        return cat.findall(query)

