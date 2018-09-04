import csv

from slugify import slugify

from core.models import CSV, Tag

TAG_HEADER = ['title', 'slug']


def process_csv_tag_file(instance_id):

    instance = CSV.objects.get(id=instance_id)
    reader = csv.DictReader(instance.file.read().decode('utf-8').splitlines())
    header_ = reader.fieldnames

    if TAG_HEADER != header_:
        instance.error_detail = "Cabeçalho fora do padrão"
        instance.save()
        return

    for row in reader:
        title = row['title']
        slug = row['slug']

        slug = slugify(title) if slug == "" else slugify(slug)

        tag, created = Tag.objects.get_or_create(
            owner=instance.owner,
            title=title
        )

        if created:
            tag.slug = slug
            tag.save()
        else:
            if tag.slug != slug:
                tag.slug = slug
            tag.save()
