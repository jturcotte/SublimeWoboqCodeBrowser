import sublime, sublime_plugin
import http.client
import webbrowser

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
        entries = sublime.decode_value(c.getresponse().read().decode())
        c.close()

        self.window.show_quick_panel(
            [e['name'] for e in entries],
            lambda x: webbrowser.open(entries[x]['url']) if x > -1 else sublime.status_message("Unable to find " + symbol))
