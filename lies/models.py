from django.db import models
from django.contrib.auth.models import User
from django.db.models import permalink

class Lie(models.Model):
    """
    Class to handle the main lie message
    >>> a = Lie(lie="Testing is for sissies")
    >>> a.created == a.modified
    True
    >>> a.lie
    'Testing is for sissies'
    >>> a.lie = 'Testing is for bad programmers'
    >>> a.save()
    >>> a.created == a.modified
    False
    """
    lie = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return ('lie_detail',  [str(self.id)])
    get_absolute_url = permalink(get_absolute_url)

    def vote_total(self):
        """
        Calculate the total votes on this Lie
        >>> a = Lie(lie="This function doesn't work")
        >>> a.save()
        >>> Vote(lie=a,value=1).save()
        >>> Vote(lie=a,value=1).save()
        >>> Vote(lie=a,value=-1).save()
        >>> a.vote_total()
        1
        """
        return reduce(lambda init, item: init + item.value, self.votes.all(), 0)

class Vote(models.Model):
    """
    Class to handle up and down votes on a Lie
    >>> a = Lie(lie="Votes are stupid")
    >>> a.save()
    >>> b = Vote(lie=a,value=1)
    >>> b.save()
    >>> c = Vote(lie=a,value=-1)
    >>> c.save()
    >>> b.value
    1
    >>> c.value
    -1
    >>> b.lie.lie
    'Votes are stupid'
    >>> a.votes.count()
    2
    """
    lie = models.ForeignKey(Lie, related_name='votes')
    value = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def to_str(self):
        "For %s with value %i" % (lie.id, value)

