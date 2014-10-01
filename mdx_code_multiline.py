from markdown import Extension
from markdown.util import etree
from markdown.inlinepatterns import Pattern

RE = r'\[code\](.*?)\[\/code\]'


class MultilineCodeExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        element = NestedElements(RE)
        md.inlinePatterns.add('pre', element, '<not_strong')


class NestedElements(Pattern):
    def handleMatch(self, m):
        el1 = etree.Element('pre')
        el2 = etree.SubElement(el1, 'cite')
        el2.text = m.group(2).strip()
        return el1


def makeExtension(configs=None):
    return MultilineCodeExtension(configs=configs)