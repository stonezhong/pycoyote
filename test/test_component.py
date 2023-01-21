# !/usr/bin/python
# -*- coding: UTF-8 -*-

import pytest

from pycoyote.component import _is_primitive, _is_non_primitive, DIV, P, Component, get_virtual_dom


class MyComponent(Component):
    def render(self):
        pass


def test_is_primitive():
    assert _is_primitive("abc") is False
    assert _is_primitive(DIV()) is True
    assert _is_primitive(MyComponent()) is False


def test_is_non_primitive():
    assert _is_non_primitive("abc") is False
    assert _is_non_primitive(DIV()) is False
    assert _is_non_primitive(MyComponent()) is True


# def test_get_actual_prop_value():
#     assert _get_actual_prop_value("class", "foo") == (True, "class", "foo")
#     assert _get_actual_prop_value("class", ["foo", "bar"]) == (True, "class", "foo bar")
#     assert _get_actual_prop_value("class", "foo>bar") == (True, "class", "foo>bar")
#
#     assert _get_actual_prop_value("style", "font-size: 10px;") == (False, "style", "font-size: 10px;")
#     assert _get_actual_prop_value("style", "font-size: a>b") == (False, "style", "font-size: a&gt;b")
#
#     assert _get_actual_prop_value("style", {"font-size: 10px"}) == (False, "style", "font-size: 10px;")

def test_primitive_component_get_physical_dom():
    div = DIV()
    assert div.get_physical_dom() == '<div />'

    div = DIV({"x": 1})
    assert div.get_physical_dom() == '<div x="1" />'

    div = DIV({"x": 1, "y": "foo"})
    assert div.get_physical_dom() == '<div x="1" y="foo" />'

    div = DIV({"class": "red"})
    assert div.get_physical_dom() == '<div class="red" />'

    div = DIV({"class": ["red", "green"]})
    assert div.get_physical_dom() == '<div class="red green" />'

    div = DIV({"style": {"color": "red"}})
    assert div.get_physical_dom() == '<div style="color:red" />'

    div = DIV({"style": {"color": "red", "background-color": "green"}})
    assert div.get_physical_dom() == '<div style="color:red;background-color:green" />'

    div = DIV({"style": {"color": "red", "background-color": "'green'"}})
    assert div.get_physical_dom() == '<div style="color:red;background-color:&#x27;green&#x27;" />'

    div = DIV("foo")
    assert div.get_physical_dom() == '<div>foo</div>'

    div = DIV("foo", "bar")
    assert div.get_physical_dom() == '<div>foobar</div>'

    div = DIV({"x": 1}, "foo", "bar")
    assert div.get_physical_dom() == '<div x="1">foobar</div>'

    div = DIV("a>b")
    assert div.get_physical_dom() == '<div>a&gt;b</div>'

    div = DIV({"x": 1}, "a>b")
    assert div.get_physical_dom() == '<div x="1">a&gt;b</div>'


class MyTestComponent1(Component):
    # A component that missing render method
    pass


class MyTestComponent2(Component):
    # simple component
    def render(self):
        return DIV({"x": 1}, "foo")


class MyTestComponent3(Component):
    # a component returns another component
    def render(self):
        return MyTestComponent2()


class MyTestComponent4(Component):
    # a component that has string as falsy value as child
    def render(self):
        return DIV({"x": 1},
            "foo",
            False,
            None
        )


class MyTestComponent5(Component):
    # a component that return an array
    def render(self):
        return [
            DIV({"x": 1}, "foo"),
            DIV({"y": 1}, "bar"),
        ]


class MyTestComponent6(Component):
    # a component that return an indirectory
    def render(self):
        return DIV({"x": 1},
            P("foo"),
            MyTestComponent5()
        )


def assert_same_element(element1, element2):
    assert element1.__class__ == element2.__class__
    if isinstance(element1, Component) and isinstance(element2, Component):
        assert_same_elements(element1.children, element2.children)


def assert_same_elements(elements1, elements2):
    assert len(elements1) == len(elements2)
    for i in range(len(elements1)):
        assert_same_element(elements1[i], elements2[i])


def test_get_virtual_dom():
    # You should get exception if your component derive from Component but did not implement
    # render method
    with pytest.raises(TypeError) as excinfo:
        _ = MyTestComponent1()
    assert "Can't instantiate abstract class" in excinfo.value.args[0]

    assert_same_elements(
        get_virtual_dom([MyTestComponent2()]),
        [
            DIV({"x": 1}, "foo")
        ]
    )

    assert_same_elements(
        get_virtual_dom([MyTestComponent3()]),
        [
            DIV({"x": 1}, "foo")
        ]
    )

    assert_same_elements(
        get_virtual_dom([MyTestComponent4()]),
        [
            DIV({"x": 1}, "foo", False, None),
        ]
    )

    assert_same_elements(
        get_virtual_dom([MyTestComponent5()]),
        [
            DIV({"x": 1}, "foo"),
            DIV({"x": 1}, "bar"),
        ]
    )

    assert_same_elements(
        get_virtual_dom([MyTestComponent6()]),
        [
            DIV({"x": 1},
                P("foo"),
                DIV({"x": 1}, "foo"),
                DIV({"x": 1}, "bar"),
            ),
        ]
    )
