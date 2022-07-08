import os
from pytube import Playlist, YouTube
import pathlib


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = int(bytes_downloaded / total_size * 100)
    print(f'\rЗагружено: {percentage_of_completion}%', end='')


url = input('Введите URL плейлиста или видео: ')
you_tube_instance = Playlist(url) if 'playlist' in url else YouTube(url)

current_dir = pathlib.Path().resolve()
DOWNLOAD_DIR = os.path.join(current_dir, you_tube_instance.title)

print(DOWNLOAD_DIR)


def download_video(video_one):
    is_download_video = False
    video_one.check_availability()
    print(f'Загрузка видео {video_one.title}')
    while not is_download_video:
        try:
            video_one.register_on_progress_callback(on_progress)
            videoStream = video_one.streams.filter(progressive=True, subtype="mp4").order_by("resolution").last()
            videoStream.download(output_path=DOWNLOAD_DIR)
            is_download_video = True
        except:
            print('Загрузка видео не удалась. Пытаемся ещё разок', end='')
        finally:
            print('')


if 'playlist' in url:
    print(f'Всего видео: {len(you_tube_instance.video_urls)}')
    for video in you_tube_instance.videos:
        download_video(video)
else:
    download_video(you_tube_instance)
print('Загрузка видео завершена')
