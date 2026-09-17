# SWARM development: ROS 2 Jazzy on Ubuntu 24.04.
# Apple silicon build: docker build --platform linux/arm64 -t swarm-dev:jazzy .
FROM ros:jazzy-ros-base-noble

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Development tools, numerical Python, and ROS messaging examples.
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential \
        git \
        python3-colcon-common-extensions \
        python3-numpy \
        python3-pytest \
        python3-rosdep \
        ros-jazzy-demo-nodes-cpp \
        ros-jazzy-demo-nodes-py \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1
WORKDIR /workspace

# Also initialize ROS in interactive shells opened with docker exec.
RUN mkdir -p /workspace/src \
    && printf '%s\n' \
        '' \
        'source /opt/ros/jazzy/setup.bash' \
        'if [ -f /workspace/install/setup.bash ]; then' \
        '    source /workspace/install/setup.bash' \
        'fi' \
        >> /root/.bashrc

# Keep the official ROS entrypoint, which initializes ROS for docker run.
CMD ["bash"]
