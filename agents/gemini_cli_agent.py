import subprocess
import os
import json

class GeminiCliAgent:
    def __init__(self):
        # O CLI já está autenticado conforme verificado anteriormente
        pass

    def ask(self, prompt, use_yolo=False):
        """
        Executa o Gemini CLI via terminal usando STDIN para o prompt real.
        Isso evita TODOS os problemas de limite de caracteres e escape do Windows.
        """
        try:
            # Usamos o caractere "." como dummy para o -p, e passamos o prompt real via STDIN
            yolo_flag = "--yolo" if use_yolo else ""
            command = f'npx gemini -p "." {yolo_flag}'
            
            result = subprocess.run(
                command,
                input=prompt, # O prompt real vai por aqui (sem limite de shell)
                capture_output=True,
                text=True,
                encoding='utf-8',
                shell=True
            )

            if result.returncode != 0:
                # Se falhar, tenta com flag curta
                command = f'npx gemini -p . {yolo_flag}'
                result = subprocess.run(command, input=prompt, capture_output=True, text=True, encoding='utf-8', shell=True)

            output = result.stdout.strip()
            
            # Extração de JSON
            if "{" in output and "}" in output:
                import re
                json_match = re.search(r'\{.*\}', output, re.DOTALL)
                if json_match:
                    return json_match.group(0)
            
            # Limpeza padrão de banners
            if "✦" in output:
                output = output.split("✦")[-1].strip()
            
            lines = output.split("\n")
            clean_lines = [l for l in lines if not l.startswith("ℹ") and not l.startswith(">")]
            output = "\n".join(clean_lines).strip()
            
            return output

        except Exception as e:
            return f"Erro ao chamar Gemini CLI: {str(e)}"

if __name__ == "__main__":
    agent = GeminiCliAgent()
    print(agent.ask("Responda apenas com a palavra TESTE."))
