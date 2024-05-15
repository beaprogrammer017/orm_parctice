from quickstart.models import Entry, Blog,Author
from rest_framework import serializers
from rest_framework import generics


class EntrySerializer(serializers.ModelSerializer):
    num_authors = serializers.IntegerField()
    class Meta:
        model = Entry
        fields=['id','headline', 'num_authors']
        # fields = '__all__'


class BlogListSerializer(serializers.ModelSerializer):
    # num_entries = serializers.IntegerField()
    # tagline = serializers.CharField()
    class Meta:
        model = Blog
        # fields = '__all__'
        # fields = ['id', 'name', 'num_entries']
        fields = ['name']


class AutherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):
    num_entries = serializers.IntegerField(source='entry_count', read_only=True)  # Define a custom field to represent entry count

    class Meta:
        model = Blog
        fields = ['name', 'num_entries']        