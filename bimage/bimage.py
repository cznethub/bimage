#! /usr/bin/env python

"""
bimage.py, master program that brings all the modules in the bimage package together
"""

from bimage.build_image import build_image
from bimage.clone_repo import clone_repo
from bimage.register_image import register_image
from bimage.exceptions import BimageException


def bimage(github_org: str, repo_name: str, branch_or_tag: str, local_image_name: str,
           local_image_tag: str, path_to_dockerfile: str, target_image_name: str,
           target_image_tag: str, region: str, gcloud_project_id: str, repository_name: str,
           path_to_local_environment: str = "", path_to_remote_environment: str = "",
           platform: str = ""):
    """The bimage function, that brings together cloning a repository, building an image, and
    registering that image to the google cloud artifact registry. Given the bash shell
    is authenticated with google cloud before running the program.

    Args:
        github_org (str): The organization hosting the github repository (cznet)
        repo_name (str): The name of the repository we are trying to clone
        branch_or_tag (str): The branch or tag we are trying to check out to
        local_image_name (str): Choose the name of the image we create locally from the
              Dockerfile
        local_image_tag (str): The tag of the image we create locally from the
              Dockerfile (v1, 1.0.1, version2.0)
        path_to_dockerfile (str): The path to the docker file from the repository
              we cloned, usually "."
        targetImageName (str): The target image name, i.e. the name of the image
              we store in the google cloud artifact registry
        targetImageTag (str): The target image tag, i.e. the tag of the image we
              store in the google cloud artifact registry (v1, 1.0.1, version2.0)
        region (str): Region the image will be stored in the google cloud (e.g.
              us-east1, us, eu)
        gcloudProjectId (str): The project id from which the image will be stored
              under in a google artifact registry
        repositoryName (str): The name of the google cloud artifact registry that
              holds docker images
        path_to_local_environment (str, optional): The path to a local environment
                file with secrets not to be seen on github (e.g usr/home/bimage/.env).
                Defaults to "".
        path_to_remote_environment (str, optional): The path to the dummy environment
                files found on github (e.g usr/home/bimage/.env). Defaults to "".
        platform (str, optional): The target platform of the image in the form of
              os[/arch[/variant]]
    """
    try:
        clone_repo(github_org, repo_name, branch_or_tag)
        build_image(f"{local_image_name}:{local_image_tag}", path_to_dockerfile,
                    path_to_local_environment, path_to_remote_environment, platform)
        response = register_image(local_image_name, local_image_tag, target_image_name,
                                  target_image_tag, region, gcloud_project_id, repository_name)
    except Exception as exc:
        raise BimageException from exc

    return response
