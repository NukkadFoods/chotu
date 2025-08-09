# utils/wake_word_detector.py
import speech_recognition as sr
import threading
import time
from queue import Queue

class WakeWordDetector:
    """Advanced wake word detection for hands-free operation"""
    
    def __init__(self, wake_words=['hey chotu', 'chotu', 'jarvis']):
        self.wake_words = [word.lower() for word in wake_words]
        self.is_listening = False
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.audio_queue = Queue()
        self.stop_listening = None
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
    
    def start_listening(self, callback=None):
        """Start continuous listening for wake words"""
        self.is_listening = True
        
        def audio_callback(recognizer, audio):
            """Callback for audio processing"""
            self.audio_queue.put(audio)
        
        # Start background listening
        self.stop_listening = self.recognizer.listen_in_background(
            self.microphone, 
            audio_callback,
            phrase_time_limit=2
        )
        
        # Start processing thread
        processing_thread = threading.Thread(target=self._process_audio, args=(callback,))
        processing_thread.daemon = True
        processing_thread.start()
        
        print("👂 Wake word detection started. Say 'Hey Chotu' to activate.")
    
    def _process_audio(self, callback):
        """Process audio queue for wake words"""
        while self.is_listening:
            if not self.audio_queue.empty():
                audio = self.audio_queue.get()
                try:
                    # Recognize speech
                    text = self.recognizer.recognize_google(audio, language='en-US')
                    text_lower = text.lower()
                    
                    # Check for wake words
                    for wake_word in self.wake_words:
                        if wake_word in text_lower:
                            print(f"🎯 Wake word detected: '{wake_word}'")
                            if callback:
                                # Extract command after wake word
                                command = text_lower.replace(wake_word, '').strip()
                                callback(command if command else None)
                            break
                            
                except sr.UnknownValueError:
                    # Could not understand audio
                    pass
                except sr.RequestError as e:
                    print(f"⚠️  Speech recognition error: {e}")
            
            time.sleep(0.1)
    
    def stop_listening_for_wake_word(self):
        """Stop wake word detection"""
        self.is_listening = False
        if self.stop_listening:
            self.stop_listening(wait_for_stop=False)
        print("🔇 Wake word detection stopped.")
    
    def listen_for_command(self, timeout=5):
        """Listen for a command after wake word detection"""
        try:
            with self.microphone as source:
                print("🎙️  Listening for command...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=5)
            
            command = self.recognizer.recognize_google(audio)
            print(f"📝 Command received: {command}")
            return command
            
        except sr.WaitTimeoutError:
            print("⏰ Listening timeout - no command received")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand the command")
            return None
        except sr.RequestError as e:
            print(f"⚠️  Speech recognition error: {e}")
            return None
