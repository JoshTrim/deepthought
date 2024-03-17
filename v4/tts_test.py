
if __name__ == '__main__':
    from RealtimeTTS import TextToAudioStream, CoquiEngine

    def dummy_generator():
        yield "Hey guys! These here are realtime spoken sentences based on local text synthesis. "
        yield "With a local, neuronal, cloned voice. So every spoken sentence sounds unique."


    # for normal use with minimal logging:
    # engine = CoquiEngine()

    # test with extended logging:
    import logging
    logging.basicConfig(level=logging.INFO)    

    engine = CoquiEngine(level=logging.INFO, thread_count=6, stream_chunk_size=50, full_sentences=False, voice="Henriette Usha")

    stream = TextToAudioStream(engine)
    print ("Starting to play stream")
    stream.feed(dummy_generator()).play(log_synthesized_text=True)

    engine.shutdown()
