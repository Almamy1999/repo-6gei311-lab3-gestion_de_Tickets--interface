from abc import ABC, abstractmethod
import os


class Attachment(ABC):
    
    def __init__(self, path):
        if path.strip() == "":
            raise ValueError("Le chemin du fichier est vide.")
        if not os.path.isfile(path):
            raise FileNotFoundError("Fichier introuvable : " + path)
        self.path = path

    def getName(self):
        
        return os.path.basename(self.path)

    @abstractmethod
    def load(self):
        
        pass


class TextAttachment(Attachment):
    def load(self):
        
        fichier = open(self.path, "r", encoding="utf-8")
        contenu = fichier.read()
        fichier.close()
        return contenu

    def __str__(self):
        return "[Texte] " + self.getName()


class ImageAttachment(Attachment):
    def load(self):
        
        return self.path 

    def __str__(self):
        return "[Image] " + self.getName()


class VideoAttachment(Attachment):
    def load(self):
        
        return self.path

    def __str__(self):
        return "[Vidéo] " + self.getName()


class AttachmentFactory:
    

    EXTENSIONS_TEXTE = [".txt", ".md", ".csv", ".log"]
    EXTENSIONS_IMAGE = [".png", ".jpg", ".jpeg", ".gif", ".bmp"]
    EXTENSIONS_VIDEO = [".mp4", ".avi", ".mov", ".mkv"]

    def create(self, path):
        
        nom, extension = os.path.splitext(path)
        extension = extension.lower()

        if extension in self.EXTENSIONS_TEXTE:
            return TextAttachment(path)
        elif extension in self.EXTENSIONS_IMAGE:
            return ImageAttachment(path)
        elif extension in self.EXTENSIONS_VIDEO:
            return VideoAttachment(path)
        else:
            raise ValueError("Type de fichier non accepté : " + extension)