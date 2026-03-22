from fontTools.ttLib import TTFont
from fontTools.feaLib.builder import addOpenTypeFeatures

font = TTFont("MicrosoftYaHei.ttf")
addOpenTypeFeatures(font, "test.fea")
font.save("yahei-mod.ttf")