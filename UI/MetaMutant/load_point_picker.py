"""Meta Mutant's Pick Points window: everything you select on your head, before exporting.

Two panels side by side: the MetaHuman on the left, already marked (points, lines, regions), and your
head on the right, where you click. Both look through one camera, so tumbling either moves both.
The tabs go through what to pick, in order:

    Points          one vertex each, click and the next one is asked for
    Lines           the loop around the mouth and around each eye opening (or each line, corner to corner)
    Regions         optional: faces of the lips, eyelids, mouth bag and eye sockets, to correct what the lines say
    Eyes & teeth    your eyes and teeth: meshes or faces

The work on the scene is in Utils/MetaMutant/mm_picker.py, what gets stored in mm_points.py. Each pick is
saved at once (<work>/points.json, meta_mutant.json), so closing halfway keeps what you did.

    from Mutant_Tools.UI.MetaMutant import load_point_picker
    load_point_picker.open_window(workflow, on_close=print)
"""
from __future__ import absolute_import

import os
import sys
import traceback

import maya.cmds as cmds
import maya.OpenMayaUI as omui

try:
    from importlib import reload
except ImportError:  # Python 2
    pass

try:
    from PySide6 import QtCore, QtWidgets
    import shiboken6 as shiboken
except ImportError:  # Maya 2024 and older
    from PySide2 import QtCore, QtWidgets
    import shiboken2 as shiboken

from Mutant_Tools.UI import QtMutantWindow

FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PIPELINE = os.path.join(FOLDER, 'Utils', 'MetaMutant')
if PIPELINE not in sys.path:
    sys.path.insert(0, PIPELINE)

import mm_workflow as wf  # noqa: E402
import mm_points as mp  # noqa: E402
import mm_regions  # noqa: E402
import mm_picker  # noqa: E402
for _module in (mp, mm_regions, mm_picker):
    reload(_module)

TITLE = 'Meta Mutant: Pick Points'
_window = globals().get('_window')  # kept across reload, so the open window can still be closed

STYLE = '''
#PickPoints QLabel { color: #bbbbbb; }
#PickPoints QLabel#Asked { color: #e8e8e8; font-size: 14px; font-weight: bold; }
#PickPoints QLabel#Hint { color: #9da1a4; }
#PickPoints QLabel#Hint[tone="failed"] { color: #e5847f; }
#PickPoints QLabel#Panel { color: #c8c8c8; font-weight: bold; padding: 2px 4px; }
#PickPoints QFrame#Side { background: #2f3133; border: none; border-radius: 8px; }
#PickPoints QListWidget { background: #2b2d2f; color: #c8c8c8; border: 1px solid #45494a; border-radius: 5px; }
#PickPoints QListWidget::item { padding: 3px 4px; }
#PickPoints QListWidget::item:selected { background: #4b6eaf; color: #ffffff; }
#PickPoints QTabWidget::pane { border: none; }
#PickPoints QTabBar::tab { background: transparent; color: #9da1a4; padding: 5px 8px; }
#PickPoints QTabBar::tab:selected { color: #ffffff; border-bottom: 2px solid #4b6eaf; }
#PickPoints QPushButton#Primary {
    background: #4b6eaf; color: #ffffff; border: none; border-radius: 5px; padding: 7px 16px; font-weight: bold; }
#PickPoints QPushButton#Primary:hover { background: #5a7fc4; }
#PickPoints QPushButton#Ghost {
    background: transparent; color: #c8c8c8; border: 1px solid #5c5f61; border-radius: 5px; padding: 4px 10px; }
#PickPoints QPushButton#Ghost:hover { border-color: #7d8184; color: #ffffff; }
#PickPoints QPushButton#Ghost:disabled { color: #6c7073; border-color: #45494a; }
#PickPoints QCheckBox { color: #bbbbbb; }
'''

POINTS, LINES, REGIONS, PARTS = range(4)
TAB_NAMES = ('Points', 'Lines', 'Regions', 'Eyes && teeth')
PARTS_ROWS = (('eyes', 'Eyes'), ('teeth', 'Teeth'))
PARTS_HINT = ('Select your {} in the right panel: whole meshes, or switch to faces (right-click the head). '
              'The other meshes of your scene show here.')


def open_window(workflow, on_close=None):
    """The window for this workflow's head, closing one already open."""
    global _window
    try:
        _window.close()
        _window.deleteLater()
    except Exception:
        pass
    _window = PointPicker(workflow, on_close)
    _window.show()
    return _window


def _named(widget, name):
    widget.setObjectName(name)
    return widget


class PointPicker(QtMutantWindow.Qt_Mutant):

    def __init__(self, workflow, on_close=None):
        super(PointPicker, self).__init__()
        self.workflow, self.on_close = workflow, on_close
        self.setWindowTitle(TITLE)
        self.set_title(TITLE)
        self.resize(1500, 860)
        self.closed = False
        self.jobs = []
        self.panels = {}
        self.maya_window = None
        self.busy = False  # our own selection changes do not count as picks
        self.previous_mode = self.selection_mode()
        s = workflow.s
        self.paths = wf.paths(s.work_dir)
        self.head = s.custom_mesh
        self.points = mp.load(self.paths.points)
        count = cmds.polyEvaluate(self.head, vertex=True)
        problem = mp.stale(self.points, self.head, count)
        if problem:
            workflow.log('{}: starting over'.format(problem))
            self.points = mp.empty()
        self.points.update(mesh=self.head, vertex_count=count)

        mm_dna, _ = workflow.modules()
        self.reader = mm_dna.load_dna(s.dna_path)
        self.scene = mm_picker.PickScene(self.reader, self.head)
        self.scene.sphere_size = float(self.points.get('sphere_size') or mp.DEFAULT_SPHERE_SIZE)
        self.scene.build()

        body = _named(QtWidgets.QWidget(), 'PickPoints')
        body.setStyleSheet(STYLE)
        row = QtWidgets.QHBoxLayout(body)
        row.setContentsMargins(6, 6, 6, 6)
        row.setSpacing(8)
        self.views = QtWidgets.QVBoxLayout()
        row.addLayout(self.views, 1)
        row.addWidget(self.side())
        self.master_ui.mutant_Layout.addWidget(body)

        try:
            self.build_panels()
            self.mark_source()
            self.show_saved()
            self.tabs.setCurrentIndex(POINTS)
            self.tab_changed(POINTS)
            self.select_first_missing()
        except Exception:  # nothing of a window that could not open stays in the scene
            self.closed = True
            self.remove_from_scene()
            raise
        self.jobs.append(cmds.scriptJob(event=['SelectionChanged', self.selection_changed], protected=True))
        for event in ('SceneOpened', 'NewSceneOpened'):
            self.jobs.append(cmds.scriptJob(event=[event, self.close], protected=True))

    # ------------------------------------------------------------------ the two views

    def build_panels(self):
        titles = QtWidgets.QHBoxLayout()
        for text in ('MetaHuman: already marked', 'Your head: pick here'):
            label = _named(QtWidgets.QLabel(text), 'Panel')
            label.setAlignment(QtCore.Qt.AlignCenter)
            titles.addWidget(label, 1)
        self.views.addLayout(titles)
        # Maya's panels need Maya's own parent: they are built in a window that never shows, then moved in here
        name = 'MetaMutantPickPointsPanels'
        if cmds.window(name, exists=True):
            cmds.deleteUI(name, window=True)
        self.maya_window = cmds.window(name)
        pane = cmds.paneLayout(configuration='vertical2', separatorThickness=2, paneSize=[(1, 50, 100), (2, 50, 100)])
        for key in ('source', 'custom'):
            panel = cmds.modelPanel(label='Meta Mutant ' + key, menuBarVisible=False, parent=pane, camera=self.scene.camera)
            cmds.modelEditor(panel, edit=True, displayAppearance='smoothShaded', wireframeOnShaded=False, grid=False,
                             headsUpDisplay=False, manipulators=False, cameras=False, lights=False, displayTextures=False,
                             viewSelected=False, joints=False, locators=False)
            cmds.isolateSelect(panel, state=True)
            cmds.frameLayout(cmds.modelPanel(panel, query=True, barLayout=True), edit=True, collapse=True)  # no icon bar
            self.panels[key] = panel
        self.views.addWidget(shiboken.wrapInstance(int(omui.MQtUtil.findLayout(pane)), QtWidgets.QWidget), 1)
        self.isolate('source', self.scene.source_panel_objects())
        self.isolate('custom', self.scene.custom_panel_objects())

    def isolate(self, key, objects):
        panel = self.panels[key]
        was = cmds.undoInfo(q=True, stateWithoutFlush=True)
        cmds.undoInfo(stateWithoutFlush=False)
        try:
            members = cmds.isolateSelect(panel, query=True, viewObjects=True)
            members = cmds.sets(members, query=True) if members and cmds.objExists(members) else []
            for node in members or []:
                cmds.isolateSelect(panel, removeDagObject=node)
            for node in objects:
                if cmds.objExists(node):
                    cmds.isolateSelect(panel, addDagObject=node)
        finally:
            cmds.undoInfo(stateWithoutFlush=was)

    # ------------------------------------------------------------------ the side column

    def side(self):
        box = _named(QtWidgets.QFrame(), 'Side')
        box.setFixedWidth(350)
        column = QtWidgets.QVBoxLayout(box)
        column.setContentsMargins(10, 10, 10, 10)
        column.setSpacing(8)
        self.asked = _named(QtWidgets.QLabel(), 'Asked')
        self.asked.setWordWrap(True)
        self.hint = _named(QtWidgets.QLabel(), 'Hint')
        self.hint.setWordWrap(True)
        self.hint.setMinimumHeight(48)
        self.hint.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        column.addWidget(self.asked)
        column.addWidget(self.hint)

        self.tabs = QtWidgets.QTabWidget()
        self.lists = []
        for name in TAB_NAMES:
            rows = QtWidgets.QListWidget()
            rows.currentRowChanged.connect(lambda *_: self.row_changed())
            self.lists.append(rows)
            self.tabs.addTab(rows, name.replace('&&', '&'))
        for label, _, _ in mp.GUIDES:
            self.lists[POINTS].addItem(label)
        for _, label, _ in mp.LINES:
            self.lists[LINES].addItem(label)
        for _, label in mm_regions.REGIONS:
            self.lists[REGIONS].addItem(label)
        for _, label in PARTS_ROWS:
            self.lists[PARTS].addItem(label)
        self.tabs.currentChanged.connect(self.tab_changed)
        column.addWidget(self.tabs, 1)

        buttons = QtWidgets.QHBoxLayout()
        self.use = _named(QtWidgets.QPushButton('Use selected'), 'Primary')
        self.use.clicked.connect(lambda *_: self.use_selected())
        self.clear_button = _named(QtWidgets.QPushButton('Clear'), 'Ghost')
        self.clear_button.clicked.connect(lambda *_: self.clear_row())
        buttons.addWidget(self.use, 1)
        buttons.addWidget(self.clear_button)
        column.addLayout(buttons)

        self.mirror = QtWidgets.QCheckBox('Mirror L to R')
        self.mirror.setToolTip('Each point you pick on the character\'s left also fills its right one, with the '
                               'vertex nearest the mirrored spot. For symmetric heads.')
        self.mirror.setChecked(bool(self.points.get('mirror')))
        self.mirror.toggled.connect(lambda on: self.points.update(mirror=bool(on)))
        column.addWidget(self.mirror)
        size_row = QtWidgets.QHBoxLayout()
        size_row.addWidget(QtWidgets.QLabel('Sphere size'))
        self.size_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.size_slider.setRange(5, 200)
        self.size_slider.setValue(int(self.scene.sphere_size * 100))
        self.size_slider.valueChanged.connect(lambda v: self.set_size(v / 100.0))
        size_row.addWidget(self.size_slider, 1)
        column.addLayout(size_row)

        self.count = _named(QtWidgets.QLabel(), 'Hint')
        self.count.setWordWrap(True)
        column.addWidget(self.count)
        done = _named(QtWidgets.QPushButton('Done'), 'Primary')
        done.clicked.connect(lambda *_: self.close())
        column.addWidget(done)
        return box

    def row_key(self):
        """What the current row is, as (tab, key): a guide label, a line key, a region key or eyes / teeth."""
        tab = self.tabs.currentIndex()
        row = self.lists[tab].currentRow()
        if row < 0:
            return tab, None
        if tab == POINTS:
            return tab, mp.GUIDES[row][0]
        if tab == LINES:
            return tab, mp.LINES[row][0]
        if tab == REGIONS:
            return tab, mm_regions.REGIONS[row][0]
        return tab, PARTS_ROWS[row][0]

    # ------------------------------------------------------------------ what is shown

    def mark_source(self):
        """The MetaHuman's side, always there: its points, lines and regions."""
        positions = self.scene.source_positions
        for label, vertex, _ in mp.GUIDES:
            self.scene.put_sphere('source', label, positions[vertex], mm_picker.POINT_WAITING)
        for key, chain in mp.METAHUMAN_LINES.items():
            self.scene.put_curve('source', key, positions[chain], mm_picker.POINT_WAITING)
        self.scene.paint_regions(self.scene.source_mesh, self.scene.source_regions)

    def show_saved(self):
        for label, picked in self.points['guides'].items():
            self.scene.put_sphere('custom', label, picked['position'])
        for key, line in self.points['lines'].items():
            self.scene.put_curve('custom', key, line['positions'])
        self.paint_custom()
        self.refresh_rows()

    def paint_custom(self):
        regions = {}
        for key, spec in (self.workflow.s.regions or {}).items():
            regions[key] = self.vertices_of(spec)
        self.scene.paint_regions(mm_picker.CUSTOM, regions)

    def vertices_of(self, spec):
        items = self.scene.to_copy_names(spec)
        items = cmds.polyListComponentConversion([i for i in items if cmds.objExists(i)], toVertex=True) or []
        return [mm_picker.component_vertex(v) for v in cmds.ls(items, flatten=True) or []]

    def refresh_rows(self):
        s = self.workflow.s
        done = [
            [g[0] in self.points['guides'] for g in mp.GUIDES],
            [k in self.points['lines'] for k, _, _ in mp.LINES],
            [bool((s.regions or {}).get(k)) for k, _ in mm_regions.REGIONS],
            [bool(getattr(s, k)) for k, _ in PARTS_ROWS],
        ]
        labels = [[g[0] for g in mp.GUIDES], [l[1] for l in mp.LINES], [r[1] for r in mm_regions.REGIONS], [p[1] for p in PARTS_ROWS]]
        for tab, flags in enumerate(done):
            for row, flag in enumerate(flags):
                self.lists[tab].item(row).setText((u'✓  ' if flag else u'     ') + labels[tab][row])
        for tab, flags in enumerate(done):
            self.tabs.setTabText(tab, '{} {}/{}'.format(TAB_NAMES[tab].replace('&&', '&'), sum(flags), len(flags)))
        self.count.setText(mp.summary(self.points, s.regions, s.eyes, s.teeth))

    def row_changed(self):
        """Light up on the MetaHuman what is being asked for, and say it."""
        tab, key = self.row_key()
        for label in self.scene.spheres['source']:
            self.scene.color_sphere('source', label, mm_picker.POINT_ACTIVE if tab == POINTS and label == key else mm_picker.POINT_WAITING)
        for line in self.scene.curves['source']:
            self.scene.color_curve('source', line, mm_picker.POINT_ACTIVE if tab == LINES and line == key else mm_picker.POINT_WAITING)
        if key is None:
            self.asked.setText('')
            self.say('')
        elif tab == POINTS:
            self.asked.setText(key)
            self.say('Click it on your head: {}.'.format(mp.guide_hint(key)))
        elif tab == LINES:
            label, text = next((l[1], l[2]) for l in mp.LINES if l[0] == key)
            self.asked.setText(label)
            self.say('The {}: double click an edge for the loop all around it, then Use selected. It splits into the '
                     'upper and lower line at its corners. Or select one line, corner to corner.'.format(text))
        elif tab == REGIONS:
            label = dict(mm_regions.REGIONS)[key]
            self.asked.setText(label)
            self.say('Optional: the lines already say which lip and lid is which. Select its faces only to correct them, '
                     'then Use selected.')
        else:
            label = dict(PARTS_ROWS)[key]
            self.asked.setText(label)
            self.say(PARTS_HINT.format(label.lower()))

    def say(self, text, failed=False):
        self.hint.setText(text)
        self.hint.setProperty('tone', 'failed' if failed else '')
        self.hint.style().unpolish(self.hint)
        self.hint.style().polish(self.hint)

    def tab_changed(self, tab):
        """The selection mode each tab needs, on the copy of your head; other meshes only for eyes and teeth."""
        self.busy = True
        try:
            cmds.select(clear=True)
            self.isolate('custom', self.scene.custom_panel_objects(with_others=tab == PARTS))
            cmds.select(mm_picker.CUSTOM, replace=True)
            cmds.hilite(mm_picker.CUSTOM, replace=True)
            cmds.select(clear=True)
            if tab == PARTS:
                cmds.hilite(mm_picker.CUSTOM, unHilite=True)
                cmds.selectMode(object=True)
            else:
                cmds.selectMode(component=True)
                kind = {POINTS: 'vertex', LINES: 'edge', REGIONS: 'facet'}[tab]
                cmds.selectType(allComponents=False, **{kind: True})
        finally:
            self.busy = False
        self.use.setVisible(tab != POINTS)
        if self.lists[tab].currentRow() < 0 and self.lists[tab].count():
            self.lists[tab].setCurrentRow(0)
        self.row_changed()

    def select_first_missing(self):
        rows = [i for i, g in enumerate(mp.GUIDES) if g[0] not in self.points['guides']]
        self.lists[POINTS].setCurrentRow(rows[0] if rows else 0)

    # ------------------------------------------------------------------ picks

    def selection_changed(self):
        """A vertex clicked while a point is asked for is that point; then the next one is asked for."""
        if self.busy or self.closed or self.tabs.currentIndex() != POINTS:
            return
        _, label = self.row_key()
        picked = cmds.ls(selection=True, flatten=True) or []
        ids = [mm_picker.component_vertex(p) for p in picked if p.split('.')[0].split('|')[-1] == mm_picker.CUSTOM]
        ids = [i for i in ids if i is not None]
        if len(ids) != 1 or not label:
            return
        try:
            self.take_point(label, ids[0])
        except Exception as error:  # a selection callback must never raise into Maya
            traceback.print_exc()
            self.say('Could not take that point: {}'.format(error), failed=True)

    def take_point(self, label, vertex):
        self.store_point(label, vertex)
        twin = mp.mirror_label(label)
        if self.mirror.isChecked() and twin and label.endswith(' L'):
            mid = mp.midline_x(self.points, float((self.scene.custom_positions[:, 0].min() + self.scene.custom_positions[:, 0].max()) / 2))
            self.store_point(twin, mp.mirrored_vertex(self.scene.custom_positions, vertex, mid))
        self.save()
        self.refresh_rows()
        self.refit()
        self.next_point()
        self.busy = True
        try:
            cmds.select(clear=True)
        finally:
            self.busy = False

    def store_point(self, label, vertex):
        position = [float(v) for v in self.scene.custom_positions[vertex]]
        self.points['guides'][label] = {'vertex': vertex, 'position': position}
        self.scene.put_sphere('custom', label, position)

    def next_point(self):
        """The next guide without a point, after the current one; the current one when all are done."""
        rows = self.lists[POINTS]
        count = rows.count()
        here = rows.currentRow()
        for step in range(1, count + 1):
            row = (here + step) % count
            if mp.GUIDES[row][0] not in self.points['guides']:
                rows.setCurrentRow(row)
                return
        self.say('All points are picked. Click a row to change one, or go on to Lines.')

    def refit(self):
        """Line the two views up better with each point."""
        positions = self.scene.source_positions
        by_label = {g[0]: g[1] for g in mp.GUIDES}
        pairs = [(positions[by_label[k]], p['position']) for k, p in self.points['guides'].items() if k in by_label]
        self.scene.fit_source(pairs)

    def use_selected(self):
        tab, key = self.row_key()
        if key is None:
            return
        picked = cmds.ls(selection=True) or []
        if not picked:
            self.say('Nothing selected.', failed=True)
            return
        try:
            if tab == LINES:
                self.take_line(key, picked)
            elif tab == REGIONS:
                self.take_region(key, picked)
            elif tab == PARTS:
                self.take_part(key, picked)
        except ValueError as error:
            self.say(str(error), failed=True)
            return
        self.save()
        self.refresh_rows()
        self.busy = True
        try:
            cmds.select(clear=True)
        finally:
            self.busy = False
        rows = self.lists[tab]
        here = rows.currentRow()
        if tab == LINES:  # past the lines this pick filled: the next one still empty, if any
            empty = [i for i, line in enumerate(mp.LINES) if line[0] not in self.points['lines']]
            later = [i for i in empty if i > here] or empty
            rows.setCurrentRow(later[0] if later else here)
        elif here < rows.count() - 1:
            rows.setCurrentRow(here + 1)

    def take_line(self, key, picked):
        found = self.scene.edges_to_lines(key, picked)
        middle = float((self.scene.custom_positions[:, 0].min() + self.scene.custom_positions[:, 0].max()) / 2)
        for line, chain in found.items():
            if len(chain) < 3:
                raise ValueError('That is too short: select the whole line, from corner to corner.')
            problem = mp.line_side_problem(line, chain, self.scene.custom_positions, mp.midline_x(self.points, middle))
            if problem:
                raise ValueError(problem)
        for line, chain in found.items():
            positions = [[float(v) for v in self.scene.custom_positions[i]] for i in chain]
            self.points['lines'][line] = {'vertices': chain, 'positions': positions}
            self.scene.put_curve('custom', line, positions)

    def take_region(self, key, picked):
        faces = [p for p in picked if p.split('.')[0].split('|')[-1] == mm_picker.CUSTOM and '.' in p]
        if not faces:
            raise ValueError('Select faces of your head, in the right panel.')
        self.workflow.s.regions = dict(self.workflow.s.regions or {}, **{key: self.scene.to_mesh_names(faces)})
        self.paint_custom()

    def take_part(self, key, picked):
        names = []
        for item in picked:
            node = item.split('.')[0].split('|')[-1]
            if node == mm_picker.CUSTOM and '.' not in item:
                raise ValueError('That is your whole head: select the {} faces on it, or their own meshes.'.format(key))
            names.append(item)
        setattr(self.workflow.s, key, self.scene.to_mesh_names(names))

    def clear_row(self):
        tab, key = self.row_key()
        if key is None:
            return
        s = self.workflow.s
        if tab == POINTS:
            self.points['guides'].pop(key, None)
            self.scene.drop_sphere('custom', key)
            self.refit()
        elif tab == LINES:
            self.points['lines'].pop(key, None)
            self.scene.drop_curve('custom', key)
        elif tab == REGIONS:
            s.regions = {k: v for k, v in (s.regions or {}).items() if k != key}
            self.paint_custom()
        else:
            setattr(s, key, [])
        self.save()
        self.refresh_rows()

    def set_size(self, size):
        self.scene.set_sphere_size(size)
        self.points['sphere_size'] = size
        self.save()

    def save(self):
        mp.save(self.points, self.paths.points)
        self.workflow.save()

    # ------------------------------------------------------------------ the end

    @staticmethod
    def selection_mode():
        return {'object': cmds.selectMode(query=True, object=True), 'vertex': cmds.selectType(query=True, vertex=True),
                'edge': cmds.selectType(query=True, edge=True), 'facet': cmds.selectType(query=True, facet=True)}

    def restore_selection_mode(self):
        was = self.previous_mode
        cmds.select(clear=True)
        if was['object']:
            cmds.selectMode(object=True)
        else:
            cmds.selectMode(component=True)
            cmds.selectType(vertex=was['vertex'], edge=was['edge'], facet=was['facet'])

    def remove_from_scene(self):
        try:
            self.restore_selection_mode()
            for panel in self.panels.values():
                if cmds.modelPanel(panel, exists=True):
                    cmds.deleteUI(panel, panel=True)
            if self.maya_window and cmds.window(self.maya_window, exists=True):
                cmds.deleteUI(self.maya_window, window=True)
            self.scene.remove()
        except Exception:
            traceback.print_exc()

    def closeEvent(self, event):
        if not self.closed:
            self.closed = True
            for job in self.jobs:
                try:
                    cmds.scriptJob(kill=job, force=True)
                except Exception:
                    pass
            try:
                self.save()
            except Exception:
                traceback.print_exc()
            self.remove_from_scene()
            if self.on_close:
                self.on_close()
        super(PointPicker, self).closeEvent(event)
