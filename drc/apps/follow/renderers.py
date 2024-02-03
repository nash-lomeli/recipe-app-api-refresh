from drc.apps.core.renderers import SrcJSONRenderer


class FollowerJSONRenderer(SrcJSONRenderer):
    object_label = 'follow'
    object_label_plural = 'followers'

class FollowingJSONRenderer(SrcJSONRenderer):
    object_label_plural = 'following'