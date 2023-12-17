import browser
import html_parser.html_parser as html_parser
import html_parser.html_tree_builder as html_tree_builder

# browser = browser.Browser()
# browser.to_website("https://browser.engineering/examples/xiyouji.html")
# browser.run()


parser = html_parser.HtmlParser()


html_src = open("test.html").read()
tokens = parser.parse(html_src)

print("Tokens:")
for token in tokens:
    print(" ",token)

print()
print("Tree:")

html_builder = html_tree_builder.HtmlTreeBuilder()
tree = html_builder.build(tokens)
html_builder.print()