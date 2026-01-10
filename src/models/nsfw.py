from transformers import pipeline

nsfw_classifier = pipeline(
    "image-classification",
    model="Falconsai/nsfw_image_detection",
    device=-1
)