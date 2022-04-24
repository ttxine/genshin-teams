import os
import datetime


def get_avatar_upload_path() -> str:
    directory = 'media/img/users/avatars/{}/'.format(
        str(int(datetime.utcnow().strftime('%d%m%Y'))),
    )
    os.makedirs(directory, exist_ok=True)
    return directory


def get_weapon_image_upload_path(name: str) -> str:
    directory = 'media/img/planner/weapons/{}/'.format(name)
    os.makedirs(directory, exist_ok=True)
    return directory


def get_artifact_upload_path(name: str) -> str:
    directory = 'media/img/planner/artifacts/{}/'.format(name)
    os.makedirs(directory, exist_ok=True)
    return directory


def get_character_upload_path(name: str) -> str:
    directory = 'media/img/planner/characters/{}/'.format(name)
    os.makedirs(directory, exist_ok=True)
    return directory
