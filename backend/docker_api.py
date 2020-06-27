import docker

if __name__ == '__main__':
    client = docker.DockerClient(base_url='tcp://localhost:2375')

    for c in client.services.list():
        print(c.name)
