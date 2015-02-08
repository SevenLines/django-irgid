# coding=utf-8
from cms.menu_bases import CMSAttachMenu
from django.core.urlresolvers import reverse
from menus.base import Modifier, NavigationNode, Menu
from menus.menu_pool import menu_pool

# class MyMode(Modifier):
"""

"""

class MyMode(Modifier):
    """

    """
    def modify(self, request, nodes, namespace, root_id, post_cut, breadcrumb):
        if post_cut:
            return nodes
        count = 0
        for node in nodes:
            node.counter = count
            count += 1
        return nodes

menu_pool.register_modifier(MyMode)

# menu_pool.register_modifier(MyMode)