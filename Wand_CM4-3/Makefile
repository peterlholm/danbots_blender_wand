#
# makefile for genrating picture
#

single:
	blender -o output -b  wand.blend -f 1

run:
	blender -o output wand.blend

render:
	blender -b wand.blend --python-text Run -- objects
	