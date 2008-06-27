from zope.interface import Interface

class ITaggable(Interface):
    """
    a taggable object. should be IList.
    """

    def tags():
        """ """

    def has_tag(tag):
        """ """

    def append(tag):
        """ """

    def remove(tag):
        """ """

class ITagQuery(Interface):
    """
    search tags->objects
    """

    def findall(tag):
        """ return all ITaggables which have ``tag`` """

class ITagValidator(Interface):
    """
    validate tags
    """

    def can_add(tag):
        """ """
