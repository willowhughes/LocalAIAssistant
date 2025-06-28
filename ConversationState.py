class ConversationState:
    def __init__(self, config):
        self.history = []
        # convert config array to string if needed and format as system message
        system_config = " ".join(config) if isinstance(config, list) else config
        self.history.append(f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system_config}<|eot_id|>")

    def append_prompt(self, prompt):
        self.history.append(f"<|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|>")

    def append_response(self, response):
        self.history.append(f"<|start_header_id|>assistant<|end_header_id|>\n\n{response}<|eot_id|>")

    def get_history(self):
        return self.history