import csv
import logging

from celery import shared_task
from slugify import slugify

from core.models import CSV, Category

logger = logging.getLogger('controller')

CATEGORY_HEADER = ['title', 'slug', 'description']


@shared_task
def process_csv_category_file(instance_id):

    instance = CSV.objects.get(id=instance_id)
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

        slug = slugify(title) if slug == "" else slugify(slug)

        category, created = Category.objects.get_or_create(
            owner=instance.owner,
            title=title,
        )
        if created:
            category.slug = slug
            category.description = description
            category.save()
            logger.info(
                'Category #{id} {title} created for "{user}".'.format(
                    id=category.id,
                    title=category.title,
                    user=instance.owner.username,
                )
            )
        else:
            logger.warning(
                'Category #{id} {title} already existed for user "{user}".'.format(
                    id=category.id,
                    title=category.title,
                    user=instance.owner.username,
                )
            )
            if category.slug != slug:
                logger.info(
                    'Updating category #{id} {title} slug from "{old_slug}" to "{new_slug}".'.format(
                        id=category.id,
                        title=category.title,
                        old_slug=category.slug,
                        new_slug=slug,
                    )
                )
            category.slug = slug
            if category.description != description:
                logger.info(
                    'Updating category #{id} {title} description '
                    'from "{old_description}" to "{new_description}".'.format(
                        id=category.id,
                        title=category.title,
                        old_description=category.description,
                        new_description=description,
                    )
                )
            category.description = description
            category.save()
