from markdown import Extension
from markdown.util import etree
from markdown.inlinepatterns import Pattern


class GitHubGistExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        RE = r'\[gist\](\w+\W+.+)\[\/gist\]'
        gistPattern = GitHubGist(RE)
        md.inlinePatterns.add('script', gistPattern, ">not_strong")


class GitHubGist(Pattern):
    def handleMatch(self, m):
        src = m.group(2).strip()
        if src:
            script = etree.Element('script')
            script.set('src', src)
        else:
            script = ''
        return script


def makeExtension(configs=None):
    return GitHubGist(configs=configs)