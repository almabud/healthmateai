import json

import openai
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from patient.models import Patient
from patient.serializers import PatientSerializer
from text_summarizer.models import SummarizeRequest


class TextSummarizerSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(allow_null=True, read_only=True)

    class Meta:
        model = SummarizeRequest
        fields = (
            'id',
            'conversation',
            'summarize',
            'created_at',
            'updated_at',
            'patient'
        )
        read_only_fields = fields


class PatientTextSummarizeSerializer(TextSummarizerSerializer):
    class Meta:
        model = SummarizeRequest
        fields = (
            'id',
            'conversation',
            'summarize',
            'created_at',
            'updated_at'
        )
        read_only_fields = fields


class CreateTextSummarizerSerializer(serializers.ModelSerializer):
    patient = serializers.IntegerField(write_only=True)

    class Meta:
        model = SummarizeRequest
        fields = ('conversation', 'patient')

    def validate_patient(self, patient):
        try:
            return Patient.objects.get(id=patient)
        except Patient.DoesNotExist:
            raise ValidationError('Invalid patient.')

    def create(self, validated_data):
        convs = validated_data['conversation']
        messages = [
            {
                'role': 'system',
                'content': "You are a doctor's assistant. List down only the "
                           "patient's problems and any suggested tests "
                           "by the doctor. Moreover ignore the medication."
            },
            {
                'role': 'user',
                'content': json.dumps(convs)
            }
        ]
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
            max_tokens=100,
            temperature=0.7
        )

        if response and response.choices:
            validated_data['summarize'] = response.choices[0].message['content']

            return super().create(validated_data)
        else:
            raise ValidationError('Error occurred during API request.')
