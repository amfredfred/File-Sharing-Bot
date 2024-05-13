from html2image import Html2Image as HTMLTOIMAGE

direct = __path__[0]


class HTML2Image(HTMLTOIMAGE):

    def screenshot(
        self,
        html_str=[],
        html_file=[],
        css_str=[],
        css_file=[],
        other_file=[],
        url=[],
        save_as="screenshot.png",
        size=[],
    ):
        return super().screenshot(
            html_str, html_file, css_str, css_file, other_file, url, save_as, size
        )

    def make_qa_screenshot(self, content: str):
        with open(f"{direct}\\html\\post_item.html") as post_item_html:
            template = post_item_html.read()
            with open(f"{direct}\\html\\post_item.css") as post_item_css:
                item_css = post_item_css.read()
                # html_string = html_string.replace("_data_analyze_string_", "?")
                html_string = template.replace("_content_", content)
                html_with_css = f"{html_string}<style>{item_css}</style>"
                screen = self.screenshot(
                    html_str=html_with_css,
                    size=(3840,2160),
                )
                return screen
