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

    def list():
        """ return a list of all unique tags with which content is presently tagged """
        
    def findall(tag):
        """ return all ITaggables which have ``tag`` """

class ITagValidator(Interface):
    """
    validate tags
    """

    def can_add(tag):
        """ """
