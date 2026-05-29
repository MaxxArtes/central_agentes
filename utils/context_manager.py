import json
import os

class ContextManager:
    def __init__(self, memory_file="D:/central_agentes/utils/memory.json"):
        self.memory_file = memory_file
        self.history_limit = 10
        if not os.path.exists(os.path.dirname(self.memory_file)):
            os.makedirs(os.path.dirname(self.memory_file))
        self.load_memory()

    def load_memory(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    self.memory = json.load(f)
            except:
                self.memory = {"history": [], "shared_data": {}}
        else:
            self.memory = {"history": [], "shared_data": {}}

    def save_memory(self):
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, indent=4, ensure_ascii=False)

    def add_interaction(self, role, content):
        self.memory["history"].append({"role": role, "content": content})
        # Mantém apenas as últimas interações para não estourar o contexto
        if len(self.memory["history"]) > self.history_limit:
            self.memory["history"] = self.memory["history"][-self.history_limit:]
        self.save_memory()

    def get_context_summary(self):
        summary = "--- HISTÓRICO RECENTE DA CONVERSA ---\n"
        for msg in self.memory["history"]:
            summary += f"{msg['role'].upper()}: {msg['content'][:200]}...\n"
        return summary

    def update_shared_data(self, key, value):
        self.memory["shared_data"][key] = value
        self.save_memory()

    def clear_memory(self):
        self.memory = {"history": [], "shared_data": {}}
        self.save_memory()
