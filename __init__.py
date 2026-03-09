def classFactory(iface):
    from .api_points_plugin import ApiPointsPlugin
    return ApiPointsPlugin(iface)