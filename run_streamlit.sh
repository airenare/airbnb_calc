#!/usr/bin/env bash

SESSION_NAME="streamlit"
WINDOW_NAME="streamlit"
VENV_PATH="$HOME/venv/3.14/bin/activate"
PROJECT_DIR="."
GIT_URL="https://github.com/airenare/airbnb_calc.git"
APP_FILE="app.py"

# 1. Ensure tmux session exists
if ! tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "Creating tmux session '$SESSION_NAME'..."
    tmux new-session -d -s $SESSION_NAME -n $WINDOW_NAME
else
    echo "Session exists. Using it."
fi

# 2. Ensure window exists
if ! tmux list-windows -t $SESSION_NAME | grep -q "$WINDOW_NAME"; then
    tmux new-window -t $SESSION_NAME -n $WINDOW_NAME
fi

# Commands to run inside tmux
COMMANDS="
echo 'Activating venv...';
source $VENV_PATH;

# Ensure project exists, then update it
if [ ! -d \"$PROJECT_DIR\" ]; then
    echo 'Project directory not found. Cloning repo...';
    git clone $GIT_URL $PROJECT_DIR;
else
    echo 'Project exists. Pulling latest changes...';
    cd $PROJECT_DIR;
    git reset --hard HEAD;
    git pull --rebase;
fi

cd $PROJECT_DIR;
echo 'Starting Streamlit...';
streamlit run $APP_FILE
"

# 4. Send commands into tmux
tmux send-keys -t "$SESSION_NAME:$WINDOW_NAME" "$COMMANDS" C-m

echo "Streamlit now running in tmux window '$WINDOW_NAME'. Auto-update enabled."
