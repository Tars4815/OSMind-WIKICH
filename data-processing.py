"""
Model exported as python.
Name : modello
Group : 
With QGIS : 33408
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterMapLayer
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Modello(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterMapLayer('indoor_lines', 'Indoor lines', defaultValue=None, types=[QgsProcessing.TypeVectorLine]))
        self.addParameter(QgsProcessingParameterMapLayer('indoor_points', 'Indoor points', defaultValue=None, types=[QgsProcessing.TypeVectorPoint]))
        self.addParameter(QgsProcessingParameterFeatureSink('Wall_openings', 'wall_openings', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Artworks', 'artworks', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Rooms', 'rooms', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(7, model_feedback)
        results = {}
        outputs = {}

        # Doors extraction
        alg_params = {
            'FIELD': 'door',
            'INPUT': parameters['indoor_points'],
            'OPERATOR': 9,  # is not null
            'VALUE': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DoorsExtraction'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Doors projection
        alg_params = {
            'CONVERT_CURVED_GEOMETRIES': False,
            'INPUT': outputs['DoorsExtraction']['OUTPUT'],
            'OPERATION': '',
            'TARGET_CRS': 'ProjectCrs',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DoorsProjection'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Door openings
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 0.5,
            'END_CAP_STYLE': 0,  # Arrotondato
            'INPUT': outputs['DoorsProjection']['OUTPUT'],
            'JOIN_STYLE': 0,  # Arrotondato
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DoorOpenings'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Riproietta layer
        alg_params = {
            'CONVERT_CURVED_GEOMETRIES': False,
            'INPUT': parameters['indoor_lines'],
            'OPERATION': '',
            'TARGET_CRS': 'ProjectCrs',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RiproiettaLayer'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Artworks Extraction
        alg_params = {
            'FIELD': 'exhibit',
            'INPUT': parameters['indoor_points'],
            'OPERATOR': 9,  # is not null
            'VALUE': '',
            'OUTPUT': parameters['Artworks']
        }
        outputs['ArtworksExtraction'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Artworks'] = outputs['ArtworksExtraction']['OUTPUT']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Walls to rooms
        alg_params = {
            'INPUT': outputs['RiproiettaLayer']['OUTPUT'],
            'OUTPUT': parameters['Rooms']
        }
        outputs['WallsToRooms'] = processing.run('qgis:linestopolygons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Rooms'] = outputs['WallsToRooms']['OUTPUT']

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Wall openings
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': outputs['RiproiettaLayer']['OUTPUT'],
            'OVERLAY': outputs['DoorOpenings']['OUTPUT'],
            'OUTPUT': parameters['Wall_openings']
        }
        outputs['WallOpenings'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Wall_openings'] = outputs['WallOpenings']['OUTPUT']
        return results

    def name(self):
        return 'modello'

    def displayName(self):
        return 'modello'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Modello()
