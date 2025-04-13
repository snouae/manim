# TheoremExplainAgent
[![arXiv](https://img.shields.io/badge/arXiv-2502.19400-b31b1b.svg)](https://arxiv.org/abs/2502.19400)
<a href='https://huggingface.co/papers/2502.19400'><img src='https://img.shields.io/static/v1?label=Paper&message=Huggingface&color=orange'></a> 

[**🌐 Homepage**](https://tiger-ai-lab.github.io/TheoremExplainAgent/)  | [**📖 arXiv**](https://arxiv.org/abs/2502.19400) | [**🤗 HuggingFace Dataset**](https://huggingface.co/datasets/TIGER-Lab/TheoremExplainBench) 

[![contributors](https://img.shields.io/github/contributors/TIGER-AI-Lab/TheoremExplainAgent)](https://github.com/TIGER-AI-Lab/TheoremExplainAgent/graphs/contributors)
[![license](https://img.shields.io/github/license/TIGER-AI-Lab/TheoremExplainAgent.svg)](https://github.com/TIGER-AI-Lab/TheoremExplainAgent/blob/main/LICENSE)
[![GitHub](https://img.shields.io/github/stars/TIGER-AI-Lab/TheoremExplainAgent?style=social)](https://github.com/TIGER-AI-Lab/TheoremExplainAgent)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FTIGER-AI-Lab%2FTheoremExplainAgent&count_bg=%23C83DB9&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=visitors&edge_flat=false)](https://hits.seeyoufarm.com)

This repo contains the codebase for our paper [TheoremExplainAgent: Towards Multimodal Explanations for LLM Theorem Understanding](https://arxiv.org/abs/2502.19400)

## Introduction
TheoremExplainAgent is an AI system that generates long-form Manim videos to visually explain theorems, proving its deep understanding while uncovering reasoning flaws that text alone often hides.



https://github.com/user-attachments/assets/17f2f4f2-8f2c-4abc-b377-ac92ebda69f3


## 📰 News
* 2025 Mar 3: Generation code and Evaluation code released. Thanks for the wait!
<!--* 2025 Mar 3: Reach 404 stars without code.-->
* 2025 Feb 27: Paper available on [Arxiv](https://arxiv.org/abs/2502.19400). Thanks AK for putting our paper on [HF Daily](https://huggingface.co/papers/2502.19400).

## Installation

1. Setting up conda environment
```shell
conda create --name tea python=3.12.8
conda activate tea
pip install -r requirements.txt
```

2. You may also need to install latex and other dependencies for Manim Community. Look at [Manim Installation Docs](https://docs.manim.community/en/stable/installation.html) for more details.

3. Then Download the Kokoro model and voices using the commands to enable TTS service.

```shell
mkdir -p models && wget -P models https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/kokoro-v0_19.onnx && wget -P models https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/voices.bin
```

4. Create `.env` based on `.env.template`, filling in the environmental variables according to the models you choose to use.
See [LiteLLM](https://docs.litellm.ai/docs/providers) for reference.

Your `.env` file should look like the following:
```shell
# OpenAI
OPENAI_API_KEY=""

# Azure OpenAI
AZURE_API_KEY=""
AZURE_API_BASE=""
AZURE_API_VERSION=""

# Google Vertex AI
VERTEXAI_PROJECT=""
VERTEXAI_LOCATION=""
GOOGLE_APPLICATION_CREDENTIALS=""

# Google Gemini
GEMINI_API_KEY=""

...

# Kokoro TTS Settings
KOKORO_MODEL_PATH="models/kokoro-v0_19.onnx"
KOKORO_VOICES_PATH="models/voices.bin"
KOKORO_DEFAULT_VOICE="af"
KOKORO_DEFAULT_SPEED="1.0"
KOKORO_DEFAULT_LANG="en-us"
```
Fill in the API keys according to the model you wanted to use.

5. Configure Python path. Note that you need to do
```shell
export PYTHONPATH=$(pwd):$PYTHONPATH
```
To make it work. Otherwise you may encounter import issues.

### Generation (Single topic)
```shell
python generate_video.py \
      --model "openai/o3-mini" \
      --helper_model "openai/o3-mini" \
      --output_dir "output/your_exp_name" \
      --topic "your_topic" \
      --context "description of your topic, e.g. 'This is a topic about the properties of a triangle'" \
```

Example:
```shell
python generate_video.py \
      --model "openai/o3-mini" \
      --helper_model "openai/o3-mini" \
      --output_dir "output/my_exp_name" \
      --topic "Big O notation" \
      --context "most common type of asymptotic notation in computer science used to measure worst case complexity" \
```

### Generation (in batch)
```shell
python generate_video.py \
      --model "openai/o3-mini" \
      --helper_model "openai/o3-mini" \
      --output_dir "output/my_exp_name" \
      --theorems_path data/thb_easy/math.json \
      --max_scene_concurrency 7 \
      --max_topic_concurrency 20 \
```

### Generation with RAG
Before using RAG, download the RAG documentation from this [Google Drive link](https://drive.google.com/file/d/1Tn6J_JKVefFZRgZbjns93KLBtI9ullRv/view?usp=sharing). After downloading, unzip the file. For example, if you unzip it to `data/rag/manim_docs`, then you should set `--manim_docs_path` to `data/rag/manim_docs`. The vector database will be created the first time you run with RAG.

```shell
python generate_video.py \
            --model "openai/o3-mini" \
            --helper_model "openai/o3-mini" \
            --output_dir "output/with_rag/o3-mini/vtutorbench_easy/math" \
            --topic "Big O notation" \
            --context "most common type of asymptotic notation in computer science used to measure worst case complexity" \
            --use_rag \
            --chroma_db_path "data/rag/chroma_db" \
            --manim_docs_path "data/rag/manim_docs" \
            --embedding_model "vertex_ai/text-embedding-005"
```

We support more options for generation, see below for more details:
```shell
usage: generate_video.py [-h]
                         [--model]
                         [--topic TOPIC] [--context CONTEXT]
                         [--helper_model]
                         [--only_gen_vid] [--only_combine] [--peek_existing_videos] [--output_dir OUTPUT_DIR] [--theorems_path THEOREMS_PATH]
                         [--sample_size SAMPLE_SIZE] [--verbose] [--max_retries MAX_RETRIES] [--use_rag] [--use_visual_fix_code]
                         [--chroma_db_path CHROMA_DB_PATH] [--manim_docs_path MANIM_DOCS_PATH]
                         [--embedding_model {azure/text-embedding-3-large,vertex_ai/text-embedding-005}] [--use_context_learning]
                         [--context_learning_path CONTEXT_LEARNING_PATH] [--use_langfuse] [--max_scene_concurrency MAX_SCENE_CONCURRENCY]
                         [--max_topic_concurrency MAX_TOPIC_CONCURRENCY] [--debug_combine_topic DEBUG_COMBINE_TOPIC] [--only_plan] [--check_status]
                         [--only_render] [--scenes SCENES [SCENES ...]]

Generate Manim videos using AI

options:
  -h, --help            show this help message and exit
  --model               Select the AI model to use
  --topic TOPIC         Topic to generate videos for
  --context CONTEXT     Context of the topic
  --helper_model        Select the helper model to use
  --only_gen_vid        Only generate videos to existing plans
  --only_combine        Only combine videos
  --peek_existing_videos, --peek
                        Peek at existing videos
  --output_dir OUTPUT_DIR
                        Output directory
  --theorems_path THEOREMS_PATH
                        Path to theorems json file
  --sample_size SAMPLE_SIZE, --sample SAMPLE_SIZE
                        Number of theorems to sample
  --verbose             Print verbose output
  --max_retries MAX_RETRIES
                        Maximum number of retries for code generation
  --use_rag, --rag      Use Retrieval Augmented Generation
  --use_visual_fix_code, --visual_fix_code
                        Use VLM to fix code with rendered visuals
  --chroma_db_path CHROMA_DB_PATH
                        Path to Chroma DB
  --manim_docs_path MANIM_DOCS_PATH
                        Path to manim docs
  --embedding_model {azure/text-embedding-3-large,vertex_ai/text-embedding-005}
                        Select the embedding model to use
  --use_context_learning
                        Use context learning with example Manim code
  --context_learning_path CONTEXT_LEARNING_PATH
                        Path to context learning examples
  --use_langfuse        Enable Langfuse logging
  --max_scene_concurrency MAX_SCENE_CONCURRENCY
                        Maximum number of scenes to process concurrently
  --max_topic_concurrency MAX_TOPIC_CONCURRENCY
                        Maximum number of topics to process concurrently
  --debug_combine_topic DEBUG_COMBINE_TOPIC
                        Debug combine videos
  --only_plan           Only generate scene outline and implementation plans
  --check_status        Check planning and code status for all theorems
  --only_render         Only render scenes without combining videos
  --scenes SCENES [SCENES ...]
                        Specific scenes to process (if theorems_path is provided)
```


### Supported Models
<!--You can customize the allowed models by editing the `src/utils/allowed_models.json` file. This file specifies which `model` and `helper_model` the system is permitted to use.--> 
The model naming follows the LiteLLM convention. For details on how models should be named, please refer to the [LiteLLM documentation](https://docs.litellm.ai/docs/providers).


### Evaluation
Note that Gemini and GPT4o is required for evaluation.

Currently, evaluation requires a video file and a subtitle file (SRT format).

Video evaluation:
```shell
usage: evaluate.py [-h]
                   [--model_text {gemini/gemini-1.5-pro-002,gemini/gemini-1.5-flash-002,gemini/gemini-2.0-flash-001,vertex_ai/gemini-1.5-flash-002,vertex_ai/gemini-1.5-pro-002,vertex_ai/gemini-2.0-flash-001,openai/o3-mini,gpt-4o,azure/gpt-4o,azure/gpt-4o-mini,bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0,bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0,bedrock/anthropic.claude-3-5-haiku-20241022-v1:0,bedrock/us.anthropic.claude-3-7-sonnet-20250219-v1:0}]
                   [--model_video {gemini/gemini-1.5-pro-002,gemini/gemini-2.0-flash-exp,gemini/gemini-2.0-pro-exp-02-05}]
                   [--model_image {gemini/gemini-1.5-pro-002,gemini/gemini-1.5-flash-002,gemini/gemini-2.0-flash-001,vertex_ai/gemini-1.5-flash-002,vertex_ai/gemini-1.5-pro-002,vertex_ai/gemini-2.0-flash-001,openai/o3-mini,gpt-4o,azure/gpt-4o,azure/gpt-4o-mini,bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0,bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0,bedrock/anthropic.claude-3-5-haiku-20241022-v1:0,bedrock/us.anthropic.claude-3-7-sonnet-20250219-v1:0}]
                   [--eval_type {text,video,image,all}] --file_path FILE_PATH --output_folder OUTPUT_FOLDER [--retry_limit RETRY_LIMIT] [--combine] [--bulk_evaluate] [--target_fps TARGET_FPS]
                   [--use_parent_folder_as_topic] [--max_workers MAX_WORKERS]

Automatic evaluation of theorem explanation videos with LLMs

options:
  -h, --help            show this help message and exit
  --model_text {gemini/gemini-1.5-pro-002,gemini/gemini-1.5-flash-002,gemini/gemini-2.0-flash-001,vertex_ai/gemini-1.5-flash-002,vertex_ai/gemini-1.5-pro-002,vertex_ai/gemini-2.0-flash-001,openai/o3-mini,gpt-4o,azure/gpt-4o,azure/gpt-4o-mini,bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0,bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0,bedrock/anthropic.claude-3-5-haiku-20241022-v1:0,bedrock/us.anthropic.claude-3-7-sonnet-20250219-v1:0}
                        Select the AI model to use for text evaluation
  --model_video {gemini/gemini-1.5-pro-002,gemini/gemini-2.0-flash-exp,gemini/gemini-2.0-pro-exp-02-05}
                        Select the AI model to use for video evaluation
  --model_image {gemini/gemini-1.5-pro-002,gemini/gemini-1.5-flash-002,gemini/gemini-2.0-flash-001,vertex_ai/gemini-1.5-flash-002,vertex_ai/gemini-1.5-pro-002,vertex_ai/gemini-2.0-flash-001,openai/o3-mini,gpt-4o,azure/gpt-4o,azure/gpt-4o-mini,bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0,bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0,bedrock/anthropic.claude-3-5-haiku-20241022-v1:0,bedrock/us.anthropic.claude-3-7-sonnet-20250219-v1:0}
                        Select the AI model to use for image evaluation
  --eval_type {text,video,image,all}
                        Type of evaluation to perform
  --file_path FILE_PATH
                        Path to a file or a theorem folder
  --output_folder OUTPUT_FOLDER
                        Directory to store the evaluation files
  --retry_limit RETRY_LIMIT
                        Number of retry attempts for each inference
  --combine             Combine all results into a single JSON file
  --bulk_evaluate       Evaluate a folder of theorems together
  --target_fps TARGET_FPS
                        Target FPS for video processing. If not set, original video FPS will be used
  --use_parent_folder_as_topic
                        Use parent folder name as topic name for single file evaluation
  --max_workers MAX_WORKERS
                        Maximum number of concurrent workers for parallel processing
```
* For `file_path`, it is recommended to pass a folder containing both an MP4 file and an SRT file.

## 🖊️ Citation

Please kindly cite our paper if you use our code, data, models or results:
```bibtex
@misc{ku2025theoremexplainagentmultimodalexplanationsllm,
      title={TheoremExplainAgent: Towards Multimodal Explanations for LLM Theorem Understanding}, 
      author={Max Ku and Thomas Chong and Jonathan Leung and Krish Shah and Alvin Yu and Wenhu Chen},
      year={2025},
      eprint={2502.19400},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2502.19400}, 
}
```

## 🎫 License

This project is released under the [the MIT License](LICENSE).

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=TIGER-AI-Lab/TheoremExplainAgent&type=Date)](https://star-history.com/#TIGER-AI-Lab/TheoremExplainAgent&Date)

## 💞 Acknowledgements

We want to thank [Votee AI](https://votee.ai/) for sponsoring API keys to access the close-sourced models.

The code is built upon the below repositories, we thank all the contributors for open-sourcing.
* [Manim Community](https://www.manim.community/)
* [kokoro-manim-voiceover](https://github.com/xposed73/kokoro-manim-voiceover)
* [manim-physics](https://github.com/Matheart/manim-physics)
* [manim-Chemistry](https://github.com/UnMolDeQuimica/manim-Chemistry)
* [ManimML](https://github.com/helblazer811/ManimML)
* [manim-dsa](https://github.com/F4bbi/manim-dsa)
* [manim-circuit](https://github.com/Mr-FuzzyPenguin/manim-circuit)

## 🚨 Disclaimer

**This work is intended for research purposes only. The authors do not encourage or endorse the use of this codebase for commercial applications. The code is provided "as is" without any warranties, and users assume all responsibility for its use.**
