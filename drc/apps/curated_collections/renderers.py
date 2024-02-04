from drc.apps.core.renderers import SrcJSONRenderer


class CuratedCollectionJSONRenderer(SrcJSONRenderer):
    object_label = 'curated_collection'
    object_label_plural = 'curated_collections'


class CollectionRecipeJSONRenderer(SrcJSONRenderer):
    object_label = 'collection_recipe'
    object_label_plural = 'collection_recipes'
