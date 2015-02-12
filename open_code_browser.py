import sublime, sublime_plugin
import http.client
import webbrowser
import urllib.parse

class OpenCodeBrowser(sublime_plugin.WindowCommand):

    def run(self):
        orig_sel = None
        v = self.window.active_view()
        if v:
            orig_sel = [r for r in v.sel()]

        pt = v.sel()[0]
        symbol = v.substr(v.word(pt))

        c = http.client.HTTPConnection("code.woboq.org")
        c.request("GET", "/api/fn/" + symbol)
        r = c.getresponse()
        if r.status != 200:
            c.close()
            sublime.status_message("Error querying server: " + str(r.status) + " " + r.reason)
            return

        entries = sublime.decode_value(r.read().decode())
        c.close()

        self.window.show_quick_panel(
            [[e['name'], urllib.parse.urlparse(e['url']).path[1:-5]] for e in entries],
            lambda x: webbrowser.open(entries[x]['url']) if x > -1 else sublime.status_message("Unable to find " + symbol))
