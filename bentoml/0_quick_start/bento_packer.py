from train import clf
from bento_service import IrisClassifier

iris_classifier_service = IrisClassifier()

iris_classifier_service.pack('model', clf)

saved_path = iris_classifier_service.save()
