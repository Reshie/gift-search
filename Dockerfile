# select python image
FROM python:3.10

# Add non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && apt-get clean

# Update package lists
RUN apt-get update && \
    apt-get -y upgrade

# Install chromium
RUN curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt update -y && apt install -y google-chrome-stable

# Set the working directory in the container
WORKDIR /app

# Install pip
RUN pip install --no-cache-dir --upgrade pip

# Install pipenv
RUN pip install pipenv

# Expose the port the app runs on
EXPOSE 8080

# Set user
USER $USERNAME

# Run any command to initialize the container
CMD ["bash"]
