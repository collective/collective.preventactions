# -*- coding: utf-8 -*-
from collective.preventactions import _
from z3c.form import form, button, field
from zope import schema
from zope.interface import Interface
from zope.interface import alsoProvides
from zope.interface import noLongerProvides
from collective.preventactions.interfaces import IPreventDelete, IPreventRename
import logging
logger = logging.getLogger('collective.preventeactions')

class IPreventActions(Interface):
    """ Define form fields """

    delete = schema.Bool(
        title=_(u"This object can not be deleted"),
        description=_(u"If check, this object can not be deleted."),
        default=False,
    )

    rename = schema.Bool(
        title=_(u"This object can not be renamed (id)"),
        description=_(u"If check, this object can not be renamed."),
        default=False,
    )


class PreventActionsForm(form.Form):
    fields = field.Fields(IPreventActions)
    label = _(u"Pevent actions")
    description = _(u"What actions will you prevent ?")

    def update(self):
        super(PreventActionsForm, self).update()
        for widget in self.widgets.values():
            if IPreventDelete.providedBy(self.context):
                widget.value = [u'selected']
                import ipdb; ipdb.set_trace()
                logger.info("delete true")
            else:
                widget.value = []
                logger.info("delete false")
            if IPreventRename.providedBy(self.context):
                widget.value = [u'selected']
            else:
                widget.value = []

    @button.buttonAndHandler(_(u'Save'))
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        if data['delete']:
            alsoProvides(self.context, IPreventDelete)
        else:
            noLongerProvides(self.context, IPreventDelete)
        if data['rename']:
            alsoProvides(self.context, IPreventRename)
        else:
            noLongerProvides(self.context, IPreventRename)

        self.status = _(u"Changes saved")

    @button.buttonAndHandler(u"Cancel")
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """


def prevent(context, interface):
    if interface.providedBy(context):
        return True
    return False
