import os
import zlib
import sublime
import sublime_api
import sublime_plugin

DEFAULT_PATH = """{// Define your custom folder here
        "Compress": " ",
        "Uncompress": " ",
}"""


def get_setting(key, default=None):
    settings = sublime.load_settings('OCN_DeCompress.sublime-settings')
    os_specific_settings = {}
    return os_specific_settings.get(key, settings.get(key, default))


class CompressViewCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        compress = os.path.join(sublime.packages_path(),
                                'OCN_DeCompress\\OCN_Compressed\\')
        if not os.path.exists(os.path.dirname(compress)):
            os.makedirs(compress)

        package_dir = get_setting('Compress')
        if not os.path.exists(package_dir):
            package_dir = os.path.join(
                sublime.packages_path(), 'OCN_DeCompress\\OCN_Compressed\\')
        filename = self.view.name() if self.view.name() != '' else self.view.file_name()
        name = os.path.basename(filename)
        file = sublime_api.view_cached_substr(self.view.view_id,
                                              0, self.view.size())
        file = file.replace('\n', '\r\n')
        file = file.encode('cp1252', 'ignore')
        compress_name = package_dir + name + '_gz'
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


class DecompressViewCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        uncompress = os.path.join(
            sublime.packages_path(), 'OCN_DeCompress\\OCN_Uncompressed\\')
        if not os.path.exists(os.path.dirname(uncompress)):
            os.makedirs(uncompress)
        package_dir = get_setting('Uncompress')
        if not os.path.exists(package_dir):
            package_dir = os.path.join(
                sublime.packages_path(), 'OCN_DeCompress\\OCN_Uncompressed\\')
        filename = self.view.name() if self.view.name() != '' else self.view.file_name()
        name = os.path.basename(filename)
        file = sublime_api.view_cached_substr(self.view.view_id,
                                              0, self.view.size())
        decompress_name = package_dir + name
        file_ = open(decompress_name, 'w')
        file_.write(file)
        file_.close()
        if self.view.name() != '':
            self.view.erase(edit, sublime.Region(0, self.view.size()))
            self.view.close()
        else:
            self.view.close()


class EditFilepathUserCommand(sublime_plugin.WindowCommand):

    def run(self):
        filepath = os.path.join(sublime.packages_path(),
                                'User\OCN_DeCompress.sublime-settings')
        if not os.path.isfile(filepath):
            with open(filepath, 'w') as f:
                f.write(DEFAULT_PATH)

        # Open the settings file
        self.window.run_command('open_file', {
            'file': filepath,
        })
