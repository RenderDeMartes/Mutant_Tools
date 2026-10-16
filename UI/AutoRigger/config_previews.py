'''
Repo curve shapes and controller colors for the block config enums.

- repo_curve_names / repo_color_names: everything the repo accepts (config/curves.json
  and Tools.assign_color), so the ctrl type / color enums are not limited to the
  options of an old block json.
- curve_pixmap / color_pixmap: small previews for the AutoRigger attrs panel, the
  curves are drawn from their curves.json points (no Maya nodes created).
'''
try:
	from PySide6 import QtGui, QtCore
except ImportError:
	from PySide2 import QtGui, QtCore

import json
import math
import os
import re

FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CURVES_FILE = os.path.join(FOLDER, 'config', 'curves.json')

# same names and indices as Tools.assign_color
REPO_COLORS = [('yellow', 17), ('lightBlue', 18), ('blue', 6), ('white', 16), ('purple', 9),
			   ('green', 14), ('red', 13), ('pink', 20), ('grey', 1), ('orange', 21)]
# names used by blocks with their own color tables (only for the swatch)
EXTRA_COLOR_RGB = {
	'light_blue': (0.35, 0.75, 1.0), 'gray': (0.5, 0.5, 0.5), 'cyan': (0.0, 0.9, 0.9),
	'brown': (0.55, 0.33, 0.15),
}
# shapes built by the blocks without curves.json
EXTRA_CURVES = ['bounding_cube']

_curve_data = None
_pixmap_cache = {}


#-------------------------------------------------------------------
def _curves():
	global _curve_data
	if _curve_data is None:
		try:
			with open(CURVES_FILE) as f:
				_curve_data = json.load(f)
		except Exception:
			_curve_data = {}
	return _curve_data


def repo_curve_names():
	return list(_curves().keys()) + EXTRA_CURVES


def repo_color_names():
	return [name for name, _ in REPO_COLORS]


def is_curve_enum(attr, options):
	if not re.search(r'(Type|Shape)$', attr):
		return False
	known = set(repo_curve_names())
	return sum(1 for o in options if o in known) * 2 >= len(options)


def is_color_enum(attr, options):
	return 'Color' in attr


def can_extend_colors(options):
	"""Only enums that already use the repo color names (blocks with their own color table are left alone)."""
	known = set(repo_color_names())
	return all(o in known for o in options)


def extended_options(attr, options):
	"""Json options first (keeps the indices), then the rest of the repo options."""
	if is_curve_enum(attr, options):
		extra = repo_curve_names()
	elif is_color_enum(attr, options) and can_extend_colors(options):
		extra = repo_color_names()
	else:
		return list(options)
	return list(options) + [o for o in extra if o not in options]


#-------------------------------------------------------------------
def _color_rgb(name):
	for color_name, index in REPO_COLORS:
		if color_name == name:
			try:
				import maya.cmds as cmds
				return cmds.colorIndex(index, q=True)
			except Exception:
				break
	return EXTRA_COLOR_RGB.get(name)


def color_pixmap(name, size=18):
	key = ('color', name, size)
	if key in _pixmap_cache:
		return _pixmap_cache[key]
	rgb = _color_rgb(name)
	pixmap = QtGui.QPixmap(size, size)
	pixmap.fill(QtCore.Qt.transparent)
	painter = QtGui.QPainter(pixmap)
	painter.setRenderHint(QtGui.QPainter.Antialiasing)
	if rgb:
		painter.setBrush(QtGui.QColor.fromRgbF(*[min(max(c, 0.0), 1.0) for c in rgb]))
		painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 120), 1))
	else:
		painter.setBrush(QtCore.Qt.NoBrush)
		painter.setPen(QtGui.QPen(QtGui.QColor(150, 150, 150), 1, QtCore.Qt.DashLine))
	painter.drawRoundedRect(QtCore.QRectF(1.5, 1.5, size - 3, size - 3), 4, 4)
	painter.end()
	_pixmap_cache[key] = pixmap
	return pixmap


#-------------------------------------------------------------------
def _circle(normal, segments=32):
	points = []
	for i in range(segments + 1):
		a = 2 * math.pi * i / segments
		c, s = math.cos(a), math.sin(a)
		if normal == 'x':
			points.append((0, c, s))
		elif normal == 'y':
			points.append((c, 0, s))
		else:
			points.append((c, s, 0))
	return points


def _cube():
	v = [(-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)]
	order = [0, 1, 2, 3, 0, 4, 5, 6, 7, 4, 5, 1, 2, 6, 7, 3]
	return [[v[i] for i in order]]


def _curve_strokes(name):
	"""List of point lists for a curve shape name."""
	if name == 'bounding_cube':
		return _cube()
	cmd = _curves().get(name)
	if not cmd:
		return []
	if isinstance(cmd, (list, tuple)):
		cmd = ' '.join(cmd)
	if cmd.strip().startswith('spaceLocator'):
		return [[(-1, 0, 0), (1, 0, 0)], [(0, -1, 0), (0, 1, 0)], [(0, 0, -1), (0, 0, 1)]]
	if cmd.strip().startswith('circle'):
		match = re.search(r'-nr\s+(\S+)\s+(\S+)\s+(\S+)', cmd)
		normal = 'y'
		if match:
			nr = [abs(float(v)) for v in match.groups()]
			normal = 'xyz'[nr.index(max(nr))]
		return [_circle(normal)]
	strokes = []
	for part in re.split(r'\bcurve\b', cmd):
		points = re.findall(r'-p\s+(\S+)\s+(\S+)\s+(\S+)', part)
		if points:
			strokes.append([tuple(float(v) for v in p) for p in points])
	return strokes


def _flat_axis(points):
	"""Index of the axis a flat shape lies on (0 x, 1 y, 2 z), None for 3d shapes."""
	if not points:
		return None
	spans = [max(p[i] for p in points) - min(p[i] for p in points) for i in range(3)]
	biggest = max(spans) or 1.0
	flat = [i for i in range(3) if spans[i] < biggest * 0.08]
	return flat[0] if len(flat) == 1 else None


def _project(point, flat_axis=None):
	x, y, z = point
	# flat shapes straight on, 3d shapes from a front / top / side angle
	if flat_axis == 1:
		return x, z
	if flat_axis == 0:
		return z, -y
	if flat_axis == 2:
		return x, -y
	ry, rx = math.radians(35), math.radians(25)
	x, z = x * math.cos(ry) - z * math.sin(ry), x * math.sin(ry) + z * math.cos(ry)
	y, z = y * math.cos(rx) - z * math.sin(rx), y * math.sin(rx) + z * math.cos(rx)
	return x, -y


def curve_pixmap(name, size=36, color=None):
	key = ('curve', name, size, color)
	if key in _pixmap_cache:
		return _pixmap_cache[key]
	pixmap = QtGui.QPixmap(size, size)
	pixmap.fill(QtCore.Qt.transparent)
	raw = _curve_strokes(name)
	# circleX / Y / Z keep the angled view so their orientation shows
	is_circle = str(_curves().get(name, '')).strip().startswith('circle')
	flat_axis = None if is_circle else _flat_axis([p for stroke in raw for p in stroke])
	strokes = [[_project(p, flat_axis) for p in stroke] for stroke in raw]
	points = [p for stroke in strokes for p in stroke]
	painter = QtGui.QPainter(pixmap)
	painter.setRenderHint(QtGui.QPainter.Antialiasing)
	if points:
		min_x = min(p[0] for p in points)
		max_x = max(p[0] for p in points)
		min_y = min(p[1] for p in points)
		max_y = max(p[1] for p in points)
		span = max(max_x - min_x, max_y - min_y, 1e-6)
		margin = 3.0
		scale = (size - 2 * margin) / span
		off_x = margin + (size - 2 * margin - (max_x - min_x) * scale) / 2.0
		off_y = margin + (size - 2 * margin - (max_y - min_y) * scale) / 2.0
		painter.setPen(QtGui.QPen(QtGui.QColor(color or '#9CC7FF'), 1.3))
		for stroke in strokes:
			path = QtGui.QPainterPath()
			for i, (px, py) in enumerate(stroke):
				pt = QtCore.QPointF(off_x + (px - min_x) * scale, off_y + (py - min_y) * scale)
				if i == 0:
					path.moveTo(pt)
				else:
					path.lineTo(pt)
			painter.drawPath(path)
	else:
		painter.setPen(QtGui.QColor(140, 140, 140))
		painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter, '?')
	painter.end()
	_pixmap_cache[key] = pixmap
	return pixmap
