import flet as ft
import pygame
import os
import asyncio
from mutagen.mp3 import MP3


class Song:
    def __init__(self, filename):
        self.filename = filename
        self.title = os.path.splitext(filename)[0]
        self.duracion = self.get_duration()
    
    def get_duration(self):
        audio = MP3(os.path.join(os.path.join("canciones", self.filename)))
        return audio.info.length


async def main(page:ft.Page):
    page.title = "Music Player"
    page.bgcolor = ft.Colors.BLUE_GREY_900
    page.padding = 20
    titulo = ft.Text("Reproductor de Música", size=30, color=ft.Colors.WHITE)
    pygame.mixer.init()
    playlist = [Song(f) for f in os.listdir("canciones") if f.endswith(".mp3")]
    
    def load_song():
        pygame.mixer.music.load(os.path.join("canciones",playlist[current_sonf_index].filename))
        

    def play_pause(e):
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

    def change_info(delta):
        nonlocal current_sonf_index
        current_sonf_index = (current_sonf_index + delta) % len(playlist)
        load_song()
        pygame.mixer.music.play()
        update_song_info()
        play_button.icon = "PAUSE"
        page.update()
    
    def update_song_info():
        song = playlist[current_sonf_index]
        sonf_info.value = f"{song.title}"
        duration.value = format_time(song.duracion)
        progress_bar.value = 0.0
        current_time_text.value = "00:00"
        page.update()
    
    def format_time(seconds):
        minutes , seconds = divmod(int(seconds), 60)
        return "{minutes:02d}:{seconds:02d}".format(minutes=minutes, seconds=seconds)

    async def update_progress_bar():
        while True:
            if pygame.mixer.music.get_busy():
                current_time = pygame.mixer.music.get_pos() / 1000
                progress_bar.value = current_time / playlist[current_sonf_index].duracion
                current_time_text.value = format_time(current_time)
                page.update()
            await asyncio.sleep(1)

    current_sonf_index = 0

    sonf_info = ft.Text(size=20, color=ft.Colors.WHITE)
    current_time_text = ft.Text(value="00:00",size=20, color=ft.Colors.WHITE60)
    duration = ft.Text(value="00:00",size=20, color=ft.Colors.WHITE60)


    progress_bar = ft.ProgressBar(value=0.0, width=300, color="white", bgcolor="red")


    play_button = ft.IconButton(icon="PLAY_ARROW",icon_color="white", on_click=play_pause)
    prevet_button = ft.IconButton(icon="SKIP_PREVIOUS",icon_color="white", on_click=lambda _: change_info(-1))
    next_button = ft.IconButton(icon="SKIP_NEXT",icon_color="white", on_click=lambda _: change_info(1))

    controls = ft.Row(
        controls=[prevet_button, play_button, next_button],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    fila_reproduccion = ft.Row(
        controls=[current_time_text, progress_bar, duration],
        alignment=ft.MainAxisAlignment.CENTER,
    )


    columna = ft.Column([sonf_info, fila_reproduccion,controls],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20)
    page.add(
        columna
        )
    if playlist:
        load_song()
        update_song_info()
        page.update()
        await update_progress_bar()
    else:
        sonf_info.value = "No hay canciones"
        page.update()

ft.app(target=main)