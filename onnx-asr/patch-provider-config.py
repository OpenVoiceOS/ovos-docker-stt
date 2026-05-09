from pathlib import Path

import ovos_stt_plugin_onnxasr


plugin_path = Path(ovos_stt_plugin_onnxasr.__file__)
plugin_source = plugin_path.read_text(encoding="utf-8")

old = """        quantization = self.config.get("quantization")
        self.onnx_model = onnx_asr.load_model(model_id, quantization=quantization)
"""
new = """        quantization = self.config.get("quantization")
        providers = self.config.get("providers")
        provider_options = self.config.get("provider_options")
        self.onnx_model = onnx_asr.load_model(
            model_id,
            quantization=quantization,
            providers=providers,
            provider_options=provider_options,
        )
"""

if old not in plugin_source:
    if "providers = self.config.get(\"providers\")" in plugin_source:
        raise SystemExit(0)
    raise SystemExit(f"Could not find provider patch target in {plugin_path}")

plugin_path.write_text(plugin_source.replace(old, new), encoding="utf-8")
