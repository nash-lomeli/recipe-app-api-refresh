from drc.apps.core.renderers import SrcJSONRenderer


class RecipeJSONRenderer(SrcJSONRenderer):
    object_label = 'recipe'
    object_label_plural = 'recipes'


class RecipeImageJSONRenderer(SrcJSONRenderer):
    object_label = 'recipe_image'


class InstructionJSONRenderer(SrcJSONRenderer):
    object_label = 'instruction'
    object_label_plural = 'instructions'


# class InstructionImageJSONRenderer(SrcJSONRenderer):
#     object_label = 'instruction_image'


class ItemJSONRenderer(SrcJSONRenderer):
    object_label = 'item'
    object_label_plural = 'items'


class IngredientJSONRenderer(SrcJSONRenderer):
    object_label = 'ingredient'
    object_label_plural = 'ingredients'


class InstructionIngredientJSONRenderer(SrcJSONRenderer):
    object_label = 'instruction_ingredient'
    object_label_plural = 'instruction_ingredients'
