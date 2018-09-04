import csv
import logging

from core.models import CSV, Tag


TAG_HEADER = ['title', 'slug']


def process_csv_tag_file(instance_id):

    instance = CSV.objects.get(id=instance_id)
    reader = csv.DictReader(instance.file.read().decode('utf-8').splitlines())
    header_ = reader.fieldnames
