from flask import Flask, request, render_template, request, send_file
from flask_cors import CORS
from pydub import AudioSegment

app = Flask(__name__, template_folder="templates")
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

# Speed up audio
@app.route('/speed')
def speed():
    return render_template('speed.html')

@app.route('/speeden', methods=['POST'])
def speeden():
    if 'audioFile' not in request.files:
        return 'No file part'

    file = request.files['audioFile']

    if file.filename == '':
        return 'No selected file'

    speed = float(request.form['speed'])

    if file:
        audio = AudioSegment.from_file(file)
        if speed > 1:
            sped_up_audio = audio.speedup(playback_speed=speed)
        else:
            sped_up_audio = audio.speedup(playback_speed=0.25)

        sped_up_audio.export('sped_audio.mp3', format='mp3')
        return send_file('sped_audio.mp3', as_attachment=True)

# Merge Audio
@app.route('/merge')
def merge():
    return render_template('merge.html')

@app.route('/merge_audio', methods=['POST'])
def merge_audio():
    print("yes")
    if 'audioFile1' not in request.files or 'audioFile2' not in request.files:
        return 'No file part'

    file1 = request.files['audioFile1']
    file2 = request.files['audioFile2']

    if file1.filename == '' or file2.filename == '':
        return 'No selected file'

    audio1 = AudioSegment.from_file(file1)
    audio2 = AudioSegment.from_file(file2)

    combined_audio = audio1 + audio2
    combined_audio.export('merged_audio.mp3', format='mp3')
    return send_file('merged_audio.mp3', as_attachment=True)


# Volumize Audio
@app.route('/volumize')
def volumize():
    return render_template('volumize.html')

@app.route('/volumize_audio', methods=['POST'])
def volumize_audio():
    print("yes")
    if 'audioFile' not in request.files:
        return 'No file part'

    file = request.files['audioFile']

    if file.filename == '':
        return 'No selected file'

    volume = int(request.form['volume'])

    if file:
        audio = AudioSegment.from_file(file)
        volumized_audio = audio + volume
        volumized_audio.export('volumized_audio.mp3', format='mp3')
        return send_file('volumized_audio.mp3', as_attachment=True)
    
# Reverse Audio
@app.route('/reverse')
def reverse():
    return render_template('reverse.html')

@app.route('/reverse_audio', methods=['POST'])
def reverse_audio():
    print("yes")
    if 'audioFile' not in request.files:
        return 'No file part'

    file = request.files['audioFile']

    if file.filename == '':
        return 'No selected file'

    if file:
        audio = AudioSegment.from_file(file)
        reversed_audio = audio.reverse()
        reversed_audio.export('reversed_audio.mp3', format='mp3')
        return send_file('reversed_audio.mp3', as_attachment=True)

# Trim Audio
@app.route('/trim')
def trim():
    return render_template('trim.html')

@app.route('/trim_audio', methods=['POST'])
def trim_audio():
    print("yes")
    if 'audioFile' not in request.files:
        return 'No file part'

    file = request.files['audioFile']

    if file.filename == '':
        return 'No selected file'

    start_time = int(request.form['start_time'])
    end_time = int(request.form['end_time'])

    if file:
        audio = AudioSegment.from_file(file)
        trimmed_audio = audio[start_time*1000:end_time*1000]
        trimmed_audio.export('trimmed_audio.mp3', format='mp3')
        return send_file('trimmed_audio.mp3', as_attachment=True)

# Pitch Shift Audio
@app.route('/pitch')
def pitch():
    return render_template('pitch.html')

@app.route('/pitch_audio', methods=['POST'])
def pitch_audio():
    print("yes")
    if 'audioFile' not in request.files:
        return 'No file part'

    file = request.files['audioFile']

    if file.filename == '':
        return 'No selected file'

    pitch = int(request.form['pitch'])

    if file:
        audio = AudioSegment.from_file(file)
        pitched_audio = audio._spawn(audio.raw_data, overrides={
            "frame_rate": int(audio.frame_rate * (2 ** (pitch/12.0)))
        })
        pitched_audio = pitched_audio.set_frame_rate(audio.frame_rate)
        pitched_audio.export('pitched_audio.mp3', format='mp3')
        return send_file('pitched_audio.mp3', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

