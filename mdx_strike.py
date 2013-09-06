import markdown

STRIKE_RE = r'(-{2})(.+?)\2'


class StrikeExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('strike', markdown.inlinepatterns.SimpleTagPattern(STRIKE_RE, 'strike'), '>strong')


def makeExtension(configs=None):
    return StrikeExtension(configs = configs)