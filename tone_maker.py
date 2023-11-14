"""
A class for generating and playing tones
"""

from pyaudio import PyAudio, paContinue, paInt8, paInt16, paInt24, paInt32
import wave
import struct


class ToneMaker():
    """set tone sound parameters and then generate a wav file of the tone, or play and stop it"""
    def __init__(self):
        self._pa = PyAudio()        # initiate PyAudio
        self.set_audio_params()     # set audio parameters

    def set_audio_params(self, sample_rate:int=44100, bit_depth:int=16):
        if not bit_depth in (8, 16, 24, 32):
            raise ValueError("`bit_depth` must be 8, 16, 24, or 32")
        frmt_map = {                # use to get struct format strings, and PyAudio stream format values
            8:  ('b', paInt8),          # b = signed char
            16: ('h', paInt16),         # h = short
            24: ('l', paInt24),         # l = long
            32: ('q', paInt32)          # q = long long
        }

        self._s_bit = bit_depth
        self._wav_s_width = int(bit_depth / 8)
        self._struct_frmt_str, self._pa_frmt = frmt_map[bit_depth]
        self._s_rate = sample_rate

    #---------

    # THIS GETS INACCURATE AT HIGHER FREQUENCIES, ESPECIALLY AT LOWER SAMPE RATES
    def _generate_tone_data(self, wave_freq:int, wave_shape:str, n_samps:int, s_offset:int=0):
        """
        Generate `n_samps` samples needed to create a tone (which can be then used to write to a file, or play).

        `s_offset` is sample offset. Usually, the data samples will be produced starting from the beginning of a sound wave cycle,
        but s_offset can be used offset where the samples should start on the wave cycle. (used by `self.play` method)
        * The offset works like an index (starting from 0). So a sample offset of 7 would mean to start at the 8th sample in the cycle
        """
        
        samp_per_cyc = round(self._s_rate / wave_freq)           # determine number samples per sound wave cycle
        max_samp_value = (2 ** self._s_bit)/2 - 1                # determine max (*signed*) value of a sample with bit_depth (aka sample width)

        def generate_square_cycle():
            """generate one full cycle for square wave"""
            samp_per_half = int(samp_per_cyc / 2)               # determine number of samples in half a cycle
            
            half1 = [1] * samp_per_half                         # first half is max value
            half2 = [-1] * ( samp_per_cyc - samp_per_half )     # and second half is min value
            return half1 + half2                                # return a full cycle, which is both halves

        def generate_saw_cycle():
            """generate one full cycle for sawtooth wave"""
            # (2 / samp_per_cyc) is the increment at which to increase the value, starting from -1
            return [-1 + (2 / samp_per_cyc) * x for x in range(samp_per_cyc-1)] + [1]
            # return a list n values long (where n is samp_per_cyc), evenly spread from from -1 to 1

        def generate_tri_cycle():
            """generate one full cycle for triangle wave"""
            half_samp_per_cyc = int(samp_per_cyc/2)
            half = [-1 + (2 / half_samp_per_cyc) * x for x in range(half_samp_per_cyc +1)]
            # similar to saw, generate an even spread of values from -1 to 1 for half the samples, and then the reverse for the other half
            return half + list(reversed(half[1:-1])) + ([-1] * (samp_per_cyc % 2))  # the last addition is to add an extra `-1` sample if samp_per_cyc doesn't devide evenly 

        shape_func_map = {
            "SQUARE":   generate_square_cycle,
            "SAW":      generate_saw_cycle,
            "TRIANGLE": generate_tri_cycle
        }
        if not wave_shape in shape_func_map:
            raise ValueError("`wave_shape` must be string of 'SQUARE', 'SAW', or 'TRIANGLE'")

        full_cycle = shape_func_map[wave_shape]()           # determine wave shape, and call corresponding function to generate a wave cycle
        # data = an offset wave cycle + enough full cycles to make up the total needed number of samples
        data = (full_cycle[s_offset:]) + (full_cycle * int(n_samps / samp_per_cyc + 1))
        data = data[:n_samps]                               # then trim data down so that the number of sample matches `n_samps`        
        data = [struct.pack(self._struct_frmt_str, int(sample * max_samp_value)) for sample in data]
        # ^ multiply each sample in `data` by max_samp_value, and then convert data into a C struct, using the struct format string
        # get offset value from the remaining samples from the total, subtracting the offset cycle along with all full cyces that could fit evenly
        new_offset = (n_samps - (samp_per_cyc - s_offset)) % samp_per_cyc
        
        return data, new_offset

    #---------

    def write_wav_file(self, filepath:str, duration:int, wave_freq:int=440, wave_shape:str='SQUARE'):
        """create a wav file of a tone with all of the parameters specified in method args"""
        n_samples = int(duration * self._s_rate)        # determine total number of samples for duration of audio        
        
        data, offset = self._generate_tone_data(wave_freq, wave_shape, n_samples)   # generate audio data

        with wave.open(filepath, 'w') as file:
            file.setnchannels(1)
            file.setsampwidth(self._wav_s_width)        # number of bytes to represent one sample (related to bit depth). ex: `2` = 16 bit depth
            file.setframerate(self._s_rate)             # sample rate
            for sample in data:
                file.writeframes(sample)                # write data samples to wav file

    #---------

    def play(self, wave_freq:int=440, wave_shape='SQUARE'):
        """play a constant tone at `wave_freq` hz with `wave_shape`, in a seperate thread (this method is non-blocking)"""

        # if there is already an open stream, close it first
        self.stop()

        self._current_offset = 0

        def callback(in_data, frame_count, time_info, status):
            data, self._current_offset = self._generate_tone_data(wave_freq, wave_shape, frame_count, self._current_offset)
            data = b''.join(data)
            return (data, paContinue)

        # open stream with PyAudio-instance's open()
        self._stream = self._pa.open(
            format = self._pa_frmt,         # audio bit depth (uses paInt format)
            channels = 1, 
            rate = 44100,                   # sample rate
            frames_per_buffer=1024,         # buffer size
            output = True,                  # 'Specifies whether this is an output stream. Defaults to False.'
            stream_callback = callback
            )

        self._stream.start_stream()

    def stop(self):
        """stop playing the tone, by closing and deleting pyaudio stream"""
        if hasattr(self, '_stream'):
            self._stream.close()
            del self._stream

    def is_playing(self) -> bool:
        """return `True` if tone is playing, `False` if not"""
        if hasattr(self, '_stream') and self._stream.is_active():
            return True
        else:
            return False
