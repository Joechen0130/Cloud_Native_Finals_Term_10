
class FileRouter:
    file_db = "files"
    default_db = "default"

    def db_for_read(self, model, **hints):
        model_name = model._meta.model_name
        if model_name == 'Post':
            return self.file_db
        else:
            return None

    def db_for_write(self, model, **hints):
        model_name = model._meta.model_name
        if model_name == 'Post':
            return 'files'
        else:
            return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name == 'Post':
            return db == 'files'
        else:
            return db == 'default'
