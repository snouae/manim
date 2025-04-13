#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Run the video generation with Deepseek model
python generate_video.py \
    --topic "Pythagorean Theorem" \
    --context "A short visual explanation of the Pythagorean theorem a^2 + b^2 = c^2 for a right-angled triangle." \
    --model "deepseek/deepseek-reasoner" \
    --output_dir output/pythagorean_theorem_deepseek \
    --max_retries 3 \
    --verbose \
    --max_scene_concurrency 1

# Deactivate virtual environment
deactivate 