from fontTools.ttLib import TTFont
from fontTools.feaLib.builder import addOpenTypeFeatures



def main():
    font = TTFont("fonts/MicrosoftYaHei.ttf")
    addOpenTypeFeatures(font, "test.fea")
    font.save("fonts/yahei-mod.ttf")


if __name__ == "__main__":
    main()
