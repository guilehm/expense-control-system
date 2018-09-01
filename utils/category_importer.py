import csv
import logging

from core.models import Category


logger = logging.getLogger('controller')

CATEGORY_HEADER = ['title', 'slug', 'description']


def process_csv_category_file(instance):

    reader = csv.DictReader(instance.file.read().decode('utf-8').splitlines())
    header_ = reader.fieldnames

    if CATEGORY_HEADER != header_:
        instance.error_detail = 'Cabeçalho fora do padrão'
        instance.save()
        return

    logger.info(
        'Creating Categories for user "{user}".'.format(user=instance.owner.username)
    )

    for row in reader:
        title = row['title']
        slug = row['slug']
        description = row['description']

        category, created = Category.objects.get_or_create(
            owner=instance.owner,
            title=title,
            slug=slug,
            description=description
        )
        if created:
            logger.info(
                'Category #{id} {title} created for "{user}".'.format(
                    id=category.id,
                    title=category.title,
                    user=instance.owner.username,
                )
            )
        else:
            logger.warning(
                'Category #{title} already existed for user "{user}".'.format(
                    title=category.title,
                    user=instance.owner.username,
                )
            )
