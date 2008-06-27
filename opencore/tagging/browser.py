from opencore.browser.base import BaseView
from opencore.tagging.interfaces import ITaggable
from opencore.tagging.interfaces import ITagValidator

class TagViewlet(object):
    
    def __init__(self, context, request):
        self.context = ITaggable(context)

    def tags(self):
        return self.context.tags()

    def search_link(self, tag):
        # XXX should be generated?
        # XXX could be relative link instead of absolute;
        #     TagQueryView could then search within current context
        return "/@@search-by-tag?tag=%s" % tag 

class TagEditViewlet(object):

    def __init__(self, context, request):
        self.context = ITaggable(context)
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
            if not self.context.has_tag(tag):
                errors['tag.remove'] = "Invalid tag"
        return errors

    def save(self):
        add = self.request.form.get('tag.add', '')
        remove = self.request.form.get('tag.remove', '')

        add = add.split(',')
        for tag in add:
            self.context.append(tag)

        remove = remove.split(',')
        for tag in remove:
            self.context.remove(tag)

class TagQueryView(BaseView):

    def results(self):
        query = self.request.form.get('tag')
        cat = ITagQuery(self.portal)
        return cat.findall(query)
        
