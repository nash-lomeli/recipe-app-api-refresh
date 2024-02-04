from drc.apps.core.renderers import SrcJSONRenderer

class CompletedInstructionJSONRenderer(SrcJSONRenderer):
    object_label = 'completed_instruction'
    object_label_plural = 'completed_instructions'