from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.viewlet.viewlet import ViewletBase
from opencore.browser.base import BaseView
from opencore.tagging.interfaces import ITaggable
from opencore.tagging.interfaces import ITagValidator

class TagViewlet(ViewletBase):

    title = "Tags"
    sort_order = 0
    render = ZopeTwoPageTemplateFile('tag-list.pt')
    
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

    @property
    def tags_to_add(self):
        return self.request.form.get('tag.add', '')

    @property
    def tags_to_remove(self):
        return self.request.form.get('tag.remove', '')

    def validate(self):
        validator = getUtility(ITagValidator)
        errors = {}
        for tag in self.tags_to_add:
            is_valid = validator.can_add(tag)
            if not is_valid:
                errors['tag.add'] = "Invalid tag"
        for tag in self.tags_to_remove:
            if not self.taggable.has_tag(tag):
                errors['tag.remove'] = "Invalid tag"
        return errors

    def render(self):
        pass
    
    def save(self):
        add = self.request.form.get('tag.add', '')
        remove = self.request.form.get('tag.remove', '')

        add = add.split(',')
        for tag in add:
            self.taggable.append(tag)

        remove = remove.split(',')
        for tag in remove:
            self.taggable.remove(tag)

class TagQueryView(BaseView):

    def results(self):
        query = self.request.form.get('tag')
        cat = ITagQuery(self.portal)
        return cat.findall(query)
        
