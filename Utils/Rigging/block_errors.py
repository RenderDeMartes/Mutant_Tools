"""Block build errors the artist can fix (block order, missing nodes...), with a message written for them.

A block raises it while building:

    from Mutant_Tools.Utils.Rigging import block_errors
    raise block_errors.BlockBuildError('Jaw not built yet', 'Move Jaw_Block above Lips_Block...', block='Lips_Block')

The AutoRigger reverts the build like any other failure and the Build Log window (UI/AutoRigger/build_log.py)
shows title + message on top instead of guessing a cause. Outside the AutoRigger it is a normal exception.
"""
from __future__ import absolute_import


class BlockBuildError(RuntimeError):
    """Build error with a message written for the artist. block = the block that raised it."""

    # blocks reload their modules, so readers check this flag, not isinstance
    mutant_block_error = True

    def __init__(self, title, message, block=None):
        super(BlockBuildError, self).__init__('{}: {}'.format(title, message))
        self.title = title
        self.message = message
        self.block = block


def is_block_error(error):
    return bool(getattr(error, 'mutant_block_error', False))
