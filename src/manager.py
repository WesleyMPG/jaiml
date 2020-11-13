import jinja2 as j
from os.path import curdir, abspath, splitext
from functools import wraps


__all__ = ['JaimlManager']

#: Extensions of files that JaimlManager should look for
accepted_file_ext = [
  '.jinja',
  '.j2',
  '.aiml',
  '.xml'
]   

class JaimlManager(object):
  """This class has methods to register and manage jinja-aiml(jaiml) templates.

  JaimlManager will register any function that uses the decorator :meth:`marker`
  as a jaiml provider, which means that function follow the pattern decribed in
  :meth:`marker`.

  :param brain_file: If True a file with the output aiml will be generated.
  :type brain_file: bool, defauts to True
  :param templates_dir_name: path to templates folder.
  :type templates_dir_name: str, defaults to 'jinja-templates'

  """

  def __init__(self, module_name, brain_file=True, templates_dir_name='jinja-templates'):
    self.all_defined_jaiml = []  # Stores all functions that use marker() 
    self.__brain_file = brain_file
    self.module_name = module_name
    self.__templates_dir_name = templates_dir_name
    self.ENVIROMENT = self.__create_jinja_enviroment()
    self.__header = '<aiml version="1.0" encoding="UTF-8">\n'
    self.__footer = '\n</aiml>'
    
  @property
  def brain_file(self):
    return self.__brain_file

  @brain_file.setter
  def brain_file(self, val):
    if type(val) != bool:
      raise TypeError(f'must be a bool, not {type(val)}') 
    self.__brain_file = val

  @property
  def header(self):
    r"""The header to be placed on the output and all aiml files.

    Defauts to '<aiml version="1.0" encoding="UTF-8">\\n'.
    """
    return self.__header

  @header.setter
  def header(self, header):
    if type(header) != str:
      raise TypeError(f'must be a str, not {type(header)}')
    self.__header = header

  @property
  def footer(self):
    r"""The footer to be placed on the output and all aiml files.

    Defaults to '\\n</aiml>'.
    """
    return self.__footer
  
  @footer.setter
  def footer(self, footer):
    if type(footer) != str:
      raise TypeError(f'must be a str, not {type(footer)}.')
    self.__footer = footer

  def __create_jinja_loader(self):
    
    loader = None
    try:
      loader = j.PackageLoader(self.module_name, self.__templates_dir_name)
    except ModuleNotFoundError as exc:
      pass
    finally:
      return loader

  def __create_jinja_enviroment(self):
    return j.Environment(
      trim_blocks=True, 
      lstrip_blocks=True,
      loader=self.__create_jinja_loader()
    )

  def __create_template(self, buffer):
    if len(buffer) < 50 and splitext(buffer)[1] in accepted_file_ext:
      t = self.ENVIROMENT.get_template(buffer) 
    else:
      t = self.ENVIROMENT.from_string(buffer)
    return t

  def get_output(self):
    """Returns the result of joining all jaiml templates.

    :rtype: str
    """
    output = self.header
    for func in self.all_defined_jaiml:
      output += func()
    output += self.footer
    if self.brain_file:
      self._generate_file(output, 'brain.aiml')
    return output

  def _generate_file(self, buffer, file_name):
    with open(file_name, 'w') as file:
      file.write(buffer)

  def generate_file(self, template_name, headerless=True, ext='.aiml'):
    """Generates a file with the output of a jaiml provider function.

    :param str template_name: Name of the function to have a file generated.
    :param headerless: If False the generated file will have, defaults to True.
    :type headerless: bool, optional
    :param str ext: output file extension, defaults to '.aiml'.

    Example:
      .. code-block:: python

          @jaiml_manager_instance.marker
          def foo():
            return 'some_file.xml', vars_dict

          jaiml_manager_instance.generate_file('foo')
    """
    for i in self.all_defined_jaiml:
      if i.__name__ == template_name:
        output = i() if headerless else self.header + i() + self.footer
        self._generate_file(output, template_name + ext)

  def generate_all(self, headerless=True, ext='.aiml'):
    """Does the same as :meth:`generate_file()` but to all jaiml provider functions.
    """
    for i in self.all_defined_jaiml:
      output = i() if headerless else self.header + i() + self.footer
      self._generate_file(output, i.__name__ + ext)

  def marker(self, function):
    """This method is a decorator that marks a function as a jinja-aiml provider.

      It must be a function which returs two things:
      
        * A string buffer containing jinja-aiml (xml) syntax or the name \
          of a file from jinja-templates folder at the root of your project.

        * A dic with keys which the names are the variable names used in your template.

        Example 1:
          .. code-block:: python

              def ex1():
                buffer = \"""
                <category>
                    <pattern>HELLO</pattern>
                    <template>
                        <random>
                        {% for response in responses %}
                          <li>{{ response }}</li>
                        {% endfor %}
                    </random>
                    </template>
                </category>
                \"""
                responses = ['HELLO SIR', 'How Are you?', 'Hi!', 
                              'Hello dear', 'Hi, are you ok?']
                vars = {
                  'responses': responses,
                }
                return buffer, vars

        Example 2:
          .. code-block:: python

              def ex2():
                responses = ['HELLO SIR', 'How Are you?', 'Hi!', 
                              'Hello dear', 'Hi, are you ok?']
                vars = {
                  'responses': responses,
                }
                return 'example-file.xml', vars
    """
    @wraps(function)
    def wrapper():
      data = function()
      buffer, vars = data
      if type(buffer) != str and type(vars) != dict:
        raise TypeError(f'{function.__name__} return 0 must be srt and return 1 must be dict.')
      t = self.__create_template(buffer)
      return t.render(**vars)

    self.all_defined_jaiml.append(wrapper)
    return wrapper
