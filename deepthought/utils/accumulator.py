class Accumulator:
    def __init__(self):
        self.template = {"role": None, "type": None, "format": None, "content": None}
        self.message = self.template

    def accumulate(self, chunk):
        if type(chunk) == dict:

            if "format" in chunk and chunk["format"] == "active_line":
                # Do nothing
                return None

            if "start" in chunk:
                self.message = chunk
                self.message.pop("start")
                return None

            if "content" in chunk:

                # If new chunk data is different to existing message
                if any(self.message[key] != chunk[key] for key in self.message if key != "content"):
                    self.message = chunk
                if "content" not in self.message:
                    self.message["content"] = chunk["content"]
                else:
                    if type(chunk["content"]) == dict:
                        # can't concatenate dicts, so check if chunk content is dict
                        self.message["content"]["content"] += chunk["content"]["content"]
                    else:
                        # if chunk content is not dict, concatenate with exisiting message
                        self.message["content"] += chunk["content"]
                    return None
            
            if "end" in chunk:
                # Return final message and go back to initial state
                message = self.message
                self.message = self.template
                return message

            if type(chunk) == bytes:
                if "content" not in self.message or type(self.message["content"] != bytes):
                    self.message["content"] = b""
                self.message["content"] += chunk
                return None
