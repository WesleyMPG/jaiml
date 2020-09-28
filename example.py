from jaiml import JaimlManager

__all__ = ['manager']

manager = JaimlManager(__name__)


@manager.marker
def example():
  buffer = """
  <category>
      <pattern>HELLO _</pattern>
      <template>
          <random>
          {% for response in responses %}
          <li>{{ response }}</li>
          {% endfor %}
      </random>
      </template>
  </category>
  """

  responses = ['HELLO SIR', 'How Are you?', 'Hi!', 
                'Hello dear', 'Hi, are you ok?']
  vars = {
    'responses': responses,
  }
  return buffer, vars


if __name__ == '__main__':
  print(manager.get_output())
