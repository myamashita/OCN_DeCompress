import os
import zlib
import sublime
import sublime_api
import sublime_plugin

cache_path = sublime_api.cache_path()
path_compressed = cache_path[:-5] + 'OCN_compressed\\'
path_uncompressed = cache_path[:-5] + 'OCN_uncompressed\\'

class CompressViewCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        filename = self.view.name() if self.view.name() != '' else self.view.file_name()
        name = os.path.basename(filename)
        file = sublime_api.view_cached_substr(self.view.view_id,
                                              0, self.view.size())
        file = file.replace('\n', '\r\n')
        file = file.encode('cp1252', 'ignore')
        compress_name = path_compressed + name + '_gz'
        filegz = open(compress_name, 'wb')
        textcompre = zlib.compress(file)
        filegz.write(textcompre)
        filegz.close()
        if self.view.name() != '':
            self.view.erase(edit, sublime.Region(0, self.view.size()))
            self.view.close()
        else:
            self.view.run_command('save')
            self.view.close()

class DecompressFilesCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        filename = view.file_name()
        FileNames = askopenfilenames(filetypes=[("ADC", "*.adc"),
                                     ("FSI", "*.fsi"),
                                     ("MIR", "*.mir"),
                                     ("YNG", "*.yng")])
        print(FileNames)
