import queue

from google.cloud import speech
import sys


class SpeechClientBridge:
    def __init__(self, streaming_config, on_response):
        self._on_response = on_response
        self._queue = queue.Queue()
        self._ended = False
        self.streaming_config = streaming_config

    def start(self):
        client = speech.SpeechClient()
        stream = self.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in stream
        )
        #print ("SPEECHCLIENTBRIDGE: start, Before sending")
        responses = client.streaming_recognize(self.streaming_config, requests)
        #print ("SPEECHCLIENTBRIDGE: start, After sending")

        self.process_responses_loop(responses)
        #print ("SPEECHCLIENTBRIDGE: start")

    def terminate(self):
        #print ("SPEECHCLIENTBRIDGE: I SHOULD STOP NOW")
    
        self._ended = True
        

    def add_request(self, buffer):
        self._queue.put(bytes(buffer), block=False)
        #print ("SPEECHCLIENTBRIDGE: add_request")


    def process_responses_loop(self, responses):
        for response in responses:
            #print ("SPEECHCLIENTBRIDGE: Process_responses_loop_function")

            self._on_response(response, self._ended)

            if self._ended:
                break

    def generator(self):
        while not self._ended:
            #print ("SPEECHCLIENTBRIDGE: Generator")

            
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._queue.get()
            if chunk is None:
                #print ("SPEECHCLIENTBRIDGE: There is NO data in the queue")

                return
            #print ("SPEECHCLIENTBRIDGE: There is data in the queue")
    
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    #print ("SPEECHCLIENTBRIDGE: I am in try in the generator function")
    
                    chunk = self._queue.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    #print ("SPEECHCLIENTBRIDGE: YBreaking queue empty")
                    break

            #print ("SPEECHCLIENTBRIDGE: Yielding something")

            yield b"".join(data)