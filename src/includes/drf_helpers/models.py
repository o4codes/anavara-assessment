import uuid

from django.db import models


class UUIDPrimaryKeyMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class DateHistoryMixin(models.Model):
    """
    Tracks date of creation and modification
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseValidateMixin(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self._run_init()
        self._run_validations()
        return super().save(*args, **kwargs)

    def _run_validations(self):
        if self._state.adding:
            self._pre_save_validate()
        else:
            self._post_save_validate()

    def _run_init(self):
        if self._state.adding:
            self._pre_save_init()
        else:
            self._post_save_init()

    def _pre_save_validate(self):
        ...

    def _post_save_validate(self):
        ...

    def _pre_save_init(self):
        ...

    def _post_save_init(self):
        ...
