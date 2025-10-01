# ramalama-edge
Code for the article "Deploying Multimodal AI at the Edge: Deploying Vision Language Models with Ramalama"

# How to run the demo
1. Install Podman for your platform by following the instructions at https://podman.io/docs/installation
   
2. Install ramalama for your platform by following the instructions at https://github.com/containers/ramalama?tab=readme-ov-file#install
   
3. Create a new venv and activate it
    ```bash
    $ python -m venv venv
    $ source venv/bin/activate
    ```
4. Serve up the qwen2.5vl:3b model using ramalama
    ```bash
    $ ramalama serve --port 8081 qwen2.5vl:3b
    ```
5. Verify VLM is running with no errors
   ```bash
   $ ramalama ps
   ```
6. Install the dependencies for the scripts
   ```bash
   $ (venv) pip install -r requirements.txt
   ```
7. Run the image analysis script
   ```bash
   $ (venv) python image_analyze.py
   ```
8. Next, run the video analysis script
   ```bash
   $ (venv) python video_analyze.py
   ```