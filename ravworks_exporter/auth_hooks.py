from allianceauth import hooks
from allianceauth.services.hooks import UrlHook, MenuItemHook

from . import urls


class RavworksExporterMenuItemHook(MenuItemHook):
    def __init__(self):
        super().__init__("Ravworks Exporter", "fas fa-wrench", "ravworks_exporter:index", navactive=['ravworks_exporter:'])


@hooks.register('menu_item_hook')
def register_menu():
    return RavworksExporterMenuItemHook()


@hooks.register('url_hook')
def register_urls():
    return UrlHook(urls, 'ravworks_exporter', 'ravworks_exporter/')
