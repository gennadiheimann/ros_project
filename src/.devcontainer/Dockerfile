FROM ros:jazzy
ARG USERNAME=heimang
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user, or reuse/rename the existing user if USER_UID is already taken.
RUN if ! getent group "$USER_GID" >/dev/null; then groupadd --gid "$USER_GID" "$USERNAME"; fi \
    && if id -u "$USERNAME" >/dev/null 2>&1; then \
        true; \
    elif getent passwd "$USER_UID" >/dev/null 2>&1; then \
        EXISTING_USER="$(getent passwd "$USER_UID" | cut -d: -f1)"; \
        EXISTING_GROUP="$(id -gn "$EXISTING_USER")"; \
        usermod -l "$USERNAME" "$EXISTING_USER"; \
        if [ "$EXISTING_GROUP" != "$USERNAME" ]; then groupmod -n "$USERNAME" "$EXISTING_GROUP"; fi; \
        usermod -d "/home/$USERNAME" -m "$USERNAME"; \
    else \
        useradd --uid "$USER_UID" --gid "$USER_GID" -m "$USERNAME"; \
    fi \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3-pip
ENV SHELL=/bin/bash

# ********************************************************
# * Anything else you want to do like clean up goes here *
# ********************************************************

# [Optional] Set the default user. Omit if you want to keep the default as root.
USER $USERNAME
CMD ["/bin/bash"]
