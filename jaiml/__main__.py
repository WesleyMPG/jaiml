import click, os
from .__base_project import files, folders
from pathlib import Path


def create_files(base_path):
  for file_name in files.keys():
    path = os.path.join(base_path, file_name)
    with open(path, 'w') as file:
      file.write(files[file_name])


def create_folders(base_path):
  for folder in folders:
    path = os.path.join(base_path, folder)
    os.mkdir(path)


@click.group()
def cli():
  """A CLI to create jaiml projects."""


@cli.command()
@click.argument('path', type=click.Path(exists=True))
def create(path='.'):
  r"""Create a folder structure in a received path."""
  p = Path(path)
  create_folders(p.absolute())
  create_files(p.absolute())
  


if __name__ == '__main__':
  cli(prog_name='python -m jaiml')