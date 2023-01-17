# pycoyote - A Python library for building Web user interfaces

# Define your component
```python
# You define a class derived from Component
# You need to implement method render
# You can access self.children which represent all the children of your component
# You can access self.props which contains all the attributes passed to your component

from pycoyote import Component
class MainPage(Component):
    def render(self):
        return DIV({"style":"background-color: green;"}
            "hello world!"
        )

```

