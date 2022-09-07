import pya

# Enter your Python code here ..

layout = pya.Layout()

top = layout.create_cell("TOP")
l1 = layout.layer(1, 0)
top.shapes(l1).insert(pya.Box(0, 0, 10, 2000))

layout.write("/Users/anders/Downloads/Single_LED.GDS")

print('hello Anders')
