from PIL import Image, ImageSequence

im = Image.open("pic/rick-rick-and-morty.gif")

index = 1
for frame in ImageSequence.Iterator(im):
    print(frame)
    
    #frame.save("frame%d.png" % index)
    index += 1
