# .bashrc

# Source global definitions
if [ -f /etc/bash.bashrc ]; then
    . /etc/bash.bashrc
fi

# Activate the virtual environment
source /opt/venv/bin/activate

# Enable color support for `ls` and other commands if the terminal supports it
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# Customize the shell prompt (PS1) to include colors
# Example: Red for user@host, green for directory path, and yellow for $
PS1='\[\033[01;31m\]\u@\h\[\033[00m\]:\[\033[01;32m\]\w\[\033[00m\]\$ '

# Set terminal colors for easier visibility
export LS_COLORS='di=01;34:ln=01;36:so=01;35:pi=01;33:ex=01;32:bd=01;33:cd=01;33:su=01;37:sg=01;30:tw=01;34:ow=01;34'

