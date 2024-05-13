from templating import HTML2Image

im = HTML2Image()
l = im.make_qa_screenshot("In the quiet of my studio, surrounded by a palette of vibrant colors and an array of artistic tools, I find myself immersed in a world of boundless creativity. With each brushstroke and stroke of the pen, I give life to my imagination, transforming blank canvases into vibrant tapestries of color and form. In this sacred space, I am free to explore, to experiment, and to express myself without limits.")
print(l)
