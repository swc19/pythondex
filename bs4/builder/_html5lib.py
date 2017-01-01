# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

__all__ = [
    'HTML5TreeBuilder',
    ]

import warnings

from bs4.builder import (
    PERMISSIVE,
    HTML,
    HTML_5,
    HTMLTreeBuilder,
    )
from bs4.element import (
    NamespacedAttribute,
    whitespace_re,
)
import html5lib
from html5lib.constants import namespaces
from bs4.element import (
    Comment,
    Doctype,
    NavigableString,
    Tag,
    )

try:
    # Pre-0.99999999
    from html5lib.treebuilders import _base as treebuilder_base
    new_html5lib = False
except ImportError as e:
    # 0.99999999 and up
    from html5lib.treebuilders import base as treebuilder_base
    new_html5lib = True

class HTML5TreeBuilder(HTMLTreeBuilder):
    """Use html5lib to build a tree."""

    NAME = "html5lib"

    features = [NAME, PERMISSIVE, HTML_5, HTML]

    def prepare_markup(self, markup, user_specified_encoding,
                       document_declared_encoding=None, exclude_encodings=None):
        # Store the user-specified encoding for use later on.
        self.user_specified_encoding = user_specified_encoding

        # document_declared_encoding and exclude_encodings aren't used
        # ATM because the html5lib TreeBuilder doesn't use
        # UnicodeDammit.
        if exclude_encodings:
            warnings.warn("You provided a value for exclude_encoding, but the html5lib tree builder doesn't support exclude_encoding.")
        yield (markup, None, None, False)

    # These methods are defined by Beautiful Soup.
    def feed(self, markup):
        if self.soup.parse_only is not None:
            warnings.warn("You provided a value for parse_only, but the html5lib tree builder doesn't support parse_only. The entire document will be parsed.")
        parser = html5lib.HTMLParser(tree=self.create_treebuilder)

        extra_kwargs = dict()
        if not isinstance(markup, str):
            if new_html5lib:
                extra_kwargs['override_encoding'] = self.user_specified_encoding
            else:
                extra_kwargs['encoding'] = self.user_specified_encoding
        doc = parser.parse(markup, **extra_kwargs)

        # Set the character encoding detected by the tokenizer.
        if isinstance(markup, str):
            # We need to special-case this because html5lib sets
            # charEncoding to UTF-8 if it gets Unicode input.
            doc.original_encoding = None
        else:
            original_encoding = parser.tokenizer.stream.charEncoding[0]
            if not isinstance(original_encoding, str):
                # In 0.99999999 and up, the encoding is an html5lib
                # Encoding object. We want to use a string for compatibility
                # with other tree builders.
                original_encoding = original_encoding.name
            doc.original_encoding = original_encoding

    def create_treebuilder(self, namespaceHTMLElements):
        self.underlying_builder = TreeBuilderForHtml5lib(
            self.soup, namespaceHTMLElements)
        return self.underlying_builder

    def test_fragment_to_document(self, fragment):
        """See `TreeBuilder`."""
        return '<html><head></head><body>%s</body></html>' % fragment


class TreeBuilderForHtml5lib(treebuilder_base.TreeBuilder):

    def __init__(self, soup, namespaceHTMLElements):
        self.soup = soup
        super(TreeBuilderForHtml5lib, self).__init__(namespaceHTMLElements)

    def documentClass(self):
        self.soup.reset()
        return Element(self.soup, self.soup, None)

    def insertDoctype(self, token):
        name = token["name"]
        publicId = token["publicId"]
        systemId = token["systemId"]

        doctype = Doctype.for_name_and_ids(name, publicId, systemId)
        self.soup.object_was_parsed(doctype)

    def elementClass(self, name, namespace):
        tag = self.soup.new_tag(name, namespace)
        return Element(tag, self.soup, namespace)

    def commentClass(self, data):
        return TextNode(Comment(data), self.soup)

    def fragmentClass(self):
        self.soup = BeautifulSoup("")
        self.soup.name = "[document_fragment]"
        return Element(self.soup, self.soup, None)

    def appendChild(self, node):
        # XXX This code is not covered by the BS4 tests.
        self.soup.append(node.element)

    def getDocument(self):
        return self.soup

    def getFragment(self):
        return treebuilder_base.TreeBuilder.getFragment(self).element

class AttrList(object):
    def __init__(self, element):
        self.element = element
        self.attrs = dict(self.element.attrs)
    def __iter__(self):
        return list(self.attrs.items()).__iter__()
    def __setitem__(self, name, value):
        # If this attribute is a multi-valued attribute for this element,
        # turn its value into a list.
        list_attr = HTML5TreeBuilder.cdata_list_attributes
        if (name in list_attr['*']
            or (self.element.name in list_attr
                and name in list_attr[self.element.name])):
            # A node that is being cloned may have already undergone
            # this procedure.
            if not isinstance(value, list):
                value = whitespace_re.split(value)
        self.element[name] = value
    def items(self):
        return list(self.attrs.items())
    def keys(self):
        return list(self.attrs.keys())
    def __len__(self):
        return len(self.attrs)
    def __getitem__(self, name):
        return self.attrs[name]
    def __contains__(self, name):
        return name in list(self.attrs.keys())


class Element(treebuilder_base.Node):
    def __init__(self, element, soup, namespace):
        treebuilder_base.Node.__init__(self, element.name)
        self.element = element
        self.soup = soup
        self.namespace = namespace

    def appendChild(self, node):
        string_child = child = None
        if isinstance(node, str):
            # Some other piece of code decided to pass in a string
            # instead of creating a TextElement object to contain the
            # string.
            string_child = child = node
        elif isinstance(node, Tag):
            # Some other piece of code decided to pass in a Tag
            # instead of creating an Element object to contain the
            # Tag.
            child = node
        elif node.element.__class__ == NavigableString:
            string_child = child = node.element
        else:
            child = node.element

        if not isinstance(child, str) and child.parent is not None:
            node.element.extract()

        if (string_child and self.element.contents
            and self.element.contents[-1].__class__ == NavigableString):
            # We are appending a string onto another string.
            # TODO This has O(n^2) performance, for input like
            # "a</a>a</a>a</a>..."
            old_element = self.element.contents[-1]
            new_element = self.soup.new_string(old_element + string_child)
            old_element.replace_with(new_element)
            self.soup._most_recent_element = new_element
        else:
            if isinstance(node, str):
                # Create a brand new NavigableString from this string.
                child = self.soup.new_string(node)

            # Tell Beautiful Soup to act as if it parsed this element
            # immediately after the parent's last descendant. (Or
            # immediately after the parent, if it has no children.)
            if self.element.contents:
                most_recent_element = self.element._last_descendant(False)
            elif self.element.next_element is not None:
                # Something from further ahead in the parse tree is
                # being inserted into this earlier element. This is
                # very annoying because it means an expensive search
                # for the last element in the tree.
                most_recent_element = self.soup._last_descendant()
            else:
                most_recent_element = self.element

            self.soup.object_was_parsed(
                child, parent=self.element,
                most_recent_element=most_recent_element)

    def getAttributes(self):
        return AttrList(self.element)

    def setAttributes(self, attributes):

        if attributes is not None and len(attributes) > 0:

            converted_attributes = []
            for name, value in list(attributes.items()):
                if isinstance(name, tuple):
                    new_name = NamespacedAttribute(*name)
                    del attributes[name]
                    attributes[new_name] = value

            self.soup.builder._replace_cdata_list_attribute_values(
                self.name, attributes)
            for name, value in list(attributes.items()):
                self.element[name] = value

            # The attributes may contain variables that need substitution.
            # Call set_up_substitutions manually.
            #
            # The Tag constructor called this method when the Tag was created,
            # but we just set/changed the attributes, so call it again.
            self.soup.builder.set_up_substitutions(self.element)
    attributes = property(getAttributes, setAttributes)

    def insertText(self, data, insertBefore=None):
        if insertBefore:
            text = TextNode(self.soup.new_string(data), self.soup)
            self.insertBefore(data, insertBefore)
        else:
            self.appendChild(data)

    def insertBefore(self, node, refNode):
        index = self.element.index(refNode.element)
        if (node.element.__class__ == NavigableString and self.element.contents
            and self.element.contents[index-1].__class__ == NavigableString):
            # (See comments in appendChild)
            old_node = self.element.contents[index-1]
            new_str = self.soup.new_string(old_node + node.element)
            old_node.replace_with(new_str)
        else:
            self.element.insert(index, node.element)
            node.parent = self

    def removeChild(self, node):
        node.element.extract()

    def reparentChildren(self, new_parent):
        """Move all of this tag's children into another tag."""
        # print "MOVE", self.element.contents
        # print "FROM", self.element
        # print "TO", new_parent.element
        element = self.element
        new_parent_element = new_parent.element
        # Determine what this tag's next_element will be once all the children
        # are removed.
        final_next_element = element.next_sibling

        new_parents_last_descendant = new_parent_element._last_descendant(False, False)
        if len(new_parent_element.contents) > 0:
            # The new parent already contains children. We will be
            # appending this tag's children to the end.
            new_parents_last_child = new_parent_element.contents[-1]
            new_parents_last_descendant_next_element = new_parents_last_descendant.next_element
        else:
            # The new parent contains no children.
            new_parents_last_child = None
            new_parents_last_descendant_next_element = new_parent_element.next_element

        to_append = element.contents
        append_after = new_parent_element.contents
        if len(to_append) > 0:
            # Set the first child's previous_element and previous_sibling
            # to elements within the new parent
            first_child = to_append[0]
            if new_parents_last_descendant:
                first_child.previous_element = new_parents_last_descendant
            else:
                first_child.previous_element = new_parent_element
            first_child.previous_sibling = new_parents_last_child
            if new_parents_last_descendant:
                new_parents_last_descendant.next_element = first_child
            else:
                new_parent_element.next_element = first_child
            if new_parents_last_child:
                new_parents_last_child.next_sibling = first_child

            # Fix the last child's next_element and next_sibling
            last_child = to_append[-1]
            last_child.next_element = new_parents_last_descendant_next_element
            if new_parents_last_descendant_next_element:
                new_parents_last_descendant_next_element.previous_element = last_child
            last_child.next_sibling = None

        for child in to_append:
            child.parent = new_parent_element
            new_parent_element.contents.append(child)

        # Now that this element has no children, change its .next_element.
        element.contents = []
        element.next_element = final_next_element

        # print "DONE WITH MOVE"
        # print "FROM", self.element
        # print "TO", new_parent_element

    def cloneNode(self):
        tag = self.soup.new_tag(self.element.name, self.namespace)
        node = Element(tag, self.soup, self.namespace)
        for key,value in self.attributes:
            node.attributes[key] = value
        return node

    def hasContent(self):
        return self.element.contents

    def getNameTuple(self):
        if self.namespace == None:
            return namespaces["html"], self.name
        else:
            return self.namespace, self.name

    nameTuple = property(getNameTuple)

class TextNode(Element):
    def __init__(self, element, soup):
        treebuilder_base.Node.__init__(self, None)
        self.element = element
        self.soup = soup

    def cloneNode(self):
        raise NotImplementedError
