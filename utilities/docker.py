import docker

from django.conf import settings

client = docker.DockerClient(base_url=settings.DOCKER_URL)


def run_container(image, envs, command):
    c = client.containers.run(
        image=image,
        environment=envs,
        command=command,
        detach=True
    )
    return c.id

def check_status_container(container_id):
    container = client.containers.get(container_id)
    return container.status