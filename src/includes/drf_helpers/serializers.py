from rest_framework import serializers

from src.includes import utils


class UserHistorySerializer(serializers.Serializer):
    def _get_user_details(self):
        return utils.model_to_dict(self.context["request"].user)

    def save(self, **kwargs):
        if self.instance is None:
            self.validated_data["created_by"] = self._get_user_details()
        else:
            self.validated_data["updated_by"] = self._get_user_details()
        return super().save(**kwargs)
