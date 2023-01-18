# pycoyote - A Python library for building Web user interfaces

# Define your component
```python
# You define a class derived from Component
# You need to implement method render
# You can access self.children which represent all the children of your component
# You can access self.props which contains all the attributes passed to your component
# You can import HTML tags from Component, for example "from pycoyote import DIV"

from pycoyote import Component, DIV, SPAN
class MainPage(Component):
    def render(self):
        return DIV(
            SPAN({"class": "bold", "style": f"background-color: {self.props['color']};"},
                "Hello world!"
            ),
            *self.children
        )
```

# Using your component
```python
# You can pass attributes to your component
# You can pass children to your component
MainPage({"color": "green"}, 
    SPAN("Example ends here.")    # you can pass as much child as you need
)
```

# Examples
Please check [Examples](examples/) for details.

