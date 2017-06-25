from kivy.lang import Builder


class ScriptLoader:
    def bulk_load(self, glob):
        for file in glob:
            Builder.load_file(file)
        Builder.sync()