from drc.apps.core.renderers import SrcJSONRenderer


class NoteRecipeJSONRenderer(SrcJSONRenderer):
    object_label = 'note'
    object_label_plural = 'notes'
