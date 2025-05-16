# Refining and Editing Text with Stable Diffusion, Fine-tuning, with an MCP Infrastructure

## 1. Introduction

The increasing capability of vision-language models has opened new avenues for understanding and editing text embedded in images. This report explores the application of Stable Diffusion models—specifically Stable Diffusion 1.5—for researching text on images, performing image inpainting, and enhancing capabilities via fine-tuning on Hugging Face. One core focus is the challenge of generating coherent and legible text within images, a known limitation of diffusion-based models due to their lack of explicit text structure modeling. These issues include character-level distortion, inconsistent font rendering, and a tendency for models to hallucinate non-existent glyphs. Despite these constraints, Stable Diffusion can still be adapted through inpainting, conditioning, and fine-tuning to support workflows involving text manipulation. The report also details the deployment of these vision features using a Model Context Protocol (MCP) server, enabling scalable, modular access to visual processing tools in agent-based or programmatic systems.

## 2. Stable Diffusion for Text-on-Image Research

Stable Diffusion, a latent diffusion model for image generation, is not inherently trained to recognize or generate text with high accuracy. However, with targeted prompting and conditional inputs, it can be adapted for:

Visualizing and editing text in context, such as titles, signs, or posters within images.

Zero-shot image captioning and text placement using ControlNet or similar conditioning modules.

Semantic inpainting around text regions, where text is removed and replaced with context-appropriate imagery.

Inpainting in Stable Diffusion relies on the use of binary masks that define the areas to be regenerated. A mask is typically created using either manual annotation or automated methods like OCR-based region detection. During inpainting, the model receives both the original image with masked regions and a guiding text prompt, allowing it to fill in the blank areas while preserving spatial and semantic coherence with the unmasked parts of the image.

To improve the accuracy and consistency of text rendering and placement, fine-tuning Stable Diffusion will also be explored. This includes adapting the model to better handle fonts, character spacing, and alignment in complex scenes by training on curated datasets with annotated text regions. Fine-tuning may involve lightweight approaches such as LoRA (Low-Rank Adaptation) or full-model training, depending on the required fidelity and resource constraints.



### Key Tools:

- ControlNet: Enables structured conditioning (e.g., depth maps, edge detection, text layout) to guide Stable Diffusion’s generation process, making it possible to better localize or align visual elements like text within specific regions.

- Textual Inversion / LoRA: Supports lightweight domain adaptation by learning new embeddings or modifying attention layers. These techniques are particularly useful for customizing the model to handle specific fonts, symbols, or visual styles relevant to the desired text appearance.

- Hugging Face DreamBooth: Allows personalized fine-tuning of Stable Diffusion using a small number of example images. DreamBooth can be used to associate text prompts with unique visual concepts—including logos, character sets, or consistent text templates—which is valuable for text rendering tasks.

- Full-model Fine-tuning on Hugging Face: For more significant control over text rendering and layout, complete model fine-tuning can be conducted using Hugging Face’s diffusers and transformers libraries. This is especially useful when dealing with datasets containing annotated text regions or when aiming for higher fidelity in structured text placement (e.g., signs, labels, or digital UI mockups).

## 3. Inpainting Techniques for Text Removal and Editing
Inpainting with Stable Diffusion is commonly used for removing or replacing text in natural images. The workflow involves:

Mask Creation: Identify regions containing text using OCR.  

Context-Aware Replacement: Use the inpainting pipeline in diffusers (Hugging Face) to regenerate masked areas with semantically appropriate visuals.

Optional Text Reinsertion: New text can be added via overlays, synthetic rendering, or text-to-image synthesis using conditioned prompts.

An example of the process can be found in the repo under the inpainting directory.

## 4. Fine-Tuning on Hugging Face
To improve performance in text-heavy and stylistically unique domains—such as comic panels, educational posters, and graphic illustrations—fine-tuning the Stable Diffusion backbone is a key strategy. In this project, we began by exploring fine-tuning for specific visual styles, including line art, duo tone color schemes, and astronaut-themed comic landscapes, to ensure better compatibility with text rendering in contextually rich and stylized environments.

Fine-tuning Process:
Dataset Preparation: Curated datasets featuring the target styles (e.g., line art posters, retro duo-tone comics, and sci-fi comic environments) were collected. Where applicable, annotations such as bounding boxes and transcripts for embedded text were included to support future layout-aware training.

Tokenizer Adaptation: If style-specific tokens or structured layouts are introduced (e.g., font descriptors, panel types), the tokenizer may be extended to support custom prompts reflecting those formats.

Fine-tune Strategies:

DreamBooth / LoRA: Used for lightweight personalization—especially effective for learning the aesthetics of narrow domains (e.g., astronaut comic styles or high-contrast duo-tone art).

Full-model training: Leveraged the transformers and diffusers libraries on Hugging Face with dedicated compute resources (e.g., AWS, A100 GPUs) to perform deeper fine-tuning. This approach enables the model to generalize better to the structural and stylistic aspects of the target visual domains, laying the groundwork for more consistent and legible text integration.

This style-specific fine-tuning serves as a foundation for further experimentation with text placement, text-to-image alignment, and contextual inpainting in heavily illustrated or abstract environments.

An example can be found under the fine-tuning directory

## 5. Hosting Vision Capabilities via MCP Server

The Model Context Protocol (MCP) provides a standardized interface for exposing local model tools (vision, NLP, etc.) to agents and client systems.

Vision Capability Server Design

### Tools Exposed:
gen_image(prompt, steps): Generates an image using Stable Diffusion with a specified prompt and number of inference steps.

overlay_text(text): Renders and overlays specified text onto an existing image, optionally positioned via layout rules or OCR-guided alignment.

### Server Backend:  
Built using Python with the MCP Python SDK, enabling streamlined definition and registration of vision tools.

Images and intermediate results are stored and retrieved using Amazon S3, allowing persistent, scalable, and cloud-accessible storage for generated or modified assets.

Supports communication over FastAPI or standard I/O subprocess interfaces, ensuring compatibility with agent frameworks like LlamaIndex.

Modular Integration:
Tools are wrapped in modular classes using FunctionTool or equivalent MCP bindings, enabling clean and reusable interfaces.

New vision tools (e.g., inpaint_region, describe_image, detect_text_regions) can be added with minimal friction by extending the MCP server’s tool registry.

Benefits of MCP Integration:
Interoperability: Tools can be accessed by language models and agents in a standardized, schema-driven way.

Lightweight Deployment: Easily deployable in both local research environments and scalable cloud backends.

Composable Toolchains: Vision tasks can be orchestrated in sequences—for example:
caption → detect text → inpaint → regenerate caption—allowing rich, agent-driven image workflows.

Persistent Storage: Integration with S3 enables persistent image histories, version control, and remote collaboration.

## 5. Findings: Fine-Tuning for Line Art and Text Rendering

### Limitations on Training Text for Stable Diffusion
Data Quality and Licensing: Training Stable Diffusion models requires vast amounts of text-image pair data. Much of the high-quality captioned image data is either proprietary or lacks clear licensing, limiting the scope of publicly available training sets.

Alignment Challenges: Aligning text prompts with desired visual outputs, is fragile and subtle variations in wording can lead to vastly different results, indicating that training text often fails to encode the intent clearly or consistently.

Granularity of Control: Text descriptions frequently lack sufficient detail for fine-grained control of the output, especially in complex scenes or specific semantic edits.

### Hardware Limitations for Stable Diffusion 3
Memory Requirements: Stable Diffusion 3 (SD3) models are significantly larger than previous versions, often requiring upwards of 24–48 GB of GPU memory for inference and even more for training. This restricts development to users with high-end consumer or enterprise-grade hardware (e.g., A100, H100).

Inference Latency: Even with optimized inference backends, SD3 introduces longer render times due to increased model depth and complexity, particularly when using attention-heavy architectures.

Distributed Training Complexity: Scaling training across multiple GPUs requires sophisticated pipeline and data parallelism strategies. As a result, experimentation and prototyping are resource-intensive.

Energy Consumption: Training SD3 models is power-intensive, making sustainability a concern for independent researchers and institutions with limited infrastructure.

### MCP Server Limitations with Long-Running Clients (>30s)
Timeout Constraints: Most MCP (Model Context Protocol) servers assume near real-time interaction with clients. Jobs requiring more than 30 seconds often exceed default timeout windows, leading to disconnections or incomplete responses.

Lack of Native Async/Job Queuing: Many MCP implementations lack built-in support for background task queuing or job continuation. This makes it difficult to handle long-running or compute-heavy requests gracefully.

Statefulness and Checkpointing: Persistent state across long jobs is not reliably managed. Unless explicitly implemented, any failure in communication may result in loss of job progress.

Scalability and Load Management: MCP servers can become bottlenecks when handling concurrent long-running tasks, especially in multi-client scenarios, unless offloading and load balancing mechanisms are in place.

### Challenges in Programmatically Inpainting with Text Guidance
Text-to-Mask Ambiguity: Automatically generating masks from text (e.g., "remove the man on the left") requires robust scene understanding. Existing models struggle with spatial disambiguation without detailed segmentation or auxiliary models.

Prompt Localization: Mapping abstract or vague textual prompts to precise spatial regions is not well-supported by current inpainting pipelines. This hampers automation in iterative or fine-control applications.

Visual Context Awareness: Text prompts do not inherently encode the context of the surrounding image. As a result, inpainting can produce semantically or stylistically inconsistent patches unless the prompt is overly prescriptive.


## 7. Results

### Text on Image Generation

<p float="left">
  <img src="/report/Images/helloworld.jpeg" width="400"/>
  <img src="/report/Images/hello.jpeg" width="400"/>
  <img src="/report/Images/test.jpeg" width="400"/>
</p>

### Inpainting Images

<p float="left">
  <img src="/report/Images/inpainting/c85c291e-a9bb-493c-ba04-414cc52b088a.png" width="400"/>
  <img src="/report/Images/inpainting/7c36b67c-ff3d-4f88-bddd-7dbaf084e7a9.png" width="400"/>
  <img src="/report/Images/inpainting/342837b0-5238-42cb-a9c3-758470d93084.png" width="400"/>
</p>

### Controlnet Image Generation

<p float="left">
  <img src="/report/Images/controlnet/c3619a77-b356-434e-af56-3ff2826eb81e.png" width="400"/>
  <img src="/report/Images/controlnet/70df0481-dc0e-49fe-86cd-528dbbba530c.png" width="400"/>
</p>

### Fine-Tuning Line Art


<img src="/report/Images/line-art.png" width="800"/>

### Fine-Tuning Style

<img src="/report/Images/astro.png" width="800"/>


### Layering Text

<p float="left">
  <img src="/report/Images/layer/text1.png" width="400"/>
  <img src="/report/Images/layer/text2.png" width="400"/>
</p>


## 6. Conclusion
By combining the generative power of Stable Diffusion with structured tool deployment via MCP, researchers and developers can create powerful systems for text understanding and manipulation in images. Fine-tuning models on specific domains using Hugging Face infrastructure enhances accuracy and relevance, while the MCP server paradigm ensures these capabilities are easily accessible and modular.


Our exploration demonstrated that training visual styles on Stable Diffusion can be successfully achieved with moderate resources, particularly when fine-tuning on well-prepared image datasets. However, extending this to training or fine-tuning the model's text-conditioning components proved infeasible within the time and computational limits of this project. High-quality text-image pair datasets are both scarce and large, and the compute required to meaningfully train or adapt the text encoder exceeded our available infrastructure.

Similarly, while the MCP server framework offered a structured way to integrate vision models, its effectiveness was constrained by resource limitations. The primary bottlenecks were related to the high computational cost of vision model inference and the lack of support for long-running jobs. Reducing inference steps and optimizing model efficiency became necessary trade-offs to operate within the protocol's response constraints.

Overall, the project highlighted the potential of style transfer and image manipulation using Stable Diffusion, while also underscoring the importance of scalable infrastructure, high-quality training data, and protocol-aware model optimization when working with generative vision systems and MCP servers.
## 7. Future Work
Improve text rendering accuracy in generated images.

Train custom OCR-guided inpainting models.

Extend MCP tooling to support multimodal queries (e.g., "remove the word 'SALE' from the red banner").

Build front-end interfaces for interactive editing powered by vision agent stacks.
