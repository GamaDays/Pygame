# Example file showing a basic pygame "game loop"
import pygame
import pyaudio
import wave
import whisper

#Audio Setup

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "output.wav"

# pygame setup
pygame.init()
pygame.font.init() 
my_font = pygame.font.SysFont('Arial', 30)
text = "Hello, I am Truckie, your Virtual Assistant"
text_help = "Speaking..."
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Truckie - The Driving Companion')
clock = pygame.time.Clock()
running = True

Truckie_IMG = pygame.image.load('truckie.png')
Background_Color = pygame.Color("#ffdba5") 

pygame.display.set_icon(Truckie_IMG)

# recording setup
recording = False


#Openai Setup

import openai
openai.api_key = '' #Key removed for security reasons

def Call_GPT(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question},
        ],
    )

    # Extract and print the generated answer
    answer = response['choices'][0]['message']['content'].strip()
    return answer


# tts setup
import pyttsx3
VOICE_ID = 2
save_text = ""


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[VOICE_ID].id)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def print_screen():
    screen.fill(Background_Color)
    screen.blit(Truckie_IMG, ((SCREEN_WIDTH/2)-(Truckie_IMG.get_width()/2),5))
    text_surface = my_font.render(text, False, (0, 0, 0))
    screen.blit(text_surface, ((SCREEN_WIDTH * 0.5)-(text_surface.get_width()/2), (SCREEN_HEIGHT * 0.75)-(text_surface.get_height()/2)))
    text_1h = text_surface.get_height()/2
    text_surface = my_font.render(text_help, False, (0, 0, 0))
    screen.blit(text_surface, ((SCREEN_WIDTH * 0.5)-(text_surface.get_width()/2), (SCREEN_HEIGHT * 0.75)+text_1h+10 ))
    pygame.display.flip()


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if(recording == True):
                    recording = False
                    text_help = "Processing..."
                    print_screen()
                    stream.stop_stream()
                    stream.close()
                    p.terminate()

                    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(p.get_sample_size(FORMAT))
                    wf.setframerate(RATE)
                    wf.writeframes(b''.join(frames))
                    wf.close()
                    model = whisper.load_model("base")
                    result = model.transcribe(audio="./output.wav") #<---If this fails due to cant found file error install ffmpeg!
                    text = result["text"]
                elif (recording == False):
                    recording = True
                    screen.fill(Background_Color)
                    text_help = "Recording..."
                    print_screen()

                    p = pyaudio.PyAudio()

                    stream = p.open(format=FORMAT,
                                    channels=CHANNELS,
                                    rate=RATE,
                                    input=True,
                                    frames_per_buffer=CHUNK)

                    frames = []

    # fill the screen with a color to wipe away anything from last frame
    if recording==True:
        data = stream.read(CHUNK)
        frames.append(data)
    elif save_text!=text:
        text_help = "Speaking..."
    
    if text=="":
            text = "say: I couldn't understand you!"

    print_screen()

    if save_text!=text:
        text = Call_GPT(text)
        print_screen()
        speak(text)
        text_help = "Use space for Input"
        save_text = text
    clock.tick(60)  # limits FPS to 60

pygame.quit()