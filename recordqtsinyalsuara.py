import sys
import os
import numpy as np
import sounddevice as sd
from scipy.fft import fft, fftfreq
from scipy.io.wavfile import write
import requests
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QGraphicsView, QVBoxLayout, QWidget, QMessageBox)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class EdgeImpulseUploader:
    """Class to handle uploads and inferences with Edge Impulse."""
    def __init__(self, api_key="ei_4a68a575c617326e090088ab2077865e256760ceaeedb2d4", 
                 api_url="https://ingestion.edgeimpulse.com/api/testing/files",
                 inference_url="https://studio.edgeimpulse.com/v1/.../infer"):  # Replace with your inference endpoint
        self.api_key = api_key
        self.api_url = api_url
        self.inference_url = inference_url

    def upload_audio_to_edge_impulse(self, audio_filename, label="recording"):
        try:
            with open(audio_filename, "rb") as f:
                response = requests.post(
                    self.api_url,
                    headers={
                        "x-api-key": self.api_key,
                        "x-label": label,
                    },
                    files={"data": (os.path.basename(audio_filename), f, "audio/wav")}, 
                    timeout=30
                )
                if response.status_code == 200:
                    QMessageBox.information(None, "Upload Success", "Uploaded successfully to Edge Impulse!")
                else:
                    QMessageBox.warning(None, "Upload Failed", 
                        f"Failed with status code: {response.status_code}\nResponse: {response.text}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(None, "Upload Error", f"Error occurred: {e}")

class SignalRecorder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Recorder with Real-Time FFT and Inference")
        self.setGeometry(0, 0, 1200, 800)

        # Tambahkan uploader
        self.uploader = EdgeImpulseUploader()

        # Audio Parameters
        self.sample_rate = 40000  # Sampling rate diubah menjadi 40,000 Hz
        self.duration = 15  # Set duration of recording in seconds
        self.max_freq = 20000  # Maximum frequency untuk FFT visualization

        # Central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Widgets and buttons
        self.file_name_input = QLineEdit()
        self.file_name_input.setPlaceholderText("Enter file name (without extension)")
        self.record_button = QPushButton("Start Recording")
        self.stop_button = QPushButton("Stop Recording")
        self.save_button = QPushButton("Save Audio")
        self.upload_button = QPushButton("Upload to Edge Impulse")
        self.status_label = QLabel("Status: Ready")

        # Canvas for plotting
        self.record_canvas = FigureCanvas(plt.Figure())
        self.fft_canvas = FigureCanvas(plt.Figure())

        # Add widgets to layout
        main_layout.addWidget(self.file_name_input)
        main_layout.addWidget(self.record_button)
        main_layout.addWidget(self.stop_button)
        main_layout.addWidget(self.save_button)
        main_layout.addWidget(self.upload_button)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.record_canvas)
        main_layout.addWidget(self.fft_canvas)

        # Connect signals
        self.record_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)
        self.save_button.clicked.connect(self.save_audio)
        self.upload_button.clicked.connect(self.upload_to_edge_impulse)

        # Initialize recording variables
        self.audio_data = np.zeros(int(self.sample_rate * self.duration))
        self.stream = None

    def start_recording(self):
        """Start recording audio."""
        def audio_callback(indata, frames, time, status):
            if status:
                print(status)
            self.audio_data = np.roll(self.audio_data, -frames)
            self.audio_data[-frames:] = indata.flatten()
            self.update_realtime_plot()
            self.update_fft_plot()

        self.stream = sd.InputStream(
            callback=audio_callback, channels=1, samplerate=self.sample_rate
        )
        self.stream.start()
        self.status_label.setText("Status: Recording...")
        self.record_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_recording(self):
        """Stop recording audio."""
        if self.stream and self.stream.active:
            self.stream.stop()
            self.stream.close()
        self.status_label.setText("Status: Recording Stopped")
        self.record_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def update_realtime_plot(self):
        """Update the plot with real-time audio data."""
        self.record_canvas.figure.clear()
        ax = self.record_canvas.figure.add_subplot(111)
        t = np.linspace(0, self.duration, len(self.audio_data))
        ax.plot(t, self.audio_data, color='blue')
        ax.set_title("Real-time Audio Signal")
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Amplitude")
        self.record_canvas.draw()

    def update_fft_plot(self):
        """Update the FFT plot in real-time."""
        self.fft_canvas.figure.clear()
        ax = self.fft_canvas.figure.add_subplot(111)
        if np.any(self.audio_data):  # Periksa apakah audio_data berisi nilai selain nol
            N = len(self.audio_data)
            fft_result = fft(self.audio_data)
            fft_magnitudes = np.abs(fft_result[:N // 2])
            freqs = fftfreq(N, 1 / self.sample_rate)[:N // 2]
            ax.plot(freqs, fft_magnitudes, color='orange')
            ax.set_xlim(0, self.max_freq)  # Ubah batas hingga 20,000 Hz
            ax.set_title("Real-time FFT")
            ax.set_xlabel("Frequency [Hz]")
            ax.set_ylabel("Magnitude")
        else:
            ax.text(0.5, 0.5, "No data to display", 
                    fontsize=12, ha='center', va='center', transform=ax.transAxes)
        self.fft_canvas.draw()

    def save_audio(self):
        """Save recorded audio to a WAV file."""
        file_name = self.file_name_input.text().strip()
        if not file_name: 
            file_name = "recording"
        file_path = f"{file_name}.wav"
        scaled_data = np.int16(self.audio_data / np.max(np.abs(self.audio_data)) * 32767)
        write(file_path, self.sample_rate, scaled_data)
        self.status_label.setText(f"Status: Audio saved to {file_path}")
        return file_path

    def upload_to_edge_impulse(self):
        """Upload the audio file to Edge Impulse."""
        file_path = self.save_audio()
        self.uploader.upload_audio_to_edge_impulse(file_path, label="recording")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = SignalRecorder()
    window.show()

    sys.exit(app.exec())
