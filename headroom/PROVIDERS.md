# Headroom Provider Configuration Reference

This document lists recommended provider entries and environment variables for running Headroom with a variety of local and cloud LLM backends.

Principles
- Providers are configured via `ProviderConfig` entries in `headroom.backends.litellm.PROVIDER_REGISTRY`.
- Use LiteLLM (`--backend litellm-<provider>`) or any-llm (`--backend anyllm --anyllm-provider <provider>`) to keep Headroom provider-agnostic.
- Do not store secrets in the repo. Use environment variables or a secrets manager.

Common provider examples

- Ollama
  - Env: `OLLAMA_API_KEY`, `OLLAMA_HOST`
  - Model format: `model:tag` (e.g. `qwen2.5-coder:3b`, `forge-geralt-v6:latest`)
  - Usage: `headroom proxy --backend litellm-ollama`

- vLLM (HTTP serving)
  - Env: `VLLM_HOST`, `VLLM_API_KEY`
  - Model format: provider-specific (use the server's model name)
  - Usage: `headroom proxy --backend litellm-vllm` or via `anyllm`

- Llama (local/hosted)
  - Env: `LLAMA_HOST`, `LLAMA_API_KEY`
  - Model format: provider-specific
  - Usage: `headroom proxy --backend litellm-llama` or via `anyllm`

Cloud providers
- OpenAI: `OPENAI_API_KEY` — `headroom proxy --backend litellm-openai`
- Google Vertex/Gemini: `GOOGLE_APPLICATION_CREDENTIALS` — `headroom proxy --backend litellm-vertex --region <region>`
- AWS Bedrock: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION` — `headroom proxy --backend litellm-bedrock --region <region>`

Tips
- When using LiteLLM: set a dummy `ANTHROPIC_API_KEY=sk-ant-dummy` so Anthropic-style clients can point to Headroom.
- Prefer `--workers 1` for local testing to avoid CCR/cache fragmentation.
- Add provider `env_vars` entries to `ProviderConfig` so the CLI banner can show required credentials.

See `headroom/backends/litellm.py` for the canonical registry and examples.

