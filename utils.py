from random import choice
from json import dump

from kivy.uix.textinput import TextInput


def generate_sentence(path: str) -> str:
    with open(path, mode='r', encoding='utf-8') as f:
        return choice(f.read().split('\n\n'))


def save_and_send_data(data: str, file_path: str):
    with open(file_path, 'a+') as f:
        dump(data, f)


class NoPasteTextInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        # Check if the text is being pasted (substring length significantly larger than typical typing)
        if len(substring) > 1:
            # If it's likely a paste action, don't insert the text
            return
        # Otherwise, proceed with the normal text insertion
        super(NoPasteTextInput, self).insert_text(substring, from_undo=from_undo)


x = """The current state of the art makes it possible to create synthetic speech of such a high
quality that human listeners are unable to distinguish between real speech and spoofed
speech [1] [8] [3].
Audio DeepFakes can be divided into three different categories:
• Synthetic-based DeepFakes result in the creation of artificial human speech by a software
or hardware system. This category includes text-to-speech (TTS), which focuses on
converting text transcriptions into natural-sounding speech in real time. The process
of speech synthesis involves a number of steps, including the collection of clean and
well-structured raw speech data and the training of a TTS model to generate synthetic
speech [5].
A tandem of a text analysis model, an acoustic model and a vocoder allows the production
of speech that can imitate different speakers. For example, a neural network that has
made significant progress in this area is WaveNet, which was designed to generate raw
audio waveforms for various speaker [5].
• Imitation-based audio DeepFake, also known as voice conversion (VC) is a technique that
transforms the original voice of one speaker to make it sound as if it is being spoken by
a different speaker. VC uses speech signals as input and modifies their style, intonation,
or prosody to imitate the target speech without altering the linguistic information. It
is often confused with synthetic-based methods. However both modify the acoustic
spectrum and stylistic characteristics of the speech audio signal. The original audio is
then converted to the target audio and spoken so that it imitates the target voice. 
Moreover, other types of manipulation can be distinguished. Emotion fake is a technique
in which the emotional tone of an audio recording can be altered by changing the emotion
and by keeping other aspects such as the speaker identity or its speech content unchanged. It
allows, depending on the approach, for real-time or non-parallel manipulation, to change the 
perceived emotional state conveyed by the voice, which naturally leads to a different semantic
interpretation of the message itself. On the other hand, scene fake is a unique fake where an
utterance is manipulated to simulate it was spoken in different acoustic conditions. It uses
advanced speech enhancement technologies to add a new type of sound while keeping the
speaker identity and speech content. Changing the from a scene from office to the airport is
one of the examples of a such a fake. It is also worth mentioning the partially fakes which
modify some selected words or phrases of the utterance and leave the rest of the audio instance
valid. It does that via adding original or synthesized audio clips that are selected to resemble
the speaker’s voice, hence the speaker identity is not changed throughout the whole audio. An
example would be changing a few select words in a sentence to change its meaning or context,
whilst the speaker and the rest of audio appears to be the same.
These attacks are different from the replay-based that instead of AI, uses a variety of
means to play back a person’s voice recordings. These can be divided into categories: far-field
detection, which plays back a victim’s microphone recording in a scenario where a hands-free
telephone segment has been mimicked, and cut-and-paste detection, which assembles audio by
playing back pieces of an audio file requested by a text-dependent system, mimicking audio
captured on a two-party human line. The ASVSpoof challenge series benchmarks the capabilities of ASV systems to defend
against spoofing attacks. The ASVspoof 2019 dataset is a large-scale public database designed
for the Third Automatic Speaker Verification Spoofing and Countermeasures challenge [9]. It
encompasses presentation attack - synthesized, converted, and replayed speech. In comparison
to the previous versions of the challenge (ASVSpoof2015, ASVSpoof2017), this is a significant
extension and diversification of the scope. The ASVSpoof2015 includes a variety of attacks
generated using TTS and VC techniques. The following version introduced more diverse and
challenging datasets, including higher quality and more varied spoofing techniques, with a
focus on replay attacks [6]. Each new version presents challenges that require the development
of more robust ASV systems to make the problem more realistic. The ASVSpoof2019 is the first of its kind to consider all three types of spoofing attacks
within a single framework, namely, impersonation, replay, speech synthesis, and voice conversion attacks [9]. The main goal of this dataset is to facilitate the development and evaluation
of countermeasures for detecting these spoofing attacks in automatic speaker verification
systems. The ASVspoof 2019 database contains data with varying difficulty levels, including
spoofed data that is indistinguishable from authentic utterances even to human listeners. The primary objective of the design was to reduce the difference that exists between
the laboratory environment and the real world, thus making the ASVSpoof2021 collection
potentially more adaptable to problems encountered in production applications [6]. Initially,
the use of matched training data was discontinued, leading participants to develop algorithms
that were more adaptable to spoofing techniques they had never seen before.
The challenge consisted of three sub-tasks: logical access (LA), physical access (PA), and
deepfake (DF) which were divided into progress, evaluation, and hidden subsets [6]. The
data for each of the three sub-challenges was provided in the FLAC format, which samples
at 16 kHz and uses 16-bit quantization. ASVspoof 2021 did not introduce any new training
data, whereas, procedures for training and development with data from earlier editions of
the challenge were made accessible. While PA investigated spoofs that mimicked physical
proximity (such as replay attacks), DF addressed the growing problem of artificial intelligence
(AI)-generated voice spoofs. LA focused on identifying spoofs that mimic remote access
scenarios.
In an effort to fulfil the initial assumptions, to make the laboratory environment more
realistic, the LA task required the transmission of both bona fide and spoofed speech over
telephony systems, including VoIP and PSTN. The participants had access to the LA training
partition from ASVspoof 2019 to train their countermeasure (CM) systems for the LA and
DF tasks. With a total of 37 female and 30 male speakers in each subset, the LA task
included progress and evaluation subsets with different conditions such as codec, sampling
rate, transmission and bit rate.
The best baseline system was outperformed by a number of the LA Challenge participants’
systems, some of which had much lower t-DCFs around the ASV level, indicating low error
rates. For many systems, there was not much of a performance difference between the
progress and evaluation subsets; nevertheless, several systems displayed over-fitting because
of variations in the known and unknown circumstances that were unique to the evaluation
subset. The performance of of spoofing detection systems for the LA task was additionally
impacted by influential data elements. While wideband settings produced lower t-DCFs than
narrowband conditions, indicating the usefulness of information at higher frequencies for
detection performance, lower bit rates and unregulated transmission conditions resulted in
poorer performance.
The PA task assessed the recording of speech over a wide variety of simulated acoustic
environments. It encompassed simulated replay attacks recorded in real physical spaces [6].
The PA challenge recorded voice in many physical locations and assessed system performance
in multiple rooms using different equipment in an attempt to ascertain the robustness and
reliability of spoofing detection systems. While replay attacks are recorded and subsequently
re-presented utilizing devices of different quality, genuine trials are given to the ASV system
in an actual physical environment. The Figure 3.2 provides an illustration of the recording
procedures [13].
Participants used in the challenge a variety of systems and methodologies, such as data
augmentation techniques or one-class learning frameworks based on Gaussian Mixture Models
(GMMs). This sub-task was more challenging than that of LA because of demanding a more
comprehensive evaluation process that highlighted the distinctions between actual physical
locations and simulated replay attacks during training. The PA task in the ASVspoof 2021
competition aimed to enhance automatic speaker verification and spoofing detection solutions
in real-world scenarios by addressing the challenges of recording speech in various acoustic
environments.
The DF task examined the robustness of spoofing detection solutions to online manipulation
of compressed speech data. The adversaries attempted to introduce a speech utterance in the
voice of a target speaker from an arbitrary text, without necessarily trying to fool an ASV
system. Instead, the primary metric for evaluation in the DF task is the EER.
The results of the DF task challenge showed a notable performance difference between
the progress and evaluation subsets, with the majority of systems showing EERs greater
than 15% for the evaluation set and less than 10% for the progress subset [6]. A number of
systems outperformed the best baseline system, despite the difficulties caused by different
characteristics of the modified speech data and compression techniques. The overall goal of
the DF task of the ASVspoof 2021 challenge is to improve spoofing detection techniques for
identifying deepfake speech in real-world situations involving online postings of compressed
audio [6].
Despite significant progress in making the problem more realistic and moving away from
laboratory conditions, the authors note a number of limitations and potential directions for
development [6]. Further development is needed, e.g. using actual social media in a DF task,
collecting human speech recordings in a PA task instead using speakers, and taking ambient
noise into account in an LA task. Furthermore, the authors pointed out that non-speech
intervals can play a role in the detection of faked speech, particularly for LA and DF tasks [6].
Investigating the generation or conversion of non-speech regions and the difference between
cues used for detection in non-speech and speech intervals is of interest [6]. The training data
policy should be relaxed to allow larger, more complex models to be trained using external
data. The next versions of the ASVSpoof collection, in the opinion of the authors, could allow
a dual training policy, one fixed and one relaxed [13]. Diversity of attacks is also crucial, as
spoofing attacks are generated with advanced TTS and VC algorithms. Diversity of audio
data is essential, with ASVspoof data consisting exclusively of English read speech from the
VCTK corpus. The inclusion of two unexposed datasets in the DF database revealed a lack of
CM generalisation due to differences in bona fide speech and score distributions. In the future,
ASVspoof should increase the diversity of spoofing attacks and bona fide source data. """

print(x.replace('\n', ''))