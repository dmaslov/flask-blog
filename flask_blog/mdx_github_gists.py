from markdown import Extension
from markdown.util import etree
from markdown.inlinepatterns import Pattern


class GitHubGistExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        RE = r'\[gist\](\w+)\[\/gist\]'
        gistPattern = GitHubGist(RE)
        md.inlinePatterns.add('github-gist', gistPattern, ">not_strong")


class GitHubGist(Pattern):
    def handleMatch(self, m):
        gistid_value = m.group(2).strip()
        if gistid_value:
            element = etree.Element('github-gist')
            element.set('gistid', gistid_value)
        else:
            element = ''

        return element


def makeExtension(configs=None):
    return GitHubGist(configs=configs)