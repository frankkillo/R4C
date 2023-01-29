from rest_framework import serializers

from .models import Robot

def valid_model_or_version(value: str):
    for i in range(len(value)):
        if not (48<=ord(value[i])<=57) and not (65<=ord(value[i])<=90):
            raise serializers.ValidationError("Invalid data!")
    

class RobotSerializer(serializers.ModelSerializer):
    serial = serializers.CharField(max_length=5, required=False)
    model = serializers.CharField(max_length=2, validators=[valid_model_or_version])
    version = serializers.CharField(max_length=2, validators=[valid_model_or_version])

    class Meta:
        model = Robot
        fields = [
            "id",
            "serial",
            "model",
            "version",
            "created",
        ]

    def validate(self, data):
        serial = data["model"]+"-"+data["version"]
        if not data.get("serial"):      
            data["serial"] = serial
        else:
            if data["serial"] != serial:
                raise serializers.ValidationError(f"Invalid serial! Not iqual {serial}")
        return data