import os
from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, Form

from api import session, config
from api.schemas import container
from api.models.container import Container

router = APIRouter()


@router.get("/", response_model=List[container.Container])
def get_all_containers(db: Session = Depends(session)):
    """ Get a list of containers """

    return db.query(Container).all()


@router.post("/")
async def create_container(file: bytes = File(...), filename: str = Form(...), description: str = Form(...), db: session = Depends(session)):
    print('in here')
    # print(file)
    # print(filename)
    # print(description)

    save_path = 'C:\\Users\\kevin\\Desktop\\picom\\backend\\user_files'
    # TODO: this gave me a "permission denied error" when trying to write to file
    # with open(save_path) as f:
    #     f.write(file)
    completeFile = os.path.join(save_path, filename)
    file1 = open(completeFile, "wb")
    file1.write(file)
    file1.close()

    new_container = container.ContainerCreate(user_id=1, name=filename, description=description,
                                              dockerfile_path=completeFile, is_input_container=False, is_output_container=False)
    print(new_container)
    db_container = Container(**new_container.dict())
    db_container.save(db)

    return db_container
    # db_assignment = db.query(models.Assignment).get(assignment_id)
    # if not os.path.exists(assignment_folder := db_assignment.path):
    #     os.mkdir(assignment_folder)
    # with open('tmp', 'wb') as f:
    #     f.write(file)
    # shutil.unpack_archive('tmp', extract_dir=assignment_folder, format='zip')

# @router.post("/", response_model=container.Container)
# def create_container(container: container.ContainerCreate, db: Session = Depends(session)):
    """ Allows the creation of a new container """

    # dockerfile_path = os.path.join(container.get_path(), 'dockerfile')
    # with open(dockerfile_path) as fp:
    #     fp.write(dockerfile)
    # print(container)
    # print(container.dockerfile_path)
    # test = 'blah'
    # container.dockerfile_path = test
    # # print(container.dockerfile_path)

    # save_path = 'C:\\Users\\kevin\Desktop\\picom\\backend\\user_files'
    # completeFile = os.path.join(save_path, 'DockerfileTest')

    # file1 = open(completeFile, "w")
    # file1.write(container.dockerfile)
    # file1.close()

    # with open(completeFile) as fp:
    #     fp.write(container.dockerfile)
    #     fp.close()

    # dockerfile_path = os.path.join('backend/user_files', 'dockerfile')
    # print(dockerfile_path)
    # with open(dockerfile_path) as fp:
    #     fp.write(container.dockerfile)

    # db_container = Container(**container.dict())
    # db_container.save(db)

    # return db_container


@router.get("/{container_id}", response_model=container.Container)
def get_container(container_id: int, db: Session = Depends(session)):
    return db.query(Container).get(container_id)


@router.delete("/{container_id}", response_model=container.Container)
def delete_container(container_id: int, db: Session = Depends(session)):
    return db.query(Container).get(container_id).delete(db)
