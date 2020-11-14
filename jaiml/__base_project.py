folders = [
  'jinja-templates',
  'out',
  'src',
]

files = { 
  'Manager.py':
    """\
from jaiml import JaimlManager


__all__ = ['Manager']


Manager = JaimlManager(
  __name__,
  brain_file=False
  )
""",

  'main.py':
    """\
from pathlib import Path
from sys import path as sys_path
from Manager import Manager

sys_path.append(Path('.').absolute())

# import your source files here



Manager.generate_all()
"""
}