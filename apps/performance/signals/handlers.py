from django.db.models.signals import post_save
from django.dispatch import receiver
from analysis.benchmark.utils import create_benchmark
from performance.models import Performance


@receiver(post_save, sender=Performance)
def post_performance_handler(sender, instance=None, created=False, **kwargs):
    success = create_benchmark(sender, instance, created)
