# indextts-api

`indextts-api` 是一个基于 **FastAPI** 封装的轻量级 API 服务，用于部署 [index-tts](https://github.com/index-tts/index-tts) 项目。它将复杂的环境配置和依赖管理封装在 Docker 容器中，让你可以通过简单的 API 调用，轻松实现文本转语音（TTS）功能。

该项目旨在提供一个快速、便捷的部署方案，用户只需 `git clone` 项目，配置 `.env` 文件，即可通过 Docker 启动一个功能完备的 TTS 服务。

## ✨ 特性

- **一键部署**：通过 `docker-compose` 即可启动服务，无需手动安装 Python 环境或依赖。
- **自动安装**：Docker 镜像构建时会自动下载并安装 `index-tts` 及其所需的所有依赖。
- **API 接口**：提供清晰、简洁的 RESTful API 接口，用于文本转语音和音频文件下载。
- **卷挂载**：支持通过 Docker 卷挂载的方式，持久化存储语音模型、参考声音和生成的音频文件。

---

## ⚠️ 许可证与免责声明

**`indextts-api` 项目本身是非商业用途的。** 本项目旨在提供技术封装和部署便利，使用者需自行承担因使用本服务及相关模型所产生的一切后果。

* **项目许可证**：本项目遵循 **Apache-2.0 许可证**。你可以自由使用、修改和分发本项目代码，但需遵守该许可证的所有条款。

* **依赖项目与模型许可证**：
  * 本服务所依赖的 `index-tts` 项目代码遵循 **[Apache-2.0 许可证](https://github.com/index-tts/index-tts/blob/main/LICENSE)**。
  * `index-tts` 模型遵循 **[INDEX_MODEL_LICENSE](https://github.com/index-tts/index-tts/blob/main/INDEX_MODEL_LICENSE)** 协议。此协议的核心要点为**非商业用途**、**告知义务**和**使用限制**。
  * `index-tts` 原项目的 **[免责声明](https://github.com/index-tts/index-tts/blob/main/DISCLAIMER)** 同样适用于本项目的最终使用者。

* **合规性声明**：为了确保合规性，`index-tts` 项目的许可证文件副本（包括 `LICENSE`, `DISCLAIMER`, `INDEX_MODEL_LICENSE`）已包含在你的项目仓库的 `licenses/index-tts/` 文件夹中。请注意，项目贡献者不保证这些副本的实时性，所有用户都应以原仓库中的最新文件为准。

---

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone <你的仓库地址>
cd indextts-api
````

### 2\. 配置 `.env` 文件

本项目使用 **`.env`** 文件进行配置。你只需根据需求编辑项目根目录下的 `.env` 文件即可。

请根据你的实际情况修改以下参数：

```env
# 容器名称
CONTAINER_NAME=index-tts-app

# API 服务端口
API_PORT=8198

# 主机路径，用于持久化存储数据
# 请将 'SOMEWHERE' 替换为你的实际路径，例如：/home/user/tts_data
VOICES_HOST_PATH=SOMEWHERE/tts_data/reference_voices
OUTPUTS_HOST_PATH=SOMEWHERE/tts_data/outputs
CHECKPOINTS_HOST_PATH=SOMEWHERE/tts_data/checkpoints

# 容器内部路径，一般无需修改
CONTAINER_PROJECT_ROOT=/project
VOICES_CONTAINER_PATH=${CONTAINER_PROJECT_ROOT}/tts_files/reference_voices
OUTPUTS_CONTAINER_PATH=${CONTAINER_PROJECT_ROOT}/tts_files/outputs
CHECKPOINTS_CONTAINER_PATH=${CONTAINER_PROJECT_ROOT}/tts_files/checkpoints
```

### 3\. 启动服务

在项目根目录运行以下命令：

```bash
docker-compose up --build -d
```

  * `--build`：首次运行时会构建 Docker 镜像，并自动下载所有依赖和 TTS 模型。
  * `-d`：以“后台（detached）”模式运行。

首次启动可能需要一段时间，因为它需要下载模型文件。

-----

## 🎯 API 接口文档

服务启动后，你可以在浏览器中访问 `http://localhost:8198/docs` 查看由 FastAPI 自动生成的交互式 API 文档。

以下是两个核心接口的详细说明：

### 1\. 生成音频文件

  - **接口地址**：`POST /generate`
  - **功能**：将文本转换为音频，返回音频文件在服务器上的**相对路径**，可用于后续下载或直接从挂载卷中获取。
  - **请求体（JSON）**：
      - `text`：`string` 或 `string[]`。要生成音频的文本。
      - `speaker`：`string` 或 `string[]`。要使用的说话人 ID。
          * 如果 `speaker` 是一个字符串，则所有文本都将使用同一个说话人。
          * 如果 `speaker` 是一个列表，其长度必须与 `text` 列表长度一致，两者将一一对应。
  - **成功响应**：
      - 如果输入是单个文本，返回一个字符串，例如：`"2023-01-01/example.wav"`。
      - 如果输入是文本列表，返回一个字符串列表，例如：`["path1.wav", "path2.wav"]`。

### 2\. 下载音频文件

  - **接口地址**：`GET /download`
  - **功能**：根据相对路径下载生成的音频文件。
  - **查询参数**：
      - `relative_path`：`string`。必填。由 `/generate` 接口返回的音频文件相对路径。
  - **成功响应**：返回音频文件流（`application/octet-stream`）。

-----

## 🤝 贡献与感谢

本项目基于 [index-tts](https://github.com/index-tts/index-tts) 项目开发，在此向原项目作者表示衷心感谢。
