import flet as ft
import pygame
import os
from mutagen.mp3 import MP3
import asyncio



class Song():
    def __init__(self, filename):
        self.filename = filename
        self.title = os.path.splitext(filename)[0]
        self.duration = self.get_duration()

    def get_duration(self):
        audio = MP3(os.path.join("songs", self.filename))
        return audio.info.length

async def main(page:ft.Page):
    page.title = "Music Player"
    page.padding = 20

    ## Music Player
    pygame.mixer.init()
    pygame.display.init()
    playlist = [Song(file) for file in os.listdir("songs") if file.endswith(".mp3")]
    current_song_index = 0

    def load_song():
        pygame.mixer.music.load(os.path.join("songs",playlist[current_song_index].filename))
        

    def play_pause(e):
        # print(pygame.mixer.music.get_busy())
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            play_button.icon = "PLAY_ARROW"
        else:
            if pygame.mixer.music.get_pos() == -1:
                load_song()
                pygame.mixer.music.play()
            else:
                pygame.mixer.music.unpause()
            play_button.icon = "PAUSE"
        page.update()

    def update_song_info():
        song = playlist[current_song_index]
        song_title.value = song.title
        duration.value = format_time(song.duration)
        progress_bar.value = 0.0
        current_time_text.value = "00:00"
        page.update()

    def change_song_info(e):
        nonlocal current_song_index
        current_song_index = (current_song_index + e) % len(playlist)
        load_song()
        pygame.mixer.music.play()
        update_song_info()
        play_button.icon = "PAUSE"
        page.update()
    
    def format_time(seconds):
        minutes , seconds = divmod(int(seconds), 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    async def update_progress_bar():
        while True:
            if pygame.mixer.music.get_busy():
                current_time = pygame.mixer.music.get_pos() / 1000
                progress_bar.value = current_time / playlist[current_song_index].duration
                current_time_text.value = format_time(current_time)
                page.update()
            else:
                if auto_play_checkbox.value and pygame.mixer.music.get_pos() == -1:
                    change_song_info(1)
            await asyncio.sleep(1)

    def set_volume(e):
        pygame.mixer.music.set_volume(volumen_slider.value / 100)
        page.update()

    song_title = ft.Text( size=30 , weight=ft.FontWeight.W_700)
    play_button = ft.IconButton(icon="PLAY_ARROW", on_click= lambda e: play_pause(e))
    prevet_button = ft.IconButton(icon="SKIP_PREVIOUS", on_click= lambda _: change_song_info(-1))
    next_button = ft.IconButton(icon="SKIP_NEXT", on_click= lambda _: change_song_info(1))


    progress_bar = ft.ProgressBar(value=0.0, width=300, bgcolor="red")
    duration = ft.Text(value="0:00", size=20)
    current_time_text = ft.Text(value="0:00", size=20)
    auto_play_checkbox = ft.CupertinoSwitch(label="Auto Play", value=False)
    volumen_slider = ft.Slider(min=0, max=100, value=50, width=300 , on_change=set_volume)

    list_controls = ft.Row(
        controls= [prevet_button, play_button, next_button, auto_play_checkbox],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    info_reproduction = ft.Row(
        controls=[current_time_text,progress_bar, duration],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    
    columna = ft.Column(
        controls=[song_title,info_reproduction, list_controls],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=40
    )
    volume = ft.Row(
        controls=[volumen_slider],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    page.add(columna,volume)

    if playlist:
        update_song_info()
        page.update()
        await update_progress_bar()

ft.app(target=main)