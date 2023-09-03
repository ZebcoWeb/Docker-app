import docker

from django.conf import settings

client = docker.DockerClient(base_url=settings.DOCKER_URL)


def run_containers(image, envs, command, instance_count=1):
    instance_id = None
    for i in range(instance_count):
        c = client.containers.run(
            image=image,
            environment=envs,
            command=command,
            detach=True
        )
        if not instance_id:
            instance_id = c.id
    return instance_id

def check_status_container(container_id):
    container = client.containers.get(container_id)
    return container.status
    
