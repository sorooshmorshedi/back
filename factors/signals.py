from sanads.sanads.models import clearSanad


def clearFactorSanad(sender, instance, created=None, **kwargs):
    clearSanad(instance.sanad)
