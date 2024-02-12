from django.db import models
from django.utils.translation import gettext_lazy as _
from django_scopes import ScopedManager

from eventyay.common.mixins.models import PretalxModel
from eventyay.common.phrases import phrases


class Feedback(PretalxModel):
    """The Feedback model allows for anonymous feedback by attendees to one or
    all speakers of a.

    :class:`~eventyay.submission.models.submission.Submission`.

    :param speaker: If the ``speaker`` attribute is not set, the feedback is
        assumed to be directed to all speakers.
    """

    talk = models.ForeignKey(
        to="submission.Submission",
        related_name="feedback",
        on_delete=models.PROTECT,
        verbose_name=_("Session"),
    )
    speaker = models.ForeignKey(
        to="person.User",
        related_name="feedback",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name=_("Speaker"),
    )
    rating = models.IntegerField(null=True, blank=True, verbose_name=_("Rating"))
    review = models.TextField(
        verbose_name=_("Feedback"), help_text=phrases.base.use_markdown
    )

    objects = ScopedManager(event="talk__event")

    def __str__(self):
        """Help when debugging."""
        return f"Feedback(event={self.talk.event.slug}, talk={self.talk.title}, rating={self.rating})"
