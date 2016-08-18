import markdown

BLOCKQUOTE_RE = r'(~{2})(.+?)\2'


class QuoteExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('blockquote', markdown.inlinepatterns.SimpleTagPattern(BLOCKQUOTE_RE, 'blockquote'), '>strong')


def makeExtension(configs=None):
    return QuoteExtension(configs = configs)