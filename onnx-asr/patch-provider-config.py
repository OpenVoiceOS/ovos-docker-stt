from pathlib import Path

import ovos_stt_plugin_onnxasr


plugin_path = Path(ovos_stt_plugin_onnxasr.__file__)
plugin_source = plugin_path.read_text(encoding="utf-8")

if "from ovos_config import Configuration" not in plugin_source:
    plugin_source = plugin_source.replace(
        "import onnx_asr\n",
        "import onnx_asr\nfrom ovos_config import Configuration\n",
    )

old_blocks = [
    """        model_id = self.config.get("model", "nemo-canary-1b-v2")
        quantization = self.config.get("quantization")
        self.onnx_model = onnx_asr.load_model(model_id, quantization=quantization)
""",
    """        model_id = self.config.get("model", "nemo-canary-1b-v2")
        quantization = self.config.get("quantization")
        providers = self.config.get("providers")
        provider_options = self.config.get("provider_options")
        self.onnx_model = onnx_asr.load_model(
            model_id,
            quantization=quantization,
            providers=providers,
            provider_options=provider_options,
        )
""",
]
new = """        module_config = Configuration().get("stt", {}).get("ovos-stt-plugin-onnx-asr", {})
        plugin_config = {**module_config, **self.config}
        model_id = plugin_config.get("model", "nemo-canary-1b-v2")
        quantization = plugin_config.get("quantization")
        providers = plugin_config.get("providers")
        provider_options = plugin_config.get("provider_options")
        self.onnx_model = onnx_asr.load_model(
            model_id,
            quantization=quantization,
            providers=providers,
            provider_options=provider_options,
        )
"""

for old in old_blocks:
    if old in plugin_source:
        plugin_source = plugin_source.replace(old, new)
        break
else:
    if "plugin_config = {**module_config, **self.config}" in plugin_source:
        plugin_path.write_text(plugin_source, encoding="utf-8")
        raise SystemExit(0)
    raise SystemExit(f"Could not find provider patch target in {plugin_path}")

plugin_path.write_text(plugin_source, encoding="utf-8")
