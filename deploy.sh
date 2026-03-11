#!/usr/bin/env bash

# --------------------------
# CONFIG
SESSION_NAME="streamlit"
WINDOW_NAME="streamlit"
PYTHON_VERSION="3.12.2"
# VENV_DIR="$HOME/venv/$PYTHON_VERSION" # Changed to .venv for better organization
VENV_DIR="./.venv/$PYTHON_VERSION"
VENV_PATH="$VENV_DIR/bin/activate"
PROJECT_DIR="$HOME/Work/airbnb_calc"
GIT_URL="https://github.com/airenare/airbnb_calc.git"
APP_FILE="app.py"

# Check for --force flag
FORCE=false
if [[ "$1" == "--force" ]]; then
    FORCE=true
fi

# --------------------------
# Helper: confirmation prompt
ask() {
    if $FORCE; then
        return 0
    fi
    while true; do
        read -p "$1 [y/n]: " yn
        case $yn in
            [Yy]*) return 0 ;;
            [Nn]*) return 1 ;;
        esac
    done
}

# --------------------------
# 0️⃣ Ensure pyenv exists
if ! command -v pyenv &>/dev/null; then
    echo "pyenv not found."
    if ask "Install pyenv automatically?"; then
        curl https://pyenv.run | bash
        export PATH="$HOME/.pyenv/bin:$PATH"
        eval "$(pyenv init - bash)"
        eval "$(pyenv virtualenv-init -)"
    else
        echo "pyenv required. Exiting."
        exit 1
    fi
fi

# Reload pyenv for this script
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - bash)"
eval "$(pyenv virtualenv-init -)"

# --------------------------
# 1️⃣ Ensure Python version is installed
if ! pyenv versions --bare | grep -qx "$PYTHON_VERSION"; then
    echo "Installing Python $PYTHON_VERSION via pyenv..."
    pyenv install -s $PYTHON_VERSION
fi

# --------------------------
# 2️⃣ Ensure virtualenv exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtualenv at $VENV_DIR..."
    pyenv shell $PYTHON_VERSION
    python -m venv "$VENV_DIR"
fi

# --------------------------
# 3️⃣ Activate virtualenv
source "$VENV_PATH"
pip install --upgrade pip

# --------------------------
# 4️⃣ Clone or update project
if [ ! -d "$PROJECT_DIR" ]; then
    echo "Project not found. Cloning repository..."
    git clone $GIT_URL $PROJECT_DIR
else
    echo "Project exists. Updating repository..."
    cd $PROJECT_DIR
    git reset --hard HEAD
    git pull --rebase
fi

# --------------------------
# 5️⃣ Install dependencies
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r "$PROJECT_DIR/requirements.txt"
fi

# --------------------------
# 6️⃣ Setup tmux session
if ! tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "Creating tmux session '$SESSION_NAME'..."
    tmux new-session -d -s $SESSION_NAME -n $WINDOW_NAME
fi

if ! tmux list-windows -t $SESSION_NAME | grep -q "$WINDOW_NAME"; then
    tmux new-window -t $SESSION_NAME -n $WINDOW_NAME
fi

# --------------------------
# 7️⃣ Commands to run inside tmux
COMMANDS="
echo 'Activating venv...';
source $VENV_PATH;
cd $PROJECT_DIR;
echo 'Starting Streamlit...';
python -m streamlit run $APP_FILE
"

tmux send-keys -t "$SESSION_NAME:$WINDOW_NAME" "$COMMANDS" C-m

echo "✅ Streamlit is now running in tmux window '$WINDOW_NAME'."
echo "Use 'tmux attach -t $SESSION_NAME' to view it."
