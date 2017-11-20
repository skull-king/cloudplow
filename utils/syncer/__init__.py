import logging

from .scaleway import Scaleway

log = logging.getLogger("syncer")

SERVICES = {
    'scaleway': Scaleway
}


class Syncer:
    def __init__(self, config):
        self.config = config
        self.services = []

    def load(self, **kwargs):
        # validate required keywords were supplied
        if 'service' not in kwargs:
            log.error("You must specify a service to load with the service parameter")
            return False
        elif kwargs['service'] not in SERVICES:
            log.error("You specified an invalid service to load: %s", kwargs['service'])
            return False

        if 'sync_from' not in kwargs or 'sync_to' not in kwargs:
            log.error("You must specify a sync_form and sync_to in your configuration")
            return False

        try:
            # retrieve remotes config for sync_from and sync_to
            sync_from_config = self.config['remotes'][kwargs['sync_from']]
            sync_to_config = self.config['remotes'][kwargs['sync_to']]

            # clean kwargs before initializing the service
            chosen_service = SERVICES[kwargs['service']]
            del kwargs['service']
            del kwargs['sync_from']
            del kwargs['sync_to']

            # load service
            service = chosen_service(sync_from_config, sync_to_config, **kwargs)
            self.services.append(service)

        except Exception:
            log.exception("Exception while loading service, kwargs=%r: ", kwargs)

    """
        Commands below take 1 keyword parameter (service).
    """

    def startup(self, **kwargs):
        if 'service' not in kwargs:
            log.error("You must specify a service to startup")
            return False

        try:
            chosen_service = kwargs['service']
            for syncer in self.services:
                if chosen_service and syncer.NAME.lower() != chosen_service:
                    continue
                return syncer.startup()
        except Exception:
            log.exception("Exception starting instance kwargs=%r: ", kwargs)

    def setup(self, **kwargs):
        pass

    def destroy(self, **kwargs):
        pass

    def sync(self, **kwargs):
        pass
