from copy import copy
import html

def _is_primitive(element):
    # is an element a primitive element?
    return isinstance(element, Component) and element._cyo_is_primitive

def _is_non_primitive(element):
    # is an element a non-primitive element?
    return isinstance(element, Component) and not element._cyo_is_primitive

def _is_raw(element):
    return not isinstance(element, Component)

class Component:
    _cyo_is_primitive:bool=False         # is this component primitive?

    def __init__(self, *children):
        if len(children) == 0:
            self.children = []
            self.props = {}
        else:
            if (isinstance(children[0], dict)):
                self.props = copy(children[0])
                self.children = children[1:]
            else:
                self.children = copy(children)
                self.props = {}

    def render(self):
        raise NotImplementedError("Component must overwrite render method!")

    def __str__(self):
        return "".join([
            vdom.get_physical_dom() for vdom in get_virtual_dom([self])
        ])


class PrimitiveComponent(Component):
    def __init__(self, tag, *children):
        super().__init__(*children)
        self._cyo_is_primitive=True
        self._cyo_tag = tag
    
    def clone(self):
        return PrimitiveComponent(self._cyo_tag, *[self.props, *self.children])

    def render(self):
        raise NotImplementedError()

    def _get_actual_prop_value(self, prop_name, prop_value):
        if prop_name in ("class", "classname"):
            if isinstance(prop_value, tuple) or isinstance(prop_value, list):
                return (True, "class", " ".join([str(i) for i in prop_value]))
            return (True, "class", str(prop_value))
        if prop_name == "style":
            if isinstance(prop_value, dict):
                r = []
                for k, v in prop_value.items():
                    str_v = f"{html.escape(str(v))}"
                    r.append(f"{k}:{str_v}")
                return (False, "style", ';'.join(r))
            else:
                return (False, "style", html.escape(str(prop_value)))
        return (True, prop_name, prop_value)

    def get_physical_dom(self):
        out = f"<{self._cyo_tag}"
        for prop_name, prop_value in self.props.items():
            escape, actual_prop_name, actual_prop_value = self._get_actual_prop_value(prop_name, prop_value)
            if escape:
                v = f"{actual_prop_name}=\"{html.escape(actual_prop_value)}\""
            else:
                v = f"{actual_prop_name}=\"{actual_prop_value}\""
            out += f" {v}"
        if len(self.children) == 0:
            return f"{out} />"
        out += ">"
        for child in self.children:
            # we have already assumed self has been fully rendered, so all it transitive 
            # children are either raw or primitive element
            if _is_primitive(child):
                out += child.get_physical_dom()
            elif not child:
                # falsy does not generate any output
                pass
            else:
                out += html.escape(str(child))
        out += f"</{self._cyo_tag}>"
        return out
    

def get_virtual_dom(elements):
    out_elements = list(elements)
    while True:
        rendered = False
        tmp_elements = copy(out_elements)
        out_elements.clear()
        for current_element in tmp_elements:
            if _is_raw(current_element):
                out_elements.append(current_element)
            elif _is_primitive(current_element):
                out_elements.append(current_element)
            else:
                transformed = current_element.render()
                if isinstance(transformed, list):
                    out_elements.extend(transformed)
                else:
                    out_elements.append(transformed)
                rendered = True
        if not rendered:
            break
    # out_element should only contain primitive elements or raw elements
    out_elements = [
        element if _is_raw(element) else element.clone() for element in out_elements
    ]
    for element in out_elements:
        if _is_raw(element):
            continue
        element.children = get_virtual_dom(element.children)
    return out_elements


class A(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("a", *children)


class ABBR(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("abbr", *children)


class ADDRESS(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("address", *children)


class AREA(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("area", *children)


class ARTICLE(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("article", *children)


class ASIDE(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("aside", *children)


class AUDIO(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("audio", *children)


class B(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("b", *children)


class BASE(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("base", *children)


class BDI(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("bdi", *children)


class BDO(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("bdo", *children)


class BLOCKQUOTE(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("blockquote", *children)


class BODY(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("body", *children)


class BR(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("br", *children)


class BUTTON(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("button", *children)


class CANVAS(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("canvas", *children)


class CAPTION(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("caption", *children)


class CITE(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("cite", *children)


class CODE(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("code", *children)


class COL(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("col", *children)


class COLGROUP(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("colgroup", *children)


class DATA(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("data", *children)


class DATALIST(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("datalist", *children)


class DD(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("dd", *children)


class DEL(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("del", *children)


class DETAILS(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("details", *children)


class DFN(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("dfn", *children)


class DIALOG(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("dialog", *children)


class DIV(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("div", *children)


class DL(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("dl", *children)


class DT(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("dt", *children)


class EM(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("em", *children)


class EMBED(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("embed", *children)


class FIELDSET(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("fieldset", *children)


class FIGCAPTION(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("figcaption", *children)


class FIGURE(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("figure", *children)


class FOOTER(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("footer", *children)


class FORM(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("form", *children)


class HEAD(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("head", *children)


class HEADER(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("header", *children)


class HGROUP(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("hgroup", *children)


class H1(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("h1", *children)


class H2(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("h2", *children)


class H3(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("h3", *children)


class H4(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("h4", *children)


class H5(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("h5", *children)


class H6(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("h6", *children)


class HR(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("hr", *children)


class HTML(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("html", *children)


class I(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("i", *children)


class IFRAME(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("iframe", *children)


class IMG(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("img", *children)


class INPUT(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("input", *children)


class INS(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("ins", *children)


class KBD(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("kbd", *children)


class KEYGEN(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("keygen", *children)


class LABEL(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("label", *children)


class LEGEND(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("legend", *children)


class LI(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("li", *children)


class LINK(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("link", *children)


class MAIN(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("main", *children)


class MAP(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("map", *children)


class MARK(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("mark", *children)


class MENU(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("menu", *children)


class MENUITEM(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("menuitem", *children)


class META(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("meta", *children)


class METER(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("meter", *children)


class NAV(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("nav", *children)


class NOSCRIPT(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("noscript", *children)


class OBJECT(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("object", *children)


class OL(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("ol", *children)


class OPTGROUP(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("optgroup", *children)


class OPTION(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("option", *children)


class OUTPUT(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("output", *children)


class P(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("p", *children)


class PARAM(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("param", *children)


class PICTURE(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("picture", *children)


class PRE(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("pre", *children)


class PROGRESS(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("progress", *children)


class Q(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("q", *children)


class RP(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("rp", *children)


class RT(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("rt", *children)


class RUBY(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("ruby", *children)


class S(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("s", *children)


class SAMP(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("samp", *children)


class SCRIPT(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("script", *children)


class SECTION(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("section", *children)


class SELECT(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("select", *children)


class SMALL(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("small", *children)


class SOURCE(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("source", *children)


class SPAN(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("span", *children)


class STRONG(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("strong", *children)


class STYLE(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("style", *children)


class SUB(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("sub", *children)


class SUMMARY(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("summary", *children)


class SUP(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("sup", *children)


class SVG(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("svg", *children)


class TABLE(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("table", *children)


class TBODY(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("tbody", *children)


class TD(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("td", *children)


class TEMPLATE(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("template", *children)


class TEXTAREA(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("textarea", *children)


class TFOOT(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("tfoot", *children)


class TH(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("th", *children)


class THEAD(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("thead", *children)


class TIME(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("time", *children)


class TITLE(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("title", *children)


class TR(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("tr", *children)


class TRACK(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("track", *children)


class U(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("u", *children)


class UL(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("ul", *children)


class VAR(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("var", *children)


class VIDEO(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("video", *children)


class WBR(PrimitiveComponent):
    def __init__(self, *children):
        super().__init__("wbr", *children)

