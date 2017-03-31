import zlib
import os
import sublime
import sublime_plugin
import sublime_api

cache_path = sublime_api.cache_path()
path_compressed = cache_path[:-5] + 'OCN_compressed\\'
path_uncompressed = cache_path[:-5] + 'OCN_uncompressed\\'

class CompressViewCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        filename = self.view.name()
        name = os.path.basename(filename)
        self.view.set_encoding('Western (Windows 1252)')
        file = sublime_api.view_cached_substr(self.view.view_id, 
                                              0, self.view.size())
        file = file.replace('\n', '\r\n')
        file = file.encode('cp1252', 'ignore')
        compress_name = path_compressed + name + '_gz'
        filegz = open(compress_name, 'wb')
        textcompre = zlib.compress(file)
        filegz.write(textcompre)
        filegz.close()
        self.view.erase(edit, sublime.Region(0, self.view.size()))
        self.view.close()

class DecompressFilesCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        FileNames = askopenfilenames(filetypes=[("ADC", "*.adc"),
                                     ("FSI", "*.fsi"),
                                     ("MIR", "*.mir"),
                                     ("YNG", "*.yng")])
        print(FileNames)
