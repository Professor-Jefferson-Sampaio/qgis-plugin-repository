import os
import requests

from qgis.PyQt.QtWidgets import QAction, QMessageBox
from qgis.PyQt.QtGui import QIcon

from qgis.core import (
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsField,
    QgsProject
)

from PyQt5.QtCore import QVariant


class ApiPointsPlugin:

    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.url = "https://food-map.top/api/pontos.php"

    def initGui(self):
        
        plugin_dir = os.path.dirname(__file__)
        icon_path = os.path.join(plugin_dir, "icon.png")

        self.action = QAction(
        QIcon(icon_path),
            "Pontos Food Map",
            self.iface.mainWindow()
        )

        self.action.triggered.connect(self.load_points)

        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("API Points", self.action)

    def unload(self):

        self.iface.removePluginMenu("API Points", self.action)
        self.iface.removeToolBarIcon(self.action)

    def load_points(self):

        try:

            response = requests.get(self.url)

            data = response.json()

            layer = QgsVectorLayer(
                "Point?crs=EPSG:4326",
                "Pontos Food Map",
                "memory"
            )

            provider = layer.dataProvider()

            provider.addAttributes([
                QgsField("id", QVariant.Int),
                QgsField("nome", QVariant.String),
                QgsField("slogan", QVariant.String),
                QgsField("link", QVariant.String),
                QgsField("zap", QVariant.String)
            ])

            layer.updateFields()

            features = []

            for p in data["pontos"]:

                feat = QgsFeature()

                point = QgsPointXY(
                    float(p["lon"]),
                    float(p["lat"])
                )

                feat.setGeometry(
                    QgsGeometry.fromPointXY(point)
                )

                feat.setAttributes([
                    p["id"],
                    p["nome"],
                      p["slogan"],
                        p["link"],
                          p["zap"]
                       
                ])

                features.append(feat)

            provider.addFeatures(features)

            layer.updateExtents()

            QgsProject.instance().addMapLayer(layer)
            
            QMessageBox.information(
                self.iface.mainWindow(),
                "Sucesso",
                "Pontos carregados do Food Map"
            )

        except Exception as e:

            QMessageBox.critical(
                self.iface.mainWindow(),
                "Erro",
                str(e)
            )