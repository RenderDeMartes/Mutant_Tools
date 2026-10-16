'''
Update a block config node to another block json (version change / Update block)
without losing what the user had set.

- Attrs that exist in the new json keep their value (same name, or same name
  ignoring case and underscores, e.g. Ctrl_Size -> CtrlSize).
- Values are converted when the attr type changed (enum label -> string, '1' -> int...).
- Enum labels the new json does not have: ctrl type / color enums get the label
  appended (any repo curve or color is valid), other enums keep the json default.
- Everything that could not be kept (attr removed in the new version, value that
  does not fit) is saved in the locked MutantBackup string attr as json, and comes
  back when a later version has that attr again (going back to the old version).
'''
import json
import re

import maya.cmds as cmds

from Mutant_Tools.UI.AutoRigger import config_previews

BACKUP_ATTR = 'MutantBackup'
SKIPS = ('precode', 'postcode', 'Build_Command', 'Import_Command', BACKUP_ATTR)
# always taken from the new json
JSON_ONLY = ('Help',)
NUMERIC_TYPES = ('long', 'short', 'byte', 'double', 'float', 'doubleLinear', 'doubleAngle')


#-------------------------------------------------------------------
def _norm(name):
	return re.sub(r'[^a-z0-9]', '', name.lower())


def read_backup(config):
	if not cmds.attributeQuery(BACKUP_ATTR, node=config, exists=True):
		return {}
	try:
		return json.loads(cmds.getAttr('{}.{}'.format(config, BACKUP_ATTR)) or '{}')
	except Exception:
		return {}


def write_backup(config, data):
	attr = '{}.{}'.format(config, BACKUP_ATTR)
	if not data and not cmds.attributeQuery(BACKUP_ATTR, node=config, exists=True):
		return
	if not cmds.attributeQuery(BACKUP_ATTR, node=config, exists=True):
		cmds.addAttr(config, ln=BACKUP_ATTR, dt='string')
	cmds.setAttr(attr, lock=False)
	cmds.setAttr(attr, json.dumps(data, sort_keys=True), type='string')
	# locked so the attrs panel does not show it as a block option
	cmds.setAttr(attr, lock=True)


def pop_backup(config, attr):
	data = read_backup(config)
	entry = data.pop(attr, None)
	write_backup(config, data)
	return entry


#-------------------------------------------------------------------
def snapshot(config):
	"""attr -> {'type', 'value'} of every block option on the config (enums as labels)."""
	data = {}
	for attr in cmds.listAttr(config, ud=True) or []:
		if attr in SKIPS or '.' in attr:
			continue
		path = '{}.{}'.format(config, attr)
		try:
			attr_type = cmds.getAttr(path, type=True)
			if attr_type == 'enum':
				value = cmds.getAttr(path, asString=True)
				is_default = cmds.getAttr(path) == 0
			elif attr_type == 'string':
				value = cmds.getAttr(path) or ''
				is_default = value == ''
			else:
				value = cmds.getAttr(path)
				is_default = value == (cmds.attributeQuery(attr, node=config, listDefault=True) or [None])[0]
		except Exception:
			continue
		if isinstance(value, (list, tuple)):
			continue
		data[attr] = {'type': attr_type, 'value': value, 'is_default': is_default}
	return data


def _find(source, name, used):
	if name in source and name not in used:
		return name
	norm = _norm(name)
	for key in source:
		if key not in used and _norm(key) == norm:
			return key
	return None


#-------------------------------------------------------------------
def apply_value(config, attr, kind, value):
	"""Set value on config.attr (kind = json key suffix). Returns True when it fit."""
	path = '{}.{}'.format(config, attr)
	try:
		if kind == 'string':
			if isinstance(value, bool):
				value = 'True' if value else 'False'
			cmds.setAttr(path, '' if value is None else str(value), type='string')
			return True

		if kind == 'enum':
			options = (cmds.attributeQuery(attr, node=config, listEnum=True) or [''])[0].split(':')
			label = str(value)
			if label not in options:
				if label in config_previews.extended_options(attr, options):
					options.append(label)
					cmds.addAttr(path, e=True, enumName=':'.join(options))
				else:
					return False
			cmds.setAttr(path, options.index(label))
			return True

		if kind == 'float':
			if isinstance(value, bool) or value in (None, ''):
				return False
			number = int(round(float(value)))
			if cmds.attributeQuery(attr, node=config, maxExists=True):
				if number > cmds.attributeQuery(attr, node=config, maximum=True)[0]:
					cmds.addAttr(path, e=True, max=max(100, number))
			if cmds.attributeQuery(attr, node=config, minExists=True):
				if number < cmds.attributeQuery(attr, node=config, minimum=True)[0]:
					cmds.addAttr(path, e=True, min=number)
			cmds.setAttr(path, number)
			return True

		if kind == 'bool':
			if isinstance(value, str):
				if value.strip().lower() not in ('true', 'false', '0', '1'):
					return False
				value = value.strip().lower() in ('true', '1')
			cmds.setAttr(path, 1 if value else 0)
			return True
	except Exception as e:
		print('Could not set {}: {}'.format(path, e))
	return False


def _create_attr(mt, config, attr_name, kind, default):
	if kind == 'string':
		mt.string_attr(input=config, name=attr_name, string=default)
	elif kind == 'enum':
		mt.new_enum(input=config, name=attr_name, enums=default)
	elif kind == 'float':
		mt.new_attr_interger(input=config, name=attr_name, min=1, max=20, default=int(float(default)))
	elif kind == 'bool':
		mt.new_boolean(input=config, name=attr_name, dv=default)


#-------------------------------------------------------------------
def update_config(mt, block, config, module, icons_folder=None):
	"""Rebuild the config attrs from module['attrs'] keeping the user values. Returns a report dict."""
	attrs_in_json = module.get('attrs', {})
	current = snapshot(config)
	backup = read_backup(config)
	report = {'kept': [], 'restored': [], 'backed_up': [], 'defaults': []}

	# delete the old attrs, they are rebuilt in json order
	for attr in current:
		try:
			cmds.deleteAttr('{}.{}'.format(config, attr))
		except Exception as e:
			print('Could not delete {}.{}: {}'.format(config, attr, e))

	used_current = set()
	kept_sources = set()
	used_backup = set()
	for key, default in attrs_in_json.items():
		if '_' not in key:
			continue
		attr_name, kind = key.rsplit('_', 1)
		try:
			_create_attr(mt, config, attr_name, kind, default)
		except Exception as e:
			print('Could not create {}.{}: {}'.format(config, attr_name, e))
			continue

		if kind != 'enum':
			apply_value(config, attr_name, kind, default)
		if attr_name in JSON_ONLY:
			continue

		source_key = _find(current, attr_name, used_current)
		backup_key = _find(backup, attr_name, used_backup)
		source = current.get(source_key) if source_key is not None else None
		if source_key is not None:
			used_current.add(source_key)

		# a value the user set before (backup) wins over an untouched default
		if source and not (source['is_default'] and backup_key is not None):
			if apply_value(config, attr_name, kind, source['value']):
				kept_sources.add(source_key)
				report['kept'].append(attr_name)
				continue

		if backup_key is not None and apply_value(config, attr_name, kind, backup[backup_key].get('value')):
			used_backup.add(backup_key)
			if source_key is not None:
				kept_sources.add(source_key)
			report['restored'].append(attr_name)
			continue

		if source and apply_value(config, attr_name, kind, source['value']):
			kept_sources.add(source_key)
			report['kept'].append(attr_name)
			continue

		report['defaults'].append(attr_name)

	# values that could not be kept go to the backup (attr gone or value does not fit)
	for key in used_backup:
		backup.pop(key, None)
	for attr, entry in current.items():
		# defaults are not worth remembering
		if attr not in kept_sources and attr not in JSON_ONLY and not entry['is_default']:
			backup[attr] = {'type': entry['type'], 'value': entry['value']}
			report['backed_up'].append(attr)
	write_backup(config, backup)

	if 'Icon' in module and icons_folder:
		import os
		icon_name = module['Icon']
		if not icon_name.endswith('.png'):
			icon_name += '.png'
		if cmds.attributeQuery('iconName', node=block, exists=True):
			try:
				cmds.setAttr('{}.iconName'.format(block), os.path.join(icons_folder, icon_name), type='string')
			except Exception as e:
				print('Could not update icon for {}: {}'.format(block, e))

	msg = '{}: kept {}, restored from backup {}, backed up {}'.format(
		block, len(report['kept']), len(report['restored']), len(report['backed_up']))
	if report['restored']:
		msg += ' | restored: ' + ', '.join(report['restored'])
	if report['backed_up']:
		msg += ' | backed up: ' + ', '.join(report['backed_up'])
	print(msg)
	return report
