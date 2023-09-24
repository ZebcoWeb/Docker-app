import docker

from django.conf import settings



class DockerHandler:
    def __init__(self, base_url=settings.DOCKER_URL):
        self.client = docker.DockerClient(base_url=base_url)

    def is_running(self, container_id):
        c = self.client.containers.get(container_id)
        return c.status == "running"

    def run_app(self, image, envs, command):
        c = self.client.containers.run(
            image=image,
            environment=envs,
            command=command,
            detach=True
        )
        return c.id
    
    def start_app(self, container_id):
        c = self.client.containers.get(container_id)
        c.start()
        return
    
    
    def stop_app(self, container_id):
        c = self.client.containers.get(container_id)
        c.stop()
        return
    
    def restart_app(self, container_id):
        c = self.client.containers.get(container_id)
        c.restart()
        return
    
    def remove_app(self, container_id):
        c = self.client.containers.get(container_id)
        c.remove(force=True)
        return

    def status_app(self, container_id):
        c = self.client.containers.get(container_id)
        return c.status
    
    def logs_app_event(self, container_id):
        c = self.client.containers.get(container_id)
        return c.logs(stream=True)
    
    def stats_app_event(self, container_id):
        c = self.client.containers.get(container_id)
        return c.stats(stream=True)