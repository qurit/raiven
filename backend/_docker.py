import docker

from api import config
client = docker.from_env()


if __name__ == '__main__':
    volumes = {
        'C:\\Users\\Adam\\Programming\\picom\\examples\\input': {'bind': config.PICOM_INPUT_DIR, 'mode': 'ro'},
        'C:\\Users\\Adam\\Programming\\picom\\examples\\output': {'bind': config.PICOM_OUTPUT_DIR, 'mode': 'rw'}
    }

    res = client.containers.run('picom_example_container', detach=True, volumes=volumes)
    print(res.status)
    print(res.wait())
    res.reload()
    print(res.status)
    print(res.logs())