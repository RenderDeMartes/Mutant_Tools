'''
Attr suggestions for the block config panel, taken from the preset templates.

scan_templates() opens every template .ma the presets in Blocks/000_Presets load,
reads all the block configs and saves which value each block attr uses in which
template to template_suggestions.json (next to this file). The attrs panel reads
that json: right click an attr -> Suggestions from templates.

Rescan after changing the templates (it opens files, so save your scene first):
	from Mutant_Tools.UI.AutoRigger import template_suggestions
	template_suggestions.scan_templates()
'''
import datetime
import json
import os
import re

import maya.cmds as cmds

FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PRESETS_PATH = os.path.join(FOLDER, 'Blocks', '000_Presets')
TEMPLATES_PATH = os.path.join(FOLDER, 'Utils', 'IO', 'Guide_Data')
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template_suggestions.json')

SKIPS = ('precode', 'postcode', 'Build_Command', 'Import_Command', 'MutantBackup', 'Help', 'Code')

_cache = {'mtime': None, 'data': {}}


#-------------------------------------------------------------------
def block_key(config):
	"""Block name without version, from the config Import_Command (Limb_v002 -> Limb)."""
	if not cmds.attributeQuery('Import_Command', node=config, exists=True):
		return None
	match = re.search(r'import\s+(\w+)', cmds.getAttr('{}.Import_Command'.format(config)) or '')
	if not match:
		return None
	return re.sub(r'_v\d+$', '', match.group(1)).replace('exec_', '')


def preset_templates():
	"""Template .ma paths the preset exec scripts load."""
	paths = []
	for root, dirs, files in os.walk(PRESETS_PATH):
		for f in files:
			if not f.startswith('exec_') or not f.endswith('.py') or re.search(r'_v\d+\.py$', f):
				continue
			with open(os.path.join(root, f)) as script:
				for name in re.findall(r"'(\w+\.ma)'", script.read()):
					path = os.path.join(TEMPLATES_PATH, name)
					if os.path.exists(path) and path not in paths:
						paths.append(path)
	return sorted(paths)


def _scene_configs():
	return sorted(set(a.split('.')[0] for a in cmds.ls('*.Import_Command', '*:*.Import_Command') or []))


def _config_values(config):
	"""attr -> (maya type, value) of the block options on config (enums as labels)."""
	values = {}
	for attr in cmds.listAttr(config, ud=True) or []:
		if attr in SKIPS or '.' in attr:
			continue
		path = '{}.{}'.format(config, attr)
		try:
			attr_type = cmds.getAttr(path, type=True)
			value = cmds.getAttr(path, asString=True) if attr_type == 'enum' else cmds.getAttr(path)
		except Exception:
			continue
		if isinstance(value, (list, tuple)):
			continue
		if attr_type == 'bool':
			value = bool(value)
		elif attr_type == 'string':
			value = value or ''
		elif isinstance(value, float) and value.is_integer():
			value = int(value)
		values[attr] = (attr_type, value)
	return values


#-------------------------------------------------------------------
def scan_templates(paths=None, save=True):
	"""Open every template and collect block -> attr -> value -> templates. Leaves an empty scene."""
	paths = paths or preset_templates()
	blocks = {}
	scanned = []
	for path in paths:
		template = os.path.splitext(os.path.basename(path))[0]
		try:
			cmds.file(path, open=True, force=True, prompt=False, ignoreVersion=True)
		except Exception as e:
			# missing plugins etc. still leave the configs loaded
			print('Template {} opened with errors: {}'.format(template, e))
		scanned.append(template)
		for config in _scene_configs():
			key = block_key(config)
			if not key:
				continue
			attrs = blocks.setdefault(key, {})
			for attr, (attr_type, value) in _config_values(config).items():
				entry = attrs.setdefault(attr, {'type': attr_type, 'values': {}})
				uses = entry['values'].setdefault(json.dumps(value), {'value': value, 'templates': [], 'uses': 0})
				uses['uses'] += 1
				if template not in uses['templates']:
					uses['templates'].append(template)
	cmds.file(new=True, force=True)

	# value lists sorted by most used
	for attrs in blocks.values():
		for entry in attrs.values():
			entry['values'] = sorted(entry['values'].values(), key=lambda v: (-len(v['templates']), -v['uses'], str(v['value'])))

	data = {'scanned': datetime.date.today().isoformat(), 'templates': scanned, 'blocks': blocks}
	if save:
		with open(DATA_PATH, 'w') as f:
			json.dump(data, f, indent=1, sort_keys=True)
		print('Template suggestions: {} blocks from {} templates -> {}'.format(len(blocks), len(scanned), DATA_PATH))
	return data


#-------------------------------------------------------------------
def load():
	try:
		mtime = os.path.getmtime(DATA_PATH)
	except OSError:
		return {}
	if mtime != _cache['mtime']:
		try:
			with open(DATA_PATH) as f:
				_cache['data'] = json.load(f)
		except Exception:
			_cache['data'] = {}
		_cache['mtime'] = mtime
	return _cache['data']


def suggestions(config, attr):
	"""[{'value', 'templates', 'uses'}] the templates use for this block attr, most used first."""
	key = block_key(config)
	entry = load().get('blocks', {}).get(key or '', {}).get(attr)
	return entry['values'] if entry else []


def template_count():
	return len(load().get('templates', []))
