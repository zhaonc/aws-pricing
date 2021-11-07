FROM jupyter/scipy-notebook

# Upgrade pip
USER $NB_UID
RUN pip install --upgrade pip

# Install requirements.txt
COPY requirements.txt /tmp/
RUN pip install --upgrade --requirement /tmp/requirements.txt && \
    pip cache purge && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

# Clear /tmp
USER root
RUN rm -rf /tmp/*
USER $NB_UID